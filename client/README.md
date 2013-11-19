## Get The Data Set

	$ wget http://www.grouplens.org/system/files/ml-100k.zip
	$ unzip ml-100k.zip

## Modify AppKey and API Server Address in app_config.py

	APP_KEY = '<your appey>'
	API_URL = '<your API server>' 

## Import The Data

	$ python batch_import.py

## Run Movie Recommendation Application

	$ python movie_rec_app.py


	