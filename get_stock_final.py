from jqdatasdk import *
import argparse
import pandas as pd
import numpy as np

def parser_args():
    """Parser arg used to get commandline args"""


    parser = argparse.ArgumentParser(description="get stock final")


    parser.add_argument('--fromdate','-f',default='2010-01-01',help='start date in YYYY-MM-DD')

    parser.add_argument('--todate','-t',default='2019-01-01',help='end date in YYYY-MM-DD')

    parser.add_argument('--stockid','-s',default='000651.XSHE',help='stock id in 000000.XSHE/XSHG')


    return parser.parse_args()



def get_stock_money(args):


    """get stock money sheet to get money detail"""



    q = query(finance.STK_CASHFLOW_STATEMENT).filter(finance.STK_CASHFLOW_STATEMENT.code == args.stockid,finance.STK_CASHFLOW_STATEMENT.pub_date >= args.fromdate,
                                                     finance.STK_CASHFLOW_STATEMENT.pub_date <= args.todate,finance.STK_CASHFLOW_STATEMENT.report_type == 0).limit(2000)


    df = finance.run_query(q)


def get_stock_final(args):

    """get stock final function used to get stock final detail"""


    q = query(finance.STK_BALANCE_SHEET).filter(finance.STK_BALANCE_SHEET.code == args.stockid,finance.STK_BALANCE_SHEET.pub_date >= args.fromdate,finance.STK_BALANCE_SHEET.pub_date <= args.todate,
                                                finance.STK_BALANCE_SHEET.report_type == 0 ).limit(2000)

    df = finance.run_query(q)

    #df.fillna(value = 0 )
    #df.replace({np.nan:0})
    ###print(df)

    ###print(df.dtypes)





    pd.set_option('display.float_format','{:,}'.format)
    pd.set_option('display.max_columns',25)

    #print(df[['total_assets','total_liability','total_owner_equities']])

    #print(df['report_date'].str.contains('12-31'))
    s = df['report_date']

    test = s.apply(lambda x: x.month == 12)


    # 将会计科目分为金融资产、营运资产、长期股权投资、长期经营资产、营运负债、短期债务、长期债务、股东权益

    ## 资产

    ## 货币资金、交易性金融资产、可供出售金融资产、持有至到期投资、投资性房产、应收利息、应收股利、买入返售金融资产、（这里不考虑递延收益分项，进一步分析中才对递延收益进一步分析）
    account_subject_finance = ['cash_equivalents','trading_assets','hold_for_sale_assets','hold_to_maturity_investments','investment_property','interest_receivable','dividend_receivable','loan_and_advance_current_assets','bought_sellback_assets','loan_and_advance_noncurrent_assets']

    ## 应收票据、应收账款、预付账款、存货、其他流动资产、长期应收款、递延所得税资产（将递延所得税先纳入营运资产，靠经济不断发展的，这部分应该大才对）
    account_subject_operating_assets = ['bill_receivable','account_receivable','advance_payment','affiliated_company_receivable','inventories','expendable_biological_asset','longterm_receivable_account']

    account_subject_operating_assets.append('deferred_tax_assets')

    ## 长期股权投资
    account_subject_long_term_investment = ['longterm_equity_invest']

    ## 长期经营资产：固定资产、在建工程、工程物资、固定资产清理、生产性生物资产、油气资产、无形资产、开发支出、商誉、长期待摊费用
    account_subject_long_term_operating_assets = ['fixed_assets','constru_in_process','construction_materials','fix_assets_liquidation','biological_assets','oil_gas_assets','intangible_assets','development_expenditure','good_will','long_deferred_expense']


    ## 其他需要考虑的资产

    ## 其他应收款、一年内到期的非流动资产、其他流动资产

    account_subject_operating_assets.append('other_payable')

    account_subject_operating_assets.append('non_current_asset_in_one_year')

    account_subject_finance.append('other_current_assets')

    ## 负债

    ### 短期债务：短期借款、交易性金融负债、应付利息、应付短期债券、一年内到期的非流动负债
    account_subject_floating_debt = ['shortterm_loan','trading_libility','interest_payable','dividend_payable','non_current_liability_in_one_year']


    ### 营运负债：应付票据、应付账款、预收账款、应付手续费及佣金、应付职工薪酬、应交税费、递延收益——流动负债、其他流动负债、递延所得税负债

    account_subject_operating_liabilites = []

    account_subject_long_term_liabilites = []

    ## 权益

    account_subject_shareholder_equity = []

    df_finance_balance = finanbalance(df)

    pd.reset_option('display.float_format')
def coperationrun(df):
    """长期营运资本 = 营运资本 - 营运负债。
    营运资本包括应收票据、应收账款、预付账款、存货（含消耗性生物资产）、其他流动资产、长期应收款、营运递延所得税资产
    营运负债：应收票据、预收账款、应付手续费以及佣金、应付职工薪酬、应交税费、递延收益——流动负债、其他流动负债、递延收益——非流动负债、营运递延所得税负债"""

    print("get coperation running:")

    df_running_assets = df [['bill_receivable','account_receivable','advance_payment','other_receivable','expandable_biological_assets']]

def longinvestbalance(df):
    """长期股权投资通过持股比例享有被投资公司经济活动赚取的利益的方式，实现更多现金。"""


    print("get long invest balance:")

    df_long_invest_balance = df['longterm_equity_invest']

    return df_long_invest_balance




def finanbalance(df):
    """金融资产通过收取利息、现金股利、租金以及资产差价的方式实现更多现金。广义的金融资产包括银行存款、其他货币资金、交易型金融资产、持有至到期投资、可供出售金融资产、投资性房地产等。狭义的金融资产包括
    非现金资产以外的金融资产，包括交易型金融资产、可供出售金融资产等,包括：货币资金、交易型金融资产、发放贷款以及垫款、可供出售金融资产、持有至到期投资、投资性房地产、应收利息、应收股利、买入返售资产、
    金融资产递延所得税资产-递延所得税负债"""


    print("get finance balance:")

    df['deferred_tax_assets'] =  df['deferred_tax_assets'] - df['deferred_tax_liability']


    df_finance_balance = df[['cash_equivalents','trading_assets','hold_for_sale_assets','hold_to_maturity_investments','investment_property',
                             'interest_receivable','dividend_receivable','deferred_tax_assets']]



    df = df_finance_balance.fillna(value = 0,inplace = False)

    df['hold_to_maturity_investments'].astype(float,copy= False)

    #print(df_finance_balance.dtypes)

    s = pd.Series(df.apply(lambda x: x.sum(),axis=1))
    #print(df_finance_balance)

    df_return = pd.concat([df,s],axis=1)

    print(df_return)

    return df_return


if __name__ == '__main__':


    auth('18380152997','2wsx3edc')

    args = parser_args()

    get_stock_final(args)
