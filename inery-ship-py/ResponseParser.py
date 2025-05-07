
import struct
from SerialBuffer import SerialBuffer
from AbiType import SignedBlock 
from datetime import datetime, timezone, timedelta


def get_block_timestamp(data):
    timestamp_int = struct.unpack('<I', data[0:4])[0]  # LE uint32
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    dt = epoch + timedelta(seconds=timestamp_int)
    data = data[4:]
    return dt.isoformat(), data

def get_account_name(data):
    inery_name = struct.unpack('<Q', data[0:8])[0]  # LE uint32
    charmap = '.12345abcdefghijklmnopqrstuvwxyz'
    name = ''
    tmp = inery_name
    data = data[8:]
    for i in range(13):
        if i == 0:
            c = charmap[tmp & 0x0F]
            tmp >>= 4
        else:
            c = charmap[tmp & 0x1F]
            tmp >>= 5
        name = c + name

    return name.rstrip('.'), data

class ResponseParser() :
    

    def parse_get_blocks_result_v0(self, data):
        result = {}

        # head
        result['head'], data = self.parse_block_position(data)

        # last_irreversible
        result['last_irreversible'], data = self.parse_block_position(data)

        # this_block (optional)
        result['this_block'], data = self.parse_optional(data, self.parse_block_position)

        # prev_block (optional)
        result['prev_block'], data = self.parse_optional(data, self.parse_block_position)

        # block (optional bytes) - SPECIAL CASE
        result['block'], data = self.parse_optional_block_bytes(data)

        # traces (optional bytes)
        result['traces'], data = self.parse_optional_bytes(data)
        print(f"Remaining bytes after traces: {len(data)}")

        # deltas (optional bytes)
        result['deltas'], data = self.parse_optional_bytes(data)
        # print(f"Remaining bytes after deltas: {len(data)}")
        # exit(1)
        # if result['block']:
        #     print(f"[DEBUG] Parsing SignedBlock from block data, size: {len(result['block'])//2} bytes")
        #     buffer = SerialBuffer(bytes.fromhex(result['block']))
        #     print(result['block'])
        #     exit(1)
        #     block = SignedBlock(buffer)
        #     print("✅ Parsed block:", block)
        #     result['parsed_block'] = block  # Možeš da dodaš i to u rezultat ako želiš
        # else:
        #     print("[DEBUG] No block data present, skipping block parsing.")
        
        return result
        
    @staticmethod
    def parse_get_status_result_v0(data):
        block_num, = struct.unpack('<I', data[0:4])
        block_id = data[4:36][::-1].hex()  # Reverse bytes for ID
        last_irrev_num, = struct.unpack('<I', data[36:40])
        last_irrev_id = data[40:72][::-1].hex()
        parsed = {
            "head": {"block_num": block_num, "block_id": block_id},
            "last_irreversible": {"block_num": last_irrev_num, "block_id": last_irrev_id}
        }
        print("✅ Parsed status:", parsed)
        return parsed

    @staticmethod
    def parse_block_position(data):
        if len(data) < 36:
            raise ValueError("Insufficient data for block_position")
        block_num = struct.unpack('<I', data[:4])[0]
        block_id = data[4:36].hex()  # BEZ reverzije, jer ABI nije dao reverse
        print(f"[block_position] Block num: {block_num}, Block ID: {block_id}")
        return {"block_num": block_num, "block_id": block_id}, data[36:]
    
    @staticmethod
    def parse_optional(data, parser):
        if not data:
            return None, data
        present = data[0]  # Da li je prisutno?
        print("PRESENT FLAG:", present)
        data = data[1:]  # Skini flag
        if present == 1:
            value, data = parser(data)  # Parsiraj samo ako je prisutno
            return value, data
        else:
            return None, data

    @staticmethod
    def parse_optional_bytes(data):
        if not data:
            return None, data
        present = data[0]
        data = data[1:]
        print(f"[Optional Bytes] Present flag: {present}, remaining bytes: {len(data)}")
        if present == 1:
            length, size = ResponseParser.parse_varuint32(data)
            start = size
            end = start + length
            if len(data) < end:
                raise ValueError("Insufficient data for optional bytes.")
            value = data[start:end]
            print(f"[Optional Bytes] Length: {length}, bytes read: {len(value)}")
            return value.hex(), data[end:]
        else:
            return None, data
        
    @staticmethod
    def parse_varuint32(data):
        result = 0
        shift = 0
        i = 0
        print(f"[parse_varuint32] Raw data: {data[:5].hex()}")  # prvih 5 bajtova radi provere
        for j in range(len(data)):
            b = data[j]
            result |= (b & 0x7F) << shift
            shift += 7
            i += 1
            if not (b & 0x80):
                break
        print(f"[parse_varuint32] Value: {result}, bytes read: {i}")
        return result, i

    @staticmethod
    def parse_optional_block_bytes(data):
        if not data:
            return None, data
        present = data[0]
        data = data[1:]
        print(f"[Optional Block Bytes] Present flag: {present}, remaining bytes: {len(data)}")
        if present == 1:
            block_header={}
            block_header["timestamp"], data = get_block_timestamp(data)
            block_header["master"], data = get_account_name(data)
            print(block_header)
            
            return data.hex(), b''  # assuming no more data
        else:
            return None, data