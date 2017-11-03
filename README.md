# pslive
Show live data through terminal prompt

## Setup and run the program. Note: this was tested in python3.6 only
1. clone this repo
2. cd to repo folder
3. run python pslive.py

once step 3 is working
1. add pslive.py /usr/local/bin/
2. update PS1 prompt in .bash_profile to include pslive.py. e.g.
PS1="\[\033[01;35m\][\d:\t \u:\w] \033[1;32m\]\$(pslive.py) \n\[\033[m\]🍺  "

## Under the hook
* two data files (data.yaml, wip.yaml) are stored in <HOME DIR>/.pslive folder. pslive.py will create this folder if not exist
* if data.yaml does not exist or too old (default age 3600 seconds)
  - fetch live data from internet and save the data to data.yaml (more work to be done here, or you can add your own code to fetch live data)
* if wip.yaml does not exist
  - get a random entry in data.yaml
  - display the key
  - save the key to wip.yaml
* if wip.yaml exists
  - read wip.yaml and compare to the corresponding entry in data.yaml
  - if they equel, then repeat steps as if wip.yaml file does not exist
  - if they do not equel, display the next value that is not in the wip.yaml and update wip.yaml to add the displayed value list

## Use cases
1. flashcard: data.yaml stores words and their definition, example sentences, descriptions, etc.
2. news flash: data.yaml stores headlines and short stores
3. reminder: data.yaml stores tasks / due dates
