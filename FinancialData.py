import numpy as np
import pandas as pd
import csv
from currency_converter import CurrencyConverter

c = CurrencyConverter()


class DataLoader:
  data = pd.read_csv(r'/Users/mhanley/Desktop/stocks.csv')
  df = pd.DataFrame(data, columns=['id', 'name', 'price', 'symbol', 'industry',
                                   'market', 'currency', 'date'])

  @classmethod
  def cleandata(cls):
    cls.df['symbol'] = np.where(cls.df['symbol'].isnull(), None,
                                cls.df['symbol'])
    cls.df['industry'] = np.where(cls.df['industry'].isnull(), None,
                                  cls.df['industry'])
    cls.df['market'] = np.where(cls.df['market'].isnull(), None,
                                cls.df['market'])
    cls.df['date'] = np.where(cls.df['date'].isnull(), None, cls.df['date'])

  @classmethod
  def convertdates(cls):
    cls.df['date'] = pd.to_datetime(cls.df['date'])


class Analysis(DataLoader):
  DataLoader.cleandata()
  DataLoader.convertdates()

  @classmethod
  def minmaxvals(self, name):

    df = pd.DataFrame(DataLoader.df,
                      columns=['name', 'industry', 'market', 'price'])

    namemaxes = df.loc[
      DataLoader.df.groupby('name')['price'].idxmax()].sort_values('price',
                                                                   ascending=False)
    namemins = df.loc[
      DataLoader.df.groupby('name')['price'].idxmin()].sort_values('price',
                                                                   ascending=True)
    indmaxes = df.loc[
      DataLoader.df.groupby('industry')['price'].idxmax()].sort_values('price',
                                                                       ascending=False)
    indmins = df.loc[
      DataLoader.df.groupby('industry')['price'].idxmin()].sort_values('price',
                                                                       ascending=True)
    markmaxes = df.loc[
      DataLoader.df.groupby('market')['price'].idxmax()].sort_values('price',
                                                                     ascending=False)
    markmins = df.loc[
      DataLoader.df.groupby('market')['price'].idxmin()].sort_values('price',
                                                                     ascending=True)

    if not namemaxes.loc[df['name'] == name].empty:
      maxvalue = namemaxes.loc[df['name'] == name]['price'].iloc[0]
    elif not indmaxes.loc[df['industry'] == name].empty:
      maxvalue = indmaxes.loc[df['industry'] == name]['price'].iloc[0]
    elif not markmaxes.loc[df['market'] == name].empty:
      maxvalue = markmaxes.loc[df['market'] == name]['price'].iloc[0]

    if not namemins.loc[df['name'] == name].empty:
      minvalue = namemins.loc[df['name'] == name]['price'].iloc[0]
    elif not indmins.loc[df['industry'] == name].empty:
      minvalue = indmins.loc[df['industry'] == name]['price'].iloc[0]
    elif not markmins.loc[df['market'] == name].empty:
      minvalue = markmins.loc[df['market'] == name]['price'].iloc[0]

    return f' {minvalue:.2f}($) - {maxvalue:.2f}($) '

  @classmethod
  def findavg(self, name):

    avg_name = DataLoader.df.groupby(['name'], as_index=False).price.mean()
    avg_industry = DataLoader.df.groupby(['industry'],
                                         as_index=False).price.mean()
    avg_market = DataLoader.df.groupby(['market'], as_index=False).price.mean()

    if not avg_name.loc[avg_name['name'] == name].empty:
      avg_value = avg_name.loc[avg_name['name'] == name]['price'].iloc[0]

    elif not avg_industry.loc[avg_industry['industry'] == name].empty:
      avg_value = \
        avg_industry.loc[avg_industry['industry'] == name]['price'].iloc[0]

    elif not avg_market.loc[avg_market['market'] == name].empty:
      avg_value = avg_market.loc[avg_market['market'] == name]['price'].iloc[0]

    return avg_value

  @classmethod
  def findmedian(self, name):

    med_name = DataLoader.df.groupby(['name'], as_index=False).price.median()
    med_industry = DataLoader.df.groupby(['industry'],
                                         as_index=False).price.median()
    med_market = DataLoader.df.groupby(['market'],
                                       as_index=False).price.median()

    if not med_name.loc[med_name['name'] == name].empty:
      med_value = med_name.loc[med_name['name'] == name]['price'].iloc[0]

    elif not med_industry.loc[med_industry['industry'] == name].empty:
      med_value = \
        med_industry.loc[med_industry['industry'] == name]['price'].iloc[0]

    elif not med_market.loc[med_market['market'] == name].empty:
      med_value = med_market.loc[med_market['market'] == name]['price'].iloc[0]

    return med_value

  @classmethod
  def convertcur(cls, name, new):

    cur_name = DataLoader.df.groupby(['name'], as_index=False).currency.max()
    cur_symbol = DataLoader.df.groupby(['symbol'],
                                       as_index=False).currency.max()

    price_name = DataLoader.df.groupby(['name'], as_index=False).price.max()
    price_symbol = DataLoader.df.groupby(['symbol'], as_index=False).price.max()

    if not cur_name.loc[cur_name['name'] == name].empty:
      cur_type = cur_name.loc[cur_name['name'] == name]['currency'].iloc[0]

    elif not cur_symbol.loc[cur_symbol['symbol'] == name].empty:
      cur_type = cur_symbol.loc[cur_symbol['symbol'] == name]['currency'].iloc[
        0]

    if not price_name.loc[price_name['name'] == name].empty:
      price = price_name.loc[price_name['name'] == name]['price'].iloc[0]

    elif not price_symbol.loc[price_symbol['symbol'] == name].empty:
      price = price_symbol.loc[price_symbol['symbol'] == name]['price'].iloc[0]

    conversion = c.convert(price, cur_type, new)

    print(cur_type)
    print(price)
    print(conversion)

    return cur_type, price, conversion


class CreateReport(Analysis):

  def report(self, name):
    avg = Analysis.findavg(name)
    med = Analysis.findmedian(name)
    minmax = Analysis.minmaxvals(name)

    data = [
      f'      {name}     ' + '|' + f'  {avg:.2f}($)  ' + '|' + f'  {med:.2f}($)  ' + '|' + f'{minmax} ']

    return data

  def write_file(self, name):
    header = [
      ' name/industry/market ' + '|' + ' average_price ' + '|' + ' median_price ' + '|' + ' minimum - maximum ']

    with open('report.txt', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)

      # write the header
      writer.writerow(header)

      # write the data
      writer.writerow(self.report(name))


# Enter a stock symbol or company name followed by a comma within
# a.convertcur function.
# Next enter the currency you would like to convert to.
a = Analysis()
a.convertcur('GNRT', 'CAD')

# Creates a report based on given name, industry, or market in
# the write_file method
c = CreateReport()
c.write_file('Semiconductors')
