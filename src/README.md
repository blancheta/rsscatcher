# Welcome on RSScatcher

RSScatcher is a project which helps you to subscribe rss feeds

and manage its for free.


## Requirements

```
# Install redis server

# Install virtualenvwrapper
sudo apt-get install python-pip python-dev build-essential
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pip

# Create virtualenv
mkvirtualenv rsscatcher -p python3
workon rsscatcher

# Install python dependancies
pip install -r requirements

deactivate
```

## Testing
```
./manage.py manage test
```

## Run Celery

```
celery -A rsscatcher worker -B
```

## Let's try

##### Admin

+ **username:** admin
+ **password:** adminadmin

##### User

+ **username:** test
+ **password:** passpass


### Pre-commit hook

Tests must be ok to commit

```
mv hooks/pre-commit .git/hooks/
```

### Useful commands

```
# Create a dump
./manage.py dumpdata --exclude=auth --exclude=contenttypes > fixtures.json
# Load demo data
./manage.py loaddata fixtures.json
```