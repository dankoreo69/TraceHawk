import os
import hashlib
import zlib

banner = """\033[091m
           ___   __________    ______                __
    ____  /   | / ___/ ___/   / ____/________ ______/ /_____  _____
   / __ \/ /| | \__ \\__ \    / /   / ___/ __ `/ ___/ //_/ _ \/ ___/
  / /_/ / ___ |___/ /__/ /  / /___/ /  / /_/ / /__/ ,< /  __/ /
 / .___/_/  |_/____/____/   \____/_/   \__,_/\___/_/|_|\___/_/
/_/
\033[0m"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def launch_hash_identifier():
    clear()
    print("\033[35m[+] Launching Hash-Identifier...\033[0m")
    os.system("hash-identifier")

def crc16(data: bytes):
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def crack_hash(hash_value, algorithm, wordlist_path):
    wordlist_path = wordlist_path.strip().strip('"').strip("'")

    if not os.path.isfile(wordlist_path):
        print(f"\033[31m[-] Wordlist not found at {wordlist_path}\033[0m")
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            words = file.readlines()
    except Exception as e:
        print(f"\033[31m[-] Error reading wordlist: {e}\033[0m")
        return

    for word in words:
        word = word.strip()

        if algorithm == "NTLM":
            hash_try = hashlib.new('md4', word.encode('utf-16le')).hexdigest()
        elif algorithm == "CRC16":
            hash_try = format(crc16(word.encode()), '04x')
        elif algorithm == "CRC32":
            hash_try = format(zlib.crc32(word.encode()) & 0xFFFFFFFF, '08x')
        elif algorithm == "Adler32":
            hash_try = format(zlib.adler32(word.encode()) & 0xFFFFFFFF, '08x')
        elif algorithm == "Whirlpool":
            try:
                import whirlpool
                hash_try = whirlpool.new(word.encode()).hexdigest()
            except ImportError:
                print("\033[31m[-] Whirlpool support requires 'whirlpool' package (pip install whirlpool).\033[0m")
                return
        else:
            try:
                h = hashlib.new(algorithm.lower())
                h.update(word.encode())
                hash_try = h.hexdigest()
            except ValueError:
                print(f"\033[31m[-] Algorithm {algorithm} is not supported by hashlib.\033[0m")
                return

        if hash_try.lower() == hash_value.lower():
            print(f"\033[31m[+] Hash cracked! Password is: {word}\033[0m")
            return

    print("\033[31m[-] Password not found in wordlist.\033[0m")

def hash_cracker():
    while True:
        clear()
        print(banner)
        print("\033[35m[+] Starting Hash Cracker...\033[0m")

        hash_value = input("\033[35mEnter the hash value to crack: \033[0m").strip()

        algorithms = [
            "NTLM", "MD4", "MD5",
            "SHA1", "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512",
            "SHA-224", "SHA-256", "SHA-384", "SHA-512",
            "CRC16", "CRC32", "Adler32", "Whirlpool"
        ]

        print("\n\033[35mSupported Algorithms:\033[0m")
        for i, algo in enumerate(algorithms, 1):
            print(f"\033[35m[{i}] {algo}\033[0m")

        choice = input("\n\033[35mSelect the algorithm number (or type 'exit' to cancel): \033[0m").strip()

        if choice.lower() == 'exit':
            print("\033[31mCancelled.\033[0m")
            return

        try:
            choice = int(choice)
            algorithm = algorithms[choice - 1]
        except (ValueError, IndexError):
            print("\033[31mInvalid selection. Restarting...\033[0m")
            input("\033[35mPress Enter to try again...\033[0m")
            continue

        print("\n\033[35mDrag and drop your wordlist file into this terminal and press Enter:\033[0m")
        wordlist_path = input().strip()

        crack_hash(hash_value, algorithm, wordlist_path)
        input("\n\033[35mPress Enter to return to main menu...\033[0m")
        break

def passcrack():
    while True:
        clear()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print("\n\033[35m[1] Launch Hash-Identifier\033[0m")
        print("\033[35m[2] Start Hash Cracker\033[0m")
        print("\033[31m[0] Exit\033[0m")

        choice = input("\033[31mSelect an option: \033[0m").strip()

        if choice == '1':
            launch_hash_identifier()
            input("\n\033[35mPress Enter to return to main menu...\033[0m")
        elif choice == '2':
            hash_cracker()
        elif choice == '0':
            print("\033[31mGoodbye!\033[0m")
            break
        else:
            print("\033[31mInvalid option. Restarting...\033[0m")
            input("\033[35mPress Enter to continue...\033[0m")

if __name__ == "__main__":
    passcrack()
