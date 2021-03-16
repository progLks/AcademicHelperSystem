import psycopg2



class ClientDB():

    def __init__(self):
        self.con = self.Connect(
            database="ClientDatabase", 
            user="postgres", 
            password="12345678", 
            host="127.0.0.1", 
            port="5432"
        )
        self.cur = self.con.cursor()

    def Connect(self, database, user, password, host, port):
        return psycopg2.connect(
            database=database, 
            user=user, 
            password=password, 
            host=host, 
            port=port
        )

    def Close(self):
        self.con.close()


    def CreateTableClients(self):
        self.cur.execute('''CREATE TABLE CLIENT  
            (ID SERIAL PRIMARY KEY NOT NULL,
            FIRSTNAME TEXT NOT NULL,
            SECONDNAME TEXT NOT NULL,
            SURNAME TEXT NOT NULL);''')


    def AddClient(self, firstname, secondname, surname):
        self.cur.execute(
            "INSERT INTO CLIENT (FIRSTNAME,SECONDNAME,SURNAME) VALUES ('"+ firstname+"','"+ secondname+"','"+ surname+"')"
        )
        self.con.commit()  
