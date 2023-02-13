# Process Evidence from Open Targets
These python programs can download the targets, diseases and evidence json files and perform an analysis on them to
obtain the median and three highest scores for each disease_target pair.

# Installation
pip install -r requirements.txt

# Running
python download_from_ftp.py all
python process_json.py

This will create output.json containing a list of the target diseases pairs sorted by ascending median score.