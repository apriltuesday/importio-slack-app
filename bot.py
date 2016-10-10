# Import.io Slackbots for all!
#
# Adapted with gratitude from
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#
# Author: April Shen
# Created on 2016-10-10

import os
import requests
import time
from datetime import date
from slackclient import SlackClient

from config import config

# how bot is addressed
AT_BOT = '<@{}>'.format(config.SLACK_BOT_ID)

# instantiate Slack client
slack_client = SlackClient(config.SLACK_BOT_TOKEN)


def post_webhook():
    payload = {'text': config.MESSAGE}
    payload['attachments'] = get_attachments()

    # Make the POST request
    requests.post(slack_url, json=payload)
    print('Done!')


def get_attachments(key_val=None):
    attachments = []
    # Get the data
    r = requests.get(config.IMPORT_DATA_URL)
    if r.status_code == 200:
        print('Data request successful')
        data = r.json()['result']['extractorData']['data'][0]['group']
        data = data[:config.NUM_ROWS] if config.NUM_ROWS else data

        # Make one attachment for each data row
        for d in data:
            if config.KEY_COL and (config.KEY_COL not in d.keys() or key_val not in d[config.KEY_COL][0]['text']):
                continue

            row = {'fields': []}
            for name, props in d.items():
                props = props[0]

                # Get text and image
                if name == config.TITLE_COL:
                    row['title'] = props['text']
                    continue
                if name == config.IMAGE_COL:
                    row['image_url'] = props['src'] if 'src' in props.keys() else props['text']
                    continue
                if 'text' not in props.keys():
                    continue

                # Get other fields
                value = '<' + props['href'] + '|' + props['text'] + '>' if 'href' in props.keys() else props['text']
                f = {'title': name, 'value': value}
                if len(props['text']) < 32:
                    f['short'] = True
                row['fields'].append(f)
            attachments.append(row)

        if len(attachments) == 0:
            attachments.append({'text':
                'No data found matching {} == {} in the past {} rows'.format(config.KEY_COL, key_val, config.NUM_ROWS)})
    else:
        attachments.append({'text': 'Request not successful'})
    return attachments


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = config.DEFAULT_MESSAGE
    attach = None

    for day in weekdays:
        if day in command:
            response = config.MESSAGE
            # convert day to date, because of how data formatted
            date_string = get_formatted_date(day)
            attach = get_attachments(date_string)

    print('Done!')
    # Send response
    slack_client.api_call('chat.postMessage', channel=channel,
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


if __name__ == '__main__':  
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('{} connected and running!'.format(config.NAME))
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
