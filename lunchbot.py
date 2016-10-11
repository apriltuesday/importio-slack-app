# LunchBot wants to know what's for lunch.
#
# Adapted with gratitude from
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#
# Author: April Shen
# Created on 2016-10-06

import os
import requests
import time
from datetime import date, datetime
from slackclient import SlackClient

from slack_app import get_attachments


# bot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
# how bot is addressed
AT_BOT = "<@" + BOT_ID + ">"
# default channel to post to (e.g. for polls)
CHANNEL = "#corsham-street"

# commands
MONDAY = 'monday'
TUESDAY = 'tuesday'
WEDNESDAY = 'wednesday'
THURSDAY = 'thursday'
FRIDAY = 'friday'
SATURDAY = 'saturday'
SUNDAY = 'sunday'
TODAY = 'today'
TOMORROW = 'tomorrow'

weekdays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
weekends = [SATURDAY, SUNDAY]
all_days = weekdays + weekends
relative = [TODAY, TOMORROW]

# column names
IMAGE_COL = 'Image'
TITLE_COL = 'Meal'
KEY_COL = 'Date'
# URL for data
DATA_URL = os.environ.get("SLACK_BOT_URL")


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def next_day(day):
    return (day + 1) % 7


def get_formatted_date(day):
    # want nearest future date on the given day
    desired_day = all_days.index(day)
    current = date.today()
    while current.weekday() != desired_day:
        current = current.replace(day=current.day+1)
    return current.strftime('%d %B %Y')


def get_actual_day(day):
    # for day = TODAY or YESTERDAY
    today = date.today().weekday()
    return all_days[today if day == TODAY else next_day(today)]


def get_cat():
    attach = []
    r = requests.get('http://thecatapi.com/api/images/get')
    if r.status_code == 200:
        attach = [{
            'image_url': r.url,
            'text': '<' + r.url + '|src>'
        }]
    return attach


def post_poll():
    response = "What did you think of today's lunch?\n:+1: Loved it!\n:-1: Please, never again..."
    val = get_formatted_date(get_actual_day(TODAY))
    attach = get_attachments(DATA_URL, TITLE_COL, IMAGE_COL, key_col=KEY_COL, key_val=val)

    print 'done'
    # Send response
    slack_client.api_call("chat.postMessage", channel=CHANNEL,
                          text=response, attachments=attach,
                          as_user=True)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Try typing a day of the week!"
    attach = None

    # weekdays
    for day in weekdays:
        if day in command:
            response = "Here's what's for lunch! Yum :yum:"
            # convert day to date, because of how data formatted
            date_string = get_formatted_date(day)
            attach = get_attachments(DATA_URL, TITLE_COL, IMAGE_COL, key_col=KEY_COL, key_val=date_string)

    # weekends
    for day in weekends:
        if day in command:
            response = "There's no lunch on the weekends! Have a cat instead :cat:"
            attach = get_cat()

    # relative
    for day in relative:
        if day in command:
            # compute which day, and handle command with that day
            actual_day = get_actual_day(day)
            handle_command(actual_day, channel)
            return # so it doesn't post twice

    print 'done'
    # Send response
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, attachments=attach,
                          as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    POLL_TIME = 14 # what hour to poll after
    POLLED = False # have we polled yet today?

    if slack_client.rtm_connect():
        print("LunchBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)

            # polling
            if not POLLED and (datetime.now().hour == POLL_TIME):
                post_poll()
                POLLED = True
            if datetime.now().hour > POLL_TIME:
                POLLED = False

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
