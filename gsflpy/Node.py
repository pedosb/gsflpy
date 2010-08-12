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
    __init__(self, i, t, w, l, v, s):
	self.i = i
	self.t = t
	self.w = w
	self.l = l
	self.v = v
	self.s = s
