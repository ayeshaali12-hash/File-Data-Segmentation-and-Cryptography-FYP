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
        sql_get_query = """ SELECT extension, COUNT(DISTINCT filename) AS count  as Total FROM
         (SELECT DISTINCT filename, extension FROM testdata.segmenteddata) AS subquery GROUP BY extension;"""
        cursor.execute(sql_get_query)
        data = cursor.fetchall()
        datalst = []
        print(len(data))
        for j in range(0,len(data)):
            extension,count,total = data[j]
            count = 0 + count
            print(count)
        for i in range(0,len(data)):
            dicdata = {}
            extension,count,total = data[i]
            dicdata['extension'] = extension
            dicdata['count'] = count
            dicdata['percentage'] = (count / total) * 100
            datalst.append(dicdata)
        print(data)
        print(datalst)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
get_extension("0.tcp.in.ngrok.io","18b116cs",16864)
