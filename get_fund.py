import numpy as np
import pandas as pd
import datetime
import tushare as ts
import getopt
import sys

def run_get_fund():
    stock_name=""
    file_name = ""

    ts.set_token('25799613aa8715bb9bcc8788b295db8f95b9cdd4774a64389df0abdb')
    pro = ts.pro_api()




    try:
        opts,args = getopt.getopt(args = sys.argv[1:],shortopts="f:s:",longopts=["stockname=","filename="])


        print(sys.argv[1:])


    except getopt.GetoptError:
        print("Error:python3 get_fund.py -f sz50.csv -s sz50")


    for opt,arg in opts:
        if opt in ("-s","--stockname"):
            stock_name = arg
        elif opt in ("-f","--filename"):
            file_name = arg



    df = ts.get_hist_data(stock_name)

    df.drop(labels = ["price_change","p_change","ma5","ma10","ma20","v_ma5","v_ma10","v_ma20"],axis = 1,inplace = True)


    df4 = df.loc[:,['open','close','high','low','volume']]
    df4.sort_index(axis = 0,inplace = True)
    df4.reset_index(inplace = True)

    df4["date"] = df4["date"] + " 00:00:00.005"
    df4["openinterest"] = 0


    df4.set_index("date",inplace = True)

    df4.to_csv("./" + file_name)



if __name__ == "__main__":

    run_get_fund()
