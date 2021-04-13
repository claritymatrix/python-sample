import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from sqlalchemy import create_engine
import psycopg2
ts.set_token('')
pro = ts.pro_api()
def get_data_income(code,start='20190101',end='20190425'):
    df = pro.income(ts_code = code,start_date=start,end_date=end)
    return df
def get_data_balancesheet(code,start='20190101',end='20190425'):
    df = pro.balancesheet(ts_code = code,start_date=start,end_date=end)
    return df

def get_data_cashflow(code,start='20190101',end='20190425'):
    df = pro.cashflow(ts_code = code,start_date=start,end_date=end)
    return df


engine = create_engine('postgresql+psycopg2://postgres:kdfjasfklasjdfkajsldfjoiqwjerio  jstock_data')
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
        data=get_data_income(code,start=start_date,end=end_date)
        print('the code is: {}' .format(code))
        insert_sql(data,'stock_income')
        data=get_data_balancesheet(code,start=start_date,end=end_date)
        insert_sql(data,'stock_balancesheet')
        data=get_data_cashflow(code,start=start_date,end=end_date)
        insert_sql(data,'stock_cashflow')

if __name__ == '__main__':
    get_data_daily()
