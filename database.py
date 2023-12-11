import sqlalchemy as sa

def insert_data(name,phone_number):
    # Connect to the MySQL database
    engine = sa.create_engine("mysql+pymysql://root:Akashramdham@localhost:3306/chatbot")
    print("Successfully Connected to MySQL")

    # Insert data into the table

    engine.execute(f"INSERT INTO details (name,no) VALUES ('{name}','{phone_number}')")

    print("Data inserted successfully into the table")
