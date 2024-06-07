from fuzzywuzzy import process

import loadSongs as ls

# List of strings to search within

def return_best_match(query, list_of_lyrics):
    match, score = process.extractOne(query, list_of_lyrics)

    print("Best match:", match)
    print("Similarity score:", score)
    print(f"match {match}, score {score}")

def test():
    db = ls.import_json('songs.json')
    songs = ls.list_of_lyrics(db)
    return_best_match('for her', songs)

test()