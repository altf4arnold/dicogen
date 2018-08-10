# Simple wordlist and hash generator

## Dependencies :
* sqlite3
* hashlib
* itertools
* python 3

## How to run :

To generate the database (be carefull, the database can get very big very fast) :
```python3 dicogen.py gen```

To run to make a research (you already need the database) :
```python3 dicogen.py comp```

To run in brute force mode without database (use less RAM and 100% CPU of one core) :
```python3 dicogen.py```
