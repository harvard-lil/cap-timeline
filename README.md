Requires postgres

```
$ psql -c "CREATE DATABASE research;"
$ pip install -r requirements.txt
$ ./manage.py migrate
$ mkdir db-files
$ mkdir db-files/images
$ ./manage.py createsuperuser # follow prompts
```

To update / create new events
```bash
$ fab create_json
```