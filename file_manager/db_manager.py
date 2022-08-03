import sqlite3, os
import json5
from util.collection import Collection
from util.book import Book

class DBPipe:
    def __init__(self, db_file : str, save_config  = True):
        self.db_file = db_file
        self.save_config = save_config

    def __enter__(self):
        #create the connection and return it
        self.connect = sqlite3.connect(self.db_file)

        return self.connect.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.save_config:
            self.connect.commit()

        self.connect.close()
        del self

class DBManager:

    db_path = "db/main.db"
    tag_file_path = "db/tags.json"

    default_tags = {
        "physics" : [],
        "science" : [],
        "chemistry" : [],
        "mathematics" : [],
        "story" : [],
        "history" : [],
    }

    @staticmethod
    def buildDatabase():

        if not os.path.exists(DBManager.db_path):
            os.mkdir("db") # make the db folder

        # create the db connection
        connect = sqlite3.connect(DBManager.db_path)
        cursor = connect.cursor()

        # create the data base for collection and books
        cursor.execute(""" CREATE TABLE collections(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                    name VARCHAR(50) NOT NULL,
                                    des TEXT,
                                    index_ VARCHAR(100) NOT NULL,
                                    is_fav BOOLEAN NOT NULL)""")

        cursor.execute("""
                    CREATE TABLE books(
                                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                                path TEXT NOT NULL,
                                name TEXT NOT NULL,
                                index_ VARCHAR(100) NOT NULL,
                                is_fav BOOLEAN NOT NULL)""")
        # save the changes
        connect.commit()
        connect.close() # close the connection
        print("[INFO] DATABASE CREATE SUCCESSFUL")

        # create the tag json files
        with open(DBManager.tag_file_path, "w") as file:
            json5.dump(DBManager.default_tags , file, indent=4)

        # create the directory with name thumbnails
        os.mkdir("thumbs")

        print("[INFO] TAGS FILE CREATE SUCCESSFUL")

    @staticmethod
    def addCollection(name , root_index , des = "" , is_fav = False, tags = []):

        index = DBManager.getHighestIndex(root_index)
        # create the collection
        with DBPipe(DBManager.db_path, True) as cursor:
            cursor.execute(f"""
                        INSERT INTO collections(name , des , index_ , is_fav)
                                    VALUES('{name}', '{des}', '{index}', {is_fav})""")

            cursor.execute(f"""SELECT id FROM collections WHERE index_ = '{index}' """)
            id = int(cursor.fetchall()[0][0])

        # update the tags
        if tags:
            DBManager.updateTags(id , tags)

    @staticmethod
    def updateTags(id : int , tags : list[str] , type = "c"):

        # open the tag json file and update it
        with open(DBManager.tag_file_path) as file:
            data = json5.load(file)

        for tag in tags:
            if tag in data.keys():
                if data.get(tag).get(type):
                    data.get(tag).get(type).append(id)
                else:
                    data.get(tag)[type] = [id, ]

        # save the json file
        with open(DBManager.tag_file_path, "w") as file:
            json5.dump(data, file, indent=4)

    @staticmethod
    def addBook(path , index , is_fav = False, tags = []):

        # separate the name from the path
        name = os.path.split(path)[1].split(".")[0]
        with DBPipe(DBManager.db_path , True) as cursor:
            cursor.execute(f"""
                            INSERT INTO books(path , name, index_ , is_fav)
                                        VALUES('{path}', '{name}', '{index}', {is_fav})""")

            cursor.execute(f"""SELECT id FROM books WHERE path = '{path}' AND index_ = '{index}' """)
            id = int(cursor.fetchall()[0][0])
        if tags:
            DBManager.updateTags(id , tags , "b")

        return id

    @staticmethod
    def getCollections(index, order_by = "name"):

        with DBPipe(DBManager.db_path) as cursor:
            cursor.execute(f"SELECT * FROM collections WHERE index_ LIKE '{index}%' ORDER BY {order_by} ")
            data = cursor.fetchall()

            # create the collection object list and return it
            collection_list = []
            for coll in data:
                c = Collection(coll[1], coll[2], coll[3], coll[4])
                collection_list.append(c)

        return collection_list


    @staticmethod
    def getBooks(index , order_by = "name"):

        with DBPipe(DBManager.db_path) as cursor:
            cursor.execute(f"""SELECT * FROM books WHERE index_ = '{index}' ORDER BY {order_by} """)
            data = cursor.fetchall()

            # create the book object list
            book_list = []
            for book in data:
                b = Book(book[2], book[3], book[1], book[-1], book[0])
                book_list.append(b)


        return book_list

    @staticmethod
    def getIndexes():
        with DBPipe(DBManager.db_path) as cursor:
            cursor.execute("""SELECT index_ FROM collections""")
            data = [item[0] for item in cursor.fetchall()]

        return data

    @staticmethod
    def getHighestIndex(root_index : str):

        # first get the all of indexes of collections
        indexes = DBManager.getIndexes()
        if indexes == []:
            return "1"
        # filter the index start with given index
        filter_index = [index for index in indexes if index.startswith(root_index)]

        numbers = [int(item.split["/"][-1]) for item in filter_index]
        new_number = max(numbers) + 1

        # return the new index
        return f"{root_index}/{new_number}"
