import subprocess
import time
from tqdm import tqdm


input_file = "wallets.txt"
output_file = "results.txt"

with open(input_file, "r") as f:
    lines = f.readlines()
amount_wallet_list = [(line.strip().split()) for line in lines]

start_time = time.time()
with open(output_file, "w") as f, tqdm(total=len(amount_wallet_list)) as pbar:
    for index, (amount, wallet_id) in enumerate(amount_wallet_list, start=1):
        cmd = f"solana transfer {wallet_id} {amount}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            success_msg = f"\033[32m\u2714 Transferred {amount} SOL to {wallet_id}\033[0m"
            pbar.write(success_msg)
            f.write(success_msg + "\n")
        else:
            error_msg = f"\033[31mError transferring SOL to {wallet_id}: {result.stderr}\033[0m"
            pbar.write(error_msg)
            f.write(error_msg + "\n")
        pbar.update(1)
        elapsed_time = time.time() - start_time
        avg_time_per_wallet = elapsed_time / index
        wallets_remaining = len(amount_wallet_list) - index
        time_remaining = avg_time_per_wallet * wallets_remaining
        pbar.set_description(f"Progress: {index}/{len(amount_wallet_list)} | Avg. Time per Wallet: {avg_time_per_wallet:.2f}s | Time Remaining: {time_remaining:.2f}s")

