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


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Try typing a day of the week!"

    # weekdays
    for day in weekdays:
        if day in command:
            response = "Here's what's for lunch! Yum! :yum:"
            # TODO set api call params
            attach = X

    # weekends
    for day in weekends:
        if day in command:
            response = "There's no lunch on the weekends! Have a cat instead."
            attach = None # TODO http://thecatapi.com/api/images/get

    # relative
    for day in relative:
        if day in command:
            # compute which day, and handle command with that day
            today = date.today().weekday()
            actual_day = all_days[today if day == TODAY else (today+1)%7]
            handle_command(actual_day, channel)
            return # so it doesn't post twice

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
