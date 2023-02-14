# Process Evidence from Open Targets
These python scripts can download the targets, diseases and evidence json files and perform an analysis on them to
obtain the median and three highest scores for each disease_target pair. If you already have all the json files 
downloaded as parts, use the instructions below for alternative data sources.

# Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Running

```
python download_from_ftp.py all
python process_json.py
```


This will create output.json containing a list of the target diseases pairs sorted by ascending median score in output.json. You can use --output argument to change the output file.

The number of pairs of targets which share at least 2 diseases will be written out to the console. An example output has been saved in output2.txt

# Alternative data sources

If you already have the json files downloaded as part-00000- etc then combine them together to create one combined file for each of diseases, targets and eva:

```
mkdir download
cat *befc20b-ce53-4029-bd62-39c5b631aa3f-c000.json > download/targets.json
cat *773deead-54e9-4934-b648-b26a4bbed763-c000.json > download/diseases.json
cat *4134a310-5042-4942-82ed-565f3d91eddd.c000.json > download/eva.json
```

# Tests

```
pytest .
```

Will run some tests to ensure everything is working.

## Author
This code was written by Nick England
