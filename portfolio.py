import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
import pandas_datareader as data
import matplotlib.pyplot as plt
import csv
import math
import os
import getpass
import requests
import bs4 as bs
import sqlite3
import quandl
import sys


class Ticker:
    def __init__(self, ticker, pe, fpe, eps, pb, ps, peg, beta):
        self.ticker = ticker
        self.pe = pe
        self.fpe = fpe
        self.eps = eps
        self.pb = pb
        self.ps = ps
        self.peg = peg
        self.beta = beta


def create_database():
    try:
        conn = sqlite3.connect(r'C:\Users\jessm\uusi\portfolio.db')
        print('Opened database succesfully.')
        try:
            conn.execute('CREATE TABLE SP500(\
                id INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,\
                Symbol TEXT NOT NULL,\
                Name TEXT NOT NULL,\
                Sector TEXT NOT NULL,\
                Industry TEXT ,\
                Market_Cap FLOAT,\
                Dividends FLOAT,\
                Divident_Yield FLOAT,\
                Divident_Yield_Five_Years FLOAT ,\
                EPS FLOAT,\
                Price_to_Earnings FLOAT,\
                Forward_Price_to_Earnings FLOAT,\
                Price_to_Book FLOAT,\
                PEG_Ratio FLOAT,\
                Price_to_Sale FLOAT,\
                Beta FLOAT,\
                Yearly_Growth FLOAT,\
                Profit_Margin FLOAT)')
            conn.execute('CREATE TABLE Nasdaq100(\
                id INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,\
                Symbol TEXT NOT NULL,\
                Name TEXT NOT NULL,\
                Sector TEXT NOT NULL,\
                Industry TEXT ,\
                Market_Cap FLOAT,\
                Dividends FLOAT,\
                Divident_Yield FLOAT,\
                Divident_Yield_Five_Years FLOAT ,\
                EPS FLOAT,\
                Price_to_Earnings FLOAT,\
                Forward_Price_to_Earnings FLOAT,\
                Price_to_Book FLOAT,\
                PEG_Ratio FLOAT,\
                Price_to_Sale FLOAT,\
                Beta FLOAT,\
                Yearly_Growth FLOAT,\
                Profit_Margin FLOAT)')
            conn.commit()
        except sqlite3.Error as e:
            print("Failed to create tables. Error:",e)
    except sqlite3.Error as e:
        print("Failed to open database. Error:",e)
    finally:
        #conn.execute('Drop table SP500')
        #conn.execute('Drop table Nasdaq100')
        #conn.commit()
        conn.close()
        
def get_graph():
    
    
    while(True):

        #if user does not give any input
        start_date = '2000-01-01'
        data_ticker = 'SPY'
        end_date = dt.date.today()

        #getting user input
        ticker = input('Give ticker(AAPL, MSFT, SPY). IF empty SPY will be chosen: ')
        staring_day = input('Give starting date(if left empty date will be 2000-01-01): ')
        ending_date = input('Give ending date(if left empty date will be today): ')

        #check if user gives input
        if ticker:
            data_ticker = ticker
        if staring_day:
            start_date = staring_day
        if ending_date:
            end_daet = ending_date


        try:
            #getting data from yahoo finance
            data_ticker = data.get_data_yahoo(data_ticker,start = start_date, end= end_date)

            #getting closing price
            closing_price = data_ticker['Close']

            #interested in weekdays
            all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
            closing_price = closing_price.reindex(all_weekdays)
            closing_price = closing_price.fillna(method='ffill')

            descriped_data = closing_price.describe()

            #index_data = data.DataReader(index[0],'yahoo',start_date,end_date)
            rolling_data = closing_price

            #20,100,200 day moving averages
            short_rolling = rolling_data.rolling(window=20).mean()
            mid_rolling = rolling_data.rolling(window=100).mean()
            long_rolling = rolling_data.rolling(window=200).mean()

            #creating the chart
            fig, ax = plt.subplots(figsize=(16,9))
            ax.plot(rolling_data.index, rolling_data,label='SPY')
            ax.plot(short_rolling.index, short_rolling, label='20 days rolling')
            ax.plot(mid_rolling.index, mid_rolling, label='100 days rolling')
            ax.plot(long_rolling.index, long_rolling, label='200 days rolling')

            #adding labes
            ax.set_xlabel('Date')
            ax.set_ylabel('Adjusted closing price')
            #ax.legend()
            plt.show()
            break
        except Exception as e:
            print('Please give a correct ticker symbol with capital letters(AAPL not aapl) and date in correct format(2010-01-01)\n')


def Menu():
 

    while(1):
        print('\n1) Show the chart of a ticker')
        print('2) Show portfolio allocation')
        print('3) Add S&P 500 components to database')
        print('4) Add Nasdaq 100 components to database')
        print('5) Create SP500 and Nasdaq100 databases(takes a while)')
        print('6) Get valuation')
        print('0) End the program')
        try:
            choice = int(input('Your choice: '))
            return choice
        except ValueError:
            print('Please give one of the numbers above')



def addToTables(tickers,table,i,conn):
   
    try:
        conn = sqlite3.connect(r'C:\Users\jessm\uusi\portfolio.db')
        print(table)
        if table == 'SP500':
   
            print('SP')
            conn.execute('INSERT INTO SP500 Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(i,tickers[0],tickers[1],tickers[2],tickers[3],tickers[4],tickers[5],tickers[6],tickers[7],tickers[8],tickers[9],tickers[10],tickers[11],tickers[12],tickers[13],tickers[14],tickers[15],tickers[16]))
        elif table == 'Nasdaq100':
            print('Nasdaq')
           
            conn.execute('INSERT INTO Nasdaq100 Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(i,tickers[0],tickers[1],tickers[2],tickers[3],tickers[4],tickers[5],tickers[6],tickers[7],tickers[8],tickers[9],tickers[10],tickers[11],tickers[12],tickers[13],tickers[14],tickers[15],tickers[16]))
        conn.commit()
    except sqlite3.Error as e:
        print("Failed to add table. Error:",e)
   



def get_components(table_name):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        if (table_name == 'SP500'):
            filename  =path +'/sp_500_companies.csv'
            df = pd.read_csv(filename)
        elif (table_name == 'Nasdaq100'):
            filename  =path+'/nasdaq_100_companies.xls'
            df = pd.read_excel(filename)
        else:
            print('Wrong name')
            return
        print(df)
        print(table_name)
        #ticker_yf = yf.Ticker('WMT').info
        #print(ticker_yf)
        conn = sqlite3.connect(r'C:\Users\jessm\uusi\portfolio.db')
        tables_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print('Opened database succesfully.')

        date = dt.datetime.today()
        weekno = dt.datetime.today().weekday()
        print(weekno)
        weekday = date.replace(year=date.year-1).weekday()
        if weekday == 5:
            date = date.replace(year=date.year-1) - dt.timedelta (days=1) 
        elif weekday == 6:
            date = date.replace(year=date.year-1) - dt.timedelta (days=2) 
        else:
            date = date.replace(year=date.year-1)
        print(date)

        for column in range(len(df)):
            
            try:
                
                ticker = df.values[column][0]
                ticker_yf = yf.Ticker(ticker).info
                company_name = df.values[column][1]
                sector = df.values[column][2]
                
                price_year_ago = yf.Ticker(ticker).history(start=date,end=date)['Close'].iloc[0]
                current_price = yf.Ticker(ticker).history()
                last_price = current_price.tail(1)['Close'].iloc[0]
                price_change = round((last_price / price_year_ago-1)*100,2)
               # print(price_year_ago)
               # print(last_price)
                #print(price_change)
                tables_list[0] = df.values[column][0]
                tables_list[1] = df.values[column][1]
                tables_list[2] = ticker_yf.get('sector')
                tables_list[3] = ticker_yf.get('industry')
                tables_list[4] = round((ticker_yf.get('marketCap') / (10**9)),2)
                #tables_list[4] = ticker_yf.get('marketCap')
                tables_list[5] = ticker_yf.get('dividendRate')
                try:
                    tables_list[6] = round((ticker_yf.get('dividendYield') *100),2)
                except TypeError as e:
                    tables_list[6] = None
                #tables_list[6] = ticker_yf.get('dividendYield')
                tables_list[7] = ticker_yf.get('fiveYearAvgDividendYield')
                tables_list[8] = ticker_yf.get('trailingEps')
                tables_list[9] = ticker_yf.get('trailingPE')

                tables_list[10] = ticker_yf.get('forwardPE')
                tables_list[11] = ticker_yf.get('priceToBook')
                tables_list[12] = ticker_yf.get('pegRatio')
                tables_list[13] = ticker_yf.get('priceToSalesTrailing12Months')
                tables_list[14] = ticker_yf.get('beta')
                tables_list[15] = price_change
                #tables_list[15] = ticker_yf.get('52WeekChange')
                tables_list[16] = round((ticker_yf.get('profitMargins')*100),2)
                #tables_list[16] = ticker_yf.get('profitMargins')
                print(tables_list)
                conn.execute('UPDATE SP500 SET Sector = ? WHERE Symbol = ?',(ticker_yf.get('sector'),ticker))
                conn.execute('UPDATE SP500 SET Yearly_Growth = ?, Market_Cap = ?, Divident_Yield = ?, Profit_Margin = ?  WHERE Symbol = ?',(price_change,round((ticker_yf.get('marketCap') / (10**9)),2), tables_list[6],round((ticker_yf.get('profitMargins')*100),2),ticker))
                conn.commit()
                #addToTables(tables_list,table_name,column,conn)
            except Exception as e:
                print(e)
                continue
        conn.close()
    except sqlite3.Error as e:
        print("Failed to open database. Error:",e)
def sort(allocation,tickers):
        for i in range(len(allocation)):  
            for j in range(0, len(allocation)-i-1): 
                if allocation[j] > allocation[j+1] : 
                    allocation[j], allocation[j+1] = allocation[j+1], allocation[j]
                    tickers[j], tickers[j+1] = tickers[j+1], tickers[j]

def show_portfolio_allocation_pie():
    #lists for tickers and allcation for 
    tickers = []
    allocation = []
    price = []
    total = 0

    portfoliofile = 'quotes ({}).csv'.format(7)
    #getting portfolio name
    try:
        portfoliofile_name = input('Give filename of the portfolio(without .csv): ')
        if (portfoliofile_name):
            path = os.path.dirname(os.path.realpath(__file__))
            filename  =path+ '/' + portfoliofile_name + '.csv'
        else:
            user = getpass.getuser()
            filename = 'C:/Users/{}/Downloads/{}'.format(user,portfoliofile)
        #opening the file
        df = pd.read_csv(filename)

        #dropping the unnessessary columns
        df.drop(columns=['Date'], inplace=True)
        df.drop(columns=['Trade Date'],inplace=True)
        df.drop(columns=['Low Limit'], inplace=True)
        df.drop(columns=['High Limit'],inplace=True)
        df.drop(columns=['Time'], inplace=True)

        #showing the data
        print(df)
        #end_date = dt.date.today()
        date = dt.date.today()
        date = date.replace(year=date.year-1)

     
        #getting the values for the portfolio
        for column in range(len(df)):
            
            if not math.isnan(df.values[column][7]):
                tickers.append(df.values[column][0])
                current_price = yf.Ticker(df.values[column][0]).history()
                last_price = (current_price.tail(1)['Close'].iloc[0])
                #print(last_price)
                total_allocation = last_price * df.values[column][8]
                total += total_allocation
                #print(total_allocation)
                price.append(total_allocation)

        #allcation
        other = 0 
        i = 0 
        for ticker in price:
            
            ticker_allocation = ticker / total
            if ticker_allocation < 0.02:
                other += ticker_allocation
                print(tickers[i])
                tickers.remove(tickers[i])
                i -= 1
            else:
                allocation.append(ticker_allocation)
            i += 1    
        if other > 0:
            allocation.append(other)
            tickers.append('Others')
            sort(allocation,tickers)
        #showing the pie chart
        fig, ax = plt.subplots()
        ax.pie(allocation,labels=tickers,autopct='%1.1f%%',shadow=True,startangle=90,normalize=False)
        ax.axis('equal')
        ax.legend(loc =0 )
        plt.show()
    except FileNotFoundError:
        print('Please give a correct file name')
def Menu2():
    while(1):
        print('1) Valuation data for a specific stock')
        print('2) Valuation data for a portfolio')
        print('3) Valuation data for a S&P 500 index components')
        print('4) Valuation data for a Nasdaq 100 index components')
        try:
            choice = int(input('Your choice: '))
            return choice
        except ValueError:
            print('Please give one of the numbers above')



def get_ticker_info(ticker_symbol):
    info_list = [0,0,0,0,0,0,0,0,0,0,0,0]
    ticker_yf = yf.Ticker(ticker_symbol).info
    print(ticker_yf)
    info_list[0] = ticker_symbol
    try:
        info_list[1] = round((ticker_yf.get('marketCap') / (10**9)),2)
    except TypeError:
        info_list[1] = None
    info_list[2] = ticker_yf.get('fiveYearAvgDividendYield')
    info_list[3] = ticker_yf.get('trailingEps')
    info_list[4] = ticker_yf.get('trailingPE')
    info_list[5] = ticker_yf.get('forwardPE')
    info_list[6] = ticker_yf.get('priceToBook')
    info_list[7] = ticker_yf.get('pegRatio')
    info_list[8] = ticker_yf.get('priceToSalesTrailing12Months')
    info_list[9] = ticker_yf.get('beta')
    try:
        info_list[10] = round((ticker_yf.get('profitMargins')*100),2)
    except TypeError:
        info_list[10] = None
    info_list[11] = ticker_yf.get('sector')
    print(ticker_yf.get('sector'))
    return info_list

def get_terminal_value():
    return


def get_intrinsic_value():
    return


def compare_sp(ticker_pe,sp_pe):
   # api_key = 'u--QSx6xTWY9pbyaV-p-'
   # quandl.ApiConfig.api_key = api_key
   # sp_pe = quandl.get("MULTPL/SP500_PE_RATIO_MONTH")
   # sp = np.float(sp_pe.values[len(sp_pe)-1])
    #print(sp)
    try:
        if ticker_pe <=  sp_pe - 5:
            return 'Undervalued'
        elif (sp_pe - 5 < ticker_pe < sp_pe + 5):
            return 'Fair valued'
        else:
            return 'Overvalued'
    except TypeError as e:
        return 'No P/E Ratio'



def compare_pe(ticker_pe):
    pe_list = [0,0]
    api_key = 'u--QSx6xTWY9pbyaV-p-'
    quandl.ApiConfig.api_key = api_key
    sp_pe = quandl.get("MULTPL/SP500_PE_RATIO_MONTH")
    sp = np.float(sp_pe.values[len(sp_pe)-1])
    try:
        if not math.isnan(ticker_pe) or ticker_pe < 0:
            if (ticker_pe <= 10):
                pe_list[0] = 'Undervalued'
                pe_list[1] = compare_sp(ticker_pe,sp)
            elif(10 < ticker_pe < 15):
                pe_list[0] = 'Fairvalued'
                pe_list[1] = compare_sp(ticker_pe,sp)
            else:
                pe_list[0] = 'Overvalued'
                pe_list[1]= compare_sp(ticker_pe,sp)

        else:
            pe_list[0] = 'Overvalued'
            pe_list[1] = 'Overvalued'
        
    except TypeError as e:
        
        pe_list[0] = 'No P/E Ratio'
        pe_list[1] = 'No P/E Ratio'
        
    print('**',pe_list)
    return pe_list, sp

def compare_ps(ticker_ps):
    try:
        if 0 < ticker_ps < 1:
            return 'Undervalued'
        elif 1 <= ticker_ps <= 10:
            return 'Fairvalued'
        else:
            return 'Overvalued'
    except TypeError as e:
        return 'No P/S Ratio'

def compare_peg(ticker_peg):
    try:
        if 0 < ticker_peg < 1:
            return 'Undervalued'
        elif 1 <= ticker_peg <= 2:
            return 'Fairvalued'
        else:
            return 'Overvalued'
    except TypeError as e:
        return 'No PEG Ratio'

def compare_pb(ticker_pb):
    try:
        
        if 0 < ticker_pb < 1:
            return 'Undervalued'
        elif 1 <= ticker_pb <= 3:
            return 'Fairvalued'
        else:
            return 'Overvalued'
    except TypeError as e:
        return 'No P/B Ratio'
def compare_beta(beta):
    try:
        if 0 < beta < 1:
            return 'Less than market'
        elif 1 <= beta <= 1.2:
            return 'Same as market'
        else:
            return 'More than market'
    except TypeError as e:
        return 'No Beta available'


def compare_to_sector(ticker_industry, ticker_pe, ticker_fpe):
    print(ticker_industry,ticker_pe,ticker_fpe)
    conn = sqlite3.connect(r'C:\Users\jessm\uusi\portfolio.db')
    sp = conn.execute('SELECT Symbol, Price_to_Earnings , Forward_Price_to_Earnings, Industry FROM SP500 WHERE Sector = ?',(ticker_industry,))
    print(sp.fetchall())
    conn.commit()
    nq = conn.execute('SELECT Symbol, Price_to_Earnings , Forward_Price_to_Earnings  FROM Nasdaq100 WHERE Sector = ?',(ticker_industry,))
    #print(nq.fetchall())
    conn.commit()
    trailing_pe_all = 0
    forward_pe_all = 0
    count_fpe = 0
    count_pe = 0
    pe_values = [0,0]
    sp_500_stock  =[]
    for ticker1 in sp:
        print(ticker1[0])
        if not math.isnan(ticker1[1]):
            trailing_pe_all += ticker1[1]
            count_pe += 1
            sp_500_stock.append(ticker1[0])
        if not math.isnan(ticker1[2]):          
            forward_pe_all += ticker1[2]
            count_fpe += 1
            
    print(sp_500_stock)
    for ticker1 in nq:
        print(ticker1[0])
        if ticker1[0] in sp_500_stock:
            pass
        else:
            print(ticker1)
            try:
                trailing_pe_all += ticker1[1]
                count_pe += 1
            except TypeError as e:
                continue
            try:          
                forward_pe_all += ticker1[2]
                count_fpe += 1
            except TypeError as e:
                continue
    print(sp_500_stock)
    print(count_pe,count_fpe)
    sector_fpe_ratio = 0
    sector_pe_ratio = 0
    try:
        sector_pe_ratio = trailing_pe_all / count_pe
        sector_fpe_ratio = forward_pe_all / count_fpe
        print(sector_pe_ratio)
        print(sector_fpe_ratio)
    except ValueError as e:
        pass
    except ZeroDivisionError:
        pass
    
    try:
        if (ticker_pe < 0):
            pe_values[0] = 'Overvalued'
        elif (ticker_pe < sector_pe_ratio -5):
            pe_values[0] = 'Undervalued'
        elif (sector_pe_ratio - 5 <= ticker_pe <= sector_pe_ratio + 5):
            pe_values[0] = 'Fairvalued'
        else:
            pe_values[0] = 'Overvalued'
    except TypeError:
        pe_values[0] = 'No P/E ratio'

    try:
        if (ticker_fpe < 0):
            pe_values[1] = 'Overvalued'
        elif (ticker_fpe < sector_fpe_ratio -5):
            pe_values[1] = 'Undervalued'
        elif (sector_fpe_ratio - 5 <= ticker_fpe <= sector_fpe_ratio + 5):
            pe_values[1] = 'Fairvalued'
        else:
            pe_values[1] = 'Overvalued'
    except TypeError:
        pe_values[1] = 'No P/E ratio'
    conn.close()
    return pe_values,sector_pe_ratio,sector_fpe_ratio

    
            

    



    return
def stock_valuation():
    choice = Menu2()
    if (choice == 1):    

        ticker = input('Give ticker(AAPL, MSFT, SPY, etc.): ')
        info_list = get_ticker_info(ticker)

        pe_list,spe = compare_pe(info_list[4])
        sector_value,pe,fpe = compare_to_sector(info_list[11],info_list[4],info_list[5])
        print(sector_value)
        print('\n****Valuation statistics for {}****'.format(info_list[0]))
        print('P/E ratio on normal metrics: {} vs {} --> {}'.format(info_list[4],15,pe_list[0]))
        print('P/E ratio on vs average market: {} vs {} --> {}'.format(info_list[4],spe,pe_list[1]))
        print('P/E ratio on vs sector({}): {} vs {} --> {}'.format(info_list[11],info_list[4],round(pe,2),sector_value[0]))
        print('Forward P/E ratio on vs sector({}): {} vs {} --> {}'.format(info_list[11],info_list[5],round(fpe,2),sector_value[1]))
        print('P/S ratio (highly sector dependent. Usually Techonology has higher values): {} vs {} --> {}'.format(info_list[8],5,compare_ps(info_list[8])))
        print('P/B ratio (higher value --> growth stock): {} vs {} --> {}'.format(info_list[6],2,compare_pb(info_list[6])))
        print('PEG ratio: {} vs {} --> {}'.format(info_list[7],1,compare_peg(info_list[7])))
        print('Potential Swing: {} vs {} --> {}'.format(info_list[9],1,compare_beta(info_list[9])))
        print('*************************************\n')


    elif (choice == 2):
        portfolio_tickers = []
        path = os.path.dirname(os.path.realpath(__file__))
        portolioname = input('Give your portfolio (.csv or .xls format): ')
        filename  =path +'/'+portolioname
        if '.csv' in portolioname:
            df = pd.read_csv(filename)
        elif '.xls' in portolioname:
            df = pd.read_excel(filename)
        else:
            print('Given portfolio was not in a correct format')
            return
        for ticker in range(len(df)):
            info_list = get_ticker_info(ticker)
            new_ticker = Ticker(info_list[0],info_list[1],info_list[2],info_list[3],info_list[4],info_list[5],info_list[6],info_list[7],info_list[8],info_list[9],info_list[10])
            portfolio_tickers.append(new_ticker)


    elif (choice == 3):
        print('TODO')
        
    elif (choice == 4):
        print('TODO')
    else:
        print('Given number was not 1-4')


def main():
    
    while(True):
        choice = Menu()

        if (choice == 0):
                break
        
        elif (choice == 1):    
            get_graph()
        
        elif (choice == 2):
            show_portfolio_allocation_pie()
        
        elif (choice == 3):
            get_components('SP500')
        
        elif (choice == 4):
            get_components('Nasdaq100')
        
        elif (choice == 5):
            create_database()
        
        elif (choice == 6):
            stock_valuation()
            
        else:
            print('Please give one of the numbers above\n')

main()