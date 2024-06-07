import requests, sys
from bs4 import BeautifulSoup
import json
import re

import loadSongs as ls
import search

# Function to fetch and parse song data from the URL

def read_ids(filepath):
    list_ids = []
    with open(filepath, 'r') as f:
        for line in f:
            ll = line.strip()
            list_ids.append(ll)
    return list_ids




def fetch_song_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

# Function to parse the HTML and extract song details
def parse_song_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    song_div = soup.find('div', {'data-react-class': 'SongApp'})

    if song_div:
        data_react_props = song_div.get('data-react-props')
        if data_react_props:
            song_data = json.loads(data_react_props)
            preloaded_song = song_data.get('preloaded_song', {})
            song_id = preloaded_song.get('id')
            title = preloaded_song.get('title')
            lyrics = preloaded_song.get('lyrics')

            return {
                'id': song_id,
                'title': title,
                'lyrics': lyrics
            }

    return None

def transform_song_numbers_to_urls(song_numbers):
    base_url = "https://songbase.life/"
    return [f"{base_url}{song_number}" for song_number in song_numbers]

# List of song URLs

song_ids = [
    6200, 200, 5
]

def insert_text_into_file(template_file, output_file, body):
    with open(template_file, 'r') as tf:
        template_content = tf.read()

        pattern = r'(#insert_here)'
        replacement = body
        #output = re.sub(pattern, replacement, template_content)

        output = template_content.replace('#insert_here', body)
        with open(output_file, 'w+') as wf:
            wf.write(output)
        print("output generated")
        wf.close()
    tf.close()


def delete_hashtag(text):
    pattern= r'#'
    return re.sub(pattern, '', text)

def insert_backslash_before_opening_bracket(text):
    # Use regular expression to add the specified character before any opening bracket
    pattern = r'(\[)'  # Matches opening brackets
    replacement = r'\\\1'  # Inserts the character before the matched bracket
    return re.sub(pattern, replacement, text)

def insert_verse_spacing(text):
    # Use regular expression to add the specified character before any opening bracket
    pattern = r'(\n\n)'  # Matches opening brackets
    replacement = r'\n\\endverse\n\\beginverse\n'  # Inserts the character before the matched bracket
    return re.sub(pattern, replacement, text)

# Main function to process the URLs
'''
def main():
    for url in song_urls:
        print(f"Fetching data from {url}")
        html_content = fetch_song_data(url)
        if html_content:
            song_data = parse_song_data(html_content)
            lyrics = song_data["lyrics"]
            lyrics = insert_backslash_before_opening_bracket(lyrics)
            lyrics = insert_verse_spacing(lyrics)
            lyrics = "\\beginverse\n" + lyrics + "\n\\endverse"
            if song_data:
                print(f"Song ID: {song_data['id']}")
                print(f"Title: {song_data['title']}")
                print(f"Lyrics: {lyrics}")
            else:
                print("Failed to parse song data.")
        else:
            print(f"Failed to fetch data from {url}")
'''

def main():
    demanded_songs = sys.argv[1]
    songs_file = sys.argv[2]
    template_file = sys.argv[3]
    output_file = sys.argv[4]

    song_db = ls.import_json(songs_file)
    song_ids = read_ids(demanded_songs)

    string_output = ""


    # process song data 
    for id in song_ids:
        song_obj = ls.search_json_exact(song_db, "id", int(id))

        if (song_obj is not None):
            print((song_obj)['title'])

            lyrics = song_obj['lyrics']
            lyrics = delete_hashtag(lyrics)
            lyrics = insert_backslash_before_opening_bracket(lyrics)
            lyrics = insert_verse_spacing(lyrics)
            lyrics = "\\beginverse\n" + lyrics + "\n\\endverse"

            string_output += "\\beginsong{}\n"
            string_output += lyrics   
            string_output += "\n\\endsong{}\n"
     
        else:
            print(f"song_obj {id} not found")

    insert_text_into_file(template_file, output_file, string_output) #generate file

    print(string_output)


    return string_output
if __name__ == "__main__":
    main()
