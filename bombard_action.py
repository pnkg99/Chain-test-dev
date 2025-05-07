#!/usr/bin/python3.9
from chain import Chain
import time
import argparse
import multiprocessing
import subprocess

def transfer(chain, acc_from, acc_to):
    start = time.perf_counter()
    end = start + 10
    while time.perf_counter() < end:
        out, error = subprocess.Popen(
            ['cline', 'transfer', acc_from, acc_to, '10 INR', '-f'],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
            ).communicate()
        if error and not out:
            print(f'Failed to run command. \nerror: \n---\n{error}\n---')
if __name__ == '__main__': 
    test_chain = Chain.get_instance()

    # parser = argparse.ArgumentParser(description="Transfer 10 INR indefinetly for 10s.")
    
    # parser.add_argument("acc_from", type=str, help="The name of the account")
    # parser.add_argument("acc_to", type=str, help="The action (transfer)")
    # # parser.add_argument("-o", "--output", type=str, help="Output file name (path)")
    
    # # Parse the arguments
    # args = parser.parse_args()

    accounts = [
        ('inery', 'inery.names'),
        ('inery', 'inery.stake'),
        ('inery', 'inery.vpay'),
        ('inery', 'creator'),
        ('inery', 'orbiter'),
        ('inery', 'inery.ram'),
        ('inery', 'inery.token'),
        ('inery', 'inery.wrap'),
        ('inery', 'inery.mem'),
        ('inery', 'inery.msig')
    ]
    # num_cores = multiprocessing.cpu_count() # 12
    processes = []
    test_chain.unlock_wallet()
    # transfer(test_chain, 'inery', 'inery.names')

    for acc_from, acc_to in accounts:
        p = multiprocessing.Process(target=transfer, args=(test_chain, acc_from, acc_to))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All transfers completed!")