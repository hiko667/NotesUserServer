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
            raise Exception(f"Status code came wrong. Message: {response_data["message"]}")
        else:
            f.write(f"Account creation test succesful. Message: {response_data["message"]}, https code: {response.status_code}")
    except Exception as e:
        f.write(f"Failure. Message: {response_data["message"]}, code: {response.status_code}")
    
def get_token(username, passwrod, f):
    try:
        data = {"username": username, "password": passwrod}
        response = requests.post("http://localhost:5000/api/user/verify_login", json=data)
        response_data = response.json()
        if response.status_code > 300:
            raise Exception(f"Status code came wrong. Message: {response_data["message"]}")
        else:
            token = response_data["token"]
            f.write(f"Account token returned succesfuly. Message: {response_data["message"]}. Code: {response.status_code}, Token: {token}")
    except Exception as e:
            f.write(f"Failure. Message: {response_data["message"]}, code: {response.status_code}")



def test():
    username = "test_user"
    password = "super_secure"
    with open(f"test_raport{str(time)}", "w") as f:
        new_user(username, password, f)
        
test()