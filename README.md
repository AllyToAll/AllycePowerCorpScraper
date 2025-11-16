# Allyce Power Corporations Scraper

## Overview

The example snippets provided are in Bash, thus if your terminal uses a different shell you may need to adapt them.

## Requirements

### Bash

If instead you know how to execute it in Powershell or whatever else you're using, be my guest.

On Windows for example the default shell is not in `Bash` but in `Powershell`.

Thus you will need `Git Bash` from `Git-SCM` from https://git-scm.com/install/

### Python

If you already have this set up, skip this step

You will also need Python installed. You can download it from https://www.python.org/downloads/

Ensure Python is added to path,
see https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line

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
is by pip.
See https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line

If pip is installed, you can then install the dependencies with

```bash
pip install -r requirements.txt
```

### Google Sheets

This scraper was designed to upload its results to Google Sheets, thus you may need to set up Google Sheets API access
and download the `credentials.json` file from Google Cloud Console, I used a Service Account but if you want to modify
and use something else be my guest.
See https://developers.google.com/workspace/guides/create-credentials#service-account

This file should be placed in the same directory as this `README.md file`.

The Google Sheets API is expected a Spreadsheet named `Power` with 2 sheets named `Prices` and `Income`

### Cookies

You must provide cookies to the scraper to access the data. You can do this by exporting cookies from your browser, and
entering them in settings.py file in the `COOKIES` variable as a dictionary.

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

## Issues I am aware of:

- Money is not correctly scraped from your account. It is entered as 0 in field P2.