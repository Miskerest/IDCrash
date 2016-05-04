#!/usr/bin/env python
import os, sys, subprocess
import hashID.hashid as HID

def main():
        os.system('clear')
        proc = subprocess.Popen(["hashcat/hashcat-cli64.bin", "--help"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if "hashfile" in out:
            pass
        else:
            os.system('clear')
            print("Hashcat isn't working properly, try installing using apt-get or downloading binaries and adding them in the root program directory to a folder called \"hashcat\"")
            sys.exit(1)


        with open('hashtypes', 'w') as f:
            outfile = f
            ID = HID.HashID()
            print("Enter your hash: ")
            hash = raw_input()
            with open('hash', 'w') as h:
                h.write(hash)
            HID.writeResult(ID.identifyHash(hash), outfile, True)

        with open('hashtypes', 'r') as f: #ghetto, I know. will fix in future
            s = f.readlines()


        found = False
        while(not found):
            for line in s:
                if "Mode:" in line:
                    i = line.find("Mode: ")
                    m = line[i+6:-2]
                    proc = subprocess.call(["hashcat/hashcat-cli64.bin", "-m " + str(m), "hash", "wordlist", "-ocracked_hashes"])
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
                print(f.read())

        print("Would you like to delete the cracked_hashes file? Y/N")
        if raw_input() == "Y" or "y":
            os.system('rm cracked_hashes')
        else:
            print("Not deleted.")
        os.system('rm hashcat.pot hashtypes')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
