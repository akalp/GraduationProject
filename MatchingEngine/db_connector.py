import psycopg2
from decouple import config


def connectDB():
    try:
        connection = psycopg2.connect(user=config('DB_USER'),
                                      password=config('DB_PASSWORD'),
                                      host=config('DB_HOST'),
                                      database=config('DB_NAME'))

        #cursor = connection.cursor()s
        #  Print PostgreSQL Connection properties
        #print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        #cursor.execute("SELECT version();")
        #record = cursor.fetchone()
        #print("You are connected to - ", record, "\n")
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
