import requests
import os, sys

def upload_pdf(api_url, assessment_id, file_path):
    """
    Upload a PDF to Flask API

    :param api_url: Base API URL (e.g. http://localhost:5000)
    :param assessment_id: Assessment ID
    :param file_path: Path to PDF file
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    url = f"{api_url}/upload_report/{assessment_id}"

    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f, "application/pdf")
        }

        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("✅ Upload successful")
        return response.json()
    else:
        print("❌ Upload failed:", response.text)
        response.raise_for_status()

if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    FILE_PATH = "static/reports/sample.pdf"
    ASSESSMENT_ID = sys.argv[1] if len(sys.argv) > 1 else None

    if ASSESSMENT_ID:       

        try:
            result = upload_pdf(API_URL, ASSESSMENT_ID, FILE_PATH)
            print("Response:", result)
        except Exception as e:
            print("Error:", e)
    else:
        print("Usage: python upload_pdf.py <assessment_id>")