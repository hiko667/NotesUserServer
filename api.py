from flask import Flask, request, jsonify
import sqlite3
import time

class response():
    def __init__(self, operation_success, http_response, operation_message, data_bundle):
        self.status = "success" if operation_success else "error"
        self.http_response = http_response
        self.operation_message = operation_message
        self.data_bundle = data_bundle

class databaseException(Exception):
    def __init__(self, content, code):
        self.content = content
        self.code = code
    
class database_access():
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
    #funckje użytkowe
    def verify_token(self, username, token)->bool: 
        self.messenger.execute("SELECT token FROM users WHERE username=?", (username,))
        response = self.messenger.fetchone()
        if response == None:
            return False
        else:
            if response[0] == token:
                return True
            else:
                return False
        
    def user_exists(self, username)->bool:
        self.messenger.execute("SELECT COUNT (*) FROM users WHERE username = ?", (username, ))
        if self.messenger.fetchone()[0] == 1:
            return True
        else:
            return False
        
    #user handling
    def new_user(self, username, password)->response:
        try:
            if not username or not password:
                raise databaseException("No username or password", 400)
            if self.user_exists(username):
                raise databaseException(f"User {username} already exists", 400)
            self.messenger.execute("SELECT COUNT(*) FROM users")
            new_id = self.messenger.fetchone()[0]
            new_token = str(int(time.time()*10000)) + username
            # print(new_id, new_token, username, password)
            self.messenger.execute(f"SELECT id FROM users WHERE id = {new_id}")
            if self.messenger.fetchone() == None:
                self.messenger.execute(f"INSERT INTO users (id, username, password, token) VALUES (?, ?, ?, ?)", (new_id, username, password, new_token))
            self.connection.commit()
            return response(True, 201, "Account created successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    
      
    def verify_user(self, username, password)->response:
        try: 
            self.messenger.execute("SELECT username, password, token FROM users WHERE username = ?", (username,))
            res = self.messenger.fetchone()
            if res == None:
                raise databaseException(f"Can not find user: {username}", 400)
            else:
                if password == res[1]:
                    return response(True, 200, "Correct password", {"username": username, "token": res[2]})
                else:
                    raise databaseException("Wrong password", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)

    def update_password(self, username, token, new_password):
        self.verify_token(username, token)
        self.messenger.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username, ))
        self.connection.commit()
    def delete_user(self, username, token):
        pass
    #note handling
    def get_notes(self, user_id):
        pass
    def update_note(self, note):
        pass
    def delete_note(self, note_id):
        pass

class service_proxy():
    def __init__(self):
        self.db_access = database_access("database.db")
        self.app = Flask(__name__)
        

        
        @self.app.route('/')
        def home():
            return "<h1>You should not be here</h1>"
        
        @self.app.route('/api/user/new', methods = ["POST"])
        def new_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.new_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/verify_login', methods = ['GET'])
        def verify_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.verify_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
            # if not username or not password:
            #     return jsonify({"error": "Missing name or password"}), 406
            # try:
            #     response = self.db_access.verify_user(username, password)
            # except Exception as e:
            #     return jsonify({"error": f"An error has occuerd: {e}"}), 400
            # return jsonify({"success": "Successfuly verified", "username": f"{username}", "token": f"{response}"})
        @self.app.route('/api/user/update', methods = ['PATCH'])
        def update_password():
            data = request.get_json()
            username = data.get("username")
            new_password = data.get("new_password")
            token = data.get("token")
            try:   
                self.db_access.update_password(username, token, new_password)
            except Exception as e:
                return jsonify({"error": f"An error has occured: {e}"}), 400
            return jsonify({"success": f"Successfuly updated password for user: {username}"}), 202
        
        
        
if __name__ == '__main__':
    service = service_proxy()
    service.app.run(debug=True)
#Test message