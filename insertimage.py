# Inserts image files as BLOB data into our database musicals.db
# Modified from https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def updateBLOB(empId, vphoto, hphoto):
    try:
        sqliteConnection = sqlite3.connect('musicals.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_update_blob_query = """ UPDATE musicals SET vphoto = ?, hphoto = ? WHERE id =?"""

        vphoto = convertToBinaryData(vphoto)
        hphoto = convertToBinaryData(hphoto)
        # Convert data into tuple format
        data_tuple = (vphoto, hphoto, empId)
        cursor.execute(sqlite_update_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
updateBLOB(1, "/workspaces/112761527/finalproject/images/hamiltonv.jpg","/workspaces/112761527/finalproject/images/hamilton-inline-best-shows-1024x150.jpg")
updateBLOB(2,"/workspaces/112761527/finalproject/images/the phantom of opera_v.jpg","/workspaces/112761527/finalproject/images/the phantom of opera_h.jpg")
updateBLOB(3,"/workspaces/112761527/finalproject/images/3.mozart_v.jpg","/workspaces/112761527/finalproject/images/3.mozart_h.jpg")
updateBLOB(4,"/workspaces/112761527/finalproject/images/4.les mis_v.jpg","/workspaces/112761527/finalproject/images/4. les-miserable_h.jpg")
updateBLOB(5,"/workspaces/112761527/finalproject/images/4. west side story_v.jpg","/workspaces/112761527/finalproject/images/5.west side story_h.jpg")
updateBLOB(6,"/workspaces/112761527/finalproject/images/6.the book of mormon_v.jpg","/workspaces/112761527/finalproject/images/6.the book of mormon_h.jpg")
updateBLOB(7,"/workspaces/112761527/finalproject/images/7.wicked_v.jpg","/workspaces/112761527/finalproject/images/7.wicked_h.jpg")
updateBLOB(8,"/workspaces/112761527/finalproject/images/8.into the woods_v.jpg","/workspaces/112761527/finalproject/images/8.into the woods_h.jpg")
updateBLOB(9,"/workspaces/112761527/finalproject/images/9.cats_v.jpg","/workspaces/112761527/finalproject/images/8.into the woods_h.jpg")
updateBLOB(10,"/workspaces/112761527/finalproject/images/10.dear evan hansen_v.jpg","/workspaces/112761527/finalproject/images/10.dear evan hansen_h.jpg")
updateBLOB(11,"/workspaces/112761527/finalproject/images/11.miss saigon_v.jpg","/workspaces/112761527/finalproject/images/11.miss saigon_h.jpg")