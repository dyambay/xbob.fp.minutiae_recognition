Fingerprint verification using Bob
===========================


Overview
--------

This example demonstrates how to use Bob to build a fingerprint recognition system using Bob and the following method

* A simple minutiae-based method

References::

   Cheng Long Adam Wang, researcher
   Fingerprint Recognition System
   http://home.kimo.com.tw/carouse9/FRS.htm

   Lukasz Wieclaw, "A minutiae-based matching algorithms in fingerprint recognition systems", 
   Journal of Medical informatics and Technologies vol. 13/2009, ISSN 1642-6037
   http://www.academia.edu/2508970/A_minutiae-based_matching_algorithms_in_fingerprint_recognition_systems

   Zain S. Barham, "Fingerprint Recognition using Matlab"
   http://eng.najah.edu/sites/eng.najah.edu/files/fingerprintrecognition.pdf

Requirements
------------

To use this example, you will require Bob in version of at least 1.2.0. and the LivDet 2013 database.

LivDet 2013 Crossmatch Dataset
.................
The Crossmatch Fingerprint Verification Database is a fingerprint database which consists of one dataset which contains live images for use in fingerprint verification codes. Protocol is set so all images are installed in the database and matched against all images. 

DATA SET
 	Scanner 	Model 	        Res (dpi) 	Image size 	Live samples 	
1 	Crossmatch 	L SCAN GUARDIAN 500 	         640X480 	966 	

The actual raw data for the database should be downloaded from the original
URL. This package only contains the `Bob <http://www.idiap.ch/software/bob/>`_
accessor methods to use the DB directly from python, with our certified
protocols.

References::

1. L. Ghiani, D. Yambay, V. Mura, S. Tocco, G.L. Marcialis, F. Roli, and S. Schuckers, LivDet 2013 -  Fingerprint Liveness Detection Competition 2013, 6th IAPR/IEEE Int. Conf. on Biometrics, June, 4-7, 2013, Madrid (Spain).
 


Bob
...
If you do not have a Bob version yet, or your Bob version is too old, you can get a new one from http://www.idiap.ch/software/bob.

If your Bob version is not installed globally or not in the default path, you have to edit the *buildout.cfg* file in the root directory of this package.
In the ``[buildout]`` section, please add a line ``prefixes = <BOB_INSTALL_DIRECTORY>``, where ``<BOB_INSTALL_DIRECTORY>`` points to the root directory of your local Bob installation.

.. note::
  If you are at Idiap, Bob is installed globally, so there is no need to specify the ``prefixes``, unless you want to use another version of it.



Download
--------

Finally, to download this package, you can clone our git repository::

  $ git clone https://github.com/dyambay/xbob.fp.minutiae_recognition.git
  $ cd xbob.fp.minutiae_recognition

Afterwards, please call::

  $ python bootstrap.py
  $ ./bin/buildout

to generate the scripts that, amongst others, will run the fingerprint verification algorithms. Please verify your installation by running the test cases. For more details, please refer to the documentation, which you might create and open yourself by::

  $ ./bin/sphinx-build doc sphinx
  $ firefox sphinx/index.html

(or use any other browser of your choice).

If you have questions to or problems with this package, please send a request to bob-devel@googlegroups.com, or file a bug under https://github.com/dyambay/xbob.fp.minutiae_recognition/issues.

