import json
import re

# Define the path to your JSON file

def import_json(filepath):
    json_file_path = filepath

    # Open the JSON file and parse its content
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    
    return data['songs']

def list_of_lyrics(songs):
    output = []
    for s in songs:
        # combine title and lyrics for better fuzzy searching results ('for her' caused problems)
        output.append(s["title"] +  " " + s['lyrics'])

    return output

def list_of_titles(songs):
    output = []
    for s in songs:
        clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', s['title']) #strip all special characters except spaces
        output.append(clean_title)

    return output

# return a dict, mapping ids to titles
def id_to_title(songs):
    output = {}
    for s in songs:
        clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', s['title'])
        output[s['id']] = clean_title #int 
    return output

# return a dict, mapping titles to ids
def title_to_id(songs):
    output = {}
    for s in songs:
        clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', s['title'])
        output[clean_title] = s['id']
    return output


def search_json_exact(data, field, value):  
    result = next((item for item in data if item[field] == value), None)
    return result