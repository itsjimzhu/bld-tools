import genanki as ga
import pandas as pd     # Annoyingly, comms tend to have commas in them and ruin my csv
import numpy as np
import sys

# sys.argv[0] is the script name
# sys.argv[1] is the first argument, sys.argv[2] is the second, and so on
if len(sys.argv) == 3:
    file_path = sys.argv[1]
    sheet_name = sys.argv[2]
    print("File path: {}".format(file_path))
    print("Sheet name: {}".format(sheet_name))
else:
    print("Pass args {file_path} {sheet_name}")
    sys.exit(0)

sep = ""
sheet = pd.read_excel(file_path, sheet_name, dtype=str, header=None, index_col=None)

model = ga.Model(
    6939937105,
    'Algsheet', 
    fields=[
        {'name': 'Prompt'},
        {'name': 'Alg'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div style="display: flex; justify-content: center">{{Prompt}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer"><div style="display: flex; justify-content: center">{{Alg}}</div>',
        },
    ]
)
deck_id = np.random.randint(1<<30, 1<<31)
deck = ga.Deck(
    deck_id, 
    sheet_name,
)

rows, cols = sheet.shape 
for i in range(1, rows):
    for j in range(1, cols):
        title = sheet.iloc[i,0] + sep + sheet.iloc[0,j]
        content = sheet.iloc[i,j]
        if not isinstance(content, str):
            continue
        print(title, content)

        note = ga.Note(
            model=model, 
            fields=[title, content]
        )
        deck.add_note(note)

ga.Package(deck).write_to_file("{}.apkg".format(sheet_name))
            
