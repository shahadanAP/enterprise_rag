import psycopg2

try:

    connection = psycopg2.connect(
        database = "enterprise_rag"
    )

    #cursor object to excute sql command
    cursor = connection.cursor()

    #excusting a test query
    
    cursor.execute("INSERT INTO query_log (question, answer, confidence, sources, latency_ms ) VALUES (%s,%s,%s,%s,%s);", ("hru^", "i am fine", "10", "pdf", 5))
    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM query_log;")


    #fetch the result
    db_version = cursor.fetchone()
    print(f"The amount of rows in the server is : {db_version[0]}")

except Exception as error:
        print(f"error connecting to database{error}")


finally:
    if "cursor" in locals() and cursor:
        cursor.close()

    if "connection" in locals() and connection:
        connection.close()
        print("Databse connection closed")

    



