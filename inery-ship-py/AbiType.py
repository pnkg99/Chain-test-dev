from SerialBuffer import SerialBuffer

class ProducerSchedule:
    def __init__(self, buffer: SerialBuffer):
        print(f"[DEBUG] Start ProducerSchedule at {buffer.pos} / {len(buffer.data)}")
        self.version = buffer.get_uint32()
        print(f"[DEBUG] version: {self.version}, pos: {buffer.pos}")

        self.producers = self._parse_producers(buffer)
        print(f"[DEBUG] producers (count: {len(self.producers)}), pos: {buffer.pos}")


    @staticmethod
    def _parse_producers(buffer: SerialBuffer):
        count = buffer.get_varuint32()
        producers = []
        for _ in range(count):
            producers.append(ProducerKey(buffer))
        return producers

    def __repr__(self):
        return f"ProducerSchedule(version={self.version}, producers={self.producers})"

class BlockHeader:
    def __init__(self, buffer: SerialBuffer):
        print(f"[DEBUG] Start BlockHeader at {buffer.pos} / {len(buffer.data)}")

        self.timestamp = buffer.get_block_timestamp_type()
        print(f"[DEBUG] timestamp: {self.timestamp}, pos: {buffer.pos}")

        self.master = buffer.get_name()
        print(f"[DEBUG] master: {self.master}, pos: {buffer.pos}")

        self.confirmed = buffer.get_uint16()
        print(f"[DEBUG] confirmed: {self.confirmed}, pos: {buffer.pos}")

        self.previous = buffer.get_checksum256()
        print(f"[DEBUG] previous: {self.previous}, pos: {buffer.pos}")

        self.transaction_mroot = buffer.get_checksum256()
        print(f"[DEBUG] transaction_mroot: {self.transaction_mroot}, pos: {buffer.pos}")

        self.action_mroot = buffer.get_checksum256()
        print(f"[DEBUG] action_mroot: {self.action_mroot}, pos: {buffer.pos}")

        self.schedule_version = buffer.get_uint32()
        print(f"[DEBUG] schedule_version: {self.schedule_version}, pos: {buffer.pos}")

        self.new_producers = buffer.get_optional(ProducerSchedule)
        print(f"[DEBUG] new_producers: {self.new_producers}, pos: {buffer.pos}")

        self.header_extensions = self._parse_extensions(buffer)
        print(f"[DEBUG] header_extensions: {self.header_extensions}, pos: {buffer.pos}")


    @staticmethod

    def _parse_extensions(buffer: SerialBuffer):
        count = buffer.get_varuint32()
        print(f"[DEBUG] block_extensions count: {count}, pos: {buffer.pos}")
        extensions = []
        for i in range(count):
            print(f"[DEBUG] Parsing extension {i + 1}/{count}, pos: {buffer.pos}")
            ext_type = buffer.get_uint16()  # ✅ Ispravno: prvo type
            print(f"[DEBUG] ext_type: {ext_type}, pos: {buffer.pos}")
            ext_data = buffer.get_bytes_array()  # ✅ Onda bytes_array
            print(f"[DEBUG] ext_data len: {len(ext_data)}, pos: {buffer.pos}")
            extensions.append({'type': ext_type, 'data': ext_data})
        return extensions

    def __repr__(self):
        return f"BlockHeader(timestamp={self.timestamp}, master='{self.master}', confirmed={self.confirmed}, ...)"
    

class SignedBlock(BlockHeader):
    def __init__(self, buffer: SerialBuffer):
        print(f"[DEBUG] Start SignedBlock at {buffer.pos} / {len(buffer.data)}")
        super().__init__(buffer)
        
        self.master_signature = buffer.get_bytes_array()
        print(f"[DEBUG] master_signature: {self.master_signature}, pos: {buffer.pos}")
        
        self.transactions = self._parse_transactions(buffer)
        print(f"[DEBUG] transactions (count: {len(self.transactions)}), pos: {buffer.pos}")
        
        # ✅ Ovde rešavaš problem:
        if buffer.pos < len(buffer.data):
            print(f"[DEBUG] Before block_extensions, buffer.pos: {buffer.pos}, total: {len(buffer.data)}")
            self.block_extensions = self._parse_extensions(buffer)
        else:
            print("[DEBUG] No block_extensions (end of buffer)")
            self.block_extensions = []


    @staticmethod
    def _parse_transactions(buffer: SerialBuffer):
        count = buffer.get_varuint32()
        print(f"[DEBUG] transaction count raw: {count}, pos: {buffer.pos}")
        transactions = []
        for i in range(count):
            print(f"[DEBUG] Parsing transaction {i + 1}/{count}, pos: {buffer.pos}")
            transactions.append(TransactionReceipt(buffer))
        return transactions

    @staticmethod
    def _parse_extensions(buffer: SerialBuffer):
        if buffer.pos >= len(buffer.data):
            print("[DEBUG] No bytes left for extensions.")
            return []
        
        count = buffer.get_varuint32()
        print(f"[DEBUG] block_extensions count: {count}, pos: {buffer.pos}")
        
        if count > 1000:  # logična granica
            print(f"[ERROR] Unlikely extensions count: {count}, skipping parsing.")
            return []
        
        extensions = []
        for i in range(count):
            if buffer.pos >= len(buffer.data):
                print(f"[ERROR] Unexpected end of data while parsing extension {i+1}/{count}.")
                break
            print(f"[DEBUG] Parsing extension {i + 1}/{count}, pos: {buffer.pos}")
            ext_type = buffer.get_uint16()
            ext_data = buffer.get_bytes_array()
            extensions.append({'type': ext_type, 'data': ext_data})
        return extensions


    def __repr__(self):
        return (f"SignedBlock(header={super().__repr__()}, "
                f"master_signature={self.master_signature}, "
                f"transactions={len(self.transactions)}, "
                f"block_extensions={len(self.block_extensions)})")



class TransactionReceipt:
    def __init__(self, buffer: SerialBuffer):
        self.status = buffer.get_uint8()
        self.cpu_usage_us = buffer.get_uint32()
        self.net_usage_words = buffer.get_varuint32()
        self.trx = self._parse_transaction_variant(buffer)

    @staticmethod
    def _parse_transaction_variant(buffer: SerialBuffer):
        type_id = buffer.get_varuint32()
        if type_id == 0:
            return buffer.get_checksum256()  # packed_transaction id
        elif type_id == 1:
            return buffer.get_bytes_array()  # packed_transaction itself
        else:
            raise ValueError(f"Unknown transaction variant type id: {type_id}")

    def __repr__(self):
        return f"TransactionReceipt(status={self.status}, trx={self.trx}, ...)"


class ProducerKey:
    def __init__(self, buffer: SerialBuffer):
        print(f"[DEBUG] Start ProducerKey at {buffer.pos} / {len(buffer.data)}")
        self.producer_name = buffer.get_name()
        print(f"[DEBUG] producer_name: {self.producer_name}, pos: {buffer.pos}")

        self.block_signing_key = buffer.get_public_key()
        print(f"[DEBUG] block_signing_key: {self.block_signing_key}, pos: {buffer.pos}")


    def __repr__(self):
        return f"ProducerKey(producer_name='{self.producer_name}', block_signing_key='{self.block_signing_key}')"


