from Error import Error

class ArgumentNotFoundError(Error):
    def __init__(self, found, expected=None):
	self.expected = expected
	self.found = found

    def __str__(self):
	msg = 'ERROR: '
	if self.expected:
	    msg = msg + 'expected "' +\
	    self.expected + '" ' +\
	    'but was found "'
	else:
	    msg = msg + 'near "'
	msg = msg + self.found + '"'
	return msg
