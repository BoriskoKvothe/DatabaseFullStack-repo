import sqlite3

# Create or open a database file
conn = sqlite3.connect('cranium_bones.db')

# SQLite commands to create a new table
commands = '''
DROP TABLE IF EXISTS tblbones;
CREATE TABLE tblbones (
    boneID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT CHECK(category IN ('neurocranium', 'splanchnocranium'))
);
'''

# Execute the commands
cursor = conn.cursor()
cursor.executescript(commands)

# Close the connection
conn.close()

# Reconnect to the database
conn = sqlite3.connect('cranium_bones.db')
cursor = conn.cursor()

# List of cranial bones to insert
bones = [
    ('Frontal Bone', 'neurocranium'),
    ('Parietal Bone', 'neurocranium'),
    ('Temporal Bone', 'neurocranium'),
    ('Occipital Bone', 'neurocranium'),
    ('Sphenoid Bone', 'neurocranium'),
    ('Ethmoid Bone', 'neurocranium'),
    ('Temporal Bone - Left', 'neurocranium'),
    ('Temporal Bone - Right', 'neurocranium'),
    ('Parietal Bone - Left', 'neurocranium'),
    ('Parietal Bone - Right', 'neurocranium'),
    ('Mandible', 'splanchnocranium'),
    ('Vomer', 'splanchnocranium'),
    ('Nasal Bone', 'splanchnocranium'),
    ('Lacrimal Bone', 'splanchnocranium'),
    ('Zygomatic Bone', 'splanchnocranium'),
    ('Palatine Bone', 'splanchnocranium'),
    ('Inferior Nasal Concha', 'splanchnocranium'),
    ('Maxilla', 'splanchnocranium'),
    # The following are paired bones, so they appear twice
    ('Nasal Bone - Left', 'splanchnocranium'),
    ('Nasal Bone - Right', 'splanchnocranium'),
    ('Lacrimal Bone - Left', 'splanchnocranium'),
    ('Lacrimal Bone - Right', 'splanchnocranium'),
    ('Zygomatic Bone - Left', 'splanchnocranium'),
    ('Zygomatic Bone - Right', 'splanchnocranium'),
    ('Palatine Bone - Left', 'splanchnocranium'),
    ('Palatine Bone - Right', 'splanchnocranium'),
    ('Inferior Nasal Concha - Left', 'splanchnocranium'),
    ('Inferior Nasal Concha - Right', 'splanchnocranium'),
    ('Maxilla - Left', 'splanchnocranium'),
    ('Maxilla - Right', 'splanchnocranium')
]

# Insert data into the table
cursor.executemany('INSERT INTO tblbones (name, category) VALUES (?, ?)', bones)

# Commit changes and close the connection
conn.commit()
conn.close()
