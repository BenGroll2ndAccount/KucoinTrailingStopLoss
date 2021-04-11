import json
import kucoin.client
from kucoin.client import Client
import time
import math
########################################################################################
############################## YOUR STUFF GOES HERE ####################################

api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
api_passphrase = "API_PASSPHRASE"

########################################################################################



client = Client(api_key, api_secret, api_passphrase)
global currency
global pair
global offset
global enter
global holding
global slprice
global price_offset
def findHolding(currency):
    accounts = client.get_accounts()
    found = ""
    index = 0
    for i in range(len(accounts)):
        if accounts[i]['currency'] == currency and accounts[i]['type'] == "trade":
            found = accounts[i]
            break
    holding = found['balance']
    if holding == None:
        print("Currently not owning " + currency + " , abandoning.")
    else:
        holding = holding
        print("Currently holding " + str(holding) + " " + str(currency))
        return holding


def initialize_tracker():
    global currency
    global pair
    global offset
    global holding
    global enter
    global slprice
    global price_offset
    print("-------------------------------")
    holding = math.trunc(float(findHolding(currency)) * 10_000 ) / 10_000
    poffset = enter * ( offset / 100.0)
    first_stop_loss =  enter - poffset
    price_offset = poffset
    slprice = first_stop_loss
    print("First Stop Loss price: " + str(first_stop_loss))
    print("#####################################################################")
    while True:
        doTick()
        time.sleep(10)
    

def doTick():
    global price_offset
    global slprice
    this_tick_price = float(client.get_ticker(pair)['price'])
    this_tick_stoploss = this_tick_price - price_offset
    if this_tick_stoploss > slprice:
        print(">>")
        print("Old Stop Loss: " + str(slprice) )
        print("New Stop Loss: " + str(this_tick_stoploss))
        slprice = this_tick_stoploss
    if this_tick_price < slprice:
        print("Triggered Stop Loss. Selling out.")
        sellout()

def sellout():
    global pair
    global slprice
    order = client.create_market_order(pair, client.SIDE_SELL, size = holding)
    order_details = client.get_order(order["orderId"])
    price = float(order_details["dealFunds"]) / float(order_details["dealSize"])
    print("Sold out @  " + str(price) + "")
    input()

def startup():
    global currency
    global pair
    global offset
    global enter
    print(">> Starting....")
    print("Insert Currency: ")
    currency = str(input())
    print("Insert Pair: ")
    pair = str(input())
    print("Insert Offset ( % ): ")
    offset = float(input())
    print("Insert enter price: ")
    enter = float(input())
    initialize_tracker()
    
startup()