# Gets certain stocks listed on the NSE and saves the data in a CSV file named data.csv

import csv
import time
from nsetools import Nse

nse = Nse()

# Stocks that we're interested in
stock_codes = ["infy", "lt"]

# Gets the buy price of 'stock'
def get_buy_price(stock):
    try:
        if nse.is_valid_code(stock):
            return nse.get_quote(stock).get("buyPrice1")
        print("Invalid stock code.")    
    except:
        print("ERROR: Could not get buy price.")
    return -1

# Initialize values
x_value = 0
values = {}
for stock in stock_codes:
    values[stock] = nse.get_quote(stock).get("buyPrice1")
    
fieldNames = ["x_value", *stock_codes]

# Test to make sure the values have been initialized
# because it may take some time for the values to update
#print(*list(values.values()))

# Write the headers row to the file
with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a') as csv_file:
        for stock in stock_codes:
            values[stock] = get_buy_price(stock)

        update = False
        for stock in stock_codes:
            price = get_buy_price(stock)
            if price >= 0 and values[stock] != price:
                update = True
                values[stock] = price

        # Only write to the file if there is some change
        if update:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
            info = {"x_value": x_value}
            for val in values:
                info[val] = values.get(val)

            csv_writer.writerow(info)
            print(x_value, *list(values.values()))

            x_value += 1

    time.sleep(1)
    
