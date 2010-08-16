class Node():
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
	self.t = t
	self.w = w
	self.l = l
	self.v = v
	self.s = s
    def __str__(self):
	node_str = 'I=' + self.i
	if self.t:
	    node_str = node_str + ' t=' + self.t
	if self.w:
	    node_str = node_str + ' W=' + self.w
	if self.l:
	    node_str = node_str + ' L=' + self.l
	if self.v:
	    node_str = node_str + ' v=' + self.v
	if self.s:
	    node_str = node_str + ' s=' + self.s
	return node_str
