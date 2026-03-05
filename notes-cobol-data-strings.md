In COBOL, you don't declare types like int or string in the same way you do in Python. You use a Picture Clause to draw a map of exactly how much space the data occupies on the disk.

| Variable Name | PIC Clause | Byte Calculation | Explanation |
|---|---|---|---|
| WS-TIMESTAMP | PIC X(14) | 14 Bytes | X means any character. (14) means exactly 14 slots. This holds YYYYMMDDHHMMSS (e.g., 20260305194500) |
| WS-TRANSACTION-ID | PIC X(10) | 10 Bytes | X(10) is 10 slots for your unique ID. |
| WS-AMOUNT | PIC 9(8)V99 | 10 Bytes | 9 means numbers only. (8) is eight digits, V is a "virtual" decimal point (it doesn't take up a byte!), and 99 is two more digits. Total: 10 digits |
| WS-HASH-PREFIX | PIC X(8) | 8 Bytes | X(8) is 8 slots for the first part of your SHA-256 hash. |
| TOTAL |  | 42 Bytes | 14 + 10 + 10 + 8 = 42 |
Why the V is "Forensic Gold"
Notice the PIC 9(8)V99. This is a 10-digit number, but it only takes up 10 bytes because the decimal point (V) is implied.
 * The "Hacker" Trick: In a modern database, a decimal point is a physical character. In COBOL, the decimal is just a rule in the code.
 * The Result: On the actual disk (the "Cylinder"), the amount 1,234.56 is stored as 0000123456. The COBOL program "knows" to put the decimal before the last two digits when it reads it. This saves space and prevents rounding errors that plague modern floating-point math.
