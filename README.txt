# Process Evidence from Open Targets
These python programs can download the targets, diseases and evidence json files and perform an analysis on them to
obtain the median and three highest scores for each disease_target pair.

# Installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Running
python download_from_ftp.py all
python process_json.py

This will create output.json containing a list of the target diseases pairs sorted by ascending median score in
output.json. You can use --output argument to change the output file.

The number of pairs of targets which share at least 2 diseases will be written out to the console. An example output
has been saved in output2.txt

## Author
This code was written by Nick England