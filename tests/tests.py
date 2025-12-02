import requests
import json
from time import time
#http://localhost:5000/api/
def new_user(username, password, f):
    try:
        data = {"username": username, "password": password}
        response = requests.post("http://localhost:5000/api/user/new", json=data)
        response_data = response.json()
        if response.status_code > 300:
            raise Exception("Status code came wrong")
    
    except Exception as e:
        f.write


def test():
    username = "test_user"
    password = "super_secure"
    with open(f"test_raport{str(time)}", "w") as f:
        new_user(username, password, f)
        
test()