import struct


class SerialBuffer:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def _check(self, size):
        if self.pos + size > len(self.data):
            raise ValueError(f"Out of bounds read: position {self.pos}, size {size}, total {len(self.data)}")

    def get(self):
        self._check(1)
        byte = self.data[self.pos]
        self.pos += 1
        return byte

    def get_bytes(self, length):
        self._check(length)
        val = self.data[self.pos:self.pos + length]
        self.pos += length
        return val

    def get_uint8(self):
        return self.get()

    def get_uint16(self):
        self._check(2)
        val = struct.unpack('<H', self.data[self.pos:self.pos + 2])[0]
        self.pos += 2
        return val

    def get_uint32(self):
        self._check(4)
        val = struct.unpack('<I', self.data[self.pos:self.pos + 4])[0]
        self.pos += 4
        return val

    def get_uint64(self):
        self._check(8)
        val = struct.unpack('<Q', self.data[self.pos:self.pos + 8])[0]
        self.pos += 8
        return val

    def get_int32(self):
        self._check(4)
        val = struct.unpack('<i', self.data[self.pos:self.pos + 4])[0]
        self.pos += 4
        return val

    def get_varuint32(self):
        result = 0
        shift = 0
        i = 0
        for j in range(len(self.data) - self.pos):
            b = self.data[self.pos + j]
            result |= (b & 0x7F) << shift
            shift += 7
            i += 1
            if not (b & 0x80):
                break
        self.pos += i
        print(f"[DEBUG] get_varuint32: {result}, read bytes: {i}, pos: {self.pos}")
        return result

    def get_varint32(self):
        value = self.get_varuint32()
        return (value >> 1) ^ -(value & 1)

    def get_float32(self):
        self._check(4)
        val = struct.unpack('<f', self.data[self.pos:self.pos + 4])[0]
        self.pos += 4
        return val

    def get_float64(self):
        self._check(8)
        val = struct.unpack('<d', self.data[self.pos:self.pos + 8])[0]
        self.pos += 8
        return val

    def get_checksum256(self):
        return self.get_bytes(32).hex()

    def get_checksum160(self):
        return self.get_bytes(20).hex()

    def get_checksum512(self):
        return self.get_bytes(64).hex()

    def get_string(self):
        length = self.get_varuint32()
        return self.get_bytes(length).decode('utf-8')

    def get_symbol_code(self):
        raw = self.get_bytes(8)
        return raw.rstrip(b'\x00').decode('utf-8')

    def get_symbol(self):
        raw = self.get_bytes(8)
        precision = raw[0]
        name = raw[1:].rstrip(b'\x00').decode('utf-8')
        return {"precision": precision, "name": name}

    def get_name(self):
        raw = self.get_bytes(8)
        value = int.from_bytes(raw, byteorder='little')

        charmap = '.12345abcdefghijklmnopqrstuvwxyz'
        name = ''
        tmp = value

        for i in range(13):
            if i == 0:
                c = charmap[tmp & 0x0F]
                tmp >>= 4
            else:
                c = charmap[tmp & 0x1F]
                tmp >>= 5
            name = c + name

        return name.rstrip('.')

    def get_time_point(self):
        microseconds = self.get_uint64()
        return microseconds  # Optionally convert to datetime later

    def get_time_point_sec(self):
        seconds = self.get_uint32()
        return seconds  # Optionally convert to datetime later

    def get_block_timestamp_type(self):
        slot = self.get_uint32()
        return slot  # Optionally convert to datetime later

    def get_asset(self):
        amount = self.get_bytes(8)
        symbol = self.get_symbol()
        return {"amount": amount.hex(), "symbol": symbol}

    def get_bytes_array(self):
        if self.pos >= len(self.data):
            print("[ERROR] No bytes left for bytes_array.")
            return ""
        length = self.get_varuint32()
        if self.pos + length > len(self.data):
            print(f"[ERROR] Out of bounds when reading bytes_array: requested {length}, available {len(self.data) - self.pos}")
            return ""
        return self.get_bytes(length).hex()


    # Optional polje - koristi se za extensione ili polja koja mogu biti prisutna
    def get_optional(self, parser):
        present = self.get()
        if present == 1:
            return parser(self)
        return None

    def have_read_data(self):
        return self.pos < len(self.data)

    def restart_read(self):
        self.pos = 0


    def get_bytes_fixed(self, length):
        if self.pos + length > len(self.buffer):
            raise ValueError(f"Cannot read {length} bytes, not enough data.")
        data = self.buffer[self.pos:self.pos + length]
        self.pos += length
        return data

    def get_public_key(self):
        key_type = self.get_uint8()
        key_data = self.get_bytes_fixed(33)  # Standard 33 bytes for K1/R1
        return f"{key_type:02x}{key_data.hex()}"
