# README
This python script will help batch download phish recordings from the spreadsheet. The spreadsheet is located [here](https://docs.google.com/spreadsheets/d/1yAXu83gJBz08cW5OXoqNuN1IbvDXD2vCrDKj4zn1qmU/htmlview)

You must download it locally as an excel .xlsx file

## Installation
To install dependencies in a virtual environment (on linux or mac):
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
To use the program source the virtual environment and call main.py with the path to the spreadsheet and year. Optionally you can specify and output directory.

For example you can create a subfolder with the year you wish to download and then download the albums from that year:

```
python3 main.py -t 2021 -f index.xlsx -o 2021
```
