# CompressedEwkSummary

A repo to make summary plots for the compressed electroweak-SUSY sensitive analyses. One-time set-up commands:
```
git clone git clone https://github.com/sbein/CompressedEwkSummary.git
export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_15_0_0_pre3
```

To quickly make the summary plot:
```
cd CMSSW_15_0_0_pre3/src
cmsenv
cd ../../CompressedEwkSummary
python3 summaryplot.py
```

This produces a pdf and png of the summary plot. 

To add more analyses, you can
* Copy a needed ROOT file into a directory with a name like results_exo_18_002/root-file-name.root
* Add a line to summaryplot.py with a new entry for the analysis,
specifying names of the root file and expected and observed TGraph-based limit curves
and re-run. 
```
python3 summaryplot.py
```
You can add the results root file to the repo in a designated analysis folder. 

