# importio-slack-app
Quick script to test integrating import.io and slack. Work in progress.

```
usage: slack-app.py [-h] [-d DATA] [-s SLACK] [-m MESSAGE] [-n NUM_ROWS]

Post import.io data to a slack channel

optional arguments:
  -h, --help            show this help message and exit
  -d DATA, --data DATA  url of json data from import.io
  -s SLACK, --slack SLACK
                        url of slack webhook
  -m MESSAGE, --message MESSAGE
                        message to include with post
  -n NUM_ROWS, --num_rows NUM_ROWS
                        max number rows of data to post
```

Note that to have an image show up, you need to have a column named 'Image' with a src or text field.

## To-Do
- should ideally only post the diff...
- also needs a scheduled import api, this needs to be scheduled to match
- how to get images robustly?