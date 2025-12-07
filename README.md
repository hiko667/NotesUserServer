
# Notes User Server

A simple api server for our remote notes app project

at [Bialystok University Of Technology](https://pb.edu.pl/)


## Authors

- [@hiko667](https://github.com/hiko667)
- [@Fern-KK](https://github.com/Fern-KK)
- [@Marchewer](https://github.com/Marchewer)


## Python Packages Required

To run this project, you need to have following python packages installed on your machine

`flask`

`sqlite3`

`time`


## Deployment

To deploy this project run

```bash
  git innit
  git clone https://github.com/hiko667/NotesUserServer
  python.exe api.py
```
It would run at http://localhost:5000/
or http://your_domain
## API Reference

#### New User


```http
  POST /api/user/new
```

| Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. new account username |
| `password` | `string` | **Required**. new account password |

#### Verify User

```http
  POST /api/user/verify_login
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username to log in |
| `password`      | `string` | **Required**. password to log in |

##### Returns


| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`      | `string` | "success" or "error" |
| `message`      | `string` | message describing a reason for status |
| `data : username`      | `string` | accounts username |
| `data : token`      | `string` | accounts token |

#### Update User

```http
  PATCH /api/user/update
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username for which to change password |
| `token`      | `string` | **Required**. token to verify user (obteined during logging in)|
| `new_password`      | `string` | **Required**. new password|

```http
  DELETE /api/user/delete
```
#### Delete User
| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username for account to be deleted |
| `password`      | `string` | **Required**. password for account to be deleted|
| `token`      | `string` | **Required**. token to verify with one fetched from database, based on given username and password|


#### Fetch Notes and Tasks

```http
  POST /api/notes/fetch
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username for which to fetch notes and tasks |
| `token`      | `string` | **Required**. token to verify user (obteined during logging in)|

##### Returns


| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`      | `string` | "success" or "error" |
| `message`      | `string` | message describing a reason for status |
| `data : notes`      | `list` | list of notes. Each note is a dictionary. Contains: category, content, tags[], title, note_id |
| `data : tasks`      | `list` | list of tasks. Each task is a dictionary. Contains: category, content, tags[], title, task_id, deadline, priority|

#### New Note

```http
  POST /api/notes/new
```

| Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username for account |
| `token` | `string` | **Required**. token for account |
| `title` | `string` | **Required**. notes title |
| `tags` | `list` | notes tags |
| `category` | `string` |  notes category |
| `content` | `string` |  content of the note |

#### Delete Note

```http
  DELETE /api/notes/delete
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username of account. Used to verify user |
| `token`      | `string` | **Required**. token to verify user (obteined during logging in)|
| `note_id`      | `int` | **Required**. id of note to be deleted. Obtained during fetching process |

#### Update Note

```http
  PATCH /api/notes/update
```

| Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username for account |
| `token` | `string` | **Required**. token for account |
| `title` | `string` | **Required**. notes title |
| `tags` | `list` | notes tags |
| `category` | `string` | notes category |
| `content` | `string` | **Required**. content of the note |
| `note_id`      | `int` | **Required**. id of note to be updated. Obtained during fetching process |

#### New Task

```http
  POST /api/tasks/new
```

| Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username for account |
| `token` | `string` | **Required**. token for account |
| `title` | `string` | **Required**. tasks title |
| `tags` | `list` | tasks tags |
| `category` | `string` |  tasks category |
| `content` | `string` | **Required**. content of the task |
| `priority` | `string` |  priority of the task |
| `deadline` | `string` |  deadline of the task |

#### Delete Task

```http
  DELETE /api/tasks/delete
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username of account. Used to verify user |
| `token`      | `string` | **Required**. token to verify user (obteined during logging in)|
| `task_id`      | `int` | **Required**. id of task to be deleted. Obtained during fetching process |

#### Update Task

```http
  PATCH /api/tasks/update
```

| Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username for account |
| `token` | `string` | **Required**. token for account |
| `title` | `string` | **Required**. tasks title |
| `tags` | `list` | tasks tags |
| `category` | `string` |  tasks category. |
| `content` | `string` | **Required**. content of the task |
| `priority` | `string` |  priority of the task.  |
| `deadline` | `string` |  deadline of the task.  |
| `task_id`      | `int` | **Required**. id of task to be updated. Obtained during fetching process |


## Documentation

[UML](//www.plantuml.com/plantuml/png/fLLDRzGm4BtxLrZbG8l8IeXRXL0H7qT0j3T0bcFFPaqTsxKdRQFI_qucU2Eyn5KHbzrutfituvd9v2oXZ3ZqbZ5bPKhy7EArKV0v-jlnZZtXxoJALYPuenHCi6w5d9ycQ3ivN6u-q2-N8J1sdpLA7r99LzOWlDoyzSw1GkCTLylZd_WGau-yXvJ0TH1PmuKmpXaKuZXXv3fB2oTxE9dWrdlBho6QxIZGNuARQKE2I8pdd4wpVI4J9k3M92oeX1k7l0CKCyNeGpp7oHLuAD0NIC6x1Dp1pQosGWuofHiVTS7F4Vx5PGXQ8eWzLalhzoFbiwgYmG923bnNgEIm1LGxeRn3SFZemZYFK0_sqUDC8zPQgWzxKok98SngjHuVkYv5Ly1f-Eiw5nDAD6AjNU5XRufBZCeL7X_wGEgUVMf_W49wQUzOaz_ZHNxdUpW-AUpbA9TOERObN1dHWb9KfAPG3bX9AEUfhbs5ARiANBIvghm2_zKeAZj5u1QsUCfp1qmVBFJW43Hlns-kMBySFTz9fotm7M98FCBL00aJWri5WLRdichVxosqRMaCSgcc4_LUUGrJ0epMvxoZbsdQynDA75AcKpWHCoCJV80eAOAWxImxickZo2BZo4bPj0Dbktm7w3NQwwD1IoxM9Fmw6Rvpb5tAe988dOzZcVjJrj1n9bxuSup6TNCTipoD-7_8vvC6gQrna8yX6XyDZbCOqd_risde6gnepD6B8_wiQUZ_y0DvEijBunAh-yWG2kA1ncRpkXo4qwLTx0oS7dhx2m00)

