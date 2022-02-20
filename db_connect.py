import psycopg2 as ps2

class DataConnect:
    def __init__(self):
        try:
            self.con = ps2.connect(
                dbname = 'global_con_db',
                user = 'postgres',
                password = 'admin',
                host = '127.0.0.1',
                port = 5432 
                )
            self.con.autocommit = True
            self.cursor = self.con.cursor()
        except:
            print("error")

    
    def __del__(self):
        self.cursor.close()
        self.con.close()
        print("Соединение закрыто")


    def par_and_in_tb(self, str1, list1):
        str1 += " ("
        for item in list1:
            str1 += item +','

        str1 = str1.rstrip(str1[-1])
        str1 += ") " 
        return str1


    def cheack_data_bd(self, name_tb, name_cl, equality_cl, con_data):
        select_com = 'select count('
        select_com = self.par_and_in_tb(select_com, name_cl) + ') from ' + name_tb + ' where '

        if len(equality_cl) != len(con_data):
            print("ERROR блять")
            return
        
        for i in range (0, len(equality_cl)):
            select_com += str(equality_cl[i]) + ' = ' + str(con_data[i])  
            if i < len(equality_cl) - 1:
                select_com +=  ' and '
        print(select_com) 

        try:
            self.cursor.execute(select_com)
        except:
            print('ERROR: _cheack_data_db')
            return 

        if self.cursor.fetchall()[0][0] > 0:
            return False
        else:
            return True


    def par_and_in_tb(self, str1, list1):
        str1 += " ("
        for item in list1:
            str1 += item +','

        str1 = str1.rstrip(str1[-1])
        str1 += ") " 
        return str1

       
    def insert_db(self, name_tb, name_cl, new_data):
        insert_com = "insert into "+ name_tb
        insert_com = self.par_and_in_tb(insert_com, name_cl) + "values"
        insert_com = self.par_and_in_tb(insert_com, new_data)
        

        print(insert_com)
        try:
            self.cursor.execute(insert_com)
        except:
            "ERROR: insert_db"
    
    def custom_insert(self, com = None):
        if com ==  None:
            com = str(input())
        
        print(com)
        self.cursor.execute(com)
        
        try:
            self.cursor.execute(com)
        except:
            print('ERROR: custom_insert')
        
        

    def select_db(self, name_tb, name_cl, add_com = ''):
        select_com = 'select '
        select_com = self.par_and_in_tb(select_com, name_cl) + ' from ' + name_tb + add_com
        print(select_com)

        try:
            self.cursor.execute(select_com)
        except:
            print('ERROR: select_db')
            return

        return self.cursor.fetchall()


    def custom_select(self, com = None):
        if com == None:
            com = str(input())
        print(com)

        self.cursor.execute(com)

        try:
            self.cursor.execute(com)
        except:
            print('ERROR: custom_select')
            return
        
        return self.cursor.fatchall()