# Quick script to test integrating import.io and slack
#
# Author: April Shen
# Created on 2016-10-05

import requests
import sys
import argparse


def main(data_url, slack_url, message, text_col, image_col, num_rows):
	payload = {'text': message}
	payload['attachments'] = get_attachments(data_url, text_col, image_col, num_rows=num_rows)
			
	# Make the POST request
	requests.post(slack_url, json=payload)
	print 'Done!'


def get_attachments(data_url, text_col, image_col, num_rows=None, key_col=None, key_val=None):
	attachments = []
	# Get the data
	r = requests.get(data_url)
	if r.status_code == 200:
		print('Data request successful')
		data = r.json()['result']['extractorData']['data'][0]['group']
		data = data[:num_rows] if num_rows else data

		# Make one attachment for each data row
		for d in data[:num_rows]:
			if key_col and (key_col not in d.keys() or key_val not in d[key_col][0]['text']):
				continue

			row = {'fields': []}
			for name, props in d.items():
				props = props[0]

				# Get text and image
				if name == text_col:
					row['text'] = props['text']
					continue
				if name == image_col:
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
			attachments.append({'text': 'Reply hazy, try again'})

	else:
		attachments.append({'text': 'Request not successful'})
	return attachments


if __name__ == '__main__':
	# Default values
	data_url = '' #config
	slack_url = '' #config
	num_rows = 5
	message = 'What\'s for lunch?'
	text_col = 'Meal'
	image_col = 'Image'

	# Command line args
	parser = argparse.ArgumentParser(description='Post import.io data to a slack channel')
	parser.add_argument('-d', '--data', help='url of json data from import.io')
	parser.add_argument('-s', '--slack', help='url of slack webhook')
	parser.add_argument('-m', '--message', help='message to include with post')
	parser.add_argument('-t', '--text_col', help='name of column to use as main text')
	parser.add_argument('-i', '--image_col', help='name of column to use as main image')
	parser.add_argument('-n', '--num_rows', type=int, help='max number rows of data to post')
	args = parser.parse_args()

	if args.data:
		data_url = args.data
	if args.slack:
		slack_url = args.slack
	if args.message:
		message = args.message
	if args.text_col:
		text_col = args.text_col
	if args.image_col:
		image_col = args.image_col
	if args.num_rows:
		num_rows = args.num_rows
	
	main(data_url, slack_url, message, text_col, image_col, num_rows)
