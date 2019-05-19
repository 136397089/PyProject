import MySQLdb
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def GetAllCloseDate(tablename,NumType,engine):
    sql = "select close from " + tablename+' ; '
    data = pd.read_sql_query(sql, engine)


