# Timeline

![timeline view](./timeline.png)


![details view](./timeline-details.png)


Requires postgres

```
$ psql -c "CREATE DATABASE research;"
$ pip install -r requirements.txt
$ ./manage.py migrate
$ mkdir db-files
$ ./manage.py createsuperuser # follow prompts
```

To update / create new events
```bash
$ fab create_json
```

To generate svg icons
```
$ npm run generate-icons 
```