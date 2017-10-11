#!/bin/bash
echo "----Setting environment variables for Simon Says----"

echo "Enter your psql database url:"
read database_url
export DATABASE_URL=$database_url


echo "Enter your app secret key:"
read app_secret
export APP_SECRET_KEY=$app_secret


echo "Enter your salt string:"
read salt
export SALT=$salt
