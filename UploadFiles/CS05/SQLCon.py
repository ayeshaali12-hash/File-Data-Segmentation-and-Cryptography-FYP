import mysql.connector

def get_extension(node,password,port):
    try:
        print("Connecting to Node", node)
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)

        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        sql_get_query = """ SELECT extension, COUNT(DISTINCT filename) AS count FROM
         (SELECT DISTINCT filename, extension FROM testdata.segmenteddata) AS subquery GROUP BY extension;"""
        cursor.execute(sql_get_query)
        data = cursor.fetchone()
        extension,count = data
        return data
    except mysql.connector.Error as error:
        print("Failed getting data from MySQL table {}".format(error))



def insertblob(node_no, node, password, username, filename, extension, filedata, segmentno,port,nonce,authkey):
    try:
        print("Connecting to Node", node)
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)

        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        print("Inserting Segment into the Database\n______________________________________")
        cursor.execute('''CREATE DATABASE IF NOT EXISTS testdata''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS testdata.segmenteddata (
                                          `id` int NOT NULL AUTO_INCREMENT,
                                          `username` varchar(150) DEFAULT NULL,
                                          `filename` varchar(15) DEFAULT NULL,
                                          `extension` varchar(5) DEFAULT NULL,
                                          `filedata` longblob,
                                          `segmentno` int DEFAULT NULL,
                                          `nonce` mediumblob,
                                          `authkey` mediumblob,
                                          PRIMARY KEY (`id`)
                                        ) ENGINE=InnoDB AUTO_INCREMENT=1034 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci''')

        sql_insert_blob_query = """ INSERT INTO testdata.segmenteddata
                          ( username, filename, extension,filedata,segmentno,nonce,authkey) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

        # Convert data into tuple format
        insert_blob_tuple = (username, filename, extension, filedata, segmentno ,nonce,authkey)
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Data Inserted Successfully into Node:", node,"with port no: ",port)
        error_value = 0
        return node_no,error_value

    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
        error_value = 1
        return node_no, error_value
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")



def readblob(node, password, username, filename, segmentid,port):
    print("Connecting to Node", node)
    try:
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)
        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        print("Reading Segment from the Database")
        sql_fetch_blob_query = """SELECT filedata,nonce,authkey FROM testdata.segmenteddata
         where username = %s and filename= %s and segmentno= %s"""
        cursor.execute(sql_fetch_blob_query, (username, filename, segmentid))
        record = cursor.fetchone()
        print("Data Read Successfully from Node:", node,"with port no: ",port, "\n______________________________________ ")
        if record:
            error_value = 0
            filedata, nonce, authkey = record
            return filedata,nonce, authkey,error_value
        else:
            print("no record is found")

    except mysql.connector.Error as error:
        print("Failed to read data due to {}".format(error))
        error_value = 1
        filedata, nonce, authkey = "","",""
        return filedata,nonce, authkey,error_value

    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("connection closed")
def deleteblob(node, password, username, filename,port):
    print("Connecting to Node", node)
    try:
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)
        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        print("deleting Segment from the Database")
        sql_fetch_blob_query = """delete FROM testdata.segmenteddata
         where username = %s and filename= %s """
        cursor.execute(sql_fetch_blob_query, (username, filename))
        connection.commit()
        print("Data deleted Successfully from Node:", node,"with port no: ",port,"\n______________________________________ ")

    except mysql.connector.Error as error:
        print("Failed to delete data due to {}".format(error))

def check_all_req_server_online(node, password,port):
    try:
        connection = mysql.connector.connect(host=node,
                                                 database='testdata',
                                                 user='root',
                                                 password=password,
                                                 port=port
                                                 )

        if connection.is_connected():
            error_value = 0
            return error_value

    except mysql.connector.Error as error:
        print("Failed to read data due to {}".format(error))
        error_value = 1
        return error_value


def serverdata(node, password,port):
    print("Connecting to Node", node)
    try:
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)
        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        print("Reading Segment from the Database")
        sql_fetch_blob_query = """SELECT count(*) FROM testdata.segmenteddata;"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchone()[0]
        print("Data Read Successfully from Node:", node, "with port no: ", port)
        cursor.execute("""SELECT sum(LENGTH(filedata)/1024/1024),extension  FROM testdata.segmenteddata group by extension;""")
        admin_record = cursor.fetchall()
        print("Data Read Successfully from Node:", node, "with port no: ", port,"\n______________________________________ ")
        if admin_record is None:
            admin_record=list[(0,0)]
        return record, admin_record

    except mysql.connector.Error as error:
        record = 'none'
        admin_record =list[(0,0)]
        return record, admin_record


def userdata(node, password,port, username):
    print("Connecting to Node", node)
    try:
        connection = mysql.connector.connect(host=node,
                                             database='testdata',
                                             user='root',
                                             password=password,
                                             port=port)
        cursor = connection.cursor()
        print("Successfully Connected to Node", node)
        print("Reading data from the Database")
        sql_fetch_blob_query = """SELECT sum(LENGTH(filedata)/1024/1024)  FROM testdata.segmenteddata
                                where username = %s"""
        cursor.execute(sql_fetch_blob_query, username)
        record = cursor.fetchone()[0]
        cursor.execute("""SELECT sum(LENGTH(filedata)/1024/1024),extension  FROM testdata.segmenteddata where  username = %s group by extension;""",username)
        ext_record = cursor.fetchall()
        print("Data Read Successfully from Node:", node, "with port no: ", port,"\n______________________________________ ")
        if ext_record is None:
            ext_record=list[(0,0)]
        return record,ext_record

    except mysql.connector.Error as error:
        #print("Failed to read data due to {}".format(error))
        record = 0
        ext_record=list[(0,0)]
        return record,ext_record

