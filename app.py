from flask import Flask, render_template,send_from_directory, request, jsonify, Response
import os, json
from hashlib import sha1
import csv 
from datetime import datetime

app = Flask(__name__)

ALL_QUESTION_METADATA_FILE = "static/metadata/questions.tsv"
@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/home')
def home():
    
    assessments = safe_read_assessments()
    return render_template('home.html',  assessments=assessments)

@app.route('/library')
def library():
    '''knowledge_areas = '''
    knowledge_areas = generate_nested_list(ALL_QUESTION_METADATA_FILE)
    return render_template('qa.html', areas=knowledge_areas)

@app.route('/history')
def history():
    # Example data for the history view
    events = [
        {"timestamp": "2024-01-01 10:00:00", "event": "Assessment Created", "trace_id": "abc123", 'level': 'info', 'details': {'assessment_id': 'def456'}}, 
        {"timestamp": "2024-01-02 12:00:00", "event": "Question Answered", "trace_id": "def456", 'level': 'info', 'details': {'question_id': 'q1', 'answer': 'Yes', 'assessment_id': 'def456'}},
        {"timestamp": "2024-01-03 14:00:00", "event": "Report Generated", "trace_id": "ghi789", 'level': 'warn', 'details': {'assessment_id': 'def456', 'report_url': '/reports/def456.pdf'}},
    ]
    return render_template('history.html', events=events)

@app.route('/assessment/<assessment_id>')
def assessment_detail(assessment_id):
    # fetch assessment by id
    metadata = generate_metadata(ALL_QUESTION_METADATA_FILE, assessment_id)
    knowledge_areas = generate_nested_list(ALL_QUESTION_METADATA_FILE, assessment_id=assessment_id)
    index, assessment = safe_get_assessment_by_id(assessment_id)
    return render_template('assessment_detail.html', 
                            areas=knowledge_areas, 
                            assessment_id=assessment_id,
                            assessment=assessment,
                            metadata=metadata)

def __hash_func__(data: str) -> str:
    return sha1(data.encode()).hexdigest()
#####################################################
####### Question Metadata
#####################################################


def safe_read_question_metadata():
        all_questions = [] 
        nested_data = {}
        focus_id_map = {}
        trait_id_map = {}
        sub_capability_id_map = {}
        with open(ALL_QUESTION_METADATA_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for i, row in enumerate(reader, start=1):

                focus = row['focus']
                trait = row['care_trait']
                sub_capability = row['care_sub_capability']
                question_text = row['question'].replace("'", "`")
                
                # Create IDs
                focus_id = __hash_func__(focus)
                focus_id_map[focus_id] = focus 

                trait_id = __hash_func__(f"{focus}_{trait}")
                trait_id_map[trait_id] = trait

                sub_capability_id = __hash_func__(f"{focus}_{trait}_{sub_capability}")
                sub_capability_id_map[sub_capability_id] = sub_capability


                question_id = __hash_func__(f"{focus}_{trait}_{sub_capability}_{i}".replace(" ", "_"))

                qs = {'focus': focus, 
                      'trait': trait, 
                      'sub_capability': sub_capability, 
                      'question_text': question_text,
                      'focus_id': focus_id,
                      'trait_id': trait_id,
                      'sub_capability_id': sub_capability_id,
                      'question_id': question_id
                }
                all_questions.append(qs)
        return (all_questions, focus_id_map, trait_id_map, sub_capability_id_map)



def generate_metadata(file_path, assessment_id):
    l = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for i, row in enumerate(reader, start=1):
            focus = row['focus']
            trait = row['care_trait']
            sub_capabilities = row['care_sub_capability']
            question_id = __hash_func__(f"{focus}_{trait}_{sub_capabilities}_{i}".replace(" ", "_"))
            question_answered = safe_get_reposnse_by_qid(assessment_id, question_id)['question_answered']
            l.append({'question_id': question_id, 'question_answered': question_answered})
        
    total_questions = len(l) 
    answered_questions = sum([1 for x in l if x['question_answered']])
    pct_completed = round(100*(answered_questions/total_questions),2)
    #print(f"total_questions: {total_questions}, answered_questions: {answered_questions}, pct_completed:{pct_completed} ")


    return {'total_questions': total_questions, 'answered_questions': answered_questions, 'pct_completed': pct_completed}
        

def generate_nested_list(file_path, assessment_id=None):
    nested_data = {}

    all_questions, focus_id_map, trait_id_map, sub_capability_id_map = safe_read_question_metadata()
    ''' print(f"========>. all_questions: {all_questions}")
    print(f"========>. focus_id_map: {focus_id_map}")
    print(f"========>. trait_id_map: {trait_id_map}")
    print(f"========>. sub_capability_id_map: {sub_capability_id_map}")
    '''

    for i, row in enumerate(all_questions):

        focus = row['focus']
        trait = row['trait']
        sub_capability = row['sub_capability']
        question_text = row['question_text']
        focus_id = row['focus_id']
        trait_id = row['trait_id']
        sub_capability_id = row['sub_capability_id']
        question_id = row['question_id']
        
        # Build nesting
        if focus_id not in nested_data:
            nested_data[focus_id] = {}

        if trait_id not in nested_data[focus_id]:
            nested_data[focus_id][trait_id] = {}
        
        if sub_capability_id not in nested_data[focus_id][trait_id]:
            nested_data[focus_id][trait_id][sub_capability_id] = []
        
        if not assessment_id:
             nested_data[focus_id][trait_id][sub_capability_id].append({
                "id": question_id,
                "text": question_text
            })
        else:
            nested_data[focus_id][trait_id][sub_capability_id].append({
                "id": question_id,
                "text": question_text,
                'question_answered': safe_get_reposnse_by_qid(assessment_id, question_id)['question_answered']
            })
    
    # Convert to final list format
    result = []
    for focus_id, traits in nested_data.items():
        focus_entry = {
            "id": focus_id,
            "name": focus_id_map[focus_id],
            "traits": []
        }
        for trait_id, sub_capabilities in traits.items():
            scs = []
            for sub_capability_id, questions in sub_capabilities.items():
                scs.append({
                    "id": sub_capability_id,
                    "name": sub_capability_id_map[sub_capability_id],
                    "questions": questions
                })

            focus_entry["traits"].append({
                "id": trait_id,
                "name": trait_id_map[trait_id],
                "sub_capabilities": scs
            })            

        result.append(focus_entry)
        
    return result

def get_question_metadata(qid):
    all_questions, focus_id_map, trait_id_map, sub_capability_id_map = safe_read_question_metadata()
    for row in all_questions:
        if qid == row['question_id']:
            focus = row['focus']
            trait = row['trait']
            sub_capability = row['sub_capability']
            return (focus, trait, sub_capability)
    return (None, None, None)




#####################################################
##### QA Response ##########
#####################################################
@app.route('/save_response', methods=['POST'])
def save_response():
    data = request.get_json()
    question_id = data.get('question_id')
    assessment_id = data.get('assessment_id')
    (focus, trait, sub_capability) = get_question_metadata(question_id)
    data['focus'] = focus 
    data['trait'] = trait 
    data['sub_capability'] = sub_capability 

    print(f"data: {data}")
    print(f"question_id: {question_id}; assessment_id:{assessment_id}")
    stored_responses = safe_read_responses()
    
    stored_responses[assessment_id][question_id] = data 
    
    with open('static/data/responses.json', 'w', encoding='utf-8') as f:
        json.dump(stored_responses, f, ensure_ascii=False, indent=4)

    # Logic to save to a database, session, or file
    # Example: print(f"Saving {question_id}: {evidence}")
    
    return jsonify({"status": "success", "message": "Response saved"}), 200


def safe_read_responses():
    if not os.path.exists("static/data/responses.json"):
        stored_responses = {}
    else:
        stored_responses = json.load(open("static/data/responses.json"))
    
    return stored_responses

def safe_get_reposnse_by_metadata(focus: str=None, trait: str=None, sub_capability: str=None ):
    stored_responses = safe_read_responses()
    result = []
    filters = {"focus": focus, "trait": trait,"sub_capability": sub_capability}
    # Remove None filters
    active_filters = {k: v for k, v in filters.items() if v}
    for r in stored_responses:
        response = stored_responses[r]
        check = [] 
        for k, v in active_filters.items():
            check.append(response.get(k) == v)
        
        #if all(response.get(k) == v for k, v in active_filters.items()):
        if all(check):
            result.append(response) 
    
    print(f"active_filters: {active_filters}, Result = {result}") 


def safe_get_reposnse_by_qid(assessment_id, qid):
    stored_responses = safe_read_responses()
    res = {"question_answered": False, "response": ''}
    if assessment_id in stored_responses.keys():
        if qid in stored_responses[assessment_id].keys():
            response_text = stored_responses[assessment_id][qid]['answer']
            res = {"question_answered": True, "response": response_text}         
    return res 


@app.route("/get_response_by_qid", methods=["POST"])
def get_response_by_qid():
    question_id = request.get_json().get('question_id')
    assessment_id = request.get_json().get('assessment_id')
    print(f"question_id: {question_id}; assessment_id:{assessment_id}")
    try:
        qa = safe_get_reposnse_by_qid(assessment_id,question_id) 
        res = {"success": 'true',"qid": question_id, "assessment_id":assessment_id, "question_answered": qa['question_answered'], "response": qa['response']}
        #print(f"======== Response Text: {res}")
        return jsonify(res)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

#####################################################
############## Assessment

def safe_read_assessments():
    if not os.path.exists("static/data/assessments.json"):
        stored_assessments = {}
    else:
        with open("static/data/assessments.json") as f:
            stored_assessments = json.load(f)
    
    return stored_assessments

def safe_get_assessment_by_id(assessment_id: str):
    stored_assessments = safe_read_assessments()
    for i,a in enumerate(stored_assessments):
        if a['assessment_id'] == assessment_id:
            return (i,a) 

    return (None,None)  

def safe_write_assessment(assessment):
    with open('static/data/assessments.json', 'w', encoding='utf-8') as f:
        json.dump(assessment, f, ensure_ascii=False, indent=4)
    
@app.route("/get_assessment_by_id", methods=["POST"])
def get_assessment_by_id():
    assessment_id = request.get_json().get('assessment_id')
    try:
        index, assessment = safe_get_assessment_by_id(assessment_id)
        res = {"success": 'true', 'assessment': assessment}
        return Response(json.dumps(assessment, sort_keys=False), mimetype="application/json")
    except Exception as e:
        raise
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/create_assessment', methods=['POST'])
def create_assessment():
    data = request.get_json()
    try:
        assessment_name = data.get('assessment_name')
    except:
        assessment_name = datetime.now().isoformat()
    
    print(f"data: {data}")
    stored_assessments = safe_read_assessments()
        
    assessment_id = __hash_func__(assessment_name)
    index, assessment = safe_get_assessment_by_id(assessment_id)
    if not assessment:
        a  = {
        'assessment_id': assessment_id,
        'assessment_name': assessment_name,
        'assessment_status': 'Created',
        'assessment_start_date': datetime.now().isoformat(),
        'assessment_last_updated_date': datetime.now().isoformat(),
         "assessment_score": {"completed": False, "score": None}
        } 

        stored_assessments.append(a)        
    
    safe_write_assessment(stored_assessments)
    
    return jsonify({"status": "success", "message": "Response saved"}), 200

@app.route('/delete_assessment', methods=['POST'])
def delete_assessment():
    data = request.get_json()
    assessment_id = data.get('assessment_id')
    
    print(f"data: {data}")
    stored_assessments = safe_read_assessments()
    index, assessment = safe_get_assessment_by_id(assessment_id)
    if assessment:
        stored_assessments.remove(assessment)

    safe_write_assessment(stored_assessments)
    
    return jsonify({"status": "success", "message": "Response saved"}), 200

@app.route('/start_reporting_assessment', methods=['POST'])
def start_reporting_assessment():
    data = request.get_json()
    assessment_id = data.get('assessment_id')
    
    print(f"data: {data}")
    stored_assessments = safe_read_assessments()
    index, assessment = safe_get_assessment_by_id(assessment_id)
    if safe_get_assessment_by_id(assessment_id):
        stored_assessments[index]['assessment_status'] = "In Progress"

    safe_write_assessment(stored_assessments)
    
    return jsonify({"status": "success", "message": "Response saved"}), 200

#####################################################
@app.route('/reports/sample')
def sample_report():
    # This securely joins the path and sends the file
    return send_from_directory(os.path.join(app.root_path, 'static', 'reports'), "sample.pdf")

@app.route('/reports/<assessment_id>')
def download_assessment_report(assessment_id):
    reports_dir = os.path.join(app.root_path, 'static', 'reports')

    safe_name = f"{assessment_id}.pdf"
    file_path = os.path.join(reports_dir, safe_name)

    if not os.path.exists(file_path):
        abort(404)

    return send_from_directory(reports_dir, safe_name)


if __name__ == '__main__':
    app.run(debug=True)

