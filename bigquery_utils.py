import json


def read_bigquery_schema_from_file(filepath):
    file_content = read_file(filepath)
    json_content = json.loads(file_content)
    return json_content


def read_file(filepath):
    with open(filepath) as file_handle:
        content = file_handle.read()
        return content
