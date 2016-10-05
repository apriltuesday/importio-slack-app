# Quick script to test integrating import.io and slack
#
# Author: April Shen
# Created on 2016-10-05

import requests
import sys
import argparse

IMAGE_KEY = 'Image'


def main(data_url, slack_url, message, num_rows):
	r = requests.get(data_url)
	if r.status_code == 200:
		data = r.json()['result']['extractorData']['data'][0]['group']
		payload = {'text': message, 'attachments': []}

		# Make one attachment for each data row
		for d in data[:num_rows]:
			row = {'fields': []}

			for name, props in d.items():
				props = props[0]
				if name == IMAGE_KEY or 'text' not in props.keys():
					continue
				value = '<' + props['href'] + '|' + props['text'] + '>' if 'href' in props.keys() else props['text']
				f = {'title': name, 'value': value}
				if len(props['text']) < 32:
					f['short'] = True
				row['fields'].append(f)

			# Get an image
			if IMAGE_KEY in d.keys():
				img = d[IMAGE_KEY][0]
				row['image_url'] = img['src'] if 'src' in img.keys() else img['text']

			payload['attachments'].append(row)
			

		# Make the POST request
		requests.post(slack_url, json=payload)
		print 'Done!'

	else:
		print 'Request not successful'


if __name__ == '__main__':
	# Default values
	data_url = 'https://data.import.io/extractor/b2bf2d07-2485-451b-8718-ef6273640599/json/latest?_apikey=10fd4d0e33d846f382665a71ccdc153c77a750263b35622dc51271b446bf487f321b7fd4d0ec2cdc6e29201105536ca6cd84b316ebc6546aeab869dedb63245cdeb00fffdf2971071d421b3883422f0d'
	slack_url = 'https://hooks.slack.com/services/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'
	num_rows = 5
	message = 'What\'s for lunch?'

	# Command line args
	parser = argparse.ArgumentParser(description='Post import.io data to a slack channel')
	parser.add_argument('-d', '--data', help='url of json data from import.io')
	parser.add_argument('-s', '--slack', help='url of slack webhook')
	parser.add_argument('-m', '--message', help='message to include with post')
	parser.add_argument('-n', '--num_rows', type=int, help='max number rows of data to post')
	args = parser.parse_args()

	if args.data:
		data_url = args.data
	if args.slack:
		slack_url = args.slack
	if args.message:
		message = args.message
	if args.num_rows:
		num_rows = args.num_rows
	
	main(data_url, slack_url, message, num_rows)
