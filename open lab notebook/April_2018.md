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

2nd week
- I completed my code for the NPLS in R and ran some test analyses with either partial or random data, all worked out fine
- Unfortunately, I had some slip ups, because of the convolution of the EEG parameters (wrote code that produced an unsuitable hrf) and lost a bot of time to figuring out this mistake
- I also still had issues with what kind of data to put into the NPLS and how to arrange it the best way
- Plus, I only had group averaged spectral data and amplitude data for the EEG which is not taking full advantage of the fact that NPLS works with multidimensional signatures
- Further, I was missing some multimodal application of spectral data as a potentially closer link to BOLD variation, which is why I decided to re-write the code for my time frequency analysis, deriving single trial measures for theta, alpha and beta power
- The last one I chose, because I had previously noticed in the group level ERSP that there was interesting beta blocking around 500 ms after B
- With these measures I calculated new fMRI GLMs (BOLD predicition with single trial theta power averaged over the most interesting time window) to find voxel clusters accounted for by fluctuating spectral power and contrasted results with amplitude regressors
- In fact, the former (especially theta) had a stronger predictive power
- For the fMRI part, I extracted time course activation for ROIs, but had the feeling I was limiting the analysis too much and should preferably create single trial measures with the entire voxel space (so in the end, spatial clusters could be assigned weights for specific spectral signatures), which is why I also re-wrote the this part of the fMRI analysis and ran it

3rd
- I finally completed all uni- and multimodal analyses for my master thesis (N-PLS, times series analyses, parallel factor analysis for time-frequency data, induced and evoked time-frequency, etc) and uploaded some of the code
- I still have concerns regarding the statistical validity of some results (, which I discuss in some exerts of my discussion section), either due to the nature of different single trial measures for fMRI in my experiment, bootstrapping procedures or other issues, but I think that the current status of results is sufficient for my thesis
- In order to bring everything together, I started writing on a model for neuronal processing of cues in the DPX
- While writing, I became even more confident in the benefits of a multimodal data perspective, but the abudnance of information, selective constraints, statistical assumptions as well as drawbacks of single trial estimates are worthwhile discussing
- Next to completing both my discussion and results section, I'm still working on the selection of graphs and thereby results to include into my thesis (and what to put in the appendix)

4th
- Due to further complications with the final analyses (plotting atom weights from N-PLS, choosing the right parameters and adequate amount of data points for N-PLS, re-analysis of time series data), I got set back again in finishing my thesis
- I found errors in my single trial frequency analysis and had to re-write large parts of these codes and higher analyses building on them. Since time for my thesis to be finished in running out, I decided to drop group results for single trial BOLD prediction based on frequency power to focus on time series as well as N-PLS analyses. The former proved to be a valuable indication as to how to interpret results from jICA, pICA and N-PLS, since it provides as baseline index of co-variation between signals distinctive for cues
- I traveled to Regensburg with Peer, Rebekka and Jan Otto, so we could discuss their upcoming project on the effects of music on stress in the MRI scanner with Prof. Wuest and his doctoral student Gina-Isabelle Henze
