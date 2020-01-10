# Timeline
[![CircleCI](https://circleci.com/gh/anastasia/timeline.svg?style=svg)](https://circleci.com/gh/anastasia/timeline)

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

Create settings
```
$ cp timeline/settings/settings.example.py timeline/settings.py

```

To update / create new events
```bash
$ fab create_json
```

To generate svg icons
```
$ npm run generate-icons 
```
