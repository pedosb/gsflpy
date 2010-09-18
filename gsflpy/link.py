class Link():
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
    __init__(self, j, s, e, w, v, d, a, l, r):
	self.j = j
	self.s = s
	self.e = e
	self.w = w
	self.v = v
	selv.d = d
	self.a = a
	self.l = l
	self.r = r
