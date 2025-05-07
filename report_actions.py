#!/usr/bin/python3.9
import os
from os.path import join as join_path
from pprint import pprint
import json
import argparse

from chain import Chain
from logger import Logger


def error_msg(message):
    # NOTE: will not raise an exception
    if message:
        Logger.get_logger().error(message)
        exit()

def generate_report(target_account, target_action, report_file, fresh, progress=None):

    chain = Chain.get_instance()
    # NOTE: sorting while printing doesn't work as wanted - it sorts the numbers as strings :/
    report_data = {}
    if not fresh and os.path.exists(report_file):
        with open(report_file, 'r') as file:
            report_data = json.load(file)

    last_block = int(report_data['last_checked_block']) if 'last_checked_block' in report_data else 1

    out, error = chain.run_command(['get', 'info'])
    error_msg(error)

    no = json.loads(out)['last_irreversible_block_num']
    # no = 2000
    report_data['last_checked_block'] = no
    total = no

    while no >= last_block:
        if progress:
            progress(int((total - no) / total * 100)) # percent done
        action_list = []
        out, error = chain.run_command(['get', 'block', str(no)])
        error_msg(error)

        block = json.loads(out)
        for transaction in block['transactions']:
            for action in transaction['trx']['transaction']['actions']:
                if action['account'] == target_account and action['name'] == target_action:
                    action_list.append(action)
        if action_list:
            report_data[str(no)] = action_list
        no -= 1
    if progress:
        progress(100)
    return report_data
    # with open(report_file, 'w+') as file:
    #     json.dump(report_data, file, indent=6, sort_keys=True)
    # if os.path.exists(join_path(chain.data_path, 'master_chain', 'blockchain', 'data', 'blocks')):
    #     print('kaka')


if __name__ == '__main__':
    # test_chain = Chain.get_instance()

    parser = argparse.ArgumentParser(description="Generate a report based on account name and action.")
    
    parser.add_argument("account", type=str, help="The name of the account")
    parser.add_argument("action", type=str, help="The action (transfer)")
    parser.add_argument("-o", "--output", type=str, help="Output file name (path)")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Generate the report using the inputs
    generate_report(args.account, args.action, args.output)
