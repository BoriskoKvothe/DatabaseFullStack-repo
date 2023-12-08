import sqlite3

conn = sqlite3.connect('cranium_bones.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM tblbones")
bones = cursor.fetchall()
print(bones)
conn.close()


#project2_db/