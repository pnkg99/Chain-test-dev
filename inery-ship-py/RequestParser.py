import struct

class RequestParser():
    @staticmethod
    def build_get_blocks_request_v0(start_block, end_block, max_messages=1):
        variant_index = RequestParser.pack_varuint32(1)  # varuint32
        start_block_num = struct.pack('<I', start_block)
        end_block_num = struct.pack('<I', end_block)
        max_in_flight = struct.pack('<I', max_messages)
        have_positions_count = RequestParser.pack_varuint32(0)  # empty list

        # Boolean flags
        irreversible_only = struct.pack('<?', False)
        fetch_block = struct.pack('<?', True)
        fetch_traces = struct.pack('<?', True)
        fetch_deltas = struct.pack('<?', False)

        payload = (variant_index + start_block_num + end_block_num + max_in_flight +
                   have_positions_count +
                   irreversible_only + fetch_block + fetch_traces + fetch_deltas)
        print("Byte Request: ", payload)
        print("HEX request:", payload.hex())
        return payload

    @staticmethod
    def build_get_blocks_ack_request_v0(num_messages=1):
        variant_index = struct.pack('<B', 2)  # get_blocks_ack_request_v0 = 2
        num_messages = struct.pack('<I', num_messages)
        return variant_index + num_messages    


    @staticmethod
    def pack_varuint32(value):
        result = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                result.append(0x80 | byte)
            else:
                result.append(byte)
                break
        return bytes(result)