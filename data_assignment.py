# Note datetime is the module name, but datetime is a class two. To call the datetime class use datetime.datetime
import datetime

def remove_from_str(s, substrings_to_remove) -> str:
    """
    Pretty inefficient but whatever.
    Use regex for speedup.
    """
    ret = s
    for sub in substrings_to_remove:
        ret = ret.replace(sub, "")
    return(ret)

def next_interval(t: datetime.datetime) -> datetime.datetime:
    """
    Return the next 5 minute interval
    """
    return(t + datetime.timedelta(minutes=5))

# print(datetime.datetime(2021, 9, 13, 12, 10))
# print(next_interval(datetime.datetime(2021, 9, 13, 12, 10)))

chars_to_remove = {'$', '€', ',', "BTC"}
f = open("Assignment 1 - Data.txt", 'r')
text = f.read()

rows = text.split('\n')

d = dict()
t = []
indexes = dict()

columns = rows[0].split(';')

for trade_type in columns[2:]:
    d[trade_type] = dict()

for i in range(len(columns)):
    indexes[i] = columns[i] 

#Setting up dictionary for easy lookup
for row in rows[1:]:
    split = row.split(';')
    # print(split)
    for i in range(len(split)):
        if i == 0:
            date = split[i]
        elif i == 1:
            time_of_day = split[i]
        else:
            trade_time = datetime.datetime.strptime(date + ' ' + time_of_day, "%m/%d/%Y %I:%M %p")
            trade_type = indexes[i]
            d[trade_type][trade_time] = float(remove_from_str(split[i], chars_to_remove))

#Setting up times and 
times = []
for i in d:
    for j in d[i]:
        times.append(j)
    break
times.sort()

#USD, EUR, BTC, ETH
currency = [1000,0,0,0]

total = 0

numslots = len(times)
buyBTC_USD = [0 for n in range(0, numslots-1)]
buyBTC_EUR = [0 for n in range(0, numslots-1)]
buyETH_BTC = [0 for n in range(0, numslots-1)]
buyETH_USD = [0 for n in range(0, numslots-1)]
buyETH_EUR = [0 for n in range(0, numslots-1)]
#Compare if you can sell to bid by buying ask
for i in range(0, numslots - 1):
    if d['BTC/USD Bid'][times[i+1]] > d['BTC/USD Ask'][times[i]]:
        buyBTC_USD[i] = d['BTC/USD Bid'][times[i+1]] * d['BTC/USD Ask Size'][times[i]] \
            - d['BTC/USD Ask'][times[i]] * d['BTC/USD Ask Size'][times[i]]
        

    if d['BTC/EUR Bid'][times[i+1]] > d['BTC/EUR Ask'][times[i]]:
        buyBTC_EUR[i] = d['BTC/EUR Bid'][times[i+1]] - d['BTC/EUR Ask'][times[i]]

    if d['ETH/BTC Bid'][times[i+1]] > d['ETH/BTC Ask'][times[i]]:
        buyETH_BTC[i] = d['ETH/BTC Bid'][times[i+1]] - d['ETH/BTC Ask'][times[i]]

    if d['ETH/USD Bid'][times[i+1]] > d['ETH/USD Ask'][times[i]]:
        buyETH_USD[i] = d['ETH/USD Bid'][times[i+1]] - d['ETH/USD Ask'][times[i]]
        
    if d['ETH/EUR Bid'][times[i+1]] > d['ETH/EUR Ask'][times[i]]:
        buyETH_EUR[i] = d['ETH/EUR Bid'][times[i+1]] - d['ETH/EUR Ask'][times[i]]

#print(buyBTC_USD)
#print(buybid)
# for i in d:
#     print(i)
#     print(d[i])
output = [[]]
maxusd = [1000]
stringoutput = ['']

print(times[0].strftime("%m/%d/%y %I:%M%p"))
        

'''
INVENTORY INDEX:
0 = USD
1 = EUR
2 = BTC
3 = ETH
'''
#transaction = ['BTC/USD Bid', 'BTC/USD Ask', 'BTC/EUR Bid', 'BTC/EUR Ask', 'ETH/BTC Bid', 'ETH/BTC Ask', 'EUR/USD Bid', 'EUR/USD Ask', 'ETH/USD Bid', 'ETH/USD Ask', 'ETH/EUR Bid', 'ETH/EUR Ask', 'Nothing']
def combo(inventory, datetimeIndex, outputstring):
    if datetimeIndex == len(times):
        if inventory[0] > maxusd[0]:
            maxusd[0] = inventory[0]
            output[0] = inventory
            stringoutput[0] = outputstring
        return
    if inventory[0] > 0:
        usd_tobuy_btc_total = min(d['BTC/USD Ask'][times[datetimeIndex]] * d['BTC/USD Ask Size'][times[datetimeIndex]], inventory[0])
        btc_count = usd_tobuy_btc_total / d['BTC/USD Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,BTC/USD-{};'.format(btc_count)
        combo([inventory[0] - usd_tobuy_btc_total, inventory[1], inventory[2] + btc_count, inventory[3]], datetimeIndex + 1, tempstring)

        usd_tobuy_eth_total = min(d['ETH/USD Ask'][times[datetimeIndex]] * d['ETH/USD Ask Size'][times[datetimeIndex]], inventory[0])
        eth_count = usd_tobuy_eth_total / d['ETH/USD Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,ETH/USD-{};'.format(eth_count)
        combo([inventory[0] - usd_tobuy_eth_total, inventory[1], inventory[2], inventory[3] + eth_count], datetimeIndex + 1, tempstring)

        usd_tobuy_eur_total = min(d['EUR/USD Ask'][times[datetimeIndex]] * d['EUR/USD Ask Size'][times[datetimeIndex]], inventory[0])
        eur_count = usd_tobuy_eur_total / d['EUR/USD Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,EUR/USD-{};'.format(eur_count)
        combo([inventory[0] - usd_tobuy_eur_total, inventory[1] + eur_count, inventory[2], inventory[3]], datetimeIndex + 1, tempstring)

    if inventory[1] > 0:
        eur_tobuy_btc_total = min(d['BTC/EUR Ask'][times[datetimeIndex]] * d['BTC/EUR Ask Size'][times[datetimeIndex]], inventory[1])
        btc_count = eur_tobuy_btc_total / d['BTC/EUR Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,BTC/EUR-{};'.format(btc_count)
        combo([inventory[0], inventory[1] - eur_tobuy_btc_total, inventory[2] + btc_count, inventory[3]], datetimeIndex + 1, tempstring)

        eur_tobuy_eth_total = min(d['ETH/EUR Ask'][times[datetimeIndex]] * d['ETH/EUR Ask Size'][times[datetimeIndex]], inventory[1])
        eth_count = eur_tobuy_eth_total / d['ETH/EUR Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,ETH/EUR-{};'.format(eth_count)
        combo([inventory[0], inventory[1] - eur_tobuy_eth_total, inventory[2], inventory[3] + eth_count], datetimeIndex + 1, tempstring)

        eur_tobuy_usd_total = min(d['EUR/USD Bid Size'][times[datetimeIndex]] / d['EUR/USD Bid'][times[datetimeIndex]], inventory[1])
        usd_count = eur_tobuy_usd_total * d['EUR/USD Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,EUR/USD-{};'.format(usd_count)
        combo([inventory[0] + usd_count, inventory[1] - eur_tobuy_usd_total, inventory[2], inventory[3]], datetimeIndex + 1, tempstring)

    if inventory[2] > 0:
        btc_tobuy_usd_total = min(d['BTC/USD Bid Size'][times[datetimeIndex]] / d['BTC/USD Bid'][times[datetimeIndex]], inventory[2])
        usd_count = btc_tobuy_usd_total * d['BTC/USD Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,BTC/USD-{};'.format(usd_count)
        combo([inventory[0] + usd_count, inventory[1], inventory[2] - btc_tobuy_usd_total, inventory[3]], datetimeIndex + 1, tempstring)

        btc_tobuy_eur_total = min(d['BTC/EUR Bid Size'][times[datetimeIndex]] / d['BTC/EUR Bid'][times[datetimeIndex]], inventory[2])
        eur_count = btc_tobuy_eur_total * d['BTC/EUR Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,BTC/EUR-{};'.format(eur_count)
        combo([inventory[0], inventory[1] + eur_count, inventory[2] - btc_tobuy_eur_total, inventory[3]], datetimeIndex + 1, tempstring)

        btc_tobuy_eth_total = min(d['ETH/BTC Ask'][times[datetimeIndex]] * d['ETH/BTC Ask Size'][times[datetimeIndex]], inventory[2])
        eth_count = btc_tobuy_eth_total / d['BTC/EUR Ask'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';BUY,ETH/BTC-{};'.format(eth_count)
        combo([inventory[0], inventory[1], inventory[2] - btc_tobuy_eth_total, inventory[3] + eth_count], datetimeIndex + 1, tempstring)
    
    if inventory[3] > 0:
        eth_tobuy_usd_total = min(d['ETH/USD Bid Size'][times[datetimeIndex]] / d['ETH/USD Bid'][times[datetimeIndex]], inventory[3])
        usd_count = eth_tobuy_usd_total * d['ETH/USD Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,ETH/USD-{};'.format(usd_count)
        combo([inventory[0] + usd_count, inventory[1], inventory[2], inventory[3] - eth_tobuy_usd_total], datetimeIndex + 1, tempstring)

        eth_tobuy_eur_total = min(d['ETH/EUR Bid Size'][times[datetimeIndex]] / d['ETH/EUR Bid'][times[datetimeIndex]], inventory[3])
        eur_count = eth_tobuy_eur_total * d['ETH/EUR Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,ETH/EUR-{};'.format(eur_count)
        combo([inventory[0], inventory[1] + eur_count, inventory[2], inventory[3] - eth_tobuy_usd_total], datetimeIndex + 1, tempstring)

        eth_tobuy_btc_total = min(d['ETH/BTC Bid Size'][times[datetimeIndex]] / d['ETH/BTC Bid'][times[datetimeIndex]], inventory[3])
        btc_count = eth_tobuy_btc_total * d['ETH/BTC Bid'][times[datetimeIndex]]
        tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';SELL,ETH/BTC-{};'.format(btc_count)
        combo([inventory[0], inventory[1], inventory[2] + btc_count, inventory[3] - eth_tobuy_btc_total], datetimeIndex + 1, tempstring)
    
    tempstring = outputstring + str(times[datetimeIndex].strftime("%m/%d/%y %I:%M%p")) + ';DO NOTHING;'
    combo(inventory, datetimeIndex + 1, tempstring)

combo([1000,0,0,0],0,"")


print(output,stringoutput, "yes")