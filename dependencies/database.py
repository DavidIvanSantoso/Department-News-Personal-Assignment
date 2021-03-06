from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def registration(self,username,password):
        cursor=self.connection.cursor(dictionary=True,buffered=True)
        sql="SELECT * from user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount>0):
            cursor.close()
            return "Existed"
        else:
            sql = "INSERT INTO user VALUES(0,'{}', '{}')".format(username, password)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return "Complete"
            
    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("User not found")
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == password):
                cursor.close()
                result.append("Login Berhasil")
                return 1
    
    def getallnews(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username':row['username'],
                'news': row['news']
            })
        cursor.close()
        return result
    
    def getnewsindex(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def delete(self,id):
        cursor = self.connection.cursor(dictionary=True,buffered=True)
        sql= "DELETE FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Success"
    
    def post(self,username,news):
        cursor = self.connection.cursor(dictionary=True,buffered=True)
        sql= "INSERT INTO news VALUES(0,'{}','{}',CURRENT_DATE)".format(username,news)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Success"
    
    def edit(self,id,news):
        cursor=self.connection.cursor(dictionary=True,buffered=True)
        sql="SELECT * news WHERE id = {}".format(id)
        cursor.execute(sql)
        sql="UPDATE news SET updatenews='{}'".format(news)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Succes"

class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='department_news',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())