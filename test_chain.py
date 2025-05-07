#!/usr/bin/python3
import subprocess, requests
import time
import json
import os
from os.path import join as join_path
import sys
import shutil

def get_ubuntu_version():
    try:
        result = subprocess.run(['lsb_release', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
            lines = output.split('\n')
            for line in lines:
                if 'Release:' in line:
                    version = line.split(':')[1].strip()
                    major_version = int(version.split('.')[0])
                    if  18 <= major_version <= 24:
                        print(f"Ubuntu version : {version}")
                        return 
                    else:
                        print("Ubuntu version must be 20.04")
                        exit()
        else:
            print("Failed to obtain Ubuntu version. Make sure lsb_release is installed.")
            exit() 

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit()

def read_file(file_path, json_load=False):
    try :
        with open(file_path, "r") as file:
            return json.loads(file.read()) if json_load else file.read().strip()
    except Exception as e :
        error_msg(e)

def write_file(file_path, data, json_dump=False, mode="w+"):
    try:
        with open(file_path, mode) as file:
            json.dump(data, file, indent=6) if json_dump else file.write(data)
    except Exception as e :
        error_msg(e)

def error_msg(message):
    if "transaction executed locally" in message :
        return
    raise Exception(f"❌ Critical error: {message}")  # Ako želiš da prekine dalje izvršavanje
    


class TestChain:
    def __init__(self) :
        self.dir_path = os.getcwd()
        self.home_path = os.getenv("HOME")
        self.bashrc_path = join_path(self.home_path, '.bashrc')
        self.wallet_path = join_path(self.home_path, "inery-wallet")
        self.default_wallet_path = join_path(self.wallet_path, "default.wallet")
        
        self.config_path = join_path(self.dir_path, "config")
        self.data_path = join_path(self.dir_path, "data")
        self.packages_path = join_path(self.dir_path, "packages")
        self.contract_path = join_path(self.config_path, "contracts")
        
        self.general_path = join_path(self.config_path, "general.json")
        
        self.boot_path = join_path(self.contract_path, "inery.boot")
        self.system_path = join_path(self.contract_path, "inery.system")
        self.token_path = join_path(self.contract_path, "inery.token")
        
        self.inery_bin_path = join_path(self.packages_path, "inery", "bin")
        self.inery_cdt_path = join_path(self.packages_path, "inery.cdt", "bin")
        
        self.inery_nodine_path = join_path(self.inery_bin_path, "nodine")
        self.inery_cline_path = join_path(self.inery_bin_path, "cline")
        
        self.accounts = read_file(join_path(self.config_path, "accounts.json"), True)
        self.chains = read_file(join_path(self.config_path, "chains.json"), True)
        self.general = read_file(self.general_path, True)
        
        self.genesis_account = self.accounts["GENESIS_ACCOUNT"]
        self.system_accounts = self.accounts["SYSTEM_ACCOUNTS"]
        
        self.master_chain = self.chains["MASTER_CHAIN"]
        self.side_chains = self.chains["SIDE_CHAINS"]
                
        self.genesis_pubkey = self.genesis_account["PUBLIC_KEY"]
        self.genesis_json = self.general["GENESIS_JSON"]
        self.genesis_json["initial_key"] = self.genesis_pubkey
        
        self.wallet_psw = self.general["WALLET_PASSWORD"]
        self.features = self.general["PROTOCOL_FEATURES"]
        
    def export_binaries(self):
        bashrc_content = read_file(self.bashrc_path)
        export_path = f'export PATH="$PATH:{self.inery_bin_path}"'
        if export_path not in bashrc_content:
            new_bashrc=bashrc_content+f'\n{export_path}'
            write_file(self.bashrc_path,new_bashrc)

    def run_command(self, url, command_list, success_message=""):
        command_list.insert(0, self.inery_cline_path)
        command_list.insert(1, "-u")
        command_list.insert(2, url)
        out, error = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()
        if error and not out:
            error_msg(error)
        if success_message:
            print("✅ ", success_message)
        return out, error

    # Wallet Actions
    
    def check_default_wallet(self) :
        out = subprocess.Popen([self.inery_cline_path, "wallet", "list"], stdout=subprocess.PIPE).communicate()[0].decode()
        if "default" in out :                  
            self.unlock_wallet()
        else :
            self.create_wallet()
            
    def create_wallet(self):
        if os.path.exists(self.default_wallet_path):
            os.remove(self.default_wallet_path)
        temp_file = join_path(self.config_path, "temp.txt")
        out, error = subprocess.Popen([self.inery_cline_path, "wallet", "create", "--file", temp_file],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True).communicate()
        if out :
            wallet_password = read_file(temp_file)
            self.general["WALLET_PASSWORD"] = wallet_password
            write_file(self.general_path, self.general, True)
            os.remove(temp_file)
            self.wallet_psw = wallet_password
        else : 
            error_msg(error)
        self.import_keys()

    def unlock_wallet(self):
        error = subprocess.Popen(
            [self.inery_cline_path, "wallet", "unlock", "--password", self.wallet_psw ],
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE,  
            text=True               
        ).communicate()[1]
        if error :
            if "Already unlocked" in error:
                print("Default wallet is already unlocked.")
            elif "Invalid wallet password" in error :
                print("Incorrect wallet password")
            else :
                print(error)
        else :
            print("Unlocked default wallet")
    
    def import_key(self, private_key):
        subprocess.run([self.inery_cline_path, "wallet", "import", "--private-key", private_key])
        
    def import_keys(self) :
        self.import_key(self.genesis_account["PRIVATE_KEY"])
        for account in self.system_accounts :
            self.import_key(account["PRIVATE_KEY"])
            
    # Blockchain Account 
    
    def create_account(self, account, pubkey, creator="creator"):
        subprocess.Popen([self.inery_cline_path, "system", "opendb", creator, account, pubkey, pubkey]).communicate()[0]

    ## Main Processes
    
    def run_chain(self) :
        self.check_default_wallet()
        self.stop_chain()
        self.run_multichain()

    def run_multichain(self) :
        
        master_chain_dir = join_path(self.data_path, "master_chain")
        self.run_cluster(master_chain_dir, self.master_chain)
        chain_num=1
        for chain in self.side_chains :
            side_chain_dir = join_path(self.data_path, "side_chain_"+str(chain_num))
            self.run_cluster(side_chain_dir, chain)
            chain_num+=1
        
    def run_cluster(self,path, node) :
        os.makedirs(path, exist_ok=True)
        write_file(join_path(path, "genesis.json"), self.genesis_json, True)
        for script in ["genesis_start.sh", "hard_replay.sh", "stop.sh"] :
            script_path = join_path(path, script)     
            write_file(script_path, self.generate_script(path,node, script))
            os.chmod(script_path, 0o777)

        os.system(join_path(path, "genesis_start.sh") )
        print(f"✅ Blockchain {path} started")
        time.sleep(1)
        self.initialize_chain(url = node["HTTP"])
        
    def initialize_chain(self, url):
        url = "http://"+url
        feature_url = f"{url}/v1/master/schedule_protocol_feature_activations"
        payload = {
            "protocol_features_to_activate": [
                "0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd"
            ]
        }
        response = requests.post(feature_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code != 201 :
            error_msg("Failed to activate protocol feature")
        
        time.sleep(1) # Very Important
        
        # 1. Setovanje boot kontrakta
        self.run_command(url, ["set", "contract", "inery", f"{self.boot_path}"], success_message="Inery Boot Contract Set")

        # 2. Kreiranje system accounts
        for account in self.system_accounts:
            self.run_command(url,[ "create", "opendb", "inery", f'{account["NAME"]}', f'{account["PUBLIC_KEY"]}'],success_message=f"Created system account: {account['NAME']}")

        # 3. Aktivacija protokol feature-a
        for feature in self.features:
            self.run_command(url,["push", "action", "inery", "activate", f"[\"{feature}\"]", "-p", "inery"], success_message=f"Feature activated: {feature}") 
        time.sleep(0.5)
        # 4. Setovanje system kontrakta
        self.run_command(url,[ "set", "contract", "inery", f"{self.system_path}"],success_message="Inery System Contract Set")
        # 5. Setovanje inery.token kontrakta
        self.run_command(url, ["set", "contract", "inery.token", f"{self.token_path}"], success_message="Inery Token Contract Set")
        # 6. Kreiranje INR tokena
        self.run_command(url, ["push", "action", "inery.token", "create", "[\"inery\", \"800000000.000000 INR\"]", "-p", "inery@active"], success_message="INR Token Created")
        # 7. Issuance INR tokena
        self.run_command(url, ["push", "action", "inery.token", "issue", "[\"inery\", \"432000000.000000 INR\", \"Issuing tokens for inery account\"]", "-p", "inery@active"], success_message="INR Tokens Issued")
        # 8. Kreiranje BYTE tokena
        self.run_command(url, ["push", "action", "inery.token", "create", "[\"inery\", \"128000000000 BYTE\"]", "-p", "inery@active"], success_message="BYTE Token Created")
        # 9. Issuance BYTE tokena
        self.run_command(url, ["push", "action", "inery.token", "issue", "[\"inery\", \"128000000000 BYTE\", \"Issuing BYTE for inery account\"]", "-p", "inery@active"], success_message="BYTE Tokens Issued")
        # 10. Transfer INR ka inery.mem
        self.run_command(url, ["transfer", "inery", "inery.mem", "100000000 INR"], success_message="Transferred INR to inery.mem")
        # 11. Transfer BYTE ka creator
        self.run_command(url, ["transfer", "inery", "creator", "10000000000 BYTE"], success_message="Transferred BYTE to creator")
        # 12. Transfer INR ka creator
        self.run_command(url, ["transfer", "inery", "creator", "100000000 INR"], success_message="Transferred INR to creator")
        # 13. Inicijalizacija
        self.run_command(url, ["push", "action", "inery", "init", "[\"0\", \"4,INR\"]", "-p", "inery@active"], success_message="Inery Init Done")
        # 14. Memory sell
        self.run_command(url, ["memory", "sell", "inery", "38000000000 BYTE"], success_message="Memory Sold")
        print("Blockchain initilized")
        time.sleep(1)
            
    def stop_chain(self):
        nodine_pids = subprocess.Popen(["pidof", "nodine"], stdout=subprocess.PIPE).communicate()[0].decode()
        for pid in nodine_pids.split():
            os.system(f"kill -9 {pid}")
            print(f"Killed process pid={pid}")
            time.sleep(0.2)
        for dir in os.listdir(self.data_path):
            dir_path = join_path(self.data_path, dir)
            shutil.rmtree(dir_path)
            
    def generate_script(self, path, node, type):
        datadir = f'{path}/blockchain'
        base_command = [
            f'{self.inery_nodine_path}',
            '--plugin inery::master_plugin',
            '--plugin inery::master_api_plugin',
            '--plugin inery::chain_plugin',
            '--plugin inery::chain_api_plugin',
            '--plugin inery::http_plugin',
            '--plugin inery::net_plugin',
            '--plugin inery::net_api_plugin',
            # '--plugin inery::trace_api_plugin',
            # '--plugin inery::state_history_plugin',
            # '--trace-history',
            # '--trace-no-abis',
            # '--disable-replay-opts',
            # '--chain-state-history',
            # '--state-history-endpoint 0.0.0.0:8080',
            # '--state-history-dir $DATADIR"/data/state-history"',
            # '--max-retained-history-files 10',
            # '--state-history-stride 1000000',
            '--context-free-data-compression zlib',
            '--data-dir $DATADIR"/data"',
            '--blocks-dir $DATADIR"/data/blocks"',
            '--config-dir $DATADIR"/config"',
            '--access-control-allow-origin=*',
            '--contracts-console',
            '--http-validate-host=false',
            '--verbose-http-errors',
            '--enable-stale-production',
            '--connection-cleanup-period 10',
            f'--master-name {self.genesis_account["NAME"]}',
            f'--http-server-address {node["HTTP"]}',
            f'--p2p-listen-endpoint {node["PEER"]}',
            f'--signature-provider {self.genesis_account["PUBLIC_KEY"]}=KEY:{self.genesis_account["PRIVATE_KEY"]}'
        ]

        if type == "genesis_start.sh":
            base_command.insert(1, f'--genesis-json "{path}/genesis.json"')
        elif type == "hard_replay.sh":
            base_command.append('--hard-replay-blockchain')           
        elif type == "stop.sh":
            return (
                f'#!/bin/bash\nDATADIR="{path}/blockchain"\n\nif [ -f $DATADIR"/ined.pid" ]; then\n'
                f'pid=`cat $DATADIR"/ined.pid"`\nkill $pid\nrm -r $DATADIR"/ined.pid"\n'
                f'while [ -d "/proc/$pid/fd" ]; do sleep 1; done\n'
                f'echo "Node Stopped."\nfi'
            )

        command_string = " \\\n".join(base_command)

        script = (
            f'#!/bin/bash\n'
            f'DATADIR="{datadir}"\n\n'
            f'if [ ! -d $DATADIR ]; then\n  mkdir -p $DATADIR;\nfi\n\n'
            f'{command_string} \\\n'
            f'>> $DATADIR"/nodine.log" 2>&1 & \\\n'
            f'echo $! > $DATADIR"/ined.pid"'
        )

        return script



if __name__== '__main__':
    test_chain = TestChain()
    if len(sys.argv) < 2:
        print("invalid number of arguments try --help")
        exit()

    elif sys.argv[1] == "start":
        get_ubuntu_version()
        test_chain.export_binaries()
        test_chain.run_chain()
    
    elif sys.argv[1] == "stop":
        test_chain.stop_chain()

    elif sys.argv[1] == "restart":
        test_chain.stop_chain()
        test_chain.run_chain()
        
    elif sys.argv[1] == "unlock":
        test_chain.unlock_wallet()

    else:
        print(sys.argv[1])
        print("wrong flags try:")
        print("\tstart      - to run chain ")
        print("\tstop       - to stop chain")

