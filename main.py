import sys
import json
import re

# custom imrpots
import loadSongs as ls
import search


# this function can read lines of either song ID or song name
'''
Return:
    ids: list of song ids
    s_count: sucessfully processed songs
    f_count: songs that failed in intake
'''
def intake_song_general(filepath, songs):


    ids = [] # output, string of ids

    # all these have been stripped, will not match the original string
    list_of_titles = ls.list_of_titles(songs)

    id_to_title = ls.id_to_title(songs)
    title_to_ids = ls.title_to_id(songs)

    # read in files

    s_count = 0 #successes
    f_count = 0 #fails
    with open(filepath, 'r') as f:
            for line in f:
                ll = line.strip()
                if (ll.isdigit()): # IDs
                    id = int(ll)
                    if (id in id_to_title):
                        s_count += 1
                        ids.append(id)
                    else:
                        f_count += 1
                        print(f"id {id} not found.")

                else: # song name
                    res = search.return_best_match(ll, list_of_titles)
                    song_title = res[0]
                    if song_title:
                        s_count = 0
                        id = title_to_ids[song_title]
                        ids.append(id) #append song id as a string
                    else:
                        f_count += 1
                        print(f"no song found for song title: {ll}")
                        ids.append(-1)
                
                    
                    
    f.close()
    print()
    print("song titles based on search in songbase: ", ids)
    print()
    return ids, s_count, f_count

def insert_text_into_file(template_file, output_file, body):
    with open(template_file, 'r') as tf:

        template_content = tf.read()
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

def main():
    # command line arguments 
    demanded_songs = sys.argv[1] #song list
    songs_file = sys.argv[2]     #all songs database
    template_file = sys.argv[3]  #template latex file, with somewhere to insert body
    output_file = sys.argv[4]    #name of output file

    # read in song database (json)
    song_db = ls.import_json(songs_file)

    string_output = ""

    list_ids, s_count, f_count = intake_song_general(demanded_songs, song_db)
    count = 0

    # process song data 
    for id in list_ids:
        count += 1
        song_obj = ls.search_json_exact(song_db, "id", id) # should exist for sure, validaiton is already done
        if (song_obj is not None):
            print(f"{count} title: {song_obj['title']}, id: {song_obj['id']}")
            lyrics = song_obj["lyrics"]
            lyrics = delete_hashtag(lyrics)
            lyrics = insert_backslash_before_opening_bracket(lyrics)
            lyrics = insert_verse_spacing(lyrics)
            lyrics = "\\beginverse\n" + lyrics + "\n\\endverse"

            string_output += "\\beginsong{}\n"
            string_output += lyrics   
            string_output += "\n\\endsong{}\n"
     
        else: #should not happen
            print(f"song_obj {id} not found")

    insert_text_into_file(template_file, output_file, string_output) #generate file

    print(f"{count} songs generated. {f_count} songs failed to be found.")


    return string_output
if __name__ == "__main__":
    main()
