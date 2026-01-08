
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

[UML](//www.plantuml.com/plantuml/png/fLN1RXCn4BtxAwnoe9NOI8XRXL1HWMD1j3T0bhEU9APUU-kPRHkr_NTsB6U5qtKLn2LPptlptdWywpr3qf66pedMQKHv2V7Mjl0jXlljWtWbFsdIIutmiMrXXCrIwVGqGginuNhnXN-bxdiXdh96cSCgUECimRl5UV0UMhB1otPw_1iV8eOeEq04luOe6gcKzTwIKiT8KPeihRpku6I4bo4uUGlHhhQAmZNuH1iG8ZFUI5wb-4HcJC6zHIgeZ5jFSWsa4iMQVJpxv0wyPFGTi0yUGNguIsepv5uZteLe2dvs-9UKeJUQGEsmMbdfCTKpgsB00S5aN5UOpLu1jHlL1a_WwU36-41GDxi8b6ZCcYlrvMm-IcOeEzkjmwthKhm5qdXTrxaQKQOnQsuBBsUpBpCgMpZSUa_gINnT_eQM-ALz44r-ZoVvJUZW-AIC5wDSOkNO5d1rH0jAqP6QGZbW9Q6Sfxesm_Nggl1qp5Nb6VZPGN7RsK4wMD6fp2TWkzv11vx0oENsfo-kNqb1RhGt3kI6g4SPuMO091HmtqBFL-TqrNxUHT9jIr7cLeqhwsbS6HWB46QafpjwcgOT7qdJW9dETYfcHYQ47g9c1yMtirvptDYM8pfk9IkhvS3LJj-1Yq2JFbbodE8iqeyny4kINkEkM4sm3d5RrlvQDBnCnAjmIT7wTUfZbkSH_m_vl3AWZRCUyhAFDaHBsz66zTy_DWrlGnG7S_JsI8QcuV_z3-HfajVMewZdwBulY7iQYyNZXyoP9Yq23T63aHGO4Wmpxxd_kNOEfx1S3JuT4eepy6Ret1y0)

