from hashlib import sha1


ALL_QUESTION_METADATA_FILE = "static/metadata/questions.tsv"
REPORT_FOLDER = "static/reports"

def __hash_func__(data: str) -> str:
    return sha1(data.encode()).hexdigest()

