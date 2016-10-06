# importio-slack-app

## slack_app
Quick script to test integrating import.io and slack. Work in progress.

```
usage: slack_app.py [-h] -d DATA -s SLACK [-m MESSAGE] [-t TEXT_COL]
                    [-i IMAGE_COL] [-n NUM_ROWS]

Post import.io data to a slack channel

optional arguments:
  -h, --help            show this help message and exit
  -d DATA, --data DATA  url of json data from import.io
  -s SLACK, --slack SLACK
                        url of slack webhook
  -m MESSAGE, --message MESSAGE
                        message to include with post
  -t TEXT_COL, --text_col TEXT_COL
                        name of column to use as main text
  -i IMAGE_COL, --image_col IMAGE_COL
                        name of column to use as main image
  -n NUM_ROWS, --num_rows NUM_ROWS
                        max number rows of data to post
```

## lunchbot
A bot to post lunches from City Pantry.

## To-Do
- should ideally only post the diff...
- also needs a scheduled import api, this needs to be scheduled to match
- how to get images robustly?