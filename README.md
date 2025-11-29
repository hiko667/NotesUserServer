
# Notes User Server

A simple api server for our remote notes app project


## Authors

- [@hiko667](https://github.com/hiko667)


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
| `category` | `string` | **Required** notes category. If there is no cathegory, send 'No Category' |
| `content` | `string` | **Required**. content of the note |


