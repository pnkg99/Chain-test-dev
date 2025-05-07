#!/usr/bin/python3
import subprocess
import os
inery_cline_path = "packages/inery/bin/cline"

# out = subprocess.Popen([inery_cline_path, "wallet", "list"], stdout=subprocess.PIPE).communicate()[0].decode()

# os.remove('/home/user/inery-wallet/default.wallet')

# out, error = subprocess.Popen([inery_cline_path, "wallet", "create", "--to-console"],
#                                  stdout=subprocess.PIPE,
#                                  stderr=subprocess.PIPE,
#                                  text=True).communicate()

# out2 = subprocess.run(["ls", "-lash"],
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE, 
#                     text=True)

import logging

LOG_FILE = "chain.log"
# logging.basicConfig(
#     # filename=LOG_FILE,
#     # filemode="w",  
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     level=logging.INFO,  # Change to DEBUG for more detailed logs
#     handlers=[
#         logging.StreamHandler(),  # Keep console output too
#         logging.FileHandler(LOG_FILE, mode="w") # or "a" to append
#     ]
# )

# logger = logging.getLogger(__name__)


# print("\u2705")      # ✅
# print("\u274C")      # ❌
# print("lala")


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example logs
logger.info("This is an info message")
logger.error("This is an error message")

logger.info("\u2705")
logger.critical("\u274C")