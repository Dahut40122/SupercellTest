# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:55:16 2023

@author: mathias BERNARD
"""
import pandas as pd
import matplotlib.pyplot as plt
import dateutil as dt
import sqlite3

fileLocation="path to the file sample.sqlite"
chartsLocation="path to the charts"
fileName="sample.sqlite"
debug=False

accountTable=pd.DataFrame();
sessionTable=pd.DataFrame();
purchaseTable=pd.DataFrame();

#SQL part

def loadData():
    try:
        connection=sqlite3.connect(fileLocation+fileName)
    except:
        print("ERROR: the file "+fileName+" could not be opened : check the path in the variable 'fileLocation'")
        quit()
    accountTable=pd.read_sql_query("SELECT * from account", connection)
    accountTable["created_time"]=pd.to_datetime(accountTable["created_time"], format="mixed").dt.date
    accountTable["account_id"]=pd.to_numeric(accountTable["account_id"])    
    sessionTable=pd.read_sql_query("SELECT * from account_date_session", connection)
    sessionTable["date"]=pd.to_datetime(sessionTable["date"])
    purchaseTable=pd.read_sql_query("SELECT * from iap_purchase", connection)
    purchaseTable["created_time"]=pd.to_datetime(purchaseTable["created_time"], format="mixed").dt.date
    
    connection.close()
    return accountTable, sessionTable, purchaseTable
 
def queryPart3():
    try:
        connection=sqlite3.connect(fileLocation+fileName)
    except:
        print("ERROR: the file "+fileName+" could not be opened : check the path in the variable 'fileLocation'")
        quit() 
    res=pd.read_sql_query("SELECT account.account_id, country_code, iap_price_usd_cents FROM account join iap_purchase on (iap_purchase.account_id=account.account_id)", connection)
    res["account_id"]=pd.to_numeric(res["account_id"])
    return res





#"pure" python part   
    
def simpleCharts():
    #those charts where not requested, it's to understand the given data
    tmp=accountTable[["created_time", "account_id"]].groupby(["created_time"]).count()
    curve= tmp.rename(columns={"account_id":"number of account created"})
    curve.plot(legend=None, figsize=(15,9),color="purple")
    plt.xlabel("")
    plt.ylabel("Number of accounts created")
    plt.title("Number of Accounts Created each Day")
    plt.savefig(chartsLocation+"\\additional1.png")
    
    tmp=tmp.cumsum()
    curve= tmp.rename(columns={"account_id":"total amount of accounts"})
    curve.plot(legend=None, figsize=(15,9), color="purple")
    plt.xlabel("")
    plt.ylabel("Number of accounts")
    plt.title("Total Number of Accounts")
    plt.savefig(chartsLocation+"\\additional2.png")
    
    curve=purchaseTable[["created_time", "iap_price_usd_cents"]].groupby(["created_time"]).sum()
    curve["iap_price_usd_cents"]=curve["iap_price_usd_cents"]/100
    curve.plot(legend=None, figsize=(15,9), color="Green")
    plt.title("Average Daily Revenues from In-app Purchasses in USD")
    plt.xlabel("")
    plt.ylabel("Daily revenues in USD")
    plt.savefig(chartsLocation+"\\additional3.png")
    
    curve=curve.cumsum()
    curve.plot(legend=None, figsize=(15,9), color="Green")
    plt.title("Cumulated Revenues of In-app Purchases in USD")
    plt.xlabel("")
    plt.ylabel("Cumulated revenues in USD")
    plt.savefig(chartsLocation+"\\additional4.png")
    
    
def part2Charts():
    curve=sessionTable[["date","session_count"]].groupby(["date"]).mean()
    
    curve.plot(legend=None, figsize=(15,9))
    plt.title("Average Daily Session Count")
    plt.xlabel("")
    plt.savefig(chartsLocation+"\\fig3.png")
    
    curve=sessionTable[["date","session_duration_sec"]].groupby(["date"]).mean()
    curve["session_duration_sec"]=curve["session_duration_sec"]/60
    
    
    
    curve.plot(legend=None, figsize=(15,9))
    plt.title("Average Daily Session Duration in Minutes")
    plt.xlabel("")
    plt.ylabel("Average duration in minutes")
    plt.savefig(chartsLocation+"\\fig2.png")
    
    
    curve=sessionTable[["date","session_count"]].groupby(["date"]).count()
    curve.plot(legend=None, figsize=(15,9), color="purple")
    plt.title("Number of Daily Active Users")
    plt.ylabel("Number of active users")
    plt.savefig(chartsLocation+"\\fig1.png")
    
    
def part3Charts():
    #top=20 for top 20
    top=20
    
    #Top 20 of the countries by users count
    data=accountTable[["country_code", "account_id"]].groupby(["country_code"]).count()
    data.sort_values(by=["account_id"], inplace=True, ascending=False)
    chart=data.iloc[0:top]
    
    #drawing the chart
    chart.plot(kind='bar', y='account_id', legend=None, color='purple', figsize=(15,9))
    plt.xlabel("Country code")
    plt.ylabel("Number of Users")
    plt.title("Top 20 Countries by User Count in 2016")
    plt.savefig(chartsLocation+"\\fig4.png")
    
    top=20
    
    #top 20 of the countries by revenue
    #using SQL query because it's more effective than pandas
    data2=queryPart3()
    data2=data2[["country_code", "iap_price_usd_cents"]].groupby(["country_code"]).sum()
    data2/=100
    data2.sort_values(by=["iap_price_usd_cents"], inplace=True, ascending=False)
    chart=data2.iloc[0:top+1]
    
    #chart drawing
    chart.plot(kind='bar', y='iap_price_usd_cents', legend=None, color='green', figsize=(15,9))
    plt.xlabel("Country code")
    plt.ylabel("Total revenues in USD")
    plt.title("Top 20 Countries by revenues in 2016")
    plt.savefig(chartsLocation+"\\fig5.png")
    
    
    #Top 20 of the countries by revenue per user
    data3=data.merge(data2, on="country_code")
    data3["revPerUsr"]=data3["iap_price_usd_cents"]/data3["account_id"]
    data3.sort_values(by=["revPerUsr"],inplace=True, ascending=False)
    chart=data3.iloc[0:top+1]
    
    #chart drawing
    chart.plot(kind='bar', y='revPerUsr', legend=None, color='green', figsize=(15,9))
    plt.xlabel("Country code")
    plt.ylabel("Average revenue per user in USD cents")
    plt.title("Top 20 Countries by revenue per user in 2016")
    plt.savefig(chartsLocation+"\\fig6.png")
    
    
    
    
    
    
    
    
accountTable, sessionTable, purchaseTable=loadData()
simpleCharts()
part2Charts()
part3Charts()
