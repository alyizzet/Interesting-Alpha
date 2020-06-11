from QuantConnect.Python import PythonQuandl
from NodaTime import DateTimeZone

class ForexCarryTradeAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1) 
        self.SetEndDate(2019, 12, 11)  
        self.SetCash(25000)
        
        tickers = ["USDEUR", "USDZAR", "USDAUD",
                   "USDJPY", "USDTRY", "USDINR",
                   "USDCNY", "USDMXN", "USDCAD"]
                   
        rate_symbols = ["BCB/17900","BCB/17906","BCB/17880",
                        "BCB/17903","BCB/17907","BCB/17901",
                        "BCB/17899", "BCB/17904", "BCB/17881"]  
        self.symbols = {}
        
        for i in range(len(tickers)):
            symbol = self.AddForex(tickers[i], Resolution.Daily, Market.Oanda).Symbol
            self.AddData(QuandlRate, rate_symbols[i], Resolution.Daily, DateTimeZone.Utc, True)
            self.symbols[str(symbol)] = rate_symbols[i]
        self.Schedule.On(self.DateRules.MonthStart("USDEUR"), self.TimeRules.AfterMarketOpen("USDEUR"), Action(self.Rebalance))
    def Rebalance(self):
        top_symbols = sorted(self.symbols, key = lambda x: self.Securities[self.symbols[x]].Price)

        self.SetHoldings(top_symbols[0], -0.5)
        self.SetHoldings(top_symbols[-1], 0.5)
    def OnData(self, data):
        pass
class QuandlRate(PythonQuandl):
    def __init__(self):
        self.ValueColumnName = 'Value'
        
        # This is a Carry Trade Algorithm which utilizes the differemce between interest rates in forex pairs.