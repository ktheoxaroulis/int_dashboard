# -*- coding: utf-8 -*-
import pandas as pd
import pathlib
from datetime import timedelta, datetime
import datetime as dt

###########################################
# Temp Read data from files directly
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df_finalorders = pd.read_csv(DATA_PATH.joinpath("finalorders.csv"))

df_finalorders= df_finalorders[["OrderId","OrderCounter","Store","TotalValue","CashValue","CardsValue","DiscountValue","Quantity",\
                                "UnitPrice","IsPayed","IsCanceled","IsDisposed","IsTreated","AfterOrderDiscountValue","ProductName_y",\
                                "MenuCategoryName","Division","BusinessMeals","Hour","Month","Year","WeekofYear","Quarter","DayofWeek",\
                                "OrderDate","Delivery","DayofMonth","DayofYear","UniqueItems","Orders","UniqueCls","UniqueScls","OrdersItems","OrdersSclsItems","OrdersClsItems","Μέση Θερμοκρασία Ημέρας","Μέγιστη Θερμοκρασία Ημέρας","Μικρότερη Θερμοκρασία Ημέρας","Βροχή","month","day","event"]]

#df_finalorders = [df_finalorders.columns.values.tolist()] + df_finalorders.values.tolist()

def getunique(name):
    return (df_finalorders[name].unique())

def filter_dataframe(df, store_statues,start_date, end_date):
    return df[
        (df["Store"].isin(store_statues)) & (df["OrderDate"]>=start_date) &  (df["OrderDate"]<= end_date)
    ]

def return_orders():
    return  df_finalorders.groupby(['Store','OrderDate']).agg(orders = ('OrderId','nunique') ).reset_index()

def return_sales():
    return  df_finalorders.groupby(['Store','OrderDate']).agg(sales = ('AfterOrderDiscountValue','sum') ).reset_index()

def return_quantity():
    return  df_finalorders.groupby(['Store','OrderDate']).agg(quantity = ('Quantity','sum') ).reset_index()



today = datetime.strptime(max(df_finalorders['OrderDate']), '%Y-%m-%d')
startweeks =(today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
endweeks = ((today - timedelta(days=today.weekday())) + timedelta(days=6)).strftime('%Y-%m-%d')

ltoday= datetime.strptime(max(df_finalorders['OrderDate']), '%Y-%m-%d')  - dt.timedelta(weeks=52)
startlweeks =(ltoday - timedelta(days=ltoday.weekday())).strftime('%Y-%m-%d')

first_day_of_month = today.replace(day=1).strftime('%Y-%m-%d')
first_day_of_lmonth = ltoday.replace(day=1).strftime('%Y-%m-%d')

last_day_of_month= (dt.date(today.year + today.month//12, today.month % 12 + 1, 1) - dt.timedelta(days=1)).strftime('%Y-%m-%d')
first_day_of_the_quarter= (dt.datetime(today.year,(today.month-1)//3+1,1)).strftime('%Y-%m-%d')
first_day_of_the_lquarter= (dt.datetime(ltoday.year,(ltoday.month-1)//3+1,1)).strftime('%Y-%m-%d')

last_day_of_the_quarter=(dt.datetime(today.year + 3*((today.month - 1) // 3 + 1)//12, 3*((today.month - 1) // 3 + 1)%12+1, 1) + dt.timedelta(days=-1)).strftime('%Y-%m-%d')

starting_day_of_cyear = (today.replace(month=1, day=1)).strftime('%Y-%m-%d')
starting_day_of_lyear = (ltoday.replace(month=1, day=1)).strftime('%Y-%m-%d')

ending_day_of_cyear = (today.replace(month=12, day=31)).strftime('%Y-%m-%d')

def return_meltdf(store_statues):
    df=df_finalorders[(df_finalorders["Store"].isin(store_statues))].groupby(["WeekofYear","Year"]).agg(Sales = ('AfterOrderDiscountValue','sum'), Orders = ('Orders','sum'),Quantity = ('Quantity','sum') ).reset_index()
    df['Avg Sales per Order'] = df.Sales / df.Orders
    df['Avg Item per Order'] = df.Quantity / df.Orders
    df['Avg Sales per Item'] = df.Sales / df.Quantity
    return df.melt(["WeekofYear","Year"])




