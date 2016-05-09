#!/usr/bin/env python
import os, sys, subprocess, time
import hashID.hashid as HID

##In the future, add argument that passes wordlist and hashfile, so that program will ID and attempt to crack
## all hashes in the file with a given wordlist

wordlistnames = ["rockyou", "rockyou.txt", "wordlist", "wordlist.txt", "passwords", "passwords.txt"]

def main():
        os.system('clear')
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
                os.system('clear')
                print("Hashcat isn't working properly, try installing using apt-get or downloading binaries and adding them in the root program directory to a folder called \"hashcat\"")
                sys.exit(1)


        with open('hashtypes', 'w') as hashtype:
            ID = HID.HashID()
            print("Enter your hash: ")
            hash = raw_input()
            with open("hash", "w") as h:
                h.write(hash)
            HID.writeResult(ID.identifyHash(hash), hashtype, True)

        with open('hashtypes', 'r') as f: #ghetto, I know. will fix in future
            s = f.readlines()

        hashtype = ""
        found = False
        wordlist = None

        while(not found):
            for line in s:
                if "Mode:" in line:
                    i = line.find("Mode: ")
                    m = line[i+6:-2]
                    hashtype = line[:line.find("[Hashcat")]
                    print("\n\nStarting hashcat with m = " + m + "\n\n")
                    if(os.path.isfile("wordlist")):
                        wordlist = "wordlist"
                    elif(os.path.isfile("rockyou.txt")):
                        wordlist = "rockyou.txt"
                    elif(os.path.isfile("wordlist.txt")):
                        wordlist = "wordlist.txt"
                    elif(wordlist == None):
                        print("Specify wordlist filename: ")
                        wordlist = raw_input()
                        if(!os.path.isfile(wordlist)):
                            print("Wordlist not found, using default wordlist of \"wordlist\".")
                            wordlist = "wordlist"
                            time.sleep(5)
                    proc = subprocess.call(["hashcat/hashcat-cli64.bin", "-m" + str(m), "hash", wordlist, "-ocracked_hashes"])
                    try:
                        with open('cracked_hashes', 'r') as f:
                            if ":" in f.read():
                                found = True
                                break
                    except IOError:
                        pass
            if not found:
                print("Sorry, no hashes cracked.")
            break

        if found:
            print("Hashes cracked:\n")
            with open('cracked_hashes', 'r') as f:
                print("Type: " + hashtype + ":: " + f.read())

        print("Would you like to delete the cracked_hashes file? Y/N")
        if raw_input() == "Y" or "y":
            os.system('rm cracked_hashes')
        else:
            print("Not deleted.")
        os.remove('hashtypes')
        os.remove('hash')
        os.remove('hashcat.pot')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
