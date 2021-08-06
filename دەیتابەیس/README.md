# Python utility

A simple python CLI which downloads existing poems from allekok using its API.
And stores the retrieved data in sqlite database named `allekok.db`.
Database tables are defined with `peewee ORM` models in `models.py`.

Due to using an ORM, the db itself is swappable and, it can be changed to other SQL-based DBs.

## Install dependencies
```bash
# If you don't have python installed already, first install python 
# see https://www.python.org/


# It's recommended to install dependencies in a virtualenv, 
# but you can install it directly in your main python.

# cd into root of repo
pip install -r requirements.txt
```

## See the available options
```Bash
python cli.py --help
```

### Output
```Bash
usage: cli.py [-h] [-v]

A simple CLI for exporting allekok data to a sqlite database.
It will have a file-based output as well in future.
Use -v or -vv to see the logs.

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity
```

Currently, it's supports two level of verbosity `-v` and `-vv` for `logging.INFO` and `logging.DEBUG`.

### Run the script
```python
python3 cli.py -v

# As we've specified -v, it will output some basic logs and inserts data into the mentioned db.
```

## Author
[@Dawood](https://github.com/Dawoodkhorsandi)

