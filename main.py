#!/usr/bin/env python
import os, sys, subprocess, time, platform
import hashID.hashid as HID

##TODO: Add argument that passes wordlist and hashfile, so that program will ID and attempt to crack
## all hashes in the file with a given wordlist
##TODO: Add detection for hashcat success without querying cracked_hashes.txt

wordlistnames = ["rockyou", "rockyou.txt", "wordlist", "wordlist.txt", "passwords", "passwords.txt"]
OS = ""

def cls():
    if OS == "Windows":
        os.system("cls")
    elif OS == "Linux" or OS.lower() == "Darwin".lower():
        os.system("clear")

def findWordlist():
    if(os.path.isfile("wordlist")):
        return "wordlist"
    elif(os.path.isfile("rockyou.txt")):
        return "rockyou.txt"
    elif(os.path.isfile("wordlist.txt")):
        return "wordlist.txt"
    elif(wordlist == None):
        return raw_input("Specify wordlist: ")
        time.sleep(3)

def crack(m, wordlist):
    try:
        if "Windows" in OS and "64" in platform.machine():
            proc = subprocess.call(["hashcat/hashcat-cli64.exe", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Windows" in OS and "64" not in platform.machine():
            proc = subprocess.call(["hashcat/hashcat-cli32.exe", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Linux" or "Darwin" in OS and "64" in platform.machine():
            proc = subprocess.call(["hashcat\hashcat-cli64.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Linux" or "Darwin" in OS and "64" not in platform.machine():
            proc = subprocess.call(["hashcat\hashcat-cli32.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
    except:
        cls()
        print("Hashcat isn't working properly. This may be a bug, or your system is not currently supported by Hashcat.")

def cracked():
    try:
        with open('cracked_hashes.txt', 'r') as f:
            if ":" in f.read():
                return True
    except IOError:
        return False

def printResults(found, hashtype):
    if found:
        cls()
        print("\n\nSUCCESS!\n")
        print("Hashes cracked: " + crackedHashes(hashtype) + "\n")
        return

    print("Sorry, no hashes cracked.")

def crackedHashes(hashtype):
    with open('cracked_hashes.txt', 'r') as f:
        return("Type: " + hashtype + ":: " + f.read())

def main():
        cls()

        ID = HID.HashID()
        hash = raw_input("Enter your hash: ")
        with open("hash", "w") as h:
            h.write(hash)
        s = HID.writeResult(ID.identifyHash(hash), True).split("\n")

        count = "".join(s).count("Mode: ")

        for i in range(count):
            for line in s:
                if "Mode:" in line:
                    i = line.find("Mode: ")
                    m = line[i+6:-1]
                    hashtype = line[:line.find("[Hashcat")]
                    print("\n\nStarting hashcat with m = " + m + "\n\n")

                    wordlist = findWordlist()
                    crack(m, wordlist)
                    found = cracked()

                    if found:
                        printResults(found, hashtype)
                        if "Y" in raw_input("Save cracked hashes? Y/N: ").upper():
                            print("Writing previous results to \"old_cracked_hashes.txt\"...")
                            with open("old_cracked_hashes.txt", "a") as old:
                                old.write(crackedHashes(hashtype))
                                os.remove('cracked_hashes.txt')
                        break

            if not found:
                cls()
                print("No results or valid hash-types found.")
            os.remove('hash')
            sys.exit(0)

if __name__ == "__main__":
    try:
        OS = platform.system()
        if os.path.isfile("cracked_hashes.txt"):
            os.remove("cracked_hashes.txt")

        if len(sys.argv) <= 1:
            main()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\nUsage: run \"python main.py\" with no arguments. \n\nAlternatively: \nrun with --wordlist [wordlist] to specify a wordlist \nrun with --hashfile [hashfile] to specify a hashfile")
            print("(NOT ADDED YET)")
            sys.exit(0)

    except KeyboardInterrupt:
        os.remove("hashtypes")
        sys.exit(0)
