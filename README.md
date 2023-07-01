# 🚀 Unlock Accounting System
A utility software that helps with summer camp shift organisation. 
The main goal, on the one hand, is to provide convenient tools for staff members and, 
on the other hand, is to establish solid communication with the IT-community 
and consolidate it using such information technologies.

Expected features:
- attendance record using QR codes;
- points accounting for activities such as lectures, workshops, etc;
- registration on activities;
- polls and surveys;
- reports;

## Project structure
UAS backend is written using the Django framework and currently consists 
of 6 modules.

| Module name | Description                                                                                         |
|-------------|-----------------------------------------------------------------------------------------------------|
| `unlock`      | Core Django module. Contains global settings and scripts.                                           |
| `admin_app`   | Responsible for the reports (participants scores, teams leaderboard, etc).                          |
| `bot_app`     | Responsible for communication with the frontend (bot). Provides API interface for other modules.    |
| `events_app`  | Responsible for broadcasts, registration on activities, polls and surveys.                          |
| `score_app`   | Counts participants scores, records attendance. Responsible for promo-codes emission and activation. |
| `users_app`   | Contains authentication logic and responsible for user management.                                  |

## Environment variables
| Variable                     | Required | Default value | Description                                                                                                                                           |
|------------------------------|----------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `UNLOCK_DEBUG`               | No       | `false`       | Toggles Django debug mode.                                                                                                                            |
| `UNLOCK_ALLOWED_HOSTS`       | No       | `[]`          | List of hosts, separated by a space character, that are allowed to connect to the application. Required in production. Do not required in debug mode. |
| `UNLOCK_SECRET_KEY`          | Yes      | -             | The key used by Djnago for security. Must be a secure random string.                                                                                  |
| `UNLOCK_DATABASE`            | No       | `sqlite`      | Name of the DBMS to use. Possible options: `sqlite` or `postgres`.                                                                                    |
| `UNLOCK_DATABASE_HOST`       | No       | `None`        | Database host. Do not required for sqlite.                                                                                                            |
| `UNLOCK_DATABASE_PORT`       | No       | `None`        | Database port. Do not required for sqlite.                                                                                                            |
| `UNLOCK_DATABASE_NAME`       | No       | `db.sqlite3`  | Database name. For sqlite specify the filename relative to the project root.                                                                          |
| `UNLOCK_DATABASE_USER`       | No       | `None`        | Database user. Do not required for sqlite.                                                                                                            |
| `UNLOCK_DATABASE_PASSWORD`   | No       | `None`        | Database user password. Do not required for sqlite.                                                                                                   |
| `UNLOCK_EMAIL_HOST`          | No       | `None`        | SMTP server host used to send email.                                                                                                                  |
| `UNLOCK_EMAIL_PORT`          | No       | `None`        | SMTP server port.                                                                                                                                     |
| `UNLOCK_EMAIL_HOST_USER`     | No       | `None`        | SMTP server user.                                                                                                                                     |
| `UNLOCK_EMAIL_HOST_PASSWORD` | No       | `None`        | SMTP server user password.                                                                                                                            |


Example development config:
```
UNLOCK_DEBUG=true
UNLOCK_SECRET_KEY=unsecure
```


## Development
Follow the steps below in order to set up development environment.
1. Install dependencies: `pip install -r requirements.txt`.
2. Create `config.env` at the root of the project and set required environment variables.
3. Migrate a database: `python manage.py migrate`.
4. Run server: `python manage.py runserver`.


## Deploy
Follow the steps below in order to deploy the system using Docker.
