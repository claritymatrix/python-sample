import numpy as np
import pandas as pd
import datetime
import jqdatasdk
import sys
import getopt
import time

if __name__ == "__main__":

    stock_name = ""
    file_name = ""
    jqdatasdk.auth('18380152997','2wsx3edc')


    try:

        # 获取命令行的数据
        # 输入：股票代码 、保存的文件名
        # 输出：将股票的当前数据保存到指定文件
        # 时间：从2011-01-01 至今

        opts,args = getopt.getopt(args = sys.argv[1:],shortopts = "f:s:",longopts=["stockname=","filename="])
        print(sys.argv[1:])

    except getopt.GetoptError:

        print('Error:python3 get_stock.py -f 000651.csv -s 000651.XSHE')
        print('or python3 get_stock.py --filename=000651.csv --stockname=000651.XSHE')


    for opt,arg in opts:
        if opt in ("-s","--stockname"):
            stock_name = arg
        elif opt in ("-f","--filename"):
            file_name = arg

    #print("stock_name is ",stock_name)

    #print("file name is",file_name)


    df = jqdatasdk.get_price(security = stock_name,start_date='2011-1-1',end_date=datetime.datetime.today(),frequency='daily')


    df.to_csv(file_name)


    df_stock = pd.read_csv(file_name)

    df_stock["Unnamed: 0"] = df_stock["Unnamed: 0"] + " 00:00:00.005"

    df_stock.to_csv(file_name,index=0)
