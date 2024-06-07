import json

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


def search_json_exact(data, field, value):  
    result = next((item for item in data if item[field] == value), None)
    return result

#db = import_json('songs.json')
#print(search_json_exact(db, 'id', 1)['title'])