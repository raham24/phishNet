import psycopg2
from psycopg2 import Error
from time import gmtime, strftime

def insert_attempts(conn):
    try:
        cursor = conn.cursor()

        # Sample test data for Phishing Attempts table
        attempts_data = [
            (strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'http://phishing-site.com', 1, 5),
            (strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'http://phishing-site2.com', -1, 6),
            (strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'http://phishing-site3.com', 0, 7)
        ]

        # SQL query to insert test data into Phishing Attempts table
        insert_query = """INSERT INTO "phishingAttempts" ("timestamp", phishing_url, decision_tree_prediction, user_id)
                          VALUES (%s, %s, %s, %s)"""

        # Execute the SQL query for each attempt
        for attempt_data in attempts_data:
            cursor.execute(insert_query, attempt_data)

        # Commit the transaction
        conn.commit()
        print("Test data inserted into Phishing Attempts table successfully.")

    except (Exception, Error) as error:
        print("Error inserting test data into Phishing Attempts table:", error)

    finally:
        # Close the cursor
        cursor.close()

def insert_test_data():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(user="postgres",
                                      password="673636",
                                      host="localhost",
                                      port="5432",
                                      dbname="postgres")

        # Call function to insert test data into Phishing Attempts table
        insert_attempts(connection)

    except (Exception, Error) as error:
        print("Error connecting to PostgreSQL database:", error)

    finally:
        # Close database connection
        if connection:
            connection.close()
            print("PostgreSQL connection is closed.")

# Call the main function to insert test data into Phishing Attempts table
insert_test_data()
