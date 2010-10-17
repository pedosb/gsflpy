load the model file.

	    InputStream is = new FileInputStream(objectInputFileName);

	      objectInputStream = null;
	      xmlInputStream    = new BufferedInputStream(is);

    if (objectInputFileName.length() != 0) {
      // Load classifier from file
      if (objectInputStream != null) {
	classifier = (Classifier) objectInputStream.readObject();
        // try and read a header (if present)
        Instances savedStructure = null;
        try {
          savedStructure = (Instances) objectInputStream.readObject();
        } catch (Exception ex) {
          // don't make a fuss
        }
        if (savedStructure != null) {
          // test for compatibility with template
          if (!template.equalHeaders(savedStructure)) {
            throw new Exception("training and test set are not compatible");
          }
        }
	objectInputStream.close();
      }
      else if (xmlInputStream != null) {
	// whether KOML is available has already been checked (objectInputStream would null otherwise)!
	classifier = (Classifier) KOML.read(xmlInputStream);
	xmlInputStream.close();
      }
    }


    DataSource trainSource = null, testSource = null;

	  testSetPresent = true;
	  testSource = new DataSource(testFileName);

	template = test = testSource.getStructure();


    Evaluation testingEvaluation = new Evaluation(new Instances(template, 0), costMatrix);

Test with spplied test set

    if (testSource != null) {
      // Testing is on the supplied test data
      testSource.reset();
      test = testSource.getStructure(test.classIndex());
      Instance testInst;
      while (testSource.hasMoreElements(test)) {
	testInst = testSource.nextElement(test);
	testingEvaluation.evaluateModelOnceAndRecordPrediction(
            (Classifier)classifier, testInst);
      }

      if (splitPercentage > 0) {
        if (!printClassifications) {
          text.append("\n\n" + testingEvaluation.
              toSummaryString("=== Error on test split ===\n",
                  printComplexityStatistics));
        }
      } else {
        if (!printClassifications) {
          text.append("\n\n" + testingEvaluation.
              toSummaryString("=== Error on test data ===\n",
                  printComplexityStatistics));
        }
      }
