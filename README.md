# lob-letter-gen
This is the coding challenge for Lob. The github link is: https://github.com/lx5491/lob-letter-gen.git

## Pre-requisites:
1. Python2.7
2. All the necessary python packages are in requirements.txt

## Instructions for running
1. pip install -r requirements.txt
2. The usage of letter.py:
    python letter.py [-h] -name NAME -addr1 ADDRESS_LINE1 [-addr2 ADDRESS_LINE2] -city CITY -state
                 STATE -zip ZIPCODE -message MESSAGE [-html HTML] [-lobkey LOBKEY] [-googlekey GOOGLEKEY]
    2a. The string after each argument name is the argument itself
    2b. Arguments in brackets are optional
    2c. HTML template file is default to be index.html
    2d. LOBKEY and GOOGLEKEY are the keys to access Lob's and Google Civic's APIs
    2d. use "python letter.py -h" to see more detailed usage
    2e. Example command: python letter.py -name "Xi Liu" -addr1 "2226 Stone Rd" -state "MI" -zip 48105 -city "Ann Arbor" -message "This is an example" -html index.html