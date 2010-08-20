class Sentence():
   def __init__(self, link = None):
      self.links = []
      self.nodes = []
      if link:
	 self += link

   def __add__(self, link):
      if isinstance(link, Link):
	 self.links.append(link)
	 self.nodes.append(link.e)
      else:
	 #TODO: Create an exception
	 pass

   def __str__(self):
      #TODO: Make return the phase formed by the nodes
      return 'working to show it'
