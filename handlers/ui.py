from flask import Blueprint, Flask, render_template,send_from_directory, request, jsonify, Response
import os, json
from hashlib import sha1
import csv 
from datetime import datetime
from .util import ALL_QUESTION_METADATA_FILE, REPORT_FOLDER
from .api import (safe_get_assessment_by_id, 
                  generate_nested_list, 
                  generate_metadata,
                  safe_read_assessments
                  )

bp = Blueprint('ui', __name__)

@bp.route('/')
def landing():
    return render_template('index.html')

@bp.route('/home')
def home():    
    assessments = safe_read_assessments()
    return render_template('home.html',  assessments=assessments)


@bp.route('/reports/sample')
def sample_report():
    # This securely joins the path and sends the file
    return send_from_directory(os.path.join(app.root_path, 'static', 'reports'), "sample.pdf")

@bp.route('/history')
def history():
    # Example data for the history view
    events = [
        {"timestamp": "2024-01-01 10:00:00", "event": "Assessment Created", "trace_id": "abc123", 'level': 'info', 'details': {'assessment_id': 'def456'}}, 
        {"timestamp": "2024-01-02 12:00:00", "event": "Question Answered", "trace_id": "def456", 'level': 'info', 'details': {'question_id': 'q1', 'answer': 'Yes', 'assessment_id': 'def456'}},
        {"timestamp": "2024-01-03 14:00:00", "event": "Report Generated", "trace_id": "ghi789", 'level': 'warn', 'details': {'assessment_id': 'def456', 'report_url': '/reports/def456.pdf'}},
    ]
    return render_template('history.html', events=events)

#####################################################
### UI Routes for Assessment Details
#################################################

@bp.route('/assessment/<assessment_id>')
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

@bp.route('/reports/<assessment_id>')
def download_assessment_report(assessment_id):
    safe_name = f"{assessment_id}.pdf"
    print(f"Attempting to serve report: {safe_name} from {REPORT_FOLDER}")
    file_path = os.path.join(REPORT_FOLDER, safe_name)

    if not os.path.isfile(file_path):
        return "Report not found", 404

    return send_from_directory(REPORT_FOLDER, safe_name)

#####################################################
### UI Routes for QA Library 
#################################################
@bp.route('/library')
def library():
    '''knowledge_areas = '''
    knowledge_areas = generate_nested_list(ALL_QUESTION_METADATA_FILE)
    return render_template('qa.html', areas=knowledge_areas)


@bp.route('/test_report')
def test_report():
    # Simulated data from your Trustably Report PDF
    report_data = {
        "org_name": "Acme Technologies Pty Ltd",
        "report_date": "April 2026",
        "overall_score": 5.3,
        "focus_scores": {
            "Functional Gov": 6.4,
            "Observability": 4.8,
            "Culture": 2.5,
            "Unified Platform": 8.1,
            "Security": 9.1
        },
        "cell_scores": {
            "Consistent|Functional Gov": 6.4, # Example mapping
            "Accurate|Functional Gov": 7.0,
            # ... and so on for all 20 cells
        },
        "gaps": [
            {
                "name": "Culture x Observability",
                "current": "Experiment",
                "target": "Enable",
                "priority": "HIGH",
                "action": "Implement enterprise AI literacy programme."
            }
        ]
    }
    return render_template('report.html', **report_data)


