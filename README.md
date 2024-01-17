# Comparison of Five Earthquake Location Workflow

This repo is used to compare the results of five mostly used earthquake location methods.

## requirement
1. pykonal the 3D fast marching method to calculate the traveltime
2. Install the five earthquake location methods (HypoDD, Growclust, VELEST, Hypoinverse, Non_Lin_Loc)
## workflow
Whole workflow is in the workflow/ directory.\
Follow the procedure as:\
shuffle_source.py, generate_tt.py, tt2velest.py, velest2\*.py, event2evlist.py, dt_form_cc.py

Sorry it is a little bit messy, I will sort out soon.
## traveltime dataset
Sep.18: We update our results in NonLinLoc with smaller step size to improve the performance. \
If you are willing to run the results over Yifan's poster at 2023 SCEC Annual Meeting, it is in the dataset/ directory.\
'o_source.npy','o_station.npy' are the sources and stations locations.\
'tt_P.npy','tt_S.npy' storage each source's traveltime on each station based on the index order.\
'velest.cnv' is the starting dataset for velest, I added some random error to the traveltime data.\
'hypoventer.CNV' is the starting results for the comparison of five location methods which I recommend where you should start with.\
'dt.cc' is the crosscorrelation results for hypoDD and Growclust.\
I normally use the velocity structure inversed by VELEST.\

If you have tested your results, please share it with me: yuyifan@stanford.edu
