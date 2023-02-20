# FLASK FEEDBACK #

Flask Python app to create and maintain a database of users, hash their passwords, authenticate them, and track feedback those users have added.

## PATHS ##

**GET/POST /register** - Allows a user to register an account and processes registration.

**GET /users/<username>** - View user details and posted feedback.

**GET/POST /login** - Authenticates/logs in user.

**GET /logout** - Logs out user.

**POST /users/<username>/delete** - Deletes user.

**GET/POST /users/<username>/feedback/add** - Loads Add Feedback Form and validates/processes form to add feedback to user's account.

**GET/POST /feedback/<feedback_id>/update** - Loads Update Feedback Form and validates/processes updates.

**POST /feedback/<feedback_id>/delete** - Deletes feedback.