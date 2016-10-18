#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config(object):

	def __init__(self):

		# REQUIRED
		self.NAME = 'testbot'
		self.SLACK_BOT_TOKEN = '<TOKEN>'
		self.SLACK_BOT_ID = '<ID>'
		self.IMPORT_DATA_URL = '<URL>'
		self.KEY_COL = 'Category'

		# OPTIONAL
		self.MESSAGE = "Recent posts:"
		self.DEFAULT_MESSAGE = "Not sure what you mean!"
		self.TITLE_COL = 'Title'
		self.IMAGE_COL = 'Image'
		self.MAX_ROWS = 5
		self.KEY_VALUES = None  # None will perform "smart" string search
		self.FIELDS = ['Date', 'Description', 'Category'] # None indicates will use everything

		# EXTENDED FUNCTIONALITY
		self.SLACK_WEBHOOK_URL = ''
		self.SLASH_COMMANDS = [] # TODO what would these be exactly? maybe \5 for last 5 rows or something?

config = Config()
