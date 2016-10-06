# LunchBot wants to know what's for lunch.
#
# Adapted with gratitude from
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#
# Author: April Shen
# Created on 2016-10-06

import os
import time
from datetime import date
from slackclient import SlackClient

from slack_app import get_attachments


# bot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
# how bot is addressed
AT_BOT = "<@" + BOT_ID + ">"

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
TEXT_COL = 'Meal'
KEY_COL = 'Date'
# URL for data
DATA_URL = 'https://data.import.io/extractor/b2bf2d07-2485-451b-8718-ef6273640599/json/latest?_apikey=10fd4d0e33d846f382665a71ccdc153c77a750263b35622dc51271b446bf487f321b7fd4d0ec2cdc6e29201105536ca6cd84b316ebc6546aeab869dedb63245cdeb00fffdf2971071d421b3883422f0d'


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
            attach = get_attachments(DATA_URL, TEXT_COL, IMAGE_COL, key_col=KEY_COL, key_val=date_string)

    # weekends
    for day in weekends:
        if day in command:
            response = "There's no lunch on the weekends! Have a cat instead :cat:"
            # TODO http://thecatapi.com/api/images/get ?

    # relative
    for day in relative:
        if day in command:
            # compute which day, and handle command with that day
            today = date.today().weekday()
            actual_day = all_days[today if day == TODAY else next_day(today)]
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
    if slack_client.rtm_connect():
        print("LunchBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
