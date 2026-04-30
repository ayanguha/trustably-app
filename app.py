from flask import Flask, render_template,send_from_directory, request, jsonify, Response
import os, json
from hashlib import sha1
import csv 


app = Flask(__name__)

ALL_QUESTION_METADATA_FILE = "static/metadata/questions.tsv"
@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/home')
def home():
    metadata = generate_metadata(ALL_QUESTION_METADATA_FILE)
    assessments = safe_read_assessments()
    return render_template('home.html', metadata=metadata, assessments=assessments)

@app.route('/history')
def history():
    # Example data for the history view
    sent_assessments = [
        {
            "id": "asmt_001",
            "client": "Test",
            "sender": "Ramya Kumar",
            "timestamp": "14 Apr 2026, 03:57 pm",
            "recipient": "ramya.kumar@versent.com.au",
            "link": "https://main.d5yl4z9pmmspb.amplifyapp.com/assessment/mny...",
            "questions": [
                {"area": "Data Governance", "sub": "Data Governance Framework", "text": "Is there a documented data governance framework?"},
                {"area": "Data Governance", "sub": "Data Governance Framework", "text": "Is the data governance framework communicated to all stakeholders?"},
                {"area": "Data Governance", "sub": "Data Standards", "text": "Are data standards enforced through data validation rules?"}
            ]
        }
    ]
    return render_template('history.html', assessments=sent_assessments)

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



def generate_metadata(file_path):
    l = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for i, row in enumerate(reader, start=1):
            focus = row['focus']
            trait = row['care_trait']
            sub_capabilities = row['care_sub_capability']
            question_id = __hash_func__(f"{focus}_{trait}_{sub_capabilities}_{i}".replace(" ", "_"))
            question_answered = safe_get_reposnse_by_qid(question_id)['question_answered']
            l.append({'question_id': question_id, 'question_answered': question_answered})
        
    total_questions = len(l) 
    answered_questions = sum([1 for x in l if x['question_answered']])
    pct_completed = round(100*(answered_questions/total_questions),2)
    #print(f"total_questions: {total_questions}, answered_questions: {answered_questions}, pct_completed:{pct_completed} ")


    return {'total_questions': total_questions, 'answered_questions': answered_questions, 'pct_completed': pct_completed}
        

def generate_nested_list(file_path):
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

        nested_data[focus_id][trait_id][sub_capability_id].append({
            "id": question_id,
            "text": question_text
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


@app.route('/library')
def library():
    '''knowledge_areas = '''
    knowledge_areas = generate_nested_list(ALL_QUESTION_METADATA_FILE)
    return render_template('qa.html', areas=knowledge_areas)


#####################################################
##### QA Response ##########
#####################################################
@app.route('/save_response', methods=['POST'])
def save_response():
    data = request.get_json()
    question_id = data.get('question_id')
    (focus, trait, sub_capability) = get_question_metadata(question_id)
    data['focus'] = focus 
    data['trait'] = trait 
    data['sub_capability'] = sub_capability 

    print(f"data: {data}")
    if not os.path.exists("static/data/responses.json"):
        stored_responses = {}
    else:
        stored_responses = json.load(open("static/data/responses.json"))
    
    stored_responses[question_id] = data 
    
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


def safe_get_reposnse_by_qid(qid):
    stored_responses = safe_read_responses()
    
    if qid in stored_responses.keys():
        response_text = stored_responses[qid]['answer']
        res = {"question_answered": True, "response": response_text}
    else:
        response_text = ''
        res = {"question_answered": False, "response": response_text}
    return res 


@app.route("/get_response_by_qid", methods=["POST"])
def get_response_by_qid():
    qid = request.get_json().get('question_id')
    try:
        qa = safe_get_reposnse_by_qid(qid) 
        res = {"success": 'true',"qid": qid, "question_answered": qa['question_answered'], "response": qa['response']}
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

def safe_get_assessment_by_id(assessment_id):
    stored_assessments = safe_read_assessments()
    for a in stored_assessments:
        print(a)
        if a['assessment_id'] == str(assessment_id):
            return a 

    return None  

@app.route("/get_assessment_by_id", methods=["POST"])
def get_assessment_by_id():
    assessment_id = request.get_json().get('assessment_id')
    print(assessment_id)
    try:
        assessment = safe_get_assessment_by_id(assessment_id)
        res = {"success": 'true', 'assessment': assessment}
        print(f"======== Response Text: {res}")
        return Response(json.dumps(assessment, sort_keys=False), mimetype="application/json")
    except Exception as e:
        raise
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

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

