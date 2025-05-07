#!/usr/bin/python3
from StateHistoryClient import StateHistoryClient

client = StateHistoryClient("ws://127.0.0.1:8080")

try:
    client.connect()

    # 1. Get status
    # status = client.send_get_status_request()

    # head_block = status["head"]["block_num"]
    # start_block = max(1, head_block - 10)
    # end_block = head_block

    # 2. Get blocks
    client.get_blocks(start_block=10, end_block=11, max_messages=1)

finally:
    client.close()
