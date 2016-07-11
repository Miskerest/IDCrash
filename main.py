#!/usr/bin/env python
import os, sys, subprocess, time, platform
import hashID.hashid as HID

##TODO: Add argument that passes wordlist and hashfile, so that program will ID and attempt to crack all hashes in the file with a given wordlist
##DONE: Add detection for hashcat success without querying cracked_hashes.txt

wordlistnames = ["rockyou", "rockyou.txt", "wordlist", "wordlist.txt", "passwords", "passwords.txt"]
OS = ""
hash = ""

def cls(): #clears terminal prompt window
    if "windows" in OS.lower():
        os.system("cls")
    elif "linux" in OS.lower() or "darwin" in OS.lower():
        os.system("clear")

def findWordlist(): #attempts to locate predefined wordlists, otherwise asks for location
    if(os.path.isfile("wordlist")):
        return "wordlist"
    elif(os.path.isfile("wordlist.txt")):
        return "wordlist.txt"
    elif(wordlist == None):
        return raw_input("Specify wordlist: ")
        time.sleep(3)

def crack(m, wordlist): #attempts to crack hash given a specific hash type "m"
    try: #automatic OS detection
        if "Windows" in OS and "64" in platform.machine():
            s = subprocess.check_output(["hashcat/hashcat-cli64.exe", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Windows" in OS and "64" not in platform.machine():
            s = subprocess.check_output(["hashcat/hashcat-cli32.exe", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Linux" or "Darwin" in OS and "64" in platform.machine():
            s = subprocess.check_output(["hashcat/hashcat-cli64.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
        elif "Linux" or "Darwin" in OS and "64" not in platform.machine():
            s = subprocess.check_output(["hashcat/hashcat-cli32.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])

        print(s) #captures output to s, prints output, looks for success
        if "All hashes have been recovered" in s:
            return True #returns True if successful, ending the loop in main()
    except:
        print("Next...")

def printResults(found, hashtype): #prints results
    if found:
        print("\n\nSUCCESS!\n")
        print("Hashes cracked: " + crackedHashes(hashtype) + "\n")
        return

    print("Sorry, no hashes cracked.")

def crackedHashes(hashtype): #gets results from cracked_hashes.txt TODO: change this to not use open()
    with open('cracked_hashes.txt', 'r') as f:
        return("Type: " + hashtype + ":: " + f.read())

def main():
        cls()
        wordlist = findWordlist() #finds wordlist
        ID = HID.HashID() #creates HashID object
        hash = raw_input("Enter your hash: ")
        with open("hash", "w") as h:
            h.write(hash)
        s = HID.writeResult(ID.identifyHash(hash), True).split("\n") #identifies hash, returns string of possible hashtypes

        count = "".join(s).count("Mode: ") #counts number of possible m values (hashtypes)

        for i in range(count): #loops through possible m values
            for line in s:
                if "Mode:" in line: #grabs m value from line
                    i = line.find("Mode: ")
                    m = line[i+6:-1]
                    hashtype = line[:line.find("[Hashcat")]
                    print("\n\nStarting hashcat with m = " + m + "\n\n")

                    found = crack(m, wordlist)#attempts to crack, returns True to found if successful

                    if found: #once found, prints results and removes temp files
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
        OS = platform.system() #detects OS, writes OS version to global OS var
        if os.path.isfile("cracked_hashes.txt"):
            os.remove("cracked_hashes.txt")

        if len(sys.argv) <= 1: #checks for args such as wordlist or hashfile
            main()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\nUsage: run \"python main.py\" with no arguments. \n\nAlternatively: \nrun with --wordlist [wordlist] to specify a wordlist \nrun with --hashfile [hashfile] to specify a hashfile")
            print("(NOT ADDED YET)") #TODO: this
            sys.exit(0)

    except KeyboardInterrupt:
        os.remove("hash")
        sys.exit(0)
