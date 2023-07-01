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

## Setup

