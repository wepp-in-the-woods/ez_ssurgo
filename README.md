# Python to identify MUKEY and query SSURGO

Requires numpy and rosetta


rosetta fork. clone to site-packages

https://github.com/rogerlew/rosetta


## usage

```python
ssc = SurgoSoilCollection([2485028])
ssc.makeWeppSoils()
for mukey, soil in ssc.weppSoils.items():
    soil.write('tests')
```


## DB Browser for sqlite3

For viewing SSURGO .db sqlite3 cache files

https://sqlitebrowser.org/

