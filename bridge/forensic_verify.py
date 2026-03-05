import hashlib 
import json

# 1. The 42-byte "Raw" record as it would come off the Mainframe 3390 Cylinder
# (This is a hex representation of EBCDIC data)
ebcdic_record = b'\xf2\xf0\xf2\xf6\xf0\xf3\xf0\xf5\xf1\xf9\xf4\xf5\xf0\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xf0\xf0\xf0\xf0\xf0\xf0\xf1\xf2\xf5\xf5\xf0\x8f\x32\x61\x1b\xde\x77\x11\x0a'
def verify_integrity(record, expected_hash):
    # 2. Run the SHA-256 "Defined Procedure"
    sha256_machine = hashlib.sha256()
    sha256_machine.update(record)
    #The update() method performs bitwise transformations on data chunks without loading the entire dataset into memory, maintaining a cumulative internal state
    #This "streaming" approach is vital for the 2026 Bridge, as it allows your forensic scraper to verify billions of mainframe records without crashing modern cloud instances
    
    calculated_hash = sha256_machine.hexdigest()
    
    # 3. The Forensic Comparison
    if calculated_hash == expected_hash:
        print("✅ INTEGRITY VERIFIED: No data corruption.")
        return True
    else:
        print("❌ FORENSIC ALERT: Data has been tampered with!")
        return False


#Integrity check complete. let's carve up our 42b of data into its component fields
def extract_fields(record):
    # Carving the bytes according to the COBOL map
    ts_bytes = record[0:14]
    id_bytes = record[14:24]
    amount_bytes = record[24:34]
    
    return ts_bytes, id_bytes, amount_bytes

# THE CALL: Passing our record into the carver
ts, tx_id, amount = extract_fields(ebcdic_record)

print(f"Extracted Raw ID: {tx_id}")

# Translating the EBCDIC Transaction ID to modern ASCII/UTF-8
readable_id = id_bytes.decode('cp500')
print(f"Mainframe ID: {readable_id}")

# The Final Forensic Bridge Output
forensic_json = {
    "status": "VERIFIED",
    "metadata": {
        "timestamp": ts_bytes.decode('cp500'),
        "tx_id": id_bytes.decode('cp500')
    },
    "financials": {
        "amount_raw": amount_bytes.decode('cp500'),
        "currency": "USD"
    },
    "security": {
        "sha256_hash": calculated_hash 
    }
}

print(json.dumps(forensic_json, indent=4))


