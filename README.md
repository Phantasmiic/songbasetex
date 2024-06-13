This program takes a list of songs as input, and generates a complete song document (pdf), for use in conferences, SSOT, etc. The source for all the song lyric and chord data is from songbase. LaTeX is used to format the documents.

### Run program with:  
`python3 main.py <list of songs > <database of songs> <template tex file> <output tex file>`

A TEX file will be produced, which you can either compile locally or with an online compiler.

If using pdflatex, run: `pdflatex output.tex`.

- list of song: ex: songs_list.txt has the songs you want to include in your packet. 

- database of songs: ex: songs.json is the name of the json file with all the songs. Collected from songbase.

- template.tex contains base styling for the document.
- output.tex - this file just needs to exist.

### Misc

Documentation for the song latex package found at: https://songs.sourceforge.net/songsdoc/songs.html#sec11.7

`Template.tex` contains many latex macros/settings that control spacing, page numbers, etc.

`enumitem.sty` is used for styling for the index.

### Improvements
- Create folder structure for outputs
- Long term: Find better way to save and edit the database file. Perhaps also automate updates to the database from songbase.
- Long term: Optimize song order placement, to minimize document length


