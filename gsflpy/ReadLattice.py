from ArgumentNotFoundError import ArgumentNotFoundError
from Lattice import Lattice
from Node import Node
from Link import Link
from Segment import Segment
from ErrorSegment import ErrorSegment
import util

class ReadLattice():
    COMMENT_CHAR = '#'

    def __init__(self, VERBOSE = None):
	self.node_number = None
	self.link_number = None
	self.nodes = []
	self.links = []
	self.VERBOSE = VERBOSE

    def split_argument_unit(self, argument_unit):
	words = argument_unit.split('=')
	if len(words) != 2:
	    #TODO create an exception for this
	    print 'syntax error in line' +\
		    self.line + '\n' +\
		    'CREATE AN EXCEPTION FOR THIS'
	    exit(-1)
	else:
	    return words

    def parse_sizespec(self):
	"""
	Here we expect a line in the format
	sizespec = "N=" intnumber "L=" intnumber
	"""
	line_splitted = self.line.split()

	for argument_unit in line_splitted:
	    #  words[0] is the identifier of the argument
	    # and words[1] is the argument value.
	    words = self.split_argument_unit(argument_unit)
	    if words[0] == 'N':
		self.node_number = int(words[1])
	    elif words[0] == 'L':
		self.link_number = int(words[1])
	    # if we do not recognize the argument an exception is raised
	    else:
	        raise ArgumentNotFoundError(found = words[0])

    def parse_node(self):
	"""
	Here we expect a line int he format

	node = "I=" intnumber
	{ "t=" floatnumber | "W=" string |
	"s=" string | "L=" string | "v=" intnumber }
	"""
	line_splitted = self.line.split()
	i=t=w=s=l=v=None
	for argument_unit in line_splitted:
	    words = self.split_argument_unit(argument_unit)

	    if words[0] == 'I':
		i = words[1]
	    elif words[0] == 't':
		t = float(words[1])
	    elif words[0] == 'W':
		w = words[1]
	    elif words[0] == 's':
		s = words[1]
	    elif words[0] == 'L':
		l = words[1]
	    elif words[0] == 'v':
		v = int(words[1])
	    else:
		raise ArgumentNotFoundError(found = words[0])
	if i != None:
	    self.nodes.append(Node(i, t, w, s, l, v))
	else:
	    ArgumentNotFoundError(self.line, 'I = identifier expected')

    def parse_segment(self, segment_unit):
       """
       The segment_unit must be a single string in the format:
       state(string),float,float
       """
       segment_values = segment_unit.split(',')
       try:
	  return Segment(segment_values[0], \
		float(segment_values[1]), \
		float(segment_values[2]))
       except IndexError:
	  raise ArgumentNotFoundError('NOTHING', \
		  'float number for segment')

    def read_segment(self, segment):
       """
       The segment must be a string in the format:
       :state(string),float,float:state(string),float,float:...:
       """
       segments = []
       for segment_unit in segment.split(':'):
	  if segment_unit == "":
	     continue
	  else:
	     segments.append(self.parse_segment(segment_unit))
       return segments

    def parse_link(self):
	"""
	Here we expect a line in the format
	arc = "J=" intnumber
	"S=" intnumber
	"E=" intnumber
	{ "a=" floatnumber | "l=" floatnumber | "a=" floatnumber | "r=" floatnumber |
	"W=" string | "v=" intnumber | "d=" segments }
	"""
	line_splitted = self.line.split()
	j=s=e=a=l=r=w=v=d=None
	nodes_i = []
	for nodes in self.nodes:
	   nodes_i.append(nodes.i)
	for argument_unit in line_splitted:
	    words = self.split_argument_unit(argument_unit)

	    if words[0] == 'J':
		j = words[1]
	    elif words[0] == 'S':
	        if words[1] not in nodes_i:
		    raise KeyNotFoundError(words[1], 'nodes')
		s = self.nodes[nodes_i.index(words[1])]
	    elif words[0] == 'E':
		if words[1] not in nodes_i:
		    raise KeyNotFoundError(words[1], 'nodes')
		e = self.nodes[nodes_i.index(words[1])]
	    elif words[0] == 'a':
		a = words[1]
	    elif words[0] == 'l':
		l = words[1]
	    elif words[0] == 'r':
		r = words[1]
	    elif words[0] == 'W':
		w = words[1]
	    elif words[0] == 'v':
		v = words[1]
	    elif words[0] == 'd':
		d = self.read_segment(words[1])
	    else:
		raise ArgumentNotFoundError(self.line)
	if j != None or s != None or e != None:
	    self.links.append(Link(j, s, e, w, v, d, a, l, r))
	else:
	    ArgumentNotFoundError(self.line, 'J, S and E expected ' +\
		    'see htkbook for arcs specifications')

    def parse_error_segment_file(self, error_segment_file):
       """
       Expected a file like this:
       error_file_name;start_time;correct_segments:recognized_segments;
       ...
       And return a list with all error segments found.
       """
       error_segments = []
       for self.line in open(error_segment_file):
	  arguments = self.line.split(';')
	  error_segment = \
		ErrorSegment(self.read_segment(arguments[2]),\
		   self.read_segment(arguments[3]),\
		   int(arguments[1]),\
		   arguments[0])
	  util.add_error_segment(error_segments, error_segment)
       return error_segments

    def parse(self, lat_file):
        """
        We expect a lattice file with at least the nodes and links specifications
        """
        self.line_number = 0
	for self.line in open(lat_file):
	    self.line_number = self.line_number + 1
	    if self.line.startswith(self.COMMENT_CHAR) or self.line.strip() == '':
		continue
	    self.current_arg_name = self.line.split()[0].split('=')[0]

	    if self.current_arg_name == 'N':
		self.parse_sizespec()

	    if self.current_arg_name == 'I':
		if not self.link_number or not self.node_number:
		    raise ArgumentNotFoundError(\
			    self.current_arg_name,\
			    'sizespec see htkbook')
	        self.parse_node()

	    if self.current_arg_name == 'J':
		if len(self.nodes) != self.node_number:
		    #TODO this must have an exception
		    print 'Number of nodes is not the same ' +\
			    'of the specified\n DO AN EXCEPTION ' + \
			    'FOR THIS.'
		    exit(-1)
		self.parse_link()

	if self.link_number != len(self.links):
	    print 'Number of links is not the same ' +\
		    'of the specified\n DO AN EXCEPTION ' +\
		    'FOR THIS.'
	    exit(-1)

	print 'Read ' + str(self.node_number) + \
	      ' nodes and ' + str(self.link_number) + ' links'
	return Lattice(self.nodes, self.links, file_name = lat_file, VERBOSE=self.VERBOSE)
