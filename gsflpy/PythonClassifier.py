#!/usr/bin/env jython

import sys

import weka.classifiers.Classifier as Classifier
from weka.classifiers import *
import weka.core.Instance
import weka.core.Instances as Instances
import weka.core.xml.KOML as KOML
import weka.core.converters.ConverterUtils.DataSource as DataSource

import java.io.InputStream as InputStream
import java.io.FileInputStream as FileInputStream
import java.io.BufferedInputStream as BufferedInputStream
import java.io.ObjectInputStream as ObjectInputStream
import java.lang.StringBuffer as StringBuffer

if __name__=='__main__':
   model_file_name = sys.argv[1]
   test_file_name = sys.argv[2]

   test_source = DataSource(test_file_name)
   template = test = test_source.getStructure()
   test.setClassIndex(test.numAttributes() -1)

   object_input_stream = ObjectInputStream(FileInputStream(model_file_name))
   classifier = object_input_stream.readObject()

   if not template.equalHeaders(Instances(object_input_stream.readObject())):
      print '####ERROR########'
      sys.exit(-1)

   object_input_stream.close()

   classifierClassifications = Classifier.makeCopy(classifier)

   testing_evaluation = Evaluation(Instances(test, 0))
   testing_evaluation.useNoPriors()

   test_source.reset()
   test = test_source.getStructure(test.classIndex())
   while test_source.hasMoreElements(test):
      test_inst = test_source.nextElement(test)
      testing_evaluation.evaluateModelOnceAndRecordPrediction(
	    classifier, test_inst)
      with_missing = test_inst.copy()
      with_missing.setDataset(test_inst.dataset())
      with_missing.setMissing(with_missing.classIndex())
      for d in classifier.distributionForInstance(with_missing):
	 print d
      print

   print testing_evaluation.toSummaryString()
   classifications = StringBuffer()
   Evaluation.printClassifications(classifierClassifications, Instances(template, 0),
	 test_source, template.numAttributes(), None,
	 False, classifications)
   print classifications
#  printClassifications(classifierClassifications, new Instances(template, 0),
#		       source, actualClassIndex + 1, attributesToOutput,
#		       printDistribution, StringBuffer());
