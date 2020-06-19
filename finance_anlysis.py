import pandas as pd
import numpy as np





def show_all_data():
    """show all data"""



    pd_finance_anlysis = pd.read_csv('600309.csv',index_col = [0],keep_default_na = False)

    select_rows=['20181231','20171231','20161231','20151231','20141231','20131231','20121231','20111231']


    pd_finance_anlysis = pd_finance_anlysis[select_rows]



    #print(pd_finance_anlysis)

    print(pd_finance_anlysis.index)

    ## 金融资产
    print(pd_finance_anlysis.iloc[2])

if __name__ == '__main__':


    show_all_data()
