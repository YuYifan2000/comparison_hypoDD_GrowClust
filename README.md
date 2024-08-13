# Comparison of Eight Earthquake Location Workflow

This repo is used to compare the results of eight mostly used earthquake location methods (HypoDD, Growclust, XCORLOC, NonLinLoc, NonLinLoc_SSST, VELEST, HypoInverse, HypoSVI) in a controlled synthetic experiment based on 2019 Ridgecrest earthquake sequence.

We implement 3D velocity structure, elevation effect, reading error, outliers... into the calculation of traveltime.

This is also a good collection of how to prepare and run the mentioned above earthquake locators.

More detailed information can be found in the 'readme.pdf'. We are going to present this work at the incoming SCEC & AGU meetings.

## requirement
1. pykonal the 3D fast marching method to calculate the traveltime
2. Install the eight earthquake location methods
## workflow
Whole workflow is in the workflow/ directory.
Follow the procedure as:
1. calculate the travetime, run the shuffle_source.py and generate_tt.py (The velocity model is too large to be hosted here)
2. calculate starting location using velest after adding reading error and outliers. Run tt2velest.py first and then run velest in this folder which serves as an associator.
3. walk into different folders to run the location program, there is velest2xx.py in each folders for specific required file format.


## traveltime dataset
If you are willing to run the results from 'readme.pdf' and compare or improve any programs,  the simplest way is to use the 'phase.csv' and 'pre_cat.csv' files in 'hyposvi' folder which contains the phases and starting location information.\
'dt.cc' in the hypoDD folder is the crosscorrelation results for hypoDD and Growclust (XCORLOC needs to run the prep_xcorloc.py in its folder).\
I normally use the velocity structure inverted by VELEST based on Shelly's model.

## Running Location Programs
After running all these programs, I do have some experience to share:\
HypoDD: 
* While the LSQR mode's error output are dominated by the damping factor, running the SVD mode with small set of data should be considered. From the source code of HypoDD.f line 16, the factor should be 2.7955 to get 95% confidence errors.

XCORLOC:
* The differential time used in XCORLOC is 't2-t1' or the '21' mode in Growclust, which is not the negative of HypoDD format.

VELEST:
* Another independent run of single event location calculating resolution matrix with zero updating iteration after the location should be used for error output. That is set 'isingle=1', 'iresolcalc=1', 'ittmax=0' for error output.

NonLinLoc and NonLinLoc_SSST:
* The control files I shared in this repo are by courtesy of Anthony Lomax. There are plenty of parameters and options to choose, I believe his scripts in this repo serve as an example for users to learn, especially NonLinLoc_SSST.

HypoSVI
* Please refer to [Julia version of HypoSVI](https://github.com/interseismic/eikonet_julia)

Growclust
* Please refer to [Julia version of Growclust](https://github.com/dttrugman/GrowClust3D.jl)
  
## util

You can compare the location result satistically by running the data_preparation and error_analysis python file in this folder, while the true_location.csv are upon requests for comparison.

If you have tested your results, please share it with me or any comments and questions: yuyifan@stanford.edu
