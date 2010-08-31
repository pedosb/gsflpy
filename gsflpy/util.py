def add_error_segment(error_segments, error_segment):
   if error_segment in error_segments:
      error_segments[error_segments.index\
	    (error_segment)].add(\
	       error_segment.correct_segments[0],\
	       error_segment.recognized_segments[0],\
	       error_segment.start_time[0],\
	       error_segment.file_name[0])
   else:
      error_segments.insert(0, error_segment)
