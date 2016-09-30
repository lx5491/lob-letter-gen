# lob-letter-gen
This is the coding challenge for Lob

## Pre-requisites: all the necessary python packages are in requirements.txt

## Instructions for running
1. pip install -r requirements.txt
2. The usage of letter.py:
    python letter.py [-h] -name "Xi Liu" -addr1 "2226 Stone Road" [-addr2 ADDR2] -city "Ann Arbor" -state
                 "MI" -zip "48105" -message "Hi there, this is an example message" [-html HTML] [-lobkey LOBKEY] [-googlekey GOOGLEKEY]
    2a. The string after each argument name is the argument itself
    2b. Arguments in brackets are optional
    2c. HTML template file is default to be index.html
    2d. LOBKEY and GOOGLEKEY are the keys to access Lob's and Google Civic's APIs
    2d. use "python letter.py -h" to see more detailed usage