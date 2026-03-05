import hashlib

# 1. The 42-byte "Raw" record as it would come off the 3390 Cylinder
# (This is a hex representation of EBCDIC data)
ebcdic_record = b'\xf2\xf0\xf2\xf6\xf0\xf3\xf0\xf5\xf1\xf9\xf4\xf5\xf0\xf0...' 

def verify_integrity(record, expected_hash):
    # 2. Run the SHA-256 "Defined Procedure"
    sha256_machine = hashlib.sha256()
    sha256_machine.update(record)
    calculated_hash = sha256_machine.hexdigest()
    
    # 3. The Forensic Comparison
    if calculated_hash == expected_hash:
        print("✅ INTEGRITY VERIFIED: No data corruption.")
        return True
    else:
        print("❌ FORENSIC ALERT: Data has been tampered with!")
        return False
