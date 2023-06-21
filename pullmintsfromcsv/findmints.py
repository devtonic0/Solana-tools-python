import csv
import json

wallets = {}  # a dictionary to store wallet information

# define the price points and their corresponding SOL denominations
price_points = {
    4.2: "4.2",
    4.8: "4.8",
    5.5: "5.5"
}

# read the CSV file and loop through each row
with open("transactions.csv", "r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # skip header row
    for row in csv_reader:
        # get the sender's address and SOL amount from the SolTransfer columns
        sender_address = row[13]
        sol_amount = row[15]

        # check if the SOL amount matches one of the desired denominations
        for price_point, sol_denomination in price_points.items():
            if sol_amount == sol_denomination:
                # exclude the specified wallet from the search
                if sender_address == "8N21adKmqy2wsDs1ofcpcivzFQSzEbEoLBCwBrvMk8dG":
                    continue
                
                # retrieve the sender's wallet information
                if sender_address not in wallets:
                    wallets[sender_address] = {"4.2 sol": 0, "4.8 sol": 0, "5.5 sol": 0}

                # update the wallet's transaction count and SOL amount for the current price point
                wallets[sender_address][f"{price_point} sol"] += 1

# print the total number of mints for each price point
for price_point in price_points:
    total_mints = sum(wallets[wallet][f"{price_point} sol"] for wallet in wallets)
    print(f"Total mints at {price_point} SOL: {total_mints}")
    
# write the wallet list to a JSON file
with open("wallet_list.json", "w") as f:
    json.dump(wallets, f)

# print a message indicating that the wallet list has been written to the JSON file
print("Wallet list written to wallet_list.json")

