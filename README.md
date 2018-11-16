# Simple Parser

## Description

A text parsing tool that takes a well-formatted text file as input and returns a total word count and count for each word.

## Installation
Clone repo and change directory to `simple-parser`
```
git clone https://github.com/egsy/simple-parser.git
cd simple-parser
```

Create a new `virtualenv` and activate
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip3 install -e .
```


## Usage
Set Flask environment variables
```
export FLASK_APP=python_parser
export FLASK_ENV=development
```
Initialize database then start builtin server
```
flask init-db
flask run
```

From a modern browser, visit http://127.0.0.1:5000/ to see the text parsing web app
