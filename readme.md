# Xero Api data fetch
## How to run
This project has been written in Python using a microframe work called flask.I have not used flask before but decided to use it here over Django to increase simplicity. 

Install virtualenv if not already installed 

    pip install virtualenv

create and activate a venv

    virtualenv venv

Follow the guide for activation in different platforms
https://virtualenv.pypa.io/en/stable/userguide/ 

once in the src folder simply use pip to install the requirements

    pip install -r requirements.txt 

Load the app using python

    python app.py
## Implementation overview
I have used the public credentials for integrating with xero and hence there is a landing page with a link to the oath flow which requires user interaction. The reason for this is problems experienced with *PyCrypto*, a library required for the private key implementation. My vision was to make this an api that synced the xero data and made it available for other applications. However the public credential developer method has the user interactions required to perform the sync and that ruined the api nature of the application.

When the user clicks on the sync button from the landing page, the oauth flow is started with xero. There is a table maintaining record of each interaction with xero, it also helps retrieve the credentials that are only required during the oath flow.

Once the credentials are verified, we fetch the data from xero's api and store it in the database. 

### Storing only new data
The data is saved if its new, for each record we check if its and updated version of an existing record, if so, we update else its ignored and if the record is new, we save that to our database.

![Simple db](db.png?raw=true "Overview")

All data is associated with an account. For the purpose of this implementation a sample account is added for all data to be associated with. The account is tied with the *consumer key*, and that is for the purpose of **this implementation only** since there are no authenticated users. When there are authenticated users, we can use uniquely identifying data for those users to associate with all this data. So for all the places we would need an unique data identifying an authenticated user, i've used consumer key.

While requesting data we only get the data that has been modified since the last time we synced with the api. For this purpose we maintain a column that tracks the date of last update. This can be cross examined with our sessions table for investigations. 

![Flow](seq.png?raw=true "App flow")