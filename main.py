#!/usr/bin/env python
import os, sys, subprocess, time, platform
import hashID.hashid as HID


##TODO: Add argument that passes wordlist and hashfile, so that program will ID and attempt to crack
## all hashes in the file with a given wordlist
##TODO: Add detection for hashcat success without querying cracked_hashes.txt
##TODO: Make $hashtype variable global for simplicity

wordlistnames = ["rockyou", "rockyou.txt", "wordlist", "wordlist.txt", "passwords", "passwords.txt"]
OS = ""

def cls():
    if OS == "Windows":
        os.system("cls")
    elif OS == "Linux":
        os.system("clear")

def checkHashcat():
    if "Linux" in OS:
        proc = subprocess.Popen(["hashcat/hashcat-cli64.bin", "--help"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if "hashfile" in out:
            pass
        else:
            try:
                proc = subprocess.Popen(["hashcat/hashcat-cli32.bin", "--help"], stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
                if "hashfile" in out:
                    pass
            except:
                cls()
                print("Hashcat isn't working properly, try installing using apt-get or downloading binaries and adding them in the root program directory to a folder called \"hashcat\"")
                sys.exit(1)

    elif "Windows" in OS:
        try:
            proc = subprocess.Popen(["hashcat\hashcat-cli64.exe", "--help"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            if "hashfile" in out:
                pass
        except:
            cls()
            print("Hashcat isn't working properly, try installing using apt-get or downloading binaries and adding them in the root program directory to a folder called \"hashcat\"")
            sys.exit(1)

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
    if "Windows" in OS:
        proc = subprocess.call(["hashcat/hashcat-cli64.exe", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])
    elif "Linux" in OS:
        proc = subprocess.call(["hashcat\hashcat-cli64.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes.txt"])

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
        checkHashcat()
        cls()

        with open('hashtypes', 'w') as hashtype:
            ID = HID.HashID()
            print("Enter your hash: ")
            hash = raw_input()
            with open("hash", "w") as h:
                h.write(hash)
            HID.writeResult(ID.identifyHash(hash), hashtype, True)

        with open('hashtypes', 'r') as f: #ghetto, I know. will fix in future
            s = f.readlines()

        found = False
        pls = "".join(s)
        count = pls.count("Mode: ")

        while(not found and count > 0):
            for line in s:
                if "Mode:" in line:
                    i = line.find("Mode: ")
                    m = line[i+6:-2]
                    hashtype = line[:line.find("[Hashcat")]
                    print("\n\nStarting hashcat with m = " + m + "\n\n")

                    wordlist = findWordlist()
                    crack(m, wordlist)
                    count -= 1
                    found = cracked()

                    if found:
                        printResults(found, hashtype)
                        break

        print("Would you like to delete the cracked_hashes.txt file? Y/N")
        if "Y" in raw_input().upper():
            print("Writing previous results to \"old_cracked_hashes.txt\"...")
            with open("old_cracked_hashes.txt", "a") as old:
                old.write(crackedHashes(hashtype))
            os.remove('cracked_hashes.txt')
        os.remove('hashtypes')
        os.remove('hash')

if __name__ == "__main__":
    try:
        OS = platform.system()
        main()

    except KeyboardInterrupt:
        pass
