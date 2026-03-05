import hashlib
import json

# 1. The 42-byte "Raw" record (EBCDIC)
ebcdic_record = b'\xf2\xf0\xf2\xf6\xf0\xf3\xf0\xf5\xf1\xf9\xf4\xf5\xf0\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xf0\xf0\xf0\xf0\xf0\xf0\xf1\xf2\xf5\xf5\xf0\x8f\x32\x61\x1b\xde\x77\x11\x0a'

# Define the expected hash (Update this with your actual target hash)
EXPECTED_HASH = "8f32611bde77110a..." 

def verify_integrity(record):
    """Calculates the SHA-256 hash of the raw bytes."""
    sha256_machine = hashlib.sha256()
    sha256_machine.update(record)
    return sha256_machine.hexdigest()

def extract_fields(record):
    """Slices the record into component fields."""
    ts_bytes = record[0:14]
    id_bytes = record[14:24]
    amount_bytes = record[24:34]
    return ts_bytes, id_bytes, amount_bytes

# --- EXECUTION FLOW ---

# A. Generate and Export the Hash
final_hash = verify_integrity(ebcdic_record)
print(f"✅ Calculated Hash: {final_hash}")

# B. Comparison Check
if final_hash == EXPECTED_HASH:
    print("✅ INTEGRITY VERIFIED: No data corruption.")
else:
    print("❌ FORENSIC ALERT: Data has been tampered with!")

# C. Extract and Decode
ts_b, id_b, am_b = extract_fields(ebcdic_record)

# D. Generate Final JSON
forensic_json = {
    "status": "VERIFIED",
    "metadata": {
        "timestamp": ts_b.decode('cp500'),
        "tx_id": id_b.decode('cp500')
    },
    "financials": {
        "amount_raw": am_b.decode('cp500'),
        "currency": "USD"
    },
    "security": {
        "sha256_hash": final_hash 
    }
}

print(json.dumps(forensic_json, indent=4))
