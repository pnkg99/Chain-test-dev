#!/usr/bin/python3.9
import subprocess, requests
import time
import json
import os
from os.path import join as join_path
import sys
import shutil
import argparse
from logger import Logger

def get_ubuntu_version():
    try:
        result = subprocess.run(['lsb_release', '-a'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                                )
        if result.returncode == 0:
            output = result.stdout
            lines = output.split('\n')
            for line in lines:
                if 'Release:' in line:
                    version = line.split(':')[1].strip()
                    major_version = int(version.split('.')[0])
                    if 18 <= major_version <= 24:
                        Logger.get_logger().info(f'Ubuntu version : {version}')
                        return
                    else:
                        error_msg('Ubuntu version must be 20.04')
        else:
            error_msg('Failed to obtain Ubuntu version. Make sure lsb_release is installed.')

    except Exception as e:
        error_msg(f'Failed to obtain Ubuntu version. {str(e)}') 

def read_file(file_path, json_load=False):
    try:
        with open(file_path, 'r') as file:
            return json.load(file) if json_load else file.read().strip()
    except Exception as e:
        error_msg(f'Failed to read file. {str(e)}') # NOTE: exception needs to be cast to string

def write_file(file_path, data, json_dump=False, mode='w+'):
    try:
        with open(file_path, mode) as file:
            json.dump(data, file, indent=6) if json_dump else file.write(data)
    except Exception as e:
        error_msg(f'Failed to write to file. {str(e)}')

def error_msg(message):
    if 'transaction executed locally' in message:
        return
    # NOTE: will not raise an exception, just inform the user to check the log file
    Logger.get_logger().error(message)
    print(f'❌ Critical error: See "{Logger.get_name()}" for details') # \u274C - backup unicode for cross mark
    exit()

class TestChain:

    def __init__(self):

        self.dir_path = os.getcwd()
        self.home_path = os.getenv('HOME')
        self.bashrc_path = join_path(self.home_path, '.bashrc')
        self.wallet_path = join_path(self.home_path, 'inery-wallet')
        self.default_wallet_path = join_path(self.wallet_path, 'default.wallet')

        self.config_path = join_path(self.dir_path, 'config')
        self.data_path = join_path(self.dir_path, 'data')
        self.packages_path = join_path(self.dir_path, 'packages')
        self.contract_path = join_path(self.config_path, 'contracts')

        self.general_path = join_path(self.config_path, 'general.json')

        self.boot_path = join_path(self.contract_path, 'inery.boot')
        self.system_path = join_path(self.contract_path, 'inery.system')
        self.token_path = join_path(self.contract_path, 'inery.token')

        self.inery_bin_path = join_path(self.packages_path, 'inery', 'bin')
        # self.inery_cdt_path = join_path(self.packages_path, 'inery.cdt', 'bin') # NOTE: not used

        self.inery_nodine_path = join_path(self.inery_bin_path, 'nodine')
        self.inery_cline_path = join_path(self.inery_bin_path, 'cline')

        self.accounts = read_file(join_path(self.config_path, 'accounts.json'), True)
        self.chains = read_file(join_path(self.config_path, 'servers.json'), True)
        self.general = read_file(self.general_path, True)

        self.genesis_account = self.accounts['GENESIS_ACCOUNT']
        self.system_accounts = self.accounts['SYSTEM_ACCOUNTS']

        self.master_chain = self.chains['MASTER_CHAIN']
        self.side_chains = self.chains['SIDE_CHAINS']

        self.genesis_pubkey = self.genesis_account['PUBLIC_KEY']
        self.genesis_json = self.general['GENESIS_JSON']
        self.genesis_json['initial_key'] = self.genesis_pubkey

        self.wallet_psw = self.general['WALLET_PASSWORD']
        self.features = self.general['PROTOCOL_FEATURES']
    
    def run_command(self, command_list, url=None, success_message='', suppress_error_for=None):
        # `suppress_error_for` is used if errors should be handled externally (like for wallet)
        suppress_error_for = suppress_error_for or []
        command_list.insert(0, self.inery_cline_path)
        if url:
            command_list.insert(1, '-u')
            command_list.insert(2, url)

        out, error = subprocess.Popen(command_list,
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      text=True
                                      ).communicate()
        
        supress = any(cmd in command_list for cmd in suppress_error_for) 
        if error and not out and not supress:
            error_msg(f'Failed to run command: \n\t{" ".join(command_list)} \nerror: \n---\n{error}\n---')
        if success_message:
            Logger.get_logger().info(f'✅ {success_message}')  # \u2705 - backup unicode for check mark
        return out, error

    def export_binaries(self):
        bashrc_content = read_file(self.bashrc_path)
        export_path = f'export PATH="$PATH:{self.inery_bin_path}"'
        if export_path not in bashrc_content:
            new_bashrc = (
                bashrc_content + f'\n\n# INERY blockchain CLI tools\n{export_path}'
            )
            write_file(self.bashrc_path, new_bashrc)


    ## Wallet Actions

    def check_default_wallet(self):
        # self.create_wallet()
        out, _ = self.run_command(['wallet', 'list'])
        if 'default' in out:
            self.unlock_wallet()
        else:
            self.create_wallet()

    def create_wallet(self):
        if os.path.exists(self.default_wallet_path):
            os.remove(self.default_wallet_path)
        temp_file = join_path(self.config_path, 'temp.txt')
        out, error = self.run_command(['wallet', 'create', '--file', temp_file])
        if out:
            wallet_password = read_file(temp_file)
            self.general['WALLET_PASSWORD'] = wallet_password
            write_file(self.general_path, self.general, True)
            os.remove(temp_file)
            self.wallet_psw = wallet_password
        else:
            error_msg(f'Failed to create wallet. {error}')
        self.import_keys()

    def unlock_wallet(self):
        _, error = self.run_command(['wallet', 'unlock', '--password', 
                                     self.wallet_psw], 
                                     suppress_error_for=['wallet']
                                     )
        if error: 
            if 'Already unlocked' in error:
                Logger.get_logger().info('Default wallet is already unlocked.')
            elif 'Invalid wallet password' in error: 
                error_msg('Incorrect wallet password')
            else:
                error_msg(error)
        else:
            Logger.get_logger().info('Unlocked default wallet')

    def import_key(self, private_key):
        self.run_command(['wallet', 'import', '--private-key', private_key])

    def import_keys(self):
        self.import_key(self.genesis_account['PRIVATE_KEY'])
        for account in self.system_accounts:
            self.import_key(account['PRIVATE_KEY'])

    ## Blockchain Account

    def create_account(self, account, pubkey, creator='creator'):
        self.run_command(['system', 'opendb', creator, account, pubkey, pubkey])

    ## Main Processes

    def run_chain(self):
        get_ubuntu_version()
        self.export_binaries()
        self.check_default_wallet()
        master_chain_dir = join_path(self.data_path, 'master_chain')
        self.run_cluster(master_chain_dir, self.master_chain)
        chain_num = 1
        for chain in self.side_chains:
            side_chain_dir = join_path(self.data_path, 'side_chain_' + str(chain_num))
            self.run_cluster(side_chain_dir, chain)
            chain_num += 1

    def run_cluster(self, path, node):
        # check if the chain is already started
        nodine_pids = subprocess.run(['pidof', 'nodine'], 
                                     stdout=subprocess.PIPE, 
                                     text=True
                                     ).stdout.strip()
        
        try:
            # Look for a nodine process with your data-dir in its args
            subprocess.check_output(
                ['pgrep', '-f', f'nodine.*--data-dir\s*{path}'],
                stderr=subprocess.DEVNULL,
                text=True
            )            
            Logger.get_logger().info(f'Blockchain {path} already started')
        except subprocess.CalledProcessError:
            # Check for files that indicate a chain was initialized
            if os.path.exists(join_path(path, 'blockchain', 'data', 'blocks')) and os.path.exists(join_path(path, 'blockchain', 'data', 'state')):
                os.system(join_path(path, 'start.sh'))
                Logger.get_logger().info(f'Blockchain {path} started')
                return
            
            # Init chain
            os.makedirs(path, exist_ok=True)
            write_file(join_path(path, 'genesis.json'), self.genesis_json, True)
            for script in ['genesis_start.sh', 'start.sh', 'hard_replay.sh']: #, 'stop.sh']:
                script_path = join_path(path, script)
                write_file(script_path, self.generate_script(path, node, script))
                os.chmod(script_path, 0o777)

            os.system(join_path(path, 'genesis_start.sh'))
            Logger.get_logger().info(f'✅ Blockchain {path} started')  # \u2705 - backup unicode for check mark
        
            time.sleep(1)
            self.initialize_chain(url=node['HTTP'])
            

    def initialize_chain(self, url):
        url = 'http://' + url
        feature_url = f'{url}/v1/master/schedule_protocol_feature_activations'
        payload = {
            'protocol_features_to_activate': [
                '0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd'
            ]
        }
        response = requests.post(
            feature_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
        )
        if response.status_code != 201:
            error_msg('Failed to activate protocol feature')

        time.sleep(2) # Very Important
        
        # 1. Setovanje boot kontrakta
        self.run_command(['set', 'contract', 'inery', f'{self.boot_path}'], url, success_message='Inery Boot Contract Set')

        # 2. Kreiranje system accounts
        for account in self.system_accounts:
            self.run_command(['create', 'opendb', 'inery', f'{account["NAME"]}', f'{account["PUBLIC_KEY"]}'], url, success_message=f'Created system account: {account["NAME"]}')

        # 3. Aktivacija protokol feature-a
        for feature in self.features:
            self.run_command(['push', 'action', 'inery', 'activate', f'["{feature}"]', '-p', 'inery'], url, success_message=f'Feature activated: {feature}') 
        time.sleep(0.5)
        # 4. Setovanje system kontrakta
        self.run_command(['set', 'contract', 'inery', f'{self.system_path}'], url, success_message='Inery System Contract Set')
        # 5. Setovanje inery.token kontrakta
        self.run_command(['set', 'contract', 'inery.token', f'{self.token_path}'], url, success_message='Inery Token Contract Set')
        # 6. Kreiranje INR tokena
        self.run_command(['push', 'action', 'inery.token', 'create', '["inery", "800000000.000000 INR"]', '-p', 'inery@active'], url, success_message='INR Token Created')
        # 7. Issuance INR tokena
        self.run_command(['push', 'action', 'inery.token', 'issue', '["inery", "432000000.000000 INR", "Issuing tokens for inery account"]', '-p', 'inery@active'], url, success_message='INR Tokens Issued')
        # 8. Kreiranje BYTE tokena
        self.run_command(['push', 'action', 'inery.token', 'create', '["inery", "128000000000 BYTE"]', '-p', 'inery@active'], url, success_message='BYTE Token Created')
        # 9. Issuance BYTE tokena
        self.run_command(['push', 'action', 'inery.token', 'issue', '["inery", "128000000000 BYTE", "Issuing BYTE for inery account"]', '-p', 'inery@active'], url, success_message='BYTE Tokens Issued')
        # 10. Transfer INR ka inery.mem
        self.run_command(['transfer', 'inery', 'inery.mem', '100000000 INR'], url, success_message='Transferred INR to inery.mem')
        # 11. Transfer BYTE ka creator
        self.run_command(['transfer', 'inery', 'creator', '10000000000 BYTE'], url, success_message='Transferred BYTE to creator')
        # 12. Transfer INR ka creator
        self.run_command(['transfer', 'inery', 'creator', '100000000 INR'], url, success_message='Transferred INR to creator')
        # 13. Inicijalizacija
        self.run_command(['push', 'action', 'inery', 'init', '["0", "4,INR"]', '-p', 'inery@active'], url, success_message='Inery Init Done')
        # 14. Memory sell
        self.run_command(['memory', 'sell', 'inery', '38000000000 BYTE'], url, success_message='Memory Sold')
        Logger.get_logger().info('Blockchain initilized')
        time.sleep(1)

    def stop_chain(self):
        nodine_pids = subprocess.run(['pidof', 'nodine'], 
                                     stdout=subprocess.PIPE, 
                                     text=True
                                     ).stdout
        for pid in nodine_pids.split():
            os.system(f'kill {pid}') # NOTE: SIGTERM (default) is cleaner than SIGKILL
            Logger.get_logger().info(f'Terminated process pid={pid}')
            time.sleep(0.2)

    def remove_chain(self):
        for dir in os.listdir(self.data_path):
            dir_path = join_path(self.data_path, dir)
            shutil.rmtree(dir_path)
            Logger.get_logger().info(f'Blockchain {dir_path} removed')

    def generate_script(self, path, node, type):
        datadir = f'{path}/blockchain'
        base_command = [
            f'{self.inery_nodine_path}',
            '\t--plugin inery::master_plugin',
            '\t--plugin inery::master_api_plugin',
            '\t--plugin inery::chain_plugin',
            '\t--plugin inery::chain_api_plugin',
            '\t--plugin inery::http_plugin',
            '\t--plugin inery::net_plugin',
            '\t--plugin inery::net_api_plugin',
            # '\t--plugin inery::trace_api_plugin',
            # '\t--plugin inery::state_history_plugin',
            # '\t--trace-history',
            # '\t--trace-no-abis',
            # '\t--disable-replay-opts',
            # '\t--chain-state-history',
            # '\t--state-history-endpoint 0.0.0.0:8080',
            # '\t--state-history-dir $DATADIR"/data/state-history"',
            # '\t--max-retained-history-files 10',
            # '\t--state-history-stride 1000000',
            '\t--context-free-data-compression zlib',
            '\t--data-dir $DATADIR"/data"',
            '\t--blocks-dir $DATADIR"/data/blocks"',
            '\t--config-dir $DATADIR"/config"',
            '\t--access-control-allow-origin=*',
            '\t--contracts-console',
            '\t--http-validate-host=false',
            '\t--verbose-http-errors',
            '\t--enable-stale-production',
            '\t--connection-cleanup-period 10',
            f'\t--master-name {self.genesis_account["NAME"]}',
            f'\t--http-server-address {node["HTTP"]}',
            f'\t--p2p-listen-endpoint {node["PEER"]}',
            f'\t--signature-provider {self.genesis_account["PUBLIC_KEY"]}=KEY:{self.genesis_account["PRIVATE_KEY"]}',
        ]

        if type == 'genesis_start.sh':
            base_command.insert(1, f'\t--genesis-json "{path}/genesis.json"')
        elif type == 'hard_replay.sh':
            base_command.append('\t--hard-replay-blockchain')
        elif type == 'stop.sh':
            return (
                f'#!/bin/bash\nDATADIR="{path}/blockchain"\n\nif [ -f "$DATADIR/ined.pid" ]; then\n'
                f'\tpid=$(cat "$DATADIR/ined.pid")\n\tkill "$pid"\n\trm -r "$DATADIR/ined.pid"\n'
                f'\twhile [ -d "/proc/$pid/fd" ]; do sleep 1; done\n'
                f'\techo "Node Stopped."\nfi'

            )

        command_string = ' \\\n'.join(base_command)

        script = (
            f'#!/bin/bash\n'
            f'DATADIR="{datadir}"\n\n'
            f'if [ ! -d "$DATADIR" ]; then\n\tmkdir -p "$DATADIR";\nfi\n\n'
            f'{command_string} \\\n'
            f'\t>> "$DATADIR/nodine.log" 2>&1 & \\\n'
            f'\techo $! > "$DATADIR/ined.pid"'
        )

        return script
    


if __name__ == '__main__':
    test_chain = TestChain()

    parser = argparse.ArgumentParser(
        description='Manage the test chain.\nOnly one of the positional arguments should be used.',
        formatter_class=argparse.RawTextHelpFormatter
        )    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'terminate', 'restart', 'unlock'],
        metavar='action',
        help=(
            'Only one of the following commands should be used:\n\n'
            'start        Run the chain\n'
            'stop         Stop the chain\n'
            'terminate    Stop the chain and remove all data\n'
            'restart      Stop and run the chain\n'
            'unlock       Unlock wallet'
        )
    )
    parser.add_argument('-v', '--verbose', action='store_true', default=False, 
                        help=f'print logs to console as well as to .log file.')    
    args = parser.parse_args()

    logger = Logger.get_logger(verbose=args.verbose)

    if args.command == 'start':
        logger.info('starting the chain...')
        test_chain.run_chain()

    elif args.command == 'stop':
        logger.info('stopping the chain...')
        test_chain.stop_chain()

    elif args.command == 'terminate':
        logger.info('terminating the chain...')
        test_chain.stop_chain()
        test_chain.remove_chain()

    elif args.command == 'restart':
        logger.info('restarting the chain...')
        test_chain.stop_chain()
        test_chain.run_chain()

    elif args.command == 'unlock':
        logger.info('unlocking the wallet...')
        # test_chain.create_wallet()
        test_chain.unlock_wallet()


    
