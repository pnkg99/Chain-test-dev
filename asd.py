def eosio_std_hash(name: str) -> int:
    """Emulira std::hash<std::string> u EOSIO WASM okruženju"""
    h = 5381  # djb2 hash početna vrednost
    for c in name:
        h = ((h << 5) + h) + ord(c)  # h * 33 + c
        h &= 0xFFFFFFFF  # Ograničavanje na 32-bitni unsigned int
    return h

# Test
print(eosio_std_hash("sidechain1"))  # Uporedi sa C++ std::hash<std::string>
