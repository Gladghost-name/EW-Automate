from xml.etree import ElementTree
from songimport import *
import os

def dumps(txt):
    pass

def generate_lyrics(*args):
    lyrics = ""
    count = 1
    for elements in args:
        for element in elements:
            line = element[0]
            split_txt = line.text.splitlines()
            txt = [txt.strip() for txt in split_txt]
            temp = count
            if element[1] == "chorus":
                count = "Chorus"
            lyrics += str(count) + "." + "\n".join(txt) + "\n\n"
            count = temp
            count += 1
            del temp
    return lyrics


def backup(dbs_dir):
    songs_db_path = os.path.join(dbs_dir, "Songs.db")
    songwords_db_path = os.path.join(dbs_dir, "SongWords.db")
    create_backup(songs_db_path, songwords_db_path)

def dump(file: any,  dbs_dir):
    """dump the file into the databases."""
    tree = ElementTree.parse(open(file))
    song_tag = tree.find("song")
    title = song_tag.find("title").text
    author = song_tag.find("author").text
    copyright_ = song_tag.find("copyright").text
    ccli = song_tag.find("ccli").text
    lines_elements = [(verse.find("lines"), "verse") for verse in song_tag.findall("verse")]
    chorus_elements = [(chorus.find("lines"), "chorus") for chorus in song_tag.findall("chorus")]
    lyrics = generate_lyrics(lines_elements, chorus_elements)

    process_song(lyrics, title, author, copyright_, dbs_dir, "./output")


# dump("song.xml", "./Databases")
song_words_db = "./Databases/SongWords.db"
# show_db_tables(song_words_db)
# print(return_db_tables())
show_table_contents(song_words_db, "word")
