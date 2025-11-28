from flask import Flask, request, jsonify
import sqlite3
import time

class database_proxy():
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        self.messenger = self.connection.cursor()
        self.messenger.execute("""CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY, 
                               username TEXT NOT NULL, 
                               password TEXT NOT NULL, 
                               token TEXT NOT NULL);""")
        self.messenger.execute("""
                               CREATE TABLE IF NOT EXISTS notes(
                               note_id TEXT PRIMARY KEY, 
                               user_id INTEGER, 
                               tags TEXT, 
                               category TEXT, 
                               content TEXT, 
                               FOREIGN KEY(user_id) 
                               REFERENCES users(id));""")
        self.connection.commit()
        #baza danych innit
    #user handling
    def new_user(self, username, password):
        self.messenger.execute("SELECT COUNT(*) FROM users")
        new_id = self.messenger.fetchone()[0]
        new_token = str(int(time.time()*10000)) + username
        print(new_id, new_token, username, password)
        self.messenger.execute(f"SELECT id FROM users WHERE id = {new_id}")
        if self.messenger.fetchone() == None:
            self.messenger.execute(f"INSERT INTO users (id, username, password, token) VALUES (?, ?, ?, ?)", (new_id, username, password, new_token))
        self.connection.commit()
    def verify_user(self, username, password):
        pass
    def update_password(self, username, token, new_password):
        pass
    def delete_user(self, username, token):
        pass
    #note handling
    def get_notes(self, user_id):
        pass
    def update_note(self, note):
        pass
    def delete_note(self, note_id):
        pass

class server():
    def __init__(self):
        self.db_communication = database_proxy("database.db")
        self.app = Flask(__name__)
        

        
        @self.app.route('/')
        def home():
            return "<h1>You should not be here</h1>"
        
        @self.app.route('/api/user/new', methods = ["POST"])
        def new_user():
            data = request.get_json()
            name = data.get("name")
            password = data.get("password")
            print(name, password)
            if not name or not password:
                return jsonify({"error": "Missing name or password"}), 400
            try:
                self.db_communication.new_user(name, password)
            except Exception as e:
                return jsonify({"error": f"An error has accured: {e}"}), 400
            return jsonify({"success": "Successfuly created new account", "username": f"{name}"})
        
        
        
if __name__ == '__main__':
    s = server()
    s.app.run(debug=True)
