1st week
- After completing all analyses for unimodal data (behavioral, EEG, fMRI), I added more nipype code scripts for the 
pre-processing of first and second level fMRI data as well as some plots for contrasts between cues
- Though the effect was most pronounced in the EEG, I could report a significant main effect of cue type in all modalities
- To prepare more multimodal data fusion analyses, I wrote R and Python code for creating data frames with single trial
EEG and fMRI data
- In the end, I brought all data frames to R, since it was most convenient and sensible for later analyses
- When building and arranging data, I (re-)encountered familiar problems concerning the imbalance between EEG and fMRI
- In the EEG there is an abundance of observations over little variables while it's the other way around for fMRI, plus,
in both cases it is hard to choose or to argue what configuration of the single trial data is best to choose for N-PLS, jICA,
pICA and behavioral prediction models (i.e., baseline correction or not, which or how many points to choose in each EEG, which
electrode to choose, contrasted fMRI data or t-maps, which threshold to choose for t-maps)
