
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
  GET /api/user/verify_login
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username to log in |
| `password`      | `string` | **Required**. password to log in |

##### Returns:


| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | accounts Username |
| `token`      | `string` | accounts token |

#### Update User

```http
  GET /api/user/verify_login
```

| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. username for which to change password |
| `token`      | `string` | **Required**. token to verify user (obteined during logging in)|
| `new_password`      | `string` | **Required**. new password|




