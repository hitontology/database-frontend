# For local testing
echo "Please enter the database password"
read -s password
echo "HITO_DATABASE_PASSWORD = '$password'" > private.py
secretKey=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
echo "SECRET_KEY = '$secretKey'" >> private.py
python -m venv venv
. venv/bin/activate
pip install -r requirements.freeze.txt
deactivate
. venv/bin/activate
export FLASK_APP=app
export HITO_DATABASE_PASSWORD=$password
echo "HITO FAB initialized. If there is no user, run 'flask fab create-admin'. Run with 'flask run'."
