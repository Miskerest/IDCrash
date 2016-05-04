# IDCrash

This is a Python script that combines psypanda's **hashID** and **hashcat** functionality.

It's likely riddled with bugs, so use at your own risk, but it should be useful for CTF events and the like.

Simply enter your hash and the program will try all hashcat options that hashID delegates to it until it cracks a hash, or runs out of options.
You will need to supply your own wordlist, titled "wordlist.txt". Put it in the root program directory.

Credit goes to **psypanda** and the **hashcat team** for two great programs that are used in this script.
