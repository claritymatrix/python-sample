import backtrader as bt
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import math
import numpy as np
import tushare as ts
import backtrader.analyzers as btanalyzers
import talib
import time


result = []
ts.set_token('217696db052cdea3e43bec347ee55a8ebbcb501e0b6d57d816a7542f')
pro = ts.pro_api()
class RVI(bt.Indicator):
    lines = ('std','pos','neg','rvi')
    plotlines = dict(
        std = dict(_plotskip = True),
        pos = dict(_plotskip = True),
        neg = dict(_plotskip = True),
        rvi = dict(_plotskip = False)
    )

    params = (
        ('period',20),
    )

    def __init__(self):
        self.lines.std = bt.talib.STDDEV(self.datas[0].close,timeperiod = 10,nbdev=2.0)


    def next(self):
        if self.lines.std[0] > self.lines.std[-1]:
            self.lines.pos[0] = self.lines.std[0]
        else:
            self.lines.pos[0] = 0

        if self.lines.std[0] < self.lines.std[-1]:
            self.lines.neg[0] = self.lines.std[0]
        else:
            self.lines.neg[0] = 0

        pos_nan = np.nan_to_num(self.lines.pos.get
                            (size = self.params.period))
        neg_nan = np.nan_to_num(self.lines.neg.get
                                (size = self.params.period))

        Usum = math.fsum(pos_nan)
        Dsum = math.fsum(neg_nan)

        if (Usum + Dsum )== 0:
            self.lines.rvi[0] = 0

        else:
            self.lines.rvi[0] = 100 * Usum /(Usum + Dsum)

def get_data(stock_id,start_date = '2018-01-01',end_date = '2020-01-11'):
    ts.set_token('217696db052cdea3e43bec347ee55a8ebbcb501e0b6d57d816a7542f')
    pro = ts.pro_api()
    df = ts.pro_bar(ts_code = stock_id,adj='qfq',start_date = start_date,end_date = end_date)
    dates = pd.to_datetime(df['trade_date'])

    df = df[['open','high','low','close','vol']]
    df['openinterest'] = 0
    df.rename(columns = {'vol':'volume'},inplace = True)
    df.index = dates
    df.sort_index(ascending = True,inplace = True)

    return df

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.rvi = RVI()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        '''need to recode place'''
        up = 60
        down = 35
        if not self.position:
            if self.rvi.rvi[0] > up:
                if self.rvi.rvi[-1] < up and self.rvi.rvi[-2] < up:
                    self.order = self.order_target_percent(target = 0.95)
        else:
            if self.rvi.rvi[0] < down:
                if self.rvi.rvi[-1] > down and self.rvi.rvi[-2] > down:
                    self.order = self.sell()

def get_code():

    codes =  pro.index_weight(index_code='000016.SH', start_date='20210101', end_date='20210131')['con_code'].sort_values()

    return codes



def stock_result_func(stock_id,start_date='2019-01-01',end_date='2021-02-10'):



    df = get_data(stock_id,start_date,end_date)

    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname = df)

    cerebro.adddata(data)

    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission= 0.01)
    cerebro.addsizer(bt.sizers.PercentSizer,percents = 100)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio,_name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns,_name='returns')

    print(f'Start Protfolio Value {cerebro.broker.getvalue()}')
    result = cerebro.run()


    ratio_result = [[ x.analyzers.returns.get_analysis()['rtot'],
                    x.analyzers.returns.get_analysis()['rnorm100'],
                    x.analyzers.drawdown.get_analysis()['drawdown'],
                    x.analyzers.sharpe.get_analysis()['sharperatio']] for x in result]


    ratio_df = pd.DataFrame(ratio_result,columns=['total return','norm100','drawdown','sharperatio'])

    print(ratio_df)

    return ratio_df



if __name__ == '__main__':

    stock_anlysis_result = pd.DataFrame(columns = ['total return','norm100','drawdown','shraperatio'])
    codes = get_code()
    code_id = pd.Series(codes)
    end_date = time.strftime("%Y-%m-%d", time.localtime())
    start_date = '2020-01-01'

    ## output settings
    output_csv = "/root/python-sample/python-stock-model/" + time.strftime("%Y%m%d", time.localtime()) + ".csv"
    i = 0

    for code in codes:
        print("----------------------------------------------------------------------------")
        print("code name is %s" % code)
        try:
            tmp = stock_result_func(code,start_date = start_date,end_date = end_date)
        except:
            continue

        stock_anlysis_result = pd.concat([stock_anlysis_result,tmp],ignore_index=True)



    stock_anlysis_result.to_csv(output_csv)
