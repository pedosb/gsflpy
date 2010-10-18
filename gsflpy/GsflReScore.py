#!/usr/bin/env jython

import sys

from Sentence import Sentence, find_correct, get_sentences
from ConsoleOptions import ConsoleOptions
from ReadLattice import ReadLattice

import weka.core.Instance as Instance
import weka.classifiers.Classifier as Classifier

def usage():
   print (sys.argv[0] + ' -L <lattice_and_transcription_file_path>' +
	 ' -m <weka_classifier_model>')
   print
   print '  -m: Model of a classifier trainned by weka.'

def classify(samples):
   test_inst = Instance(classifier_instances.numAttributes())
   for index in range(classifier_instances.numAttributes()):
      attr = classifier_instances.attribute(index)
      if index == classifier_instances.classIndex():
	 continue
      try:
	 test_inst.setValue(attr, samples[attr.name()])
	 samples[attr.name()] = None
      except KeyError:
	 test_inst.setValue(attr, 0)
   test_inst.setDataset(classifier_instances)
   test_inst.setClassMissing()

   for state in samples:
      if samples[state] != None and state != classifier_instances.classAttribute().name():
	 print 'WARNING: Classifier model has no attribute',state,'found in on frame',samples[state]
   pred_value = classifier.classifyInstance(test_inst)
   pred_value = test_inst.dataset().classAttribute().value(int(pred_value))
   d = classifier.distributionForInstance(test_inst)
   if d[0] > d[1]:
      confidence = d[0] - d[1]
   else:
      confidence = d[1] - d[0]

   return pred_value, confidence


def re_score(sentences,
      states_confusion = None):
   """
   states_confusion must be a tuple with the states of the confusion to be considered.
   The last one is who will have the gain.
   """
   if sentences == None or len(sentences) < 2:
      return

   for sentence in sentences:
      sentence.norm_segments()

   for frame in range(len(sentences[0].segments)):
      state_list = []
      segments = []
      for sentence in sentences:
	 state_list.insert(0, sentence.segments[frame].state)
	 segments.append(sentence.segments[frame])
      ok = True
#      print str(states_confusion) + '\n'
#      print str(state_list) + '\n'
      for state in states_confusion:
	 if not state in state_list:
	    ok = False
	    break
      if ok:
	 samples = dict()
	 biggest = segments[0].score
	 for segment in segments:
	    if segment.state in samples.keys():
	       if segment.score < samples[segment.state]:
		  continue
	    samples[segment.state] = segment.score
	    if biggest < segment.score:
	       biggest = segment.score
	 for samples_key in samples.keys():
	    samples[samples_key] = biggest / samples[samples_key]
	 samples['confusion'] = '?'

	 pred_value, confidence = classify(samples)

	 if pred_value == 'True':
	    for index in range(len(sentences)):
	       segment = sentences[index].segments[frame]
	       if segment.state == states_confusion[1]:
		  segment.score += 80

   for sentence in sentences:
      sentence.recalc_score()

if __name__=='__main__':
   options = ConsoleOptions(sys.argv, usage=usage)
   LAT_FILE, MAX_NODE, CORRECT_SENTENCE = options.get_option('L')
   classifier, classifier_instances = options.get_option('m')
   options.check_all_read()

   if not isinstance(LAT_FILE, list):
      options.usage('ERROR: You must specify the LATTICE_FILES')
   if not isinstance(classifier, Classifier):
      options.usage('ERROR: You must specify an weka classify model to re score.')

   for index in range(len(LAT_FILE)):
      sentences, correct_sentence_index, None = get_sentences(
	    (LAT_FILE[index],
	     MAX_NODE[index],
	     CORRECT_SENTENCE[index]))
      old = str(sentences[0])
      re_score(sentences, ('v[4]','ow1[4]'))
      Sentence.__cmp__=Sentence.cmp_score
      sentences.sort()
      sentences.reverse()

      print
      correct_sentence, correct_sentence_index = \
	    find_correct(sentences, CORRECT_SENTENCE[index])
      if not correct_sentence:
	 print 'WARNING: Correct sentence not found.'
      else:
	 if str(sentences[0]) != old:
	    print 'STATUS: New correct sentence is the number', correct_sentence_index
	    print sentences[correct_sentence_index],sentences[correct_sentence_index]._score
	    print 'MUDOU'
