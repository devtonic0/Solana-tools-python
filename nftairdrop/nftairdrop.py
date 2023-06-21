import json
import subprocess
from tqdm import tqdm
import time
import random
import os

def run_command(mint_id, wallet_id):
    command = f"spl-token transfer {mint_id} 1 {wallet_id} --fund-recipient"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error executing command: {error}")

def read_files(hashlist_file, walletlist_file):
    with open(hashlist_file, 'r') as f:
        mint_ids = json.load(f)

    with open(walletlist_file, 'r') as f:
        wallet_ids = [line.strip().split() for line in f.readlines()]

    return mint_ids, wallet_ids

def transfer_tokens(hashlist_file, walletlist_file):
    mint_ids, wallet_ids = read_files(hashlist_file, walletlist_file)

    mint_id_index = 0
    total_tokens = sum(int(w[0]) for w in wallet_ids)

    with tqdm(total=total_tokens, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for wallet in wallet_ids:
            count, wallet_id = wallet

            for _ in range(int(count)):
                run_command(mint_ids[mint_id_index], wallet_id)
                mint_id_index += 1

                # update progress bar with some fun animations
                pbar.set_postfix_str(f"Sending to {wallet_id} with mint ID {mint_ids[mint_id_index]}")
                pbar.update()
                time.sleep(random.uniform(0.1, 0.3))

if __name__ == "__main__":
    hashlist_file = 'hashlist.json'
    walletlist_file = 'walletlist.txt'

    # check if the necessary files exist
    if not os.path.isfile(hashlist_file) or not os.path.isfile(walletlist_file):
        print(f"One or both necessary files ({hashlist_file}, {walletlist_file}) do not exist.")
    else:
        transfer_tokens(hashlist_file, walletlist_file)

