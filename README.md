# list_of_clinical_trials.py
- A Python to list all phase3 clinical trials on defined conditions
- Data collected from Clinicaltrials.gov
- The program lists all clinical trials meeting the selected CONDITIONS of clinical trials
- The selected conditions is specified by an optional input after the name of the program 
- Without the optional input, the selected conditions is "infectious disease"
- The output is a CSV file with fields like "TITLE", "SPONSORS", "RESPONSIBLE PARTIES", "START DATES", "PRIMARY DATES", "COMPLETE DATES"
- The output file name is the optional input (or infectiousdisease) combined with the date the file is created
- The program is tested on Python 3.6.6 and Selenium 3.141.0
