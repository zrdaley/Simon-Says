# Simon Says
**A Flask app to Play the classic memory game**

Play at https://simon-says-by-zen.herokuapp.com

## Gameplay Instructions

1. Follow the link and create a new account or log in with existing credentials
2. Click the yellow `START` button at the bottom of the page
3. 1+ of the four coloured buttons will flicker gray
4. Click the button(s) that flickered in the order that they occured in step 4
5. Repeat steps 4 & 5

*Based on: https://en.wikipedia.org/wiki/Simon_(game)#Gameplay*


## Local Set Up Instructions

1. Clone the repo
2. Navigate to the setup folder `cd setup`
3. Create a local SQL database with the schema specified in `create_db.sql`
4. Run the environment variable setting script `source set_env.sh`
5. You will be prompted to enter 3 values:
    - DATABASE URL: This should be the url to the database you created in step 3 (ex. postgresql://localhost/simon_says)
    - APP SECRET KEY: This is a randon key used to encrpyt cookies
    - SALT: This is a random key used to enhance password encryption (See: https://en.wikipedia.org/wiki/Salt_(cryptography))
6. Return to the root directory for the repository
7. Install requirements with `pip install -r requirements.txt`
8. Run `python app.py` to start the application
9. The local application will be available via `127.0.0.1:5000` in your web browser