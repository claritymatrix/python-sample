import numpy as np
import pandas as pd
import backtrader as bt
import datetime
import backtrader.indicators as btind
import argparse
import math



class mystrategy(bt.Strategy):

    params=(('exitbars',5),
            ('mapperiod',55),
            ('mapperiod02',20),
            ('sellflag',0),
            ('buyflag',0),
            ('ownprice',0),
    )
    def log(self,txt,dt = None):
        '''Logging function for this strategy'''

        dt = dt or self.datas[0].datetime.date(0)

        print("%s,%s " %(dt.isoformat(),txt))


    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None

        #self.macd = bt.indicators.MACD(self.datas[0])
        #self.sma05 = btind.SMA(self.datas[0],period = self.params.mapperiod,subplot=False)
        self.sma20 = btind.SMA(self.datas[0],period = self.params.mapperiod02,subplot = False)
        self.bbrands = btind.BBands(self.datas[0],subplot = False)
        self.max55 = bt.talib.MAX(self.datas[0].high,period = self.params.mapperiod,plot = False)

        self.min55 = bt.talib.MIN(self.datas[0].low,period = self.params.mapperiod,plot = False)
        self.atr = btind.ATR(self.datas[0])

        self.stake = 4000

        self.ownprice = 0


        ## self.signaltop = btind.CrossOver(self.dataclose,self.bbrands.top,plot=False)







        self.buyprice = None
        self.buycomm = None




    def notify_order(self,order):

        if order.status in [order.submitted,order.accepted]:
            return

        if order.status in [order.completed]:
            if order.isbuy():
                #self.log("buy executed %.2f" % order.executed.price)
                self.log("buy executed price %.2f,cost: %.2f,comm %.2f" %(order.executed.price,
                                                                          order.executed.value,
                                                                          order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                # set sizer



            else:
                #self.log("sell executed %.2f" % order.executed.price)
                self.log("sell executed price %.2f ,cost %.2f, comm %.2f" %(order.executed.price,
                                                                            order.executed.value,
                                                                            order.executed.comm))


            self.bar_executed = len(self)

        elif order.status in [order.canceled,order.margin,order.rejected]:
            self.log("order canceled/margin/rejected")

        self.order = none

    def notify_trade(self,trade):
            if not trade.isclosed:
                return
            self.log('operation profit gross %.2f net %.2f' %(trade.pnl,trade.pnlcomm))

    def next(self):

        sizer = self.stake
        self.log('close %.2f' % self.dataclose[0])




        if self.order:
            return




        if not self.position:

            #if  (self.signallow > 0.0) and (self.params.buyflag == 1):

            if (self.dataclose[0] < self.min55[-1]) :

                #self.params.buyflag = 0
                #self.sellflag = 0

                sizer = np.where(self.stake > 0,4000,0)

                self.order = self.buy(size = sizer)

                self.log('buy create %.2f %.2f,atr is %.2f' %(self.dataclose[0],sizer,sizer * self.atr[-1]))
                self.stake = self.stake - sizer
                self.ownprice = np.where(self.params.ownprice < self.dataclose[0],self.params.ownprice,self.dataclose[0])




        else:
            #print('the crossover signal is %.2f' % self.signalcrossover[0])
            #if  (self.signalcrossover <  0.0) and (self.params.sellflag == 1) and (self.params.ownprice < self.dataclose[0]):

            if   (self.dataclose[0] > (self.ownprice + 2.0 * self.atr[0] * 4000)):
                #self.params.sellflag = 0
                print("the params stake is %.2f"  %self.stake)
                sizer = np.where(self.stake == 0,4000,0)

                self.log('sell create %.2f %.2f' %(self.dataclose[0],sizer))
                self.order = self.sell(size = sizer)

                self.stake = self.stake + sizer





def add_data(filename = 'cz50.csv'):

    dataframe = pd.read_csv(filename,index_col = 0,parse_dates =True)

    #print(dataframe)

    return dataframe

def parser_args():
    """parse args used to get command line args"""
    parser = argparse.ArgumentParser(description='atr')


    parser.add_argument('--stockid','-s',default='sz50.csv',help="input the stock file name like 000651.csv")

    parser.add_argument('--fromdate','-f',default='2011-01-01',help="start date in yyyy-mm-dd format")

    parser.add_argument('--todate','-t',default=(datetime.datetime.now() + datetime.timedelta(days = -7)).strftime("%Y-%m-%d"),help="end date in YYYY-MM-DD format")

    parser.add_argument('--cash',default='1800000',type=int,help='starting cash')

    parser.add_argument('--comm',default='0.0012',type=float,help='Commission for operation')

    parser.add_argument('--stake',default=1,type=int,help="Stake to apply in each operation")

    return parser.parse_args()






def runstrategy():
    """run strategy is use to run strategy"""

    args = parser_args()


    fromdate = datetime.datetime.strptime(args.fromdate,"%Y-%m-%d")
    todate = datetime.datetime.strptime(args.todate,"%Y-%m-%d")




    cerebro = bt.Cerebro()

    cerebro.broker.setcash(args.cash)


    data = bt.feeds.PandasData(dataname = add_data(args.stockid),fromdate = fromdate,todate=todate)


    cerebro.adddata(data)
    cerebro.addstrategy(mystrategy)
    cerebro.broker.setcommission(commission = args.comm)


    print("Start Protfolio Value:%.2f" %cerebro.broker.getvalue())
    cerebro.run()

    print("Final Protfolio Value:%.2f" % cerebro.broker.getvalue())
    cerebro.plot()



if __name__ == "__main__":
    runstrategy()
