from bigdata import BigData
from persons import Persons
from events import Events
from urls import Urls
import os


def init():
    try:
        os.remove('metric.db')
    except:
        pass
    bd = BigData()
    bd.open()
    bd.createTables()
    bd.insertTables('Input_Records-rk946c2nlklj4dcwnhqm.json')
    bd.close()

    e = Events()
    e.open()
    e.createTable()
    e.insertTable(shift="-08:00")
    e.close()

    p = Persons()
    p.open()
    p.createTable()
    p.insertPersons()
    p.close()

    u = Urls()
    u.open()
    u.createTable()
    u.insertAllTypes()
    u.close()

init()