import requests
import sqlite3
from pydantic import BaseModel, EmailStr

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT
);
'''
cursor.execute(create_table_query)
print("table is ready")

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
data = response.json()

class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str

for info in data:
    try:
        user_data = {
            "id": info["id"],
            "name": info["name"],
            "username": info["username"],
            "email": info["email"],
            "phone": info["phone"]
        }

        user = UserModel(**user_data)

        cursor.execute("INSERT INTO users (id, name, username, email, phone) VALUES(?, ?, ?, ?, ?)",
                       (info["id"], info["name"], info["username"], info["email"], info["phone"]))
        conn.commit()

        print(f"created user {info["id"]}:")

    except Exception as e:
        print(f"Error with user id {info["id"]}\n. {e}")

conn.close()
