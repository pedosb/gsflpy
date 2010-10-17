class Link(object):
    """
    Link Fields
      J=%d Link identifier. Starts link information
      START=%d S c Start node number (of the link)
      END=%d E c End node number (of the link)
      WORD=%s W wc Word (If lattice labels links rather that nodes)
      var=%d v wo Pronunciation variant number
      div=%s d wo Segmentation (modelname, duration, likelihood) triples
      acoustic=%f a wo Acoustic likelihood of link
      language=%f l o General language model likelihood of link
      r=%f r o Pronunciation probability
    """
    def __init__(self, \
	    j, \
	    s, \
	    e, \
	    w = None, \
	    v = None, \
	    d = None, \
	    a = None, \
	    l = None, \
	    r = None):
	self.j = j
	self.s = s
	self.e = e
	self.w = w
	self.v = v
	self.d = d
	self.a = a
	self.l = l
	self.r = r

    def __str__(self):
       string = 'J=' + str(self.j) + ' '  +\
	    'S=' + str(self.s.i) + ' ' + \
	    'E=' + str(self.e.i) + ' ' 
       if self.w:
           string += 'w=' + str(self.w) + ' ' 
       if self.v:
           string += 'v=' + str(self.v) + ' ' 
       if self.d:
	   segment_str = ':'
	   for segment in self.d:
	       segment_str += str(segment)
           string += 'd=' + str(segment_str) + ' ' 
       if self.a:
           string += 'a=' + str(self.a) + ' ' 
       if self.l:
           string += 'l=' + str(self.l) + ' ' 
       if self.r:
           string += 'r=' + str(self.r) + ' ' 
       return string

    def cmp_id(self, other):
       if int(self.j) > int(other.j):
	  return 1
       elif int(self.j) < int(other.j):
	  return -1
       else:
	  return 0

    def cmp_s(self, other):
      if self.s > other.s:
	 return 1
      elif self.s < other.s:
	 return -1
      else:
	 return 0
