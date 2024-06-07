from fuzzywuzzy import process

import loadSongs as ls

# List of strings to search within
# return match, score
def return_best_match(query, list_of_lyrics):
    res = process.extractOne(query, list_of_lyrics)
    return res

def return_title_from_id(id, songs):
    for s in songs:
        # ids are stored as ints
        if s['id'] == int(id):
            return s['title']
    else:
        return ""

def test():
    db = ls.import_json('songs.json')
    #songs = ls.list_of_lyrics(db)
    songs = ls.list_of_titles(db)
    res = return_best_match('We love the church life', songs)

    match = res[0]
    score = res[1]
    ind = res[2]
    #print("Best match:", res)
    print(f"match: {match}, score: {score}, index: {ind}")

if __name__ == "__main__":
    test()
