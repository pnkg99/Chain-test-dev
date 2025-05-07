import datetime

def calculate_block_timestamp(date_str, millis=0):
    """
    Funkcija za proračun block_timestamp_type vrednosti za dati datum.
    
    :param date_str: Datum kao string, npr. '2025-03-14T09:41:49'
    :param millis: Milisekunde (ako treba dodati npr. 500 za .500)
    :return: Dict sa sekundama, polusekundama i binarnim prikazima
    """
    # Pretvaranje stringa u datetime
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt + datetime.timedelta(milliseconds=millis)  # Dodaj milisekunde ako treba

    # Epoh (1970-01-01)
    epoch = datetime.datetime(1970, 1, 1)

    # Ukupno sekundi
    total_seconds = int((dt - epoch).total_seconds())

    # Polusekunde (ako koristi varijantu sa 0.5 s)
    total_half_seconds = total_seconds * 2

    # Binarni zapisi (little endian)
    seconds_bytes = total_seconds.to_bytes(4, byteorder='little')
    half_seconds_bytes = total_half_seconds.to_bytes(8, byteorder='little')

    result = {
        "datetime": dt.isoformat(),
        "total_seconds": total_seconds,
        "total_half_seconds": total_half_seconds,
        "seconds_bytes_hex": seconds_bytes.hex(),
        "half_seconds_bytes_hex": half_seconds_bytes.hex(),
    }

    # Print za debug
    print("Datetime          :", result["datetime"])
    print("Total seconds     :", result["total_seconds"])
    print("Total half seconds:", result["total_half_seconds"])
    print("Seconds bytes hex :", result["seconds_bytes_hex"])
    print("Half-sec bytes hex:", result["half_seconds_bytes_hex"])

    return result


result = calculate_block_timestamp("2025-03-14T09:41:49", millis=500)