import os
import json
import time
import requests
import arweave
from pathlib import Path
import subprocess
from tqdm import tqdm

# Set your Arweave wallet file path
wallet_file = '/home/tyler/Documents/pythonprograms/metadata/arweavekeypair.json'

# Set the path to the folder containing JSON files
json_folder_path = '/home/tyler/Documents/pythonprograms/metadata/updated_metadata'

# Load the wallet
wallet = arweave.Wallet(wallet_file)

# Get the list of JSON files in the folder
json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]

# Create a progress bar with tqdm
with tqdm(total=len(json_files), desc="Processing JSON files") as pbar:
    # Iterate through JSON files in the folder
    for json_file in json_files:
        # Extract the mint ID from the file name
        mint_id = os.path.splitext(json_file)[0]

        # Load the JSON data from the file
        with open(Path(json_folder_path) / json_file) as f:
            json_data = json.load(f)

        # Encode the JSON data as bytes
        json_data_bytes = json.dumps(json_data).encode('utf-8')

        while True:
            try:
                # Create an Arweave transaction to upload the JSON file
                tx = arweave.Transaction(wallet, data=json_data_bytes)

                # Add the necessary tags for the transaction
                tx.add_tag('Content-Type', 'application/json')
                tx.add_tag('App-Name', 'NFT-Metadata')

                # Sign the transaction
                tx.sign()

                # Send the transaction to Arweave
                tx.send()

                break  # break out of the retry loop if transaction is successfully sent
            except:
                print(f"\033[91m✗ Failed to upload metadata for mint ID {mint_id}, retrying...\033[0m")
                time.sleep(3)

        # Wait for the transaction to be confirmed
        while True:
            try:
                tx_status = requests.get(f'https://arweave.net/tx/{tx.id}/status')
                if tx_status.status_code == 202:
                    break
            except:
                print(f"\033[91m✗ Failed to get transaction status for mint ID {mint_id}, retrying...\033[0m")
                time.sleep(3)

        # Wait for the reward to be returned
        for i in range(10):
            try:
                reward = tx.reward
                break  # break out of the retry loop if reward is successfully retrieved
            except:
                print(f"\033[91m✗ Failed to get reward for mint ID {mint_id}, retrying...\033[0m")
                time.sleep(3)

        if reward is None:
            print(f"\033[91m✗ Failed to get reward for mint ID {mint_id}, skipping...\033[0m")
            continue

        # Update the Arweave URI
        update_command = f'metaboss update uri -a "{mint_id}" --new-uri "https://arweave.net/{tx.id}"'
        try:
             subprocess.run(update_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
             print(f"\033[91m✗ Failed to update URI for mint ID {mint_id}: {e}\033[0m")
             continue  # skip to the next iteration of the loop

        # Update the progress bar
        pbar.update(1)

        # Print the success message in green with a checkmark
        print(f"\033[92m✓ Successfully updated metadata for mint ID {mint_id}\033[0m")

print("All JSON files processed.")

