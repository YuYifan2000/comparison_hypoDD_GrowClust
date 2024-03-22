# Comparison of Five Earthquake Location Workflow

This repo is used to compare the results of seven mostly used earthquake location methods (HypoDD, Growclust, XCORLOC, NonLinLoc, VELEST, HypoInverse, HypoSVI) in a controlled synthetic experiment based on 2019 Ridgecrest earthquake sequence.

We implement 3D velocity structure, elevation effect, reading error, outliers... into the calculation of traveltime.

This is also a good collection of how to prepare and run the mentioned above earthquake locators.

More detailed information can be found in the 'readme.pdf' 

## requirement
1. pykonal the 3D fast marching method to calculate the traveltime
2. Install the five earthquake location methods (HypoDD, Growclust, VELEST, Hypoinverse, Non_Lin_Loc)
## workflow
Whole workflow is in the workflow/ directory.
Follow the procedure as:
1. calculate the travetime, run the shuffle_source.py and generate_tt.py 
2. calculate starting location using velest after adding reading error and outliers. Run tt2velest.py 
3. walk into different folders to run the location program, there is velest2xx.py in each folders for specific required file format.


## traveltime dataset
If you are willing to run the results from 'readme.pdf' and compare or improve any programs, it is in the dataset/ directory.
'o_source.npy','o_station.npy' are the ground truth sources and stations locations.
'tt_P.npy','tt_S.npy' storage each source's traveltime on each station based on the index order.
'velest.cnv' is the starting dataset for velest, I added some random error to the traveltime data. (This works with tt2xxx.py in each folder)
'hypoventer.CNV' is the starting results for the comparison of five location methods which I recommend where you should start with.
'dt.cc' is the crosscorrelation results for hypoDD and Growclust (XCORLOC needs to run the prep_xcorloc.py in its folder).
I normally use the velocity structure inversed by VELEST.

## util
It contains the codes building up a 3D velocity model, plot figures for paper...

If you have tested your results, please share it with me or any comments and questions: yuyifan@stanford.edu
