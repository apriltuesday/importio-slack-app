
class Config(object):

	def __init__(self):

		# REQUIRED
		self.NAME = 'lunchbot'
		self.SLACK_BOT_TOKEN = 'xoxb-88248441057-rIDo3hAUHFpFDX3F1tspeRR5'
		self.SLACK_BOT_ID = 'U2L7ACZ1P'
		self.IMPORT_DATA_URL = 'https://data.import.io/extractor/b2bf2d07-2485-451b-8718-ef6273640599/json/latest?_apikey=10fd4d0e33d846f382665a71ccdc153c77a750263b35622dc51271b446bf487f321b7fd4d0ec2cdc6e29201105536ca6cd84b316ebc6546aeab869dedb63245cdeb00fffdf2971071d421b3883422f0d'

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