import sqlite3
import json
import pprint
from PIL import Image
from io import BytesIO
import pandas as pd

db_path = "out/main.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"{len(tables)} Tables found in main.db")
# for table in tables:
#     print("-", table[0])
    
# print("\n")

data = {"ews-data": {}}
for table in tables:
    table_name = table[0]
    # print(f"--- Content of table: {table_name} ---")
    data["ews-data"][table_name] = {}
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        for row in rows:
            for idx, v in enumerate(row):
                if column_names[idx] in list(data["ews-data"][table_name].keys()):
                    data["ews-data"][table_name][column_names[idx]].append(v)
                else:
                    data["ews-data"][table_name][column_names[idx]] = [v]
        if len(data["ews-data"][table_name]) <= 0:
            del data["ews-data"][table_name]
    except sqlite3.DatabaseError as e:
        print("Could not read table {table_name}: {e}\n")
        


def display_data(dict_, include_ = ..., name="DATA"):
    headings = list(dict_.keys())
    df = pd.DataFrame(dict_)
    print(headings)
    with pd.option_context(
    "display.max_rows", None,
    "display.max_columns", None,
    "display.max_colwidth", None,
    "display.width", None
):
        print(name.upper() + " TABLE")
        print(df[include_]) if include_ != ... else print(df.head())
        
# Close connection
conn.close()

table= "file"
cursor.execute(f"PRAGMA foreign_key_list({table});")
foreign_keys = cursor.fetchall()
display_data(data["ews-data"][table], name=table)
print(foreign_keys)

print(data["ews-data"].keys())



# print(data["ews-data"]["presentation"]["ready"])
# img = Image.open(BytesIO(data["ews-data"]["presentation"]["thumbnail"][1]))
# img.show()