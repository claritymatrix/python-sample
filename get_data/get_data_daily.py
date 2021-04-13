import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from sqlalchemy import create_engine
import psycopg2
ts.set_token('f')
pro = ts.pro_api()
def get_data(code,start='20190101',end='20190425'):
    df=ts.pro_bar(ts_code=code, adj='qfq', start_date=start, end_date=end)
    return df
engine = create_engine('postgresql+psycopg2://postgres:3r123423refjlsdjfasdflajljlstock_data')
def insert_sql(data,db_name,if_exists='append'):
    #使用try...except..continue避免出现错误，运行崩溃
    try:
        data.to_sql(db_name,engine,index=False,if_exists=if_exists)
        #print(code+'写入数据库成功')
    except:
        pass

def get_code():
    codes = pro.stock_basic(list_status='L').ts_code.values
    return codes

def get_data_daily(start_date ='20100101',end_date='20210410'): 
    for code in get_code():
        time.sleep(random.randint(1,2))
        data=get_data(code,start=start_date,end=end_date)
        print('the code is: {}' .format(code))
        insert_sql(data,'stock_daily')

if __name__ == '__main__':
    get_data_daily()
