import sqlite3

#ToDo: Database für Databases
class DATABASE:
    def __init__(self, name, verbose=False):
        self.__name_db = name
        self.__verbose = verbose
        
    def create_new_db(self):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        #Lege Tabelle für die Bücher an
        sql_command = "CREATE TABLE books ( "
        sql_command+= "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        sql_command+= "title VARCHAR(1000), "
        sql_command+= "path VARCHAR(1000), "
        sql_command+= "year INTEGER, "
        sql_command+= "datatype VARCHAR(10), "
        sql_command+= "author_id INTEGER);"
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        
        #Lege Tabelle für Autoren an
        sql_command = "CREATE TABLE authors ( "
        sql_command+= "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        sql_command+= "author_name VARCHAR(50));"
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        
        #Lege Hilfstabelle an
        sql_command = "CREATE TABLE book_author ( "
        #sql_command+= "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        sql_command+= "book_id INTEGER, "
        sql_command+= "author_id INTEGER, "
        sql_command+= "FOREIGN KEY(book_id) REFERENCES books(id), "
        sql_command+= "FOREIGN KEY(author_id) REFERENCES authors(id), "
        sql_command+= "PRIMARY KEY(book_id, author_id));"
        crsr.execute(sql_command)
        if self.__verbose: print(sql_command)
        connection.commit()
        connection.close()
        
    def insert_new_dataset(self, title, year, authors, path, datatype):
        #ToDo: Wenn ein Autor schon in der Tabelle "Autor" ist, darf kein neuer Eintrag erstellt werden. Suche also nach dem Autoren (mit Gleich, nicht LIKE). Wenn die Kombination der Autoren schon vorhanden ist, nimm die ID aus "book_author", ansonsten lege eine neue ID an. Wenn das Buch vorhanden ist, lehne das Einfügen ab
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        sql_command = "INSERT INTO books(title, path, year, datatype, author_id) "
        sql_command += "VALUES ('{}', '{}', {}, '{}', {});".format(title, path, year, datatype, 1)
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        
                
        #Überprüfe, ob die Autoren schon in der Datenbank sind
        for author in authors:
            select = self.find_author(author)
        
            if len(select) == 0:
                sql_command = "INSERT INTO authors(author_name) "
                sql_command += " VALUES ('{}')".format(author)
                sql_command += ";"
                if self.__verbose: print(sql_command)
                crsr.execute(sql_command)
                connection.commit()
                author_id = -1
            else:
                author_id = select[0][0]
                
            #Füge einen neuen Datensatz ein
            sql_command = "INSERT INTO book_author(book_id, author_id) "
            sql_command+= "VALUES ({}, {});".format(-1, author_id)
            if self.__verbose: print(sql_command)
            crsr.execute(sql_command)
            connection.commit()
            
            #Füge Buch-ID ein
            sql_command = "UPDATE book_author "
            sql_command+= "SET book_id = (SELECT id FROM books WHERE title = '{}') ".format(title)
            sql_command+= "WHERE book_id = -1;"
            if self.__verbose: print(sql_command)
            crsr.execute(sql_command)
            connection.commit()
            
            #Füge Autoren-ID ein
            sql_command = "UPDATE book_author "
            sql_command+= "SET author_id = (SELECT id FROM authors "
            sql_command+= "WHERE author_name = '{}') ".format(author)
            sql_command+= "WHERE author_id = -1;"
            if self.__verbose: print(sql_command)
            crsr.execute(sql_command)
            connection.commit()
        connection.close()   
        
    def find_book(self, title="", year=-1, like_equal="LIKE"):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        sql_command = "SELECT * FROM books "
        sql_command += " WHERE title LIKE '%{}%';".format(title)
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        connection.commit()
        connection.close()
        return table
        
    def find_author(self, author="", like_equal="LIKE"):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        sql_command = "SELECT * FROM authors "
        sql_command += " WHERE author_name LIKE '%{}%';".format(author)
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        connection.commit()
        connection.close()
        return table
        
    def update_title(self, old_id, new_title):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        sql_command = "UPDATE books SET title = '{}' ".format(new_title)
        sql_command += " WHERE id = {};".format(old_id)
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        connection.commit()
        connection.close()
        
    def select_star(self):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        sql_command = "SELECT * FROM books;"
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        for row in table:
            print(row)
        
        sql_command = "SELECT * FROM authors;"
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        for row in table:
            print(row)
        connection.commit()
        
        sql_command = "SELECT book_id, author_id FROM book_author;"
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        for row in table:
            print(row)
        connection.commit()
        connection.close()
        
    def show_all(self):
        connection = sqlite3.connect(self.__name_db)
        crsr = connection.cursor()
        
        sql_command = "SELECT * "
        sql_command+= "FROM books "
        sql_command+= " LEFT JOIN (book_author LEFT JOIN authors ON authors.id = book_author.author_id) "
        sql_command+= " ON books.id = book_author.book_id; "
        if self.__verbose: print(sql_command)
        crsr.execute(sql_command)
        table = crsr.fetchall()
        for row in table:
            print(row)
            
        connection.commit()
        connection.close()