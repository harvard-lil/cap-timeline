# Timeline

![timeline view](https://hu-my.sharepoint.com/personal/aaizman_law_harvard_edu/Documents/timeline/timeline.png)


![details view](https://hu-my.sharepoint.com/personal/aaizman_law_harvard_edu/Documents/timeline/timeline-details.png)

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

To generate svg icons
```
$ npm run generate-icons 

```