import backtrader as bt


if __name__ == "__main__":


    cerebro = bt.Cerebro()

    cerebro.broker.setcash(100000.00)

    print("Starting Protfolio Value: %.2f" % cerebro.broker.getvalue())


    cerebro.run()


    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
