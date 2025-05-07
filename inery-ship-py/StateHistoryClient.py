import websocket
from websocket import ABNF
from RequestParser import RequestParser
from ResponseParser import ResponseParser

class StateHistoryClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.reqpars = RequestParser()
        self.resppars = ResponseParser()

    def connect(self):
        self.ws = websocket.create_connection(self.url, timeout=500)
        initial_data = self.ws.recv()
        print("✅ ABI primljen, dužina:", len(initial_data))

    def close(self):
        if self.ws:
            self.ws.close()
            print("🔒 Connection closed.")

    def send_get_status_request(self):
        print("📤 Sending get_status_request_v0")
        self.ws.send(b'\x00')  # get_status_request_v0
        data = self.ws.recv()
        print("✅ Status response received:", len(data), "bytes")
        return self.resppars.parse_get_status_result_v0(data[1:])  # skip variant index (1 byte)

    def get_blocks(self, start_block, end_block, max_messages=1):
        num_blocks = end_block - start_block
        print(f"📤 Requesting blocks from {start_block} to {end_block}")
        request = self.reqpars.build_get_blocks_request_v0(start_block, end_block, max_messages)
        exit(1)
        self.ws.send(request, opcode=ABNF.OPCODE_BINARY)
        print("📤 Sent get_blocks_request_v0")

        for i in range(num_blocks):
            block_response = self.ws.recv()
            parsed = self.resppars.parse_get_blocks_result_v0(block_response[1:])
            print("AAAA ", parsed)
            # Here you can parse block_response[1:] further if needed
            if i < num_blocks - 1:
                ack = self.reqpars.build_get_blocks_ack_request_v0(num_messages=1)
                self.ws.send(ack)
                print("📤 Sent get_blocks_ack_request_v0")







        




