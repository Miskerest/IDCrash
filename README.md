# IDCrash

###UPDATE - July 2016
1. Fixed lots of bugs
   * Now displays correct hash-type after cracking!
   * No longer performs needless work!
   * `cracked_hashes.txt`'s contents aren't lost after every run!
   * Now detects your OS by default!
   * Other stuff!
2. **Added Windows support**
3. Made code easier to read (I hope)
4. Changed `main()` to be much less of a clusterfμ¢*.

##About

This is a Python script that combines psypanda's **hashID** and **hashcat** functionality.

It's likely full of bugs, so use at your own risk, but it should be useful for CTF events and the like.

Simply run `main.py` with Python, enter your hash, and the program will try all hashcat options that hashID delegates to it until it either cracks a hash or runs out of options.

To test functionality, try hashing "password". This is included in the default wordlist.

####Wordlists
I only provide a sample/testing wordlist. To use this effectively, you'll need to supply your own wordlist. Check [here](https://hashcat.net/forum/thread-1236.html) for a large array of wordlists.


##### Credit goes to **psypanda** and the **hashcat team** for two great programs that are used in this script.
