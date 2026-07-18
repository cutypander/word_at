[README.txt](https://github.com/user-attachments/files/30147341/README.txt)
Hiya!

This is written by a human. No real way to kind of point that out except by saying it-
and hope you believe me to some extent. Specifically, the README.txt

This Project is designed for cyber-decks and may not be of the highest quality. 
Most of the design choices are based on concerns that things might not work, things may
not go the way I hope them to and that frankly? I have no funding, not a pound, not a
dollar, not a euro, nada.

Of course, this is AI made, that means I don't own this. HOWEVER, I do bug test the
things I work on. It's already explicit that I don't know how to code. And as stated
in previous writing, it's not like I have the money to hire anyone to work on this
irrelevent work. Floppy disks are outdated, that's part of the reason I like them.

It lets me write anything, possibly even forget that I left a floppy on a desk and know
that whatever I've written is particularly difficult to access since, why would you
still use floppy disks? Furthermore, they aren't particularly expensive but recent
floppy disks are particularly prone to dying. It's old hardware afterall, but they also
got cheaper to make because costs towards them were reduced.

Nonetheless, word processing doesn't require much space, saving texts to floppy's is 
also made easier with word@ since lots of terminal tasks are just done for you. That
includes checking the health of the floppy's you're using. It'll also automatically name
the floppy's themselves with double names using the military alphabet.

Having custom names isn't a feature, purely since it's for use with word@'s hashing and
limit checking. 

To be clear, word@ automatically places a limit on all floppy's to prevent corruption
if the sector health is lower, the limit increase to keep the floppy alive but to make
it clear that the floppy is dying.

How to install:

1: git clone https://github.com/cutypander/word_at.git

2: cd word_at

3: bash install.sh

commands and uses:

$ word@ [filename] - Standard mode:

 It'll open the file in nano with an orange theme.

$ word@ raw [filename] - Raw mode:

You just write into terminal instead of Nano. 
Meaning there's no additional interfaces: //SAVE & //REJECT , to save or cancel within
the terminal.

$ word@ TTF - Text To Floppy:

This scans the bank, checks the floppy's space and mirrors the files with duplicates.

$ word@ init - Format & Stamp:

Assigns a random NATO phonetic name to a new floppy disk, give's it an ID and registers
it to a ledger.

$ word@ ?scan - Magnetic Scan:

Triggers badblocks to physically test the magnetic surface of the floppy disk for
corruption

$ word@ update - Self updater:

As the word itself describes. It'll reach out to the Git repo of word_at to update and
overwrite itself.

$ word@ ?flop - checks if a floppy is mounted, if there's space and reads the NATO name.

$ word@ ?gath - calculates the per file size and the total size within the wordbank

$ word@ del! - Deletes file(s) with given options. Give's multiple options for deleting files.

$ word@ ?when - Show's the filenames in order of when they were last edited. 

Since this is for a Pi, there's also:

$ word@ ?work - runs a diagnostic to make sure the Pi has read/write permissions. 





Please keep in mind that while the code is written by AI, bug testing is done by me. 
AI uses a good amount of Malicious compliance when coding.
If it misses something then I need to tell it. Furthermore, if I were to learn code,
I already know I don't want to start with Bash. 

This is primarily for a personal project. I'm simply sharing what I've gotten done for
the sake of sharing. I have no obligation to continue this if it fits the task(s).

Thank you for using word@
