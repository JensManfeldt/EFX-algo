import mysql.connector
from mysql.connector import Error


try:
    connection = mysql.connector.connect(host='localhost',
                                     database='splidditfake',
                                     user='root',
                                     password='DetteErEtKodeord')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        
        instanceNumbers = []
        
        query = ("SELECT id FROM splidditfake.instances")
        cursor.execute(query)
 
        for first in cursor: 
            instanceNumbers.append(int(first[0]))         
        
        print(instanceNumbers)
        
        for i in range(len(instanceNumbers)):
            
            query = ("SELECT agent_id ,resource_id, value FROM splidditfake.valuations WHERE instance_id = " + str(instanceNumbers[i]))
            cursor.execute(query)
                
            with open("fakeData" + str(instanceNumbers[i]), "w+") as file: 
                for first, secound, thrid in cursor:
                    file.write(str(first) + ", " + str(secound) + ", " + str(int(thrid)) + "\n")
            
                
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")