
class Config(object):

	def __init__(self):

		# REQUIRED
		self.NAME = ''
		self.SLACK_BOT_TOKEN = ''
		self.SLACK_BOT_ID = ''
		self.IMPORT_DATA_URL = ''

		# OPTIONAL
		self.MESSAGE = "Here's what's for lunch! Yum :yum:"
		self.DEFAULT_MESSAGE = "Not sure what you mean!"
		self.KEY_COL = 'Date' # TODO optional or not?
		self.KEY_VALUES = [] # TODO what to do if these are not present?
		self.TITLE_COL = 'Meal'
		self.IMAGE_COL = 'Image'
		self.MAX_ROWS = 5
		self.FIELDS = []

		# EXTENDED FUNCTIONALITY
		self.SLACK_WEBHOOK_URL = ''
		self.SLASH_COMMANDS = [] # TODO what would these be exactly?

config = Config()
