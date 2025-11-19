# Allyce Power Corporations Scraper

For use with https://oppress.games/power/

# Data output

The output is

- Name
    - The name of the corporation
- Shares Owned
    - How many shares you own
- Price
    - Price per share
- Ask
    - Price per share *offered by a player*
- Total Shares
    - Total amount of shares
- Income
    - Profit of the corporation (Revenue - Expenses)
- Dividend%
    - Dividend% paid by the corporation
- For my own spreadsheets columns H to O I fill with the following:
    - H: `=if(and(E2>0,C2>0),if((G2*F2*0.8)/(E2*C2)>0,(G2*F2*0.8)/(E2*C2),),)`
        - Dividend% * Income * 0.8 / (Total Shares * Price)
    - I: `=if(and(D2>0,G2>0),(G2*F2*0.8)/(E2*D2),)`
        - Dividend% * Income * 0.8 / (Total Shares * Ask)
    - J: `=if(E2>0,if((G2*F2*0.8)/E2>0,(G2*F2*0.8)/E2,),)`
        - Dividend% * Income * 0.8 / Total Shares
    - K: `=if(B2*J2/24>0,B2*J2/24,)`
        - Shares Owned * (Dividend% * Income * 0.8 / Total Shares) / 24
    - L: `=if(and(D2>0,$P$2>0), if(floor($P$2/D2,1)>0, floor($P$2/D2,1), ""), "")`
        - Money / Ask
    - M: `=if(max(C2,D2)*B2>0,max(C2,D2)*B2,)`
        - Price or Ask * Shares Owned
    - N: `=if(C2>0,D2/C2,)`
        - Ask / Price
    - O: `=if(D2>0,C2/D2,)`
        - Price / Ask
# Example

Want to see my examples? Expect an output such as following if you follow my instructions and copy my formulae

https://allytoall.github.io/apcs

# Important settings to change

Currently in [settings.py](https://github.com/AllyToAll/AllycePowerCorpScraper/blob/master/scraper/settings.py) you will
see

```python
DOWNLOAD_DELAY = 45
# DOWNLOAD_DELAY = 1.5
```

This is intentional to delay requests to around 1 every
45 seconds to reduce stress on the Power servers since it uses an automated flow.

But if you're running this locally I recommend you change it to

```python
# DOWNLOAD_DELAY = 45
DOWNLOAD_DELAY = 1.5
```

Instead, otherwise each run will take hours.

# Installation

## Overview

The example snippets provided are in Bash, thus if your terminal uses a different shell you may need to adapt them.

## Requirements

### Bash

If instead you know how to execute it in Powershell or whatever else you're using, be my guest.

On Windows for example the default shell is not in `Bash` but in `Powershell`.

Thus you will need `Git Bash` from [Git-SCM](https://git-scm.com/install/)

### Python

If you already have this set up, skip this step

You will also need [Python](https://www.python.org/downloads/) installed.

[Ensure Python is added to path](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line).

#### Python Virtual Environment

This code has only been tested to work in with venv Python virtual environment.

To create a Python virtual environment you can use the `venv` module.

To do this you should do

```bash
python3 -m venv venv
```

Creating a venv called `venv`
To activate the venv you can do:

```bash
source venv/bin/activate
````

Or proceeed commands that need the venv with `./.venv/bin/python -m` and not have to run the command.

### Python Dependencies (pip)

You may need to install dependencies. And this will depend on your specific system and so on, but for most people this
is by
pip. [Ensure pip is added to path](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line).

If pip is installed, you can then install the dependencies with

```bash
pip install -r requirements.txt
```

### Google Sheets

#### Credentials.json

This scraper was designed to upload its results to Google Sheets, thus you may need to set up Google Sheets API access
and download the `credentials.json` file from Google Cloud Console, I used
a [Service Account](https://developers.google.com/workspace/guides/create-credentials#service-account) but if you want
to modify
and use something else be my guest.

This file should be placed in the same directory as
this [README.md](https://github.com/AllyToAll/AllycePowerCorpScraper/blob/master/README.md) file.

#### Cookies.json

This scraper requires cookies to access the data, this should be in the form of a `cookies.json` file placed in the same
directory as this [README.md](https://github.com/AllyToAll/AllycePowerCorpScraper/blob/master/README.md) file.

It should look something like this:

```json
{
  "cf_clearance": "<your_cf_clearance_cookie_here>",
  "erfereddde2": "<some numbers>",
  "gtrgioajorgjap": "<more numbers>",
  "PHPSESSID": "<your_phpsessid_cookie_here>"
}
```

#### Google Sheets Setup

The Google Sheets API is expected a Spreadsheet named `Power` with 2 sheets named `Prices` and `Income`

### Cookies

You must provide cookies to the scraper to access the data. You can do this by exporting cookies from your browser, and
entering them in [settings.py](https://github.com/AllyToAll/AllycePowerCorpScraper/blob/master/scraper/settings.py) file
in the `COOKIES` variable as a dictionary.

I have placed dummy text in place to help, simply replace it.

## Running the Scraper

To run the script ensure you are first in this directory and then run:

```bash
scrapy crawl corporations
```

Or if the venv is not activated.

```bash
./.venv/bin/python -m scrapy crawl corporations
```

# Using GitHub Actions

You can see I use GitHub Actions with
a [workflow](https://github.com/AllyToAll/AllycePowerCorpScraper/blob/master/.github/workflows/workflow.yml), to make
this work you must get your `credentials.json` and `cookies.json`.

For the `cookies.json` remove all white space and newlines such as below, leave the `credentials.json` as is

```json
{
  "cf_clearance": "<your_cf_clearance_cookie_here>",
  "erfereddde2": "<some numbers>",
  "gtrgioajorgjap": "<more numbers>",
  "PHPSESSID": "<your_phpsessid_cookie_here>"
}
```

Convert both files to Base64

Save this output into GitHub Secrets as `GOOGLE_CREDS` and `OPPRESS_COOKIES` respectively.

Then using my workflow, it will pick them up and run the scraper on a schedule every 6 hours.

## Issues I am aware of:

- Money is not correctly scraped from your account. It is entered as 0 in field P2.