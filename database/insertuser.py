import psycopg2
from psycopg2 import Error

def insert_users(conn):
    try:
        cursor = conn.cursor()

        # Sample test data for Users table
        users_data = [
            ("user1@gmail.com", "password_hash_1", "user1"),
            ("user2@gmail.com", "password_hash_2", "user2"),
            ("user3@gmail.com", "password_hash_3", "user3")
        ]

        # SQL query to insert test data into Users table
        insert_query = """INSERT INTO public.user (username, password, name)
                          VALUES (%s, %s, %s)"""

        # Execute the SQL query for each user
        for user_data in users_data:
            cursor.execute(insert_query, user_data)

        # Commit the transaction
        conn.commit()
        print("Test data inserted into Users table successfully.")

    except (Exception, Error) as error:
        print("Error inserting test data into Users table:", error)

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

        # Call function to insert test data into Users table
        insert_users(connection)

    except (Exception, Error) as error:
        print("Error connecting to PostgreSQL database:", error)

    finally:
        # Close database connection
        if connection:
            connection.close()
            print("PostgreSQL connection is closed.")

# Call the main function to insert test data into Users table
insert_test_data()
