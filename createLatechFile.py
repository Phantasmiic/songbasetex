from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape

# Sample song corpus
songs = [
    {
        "title": "Song One",
        "lyrics": """Line one of song one
Line two of song one
Line three of song one"""
    },
    {
        "title": "Song Two",
        "lyrics": """Line one of song two
Line two of song two
Line three of song two"""
    },
    # Add more songs as needed
]

def create_latex_song_document(songs):
    # Create a new document
    doc = Document()
    
    # Set document to two-column layout
    doc.preamble.append(Command('twocolumn'))
    
    # Add the title
    doc.preamble.append(Command('title', 'Songbook'))
    doc.preamble.append(Command('author', ''))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    
    # Add each song to the document
    for song in songs:
        with doc.create(Section(song['title'], numbering=False)):
            doc.append(NoEscape(r'\begin{verse}'))
            doc.append(NoEscape(song['lyrics'].replace('\n', r' \\ ')))
            doc.append(NoEscape(r'\end{verse}'))
    
    # Generate the PDF
    doc.generate_pdf('songbook', clean_tex=False)

# Generate the LaTeX document
create_latex_song_document(songs)