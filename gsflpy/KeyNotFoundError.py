from Error import Error

class KeyNotFoundError(Error):
    def __init__(self, key, where):
	self.key = key
	self.where = where

    def __str__(self):
	return 'ERROR: expected key "' + \
		self.key + '" in "' + \
		self.where + '"'
