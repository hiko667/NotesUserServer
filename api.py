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

class note():
    def __init__(self, title, tags, category, content):
        self.title = title
        self.tags = tags
        self.category = category
        self.content = content
    def tagsToString(self):
        if self.tags == None:
            return ""
        return ";".join(self.tags)
    
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
                               title TEXT,
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
        res = self.messenger.fetchone()
        return (token == res[0])
        
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
                raise databaseException("One of the following was not given: username, password", 400)
            if self.user_exists(username):
                raise databaseException(f"User {username} already exists", 400)
            self.messenger.execute("SELECT id FROM users ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id = int(temp[0]) + 1 if temp[0] is not None else 0
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
            if not username or not password:
                raise databaseException("One of the following was not given: username, password", 400)
            self.messenger.execute("SELECT username, password, token FROM users WHERE username = ?", (username,))
            res = self.messenger.fetchone()
            if res == None:
                raise databaseException(f"Can not find user: {username}", 404)
            else:
                if password == res[1]:
                    return response(True, 200, "Correct password", {"username": username, "token": res[2]})
                else:
                    raise databaseException("Wrong password", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)

    def update_password(self, username, token, new_password)->response:
        try:
            if not username or not new_password:
                raise databaseException("One of the following was not given: username, new_password, token", 400)
            if self.verify_token(username, token):
                self.messenger.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username, ))
                self.connection.commit()
                return response(True, 202, "Password updated", None)
            else:
                raise databaseException("Wrong or damaged token", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
        
        
    def delete_user(self, username, password, token)->response:
        try:
            if not username or not password or not token:
                raise databaseException("One of the following was not given: username, password, token", 400)
            res = self.verify_user(username, password)
            if res.status == "error":
                return res
            elif res.data_bundle["token"] == token:
                self.messenger.execute("SELECT id FROM users WHERE username = ?", (username, ))
                id = self.messenger.fetchone()[0]
                self.messenger.execute("DELETE FROM users WHERE username = ?", (username, ))
                self.messenger.execute("DELETE FROM notes WHERE user_id = ?", (id, ))
                self.connection.commit()
                return response(True, 202, "Account deleted", None)
            else:
                raise databaseException("Wrong or damaged token", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandleda error: {e}", None)
            
    #note handling
    def new_note(self, username, token, newnote : note)->response:
        try:
            if not username or not token or not newnote.title or not newnote.content:
                raise databaseException("One of the following was not given: username, token, note title, note content", 400)
            elif not self.user_exists(username):
                raise databaseException(f"Can not find user: {username}", 404)
            elif not self.verify_token(username, token):
                raise databaseException("Wrong or damaged token", 401)
            else: 
             
                self.messenger.execute("SELECT id FROM users WHERE username = ?", (username, ))
                user_id = self.messenger.fetchone()[0]
               
                self.messenger.execute("SELECT note_id FROM notes ORDER BY rowid DESC LIMIT 1")
                temp = self.messenger.fetchone()
                new_id = int(temp[0]) + 1 if temp[0] is not None else 0
                print("lil najdżer")
                self.messenger.execute("INSERT INTO notes (note_id, user_id, title, tags, category, content) VALUES (?, ?, ?, ?, ?, ?)", (new_id, user_id, newnote.title, newnote.tagsToString(), newnote.category, newnote.content))
                self.connection.commit()
                return response(True, 201, "Note created successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    def get_notes(self, user_id)->response:
        pass
    def update_note(self, note)->response:
        pass
    def delete_note(self, note_id)->response:
        pass

class service_proxy():
    def __init__(self):
        ##boilerplate
        self.db_access = database_access("database.db")
        self.app = Flask(__name__)
        @self.app.route('/')
        def home():
            return "<h1>You should not be here</h1>"
        
        ##user handling
        @self.app.route('/api/user/new', methods = ["POST"])
        def new_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.new_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/verify_login', methods = ['POST'])
        def verify_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.verify_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/update', methods = ['PATCH'])
        def update_password():
            data = request.get_json()
            username = data.get("username")
            new_password = data.get("new_password")
            token = data.get("token")
            rez = self.db_access.update_password(username, token, new_password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/delete', methods = ['DELETE'])
        def delete_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            token = data.get("token")
            rez = self.db_access.delete_user(username, password, token)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        
        ##notes handling
        @self.app.route('/api/notes/new', methods = ['POST'])
        def new_note():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = data.get("tags")
            category = data.get("category")
            content = data.get("content")
            rez = self.db_access.new_note(username, token, note(title, tags, category, content))
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        
        
        
if __name__ == '__main__':
    service = service_proxy()
    service.app.run(debug=True)
#Test message