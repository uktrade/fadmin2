# FFT

## The Project

## Set up

A database called "fido" will be automatically created.

Run the following to perform initial migrations:

```
make migrate
```

In order to add stub data for local development purposes run:

```
make create-stub-data
```

You can add forecast data if you are developing forecast related functions:

```
docker-compose run fido python manage.py create_stub_forecast_data
```

You can add Gift and Hospitality data if you are developing Gift and Hospitality related functions:

```
make gift-hospitality-table
```

Now access any page within the site and log in with your single sign on credentials.

You now need to elevate your user permissions in order to access the admin tool. You can do this by running:

```
make elevate
```

### Compile the front end
```
make compilescss & make collectstatic
```

### Environment variables

You need to populate the .env file in the project root folder with the following variables:

* AUTHBROKER_CLIENT_ID
* AUTHBROKER_CLIENT_SECRET

These can be provided by a member of the team.

### Integration between Django and React

The process described in this post was followed: 
https://www.techiediaries.com/django-react-rest/

To enable the forecast edit interface:
```
npm start
```

### Running docker-compose run with port access
```
docker-compose run --service-ports
```

### Important notes on design

We use Django Guardian for model instance level permissions https://github.com/django-guardian/django-guardian

Django Guardian **should not be used directly**. There is a set of wrapper functions in *forecast.permission_shortcuts*

These add an additional permission check for the user being able to view forecasts at all.

### Creating data/non-auto migrations
When adding data or non-auto generated migrations, please use the convention:
```
[number]_data_[date]_[time]
```
for example:
```
0004_data_20200501_1345
```

### Running manage.py on an app droplet
```
/home/vcap/deps/1/bin/python3.6 ~/app/manage.py
```

### Running BDD tests

## Run BDD front end from host machine
```
npm run bdd
```

## SSH into web container
```
docker-compose exec fido bash
```

## Run BDD tests
```
python manage.py behave --settings=config.settings.bdd
```


### Notes
In order to get the node docker container working, this guide was followed: https://jdlm.info/articles/2019/09/06/lessons-building-node-app-docker.html

### Product URLs

#### Dev URL
https://fft.trade.dev.uktrade.digital/core/

#### Production URL
https://fft.trade.gov.uk/core/

### Managing user permissions

4 management commands have been added to make dealing with user cost centre easier:

 * add_user_to_cost_centre
 * cost_centre_users
 * remove_user_from_cost_centre
 * user_permissions
 
The names of the management commands denote their function.

### Permissions within the system
#### Any logged in SSO user
 * Access Chart of Account Gifts and Hospitality Register
#### Specific permissions
 * Upload budget and Oracle actuals file
 * Download Oscar report file
 * View forecast (permission to view all forecast data)
 * Edit 1 - n cost centres (specific user can edit cost centre data)

#### Migrating to new user model (to be removed once complete)
 * Take the system off line
 * Add username field to HistoricalUser table (max length 150, allow null)
 * Amend the custom_usermodel table to be the same as the new User app one
 * Add the user app initial migration to the list of django migrations that have been run
 * Deploy new codebase
