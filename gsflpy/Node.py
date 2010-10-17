class Node(object):
    """
    Node Fields
      I=%d Node identifier. Starts node information
      time=%f t o Time from start of utterance (in seconds)
      WORD=%s W wc Word (If lattice labels nodes rather that links)
      L=%s wc Substitute named sub-lattice for this node
      var=%d v wo Pronunciation variant number
      s=%s s o Semantic Tag
    """
    def __init__(self, i,\
	    t = None,\
	    w = None,\
	    l = None,\
	    v = None,\
	    s = None):
	self.i = i
	if t:
           self.t = int(t)
	else:
	   self.t = None
	self.w = w
	self.l = l
	self.v = v
	self.s = s
    def __str__(self):
	node_str = 'I=' + str(self.i)
	if self.t:
	    node_str = node_str + ' t=' + str(self.t)
	if self.w:
	    node_str = node_str + ' W=' + str(self.w)
	if self.l:
	    node_str = node_str + ' L=' + str(self.l)
	if self.v:
	    node_str = node_str + ' v=' + str(self.v)
	if self.s:
	    node_str = node_str + ' s=' + str(self.s)
	return node_str
