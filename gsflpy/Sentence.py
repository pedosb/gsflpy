from Link import Link
class Sentence():
   def __init__(self, link = None):
      self.links = []
      self.nodes = []
      self.last_node = None
      self.ready = False
      if link:
	 self += link

   def __add__(self, link):
      if isinstance(link, Link):
	 self.links.append(link)
	 self.nodes.append(link.e)
	 self.last_node = link.e
	 return self
      else:
	 #TODO: Create an exception
	 pass

   def __str__(self):
      #TODO: Make return the phase formed by the nodes
      return 'working to show it'

   def copy(self):
      sentence = Sentence()
      for link in self.links:
	 sentence += link
      return sentence
