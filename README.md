# Discord rich presence for World of Warcraft

![STV](https://github.com/wodim/wow-discord-rich-presence/raw/master/images/rich-presence-1.png) ![WSG](https://github.com/wodim/wow-discord-rich-presence/raw/master/images/rich-presence-2.png)

Important: this requires a bit of patience and setup to make it work, so bear with me.

I play WotLK so this may not work on other versions of WoW, but you are welcome to try and tell me if it does.

## Requirements

* Python 3 for Windows, the [web-based installer](https://www.python.org/downloads/windows/) is OK. When it's finished installing, you will be asked if you want Python to be added to your $PATH, you have to say yes.

## Setup

1. [Download a copy of this repo](https://github.com/wodim/wow-discord-rich-presence/archive/master.zip) and decompress it. Inside you will find a WoW addon and a Python script.

2. Install the WoW addon by copying the **IPC** folder to your _Interface/Addons_ directory and make sure it loads. When you log in, you will see a few coloured squares on top of your portrait.

    ![Squares](https://github.com/wodim/wow-discord-rich-presence/raw/master/images/squares.png)

3. Open a Command Prompt and install the pywin32 and Pillow libraries for Python by typing this command:
`pip install pywin32 pillow`

4. Configure WoW in windowed mode (you need to play like that for this to work) and then maximise the window. Now we will make the squares say something longer so we can calibrate the size. Type this into your chat:

    _/ipc This is just a test I'm making to make sure my Python script can read the squares that appear in my World of Warcraft window. :-)_

    You should see many, many more squares appear.

5. Move to the directory where you decompressed this repo with the cd command, then cd into the **script** folder. For example, if you decompressed it into your Downloads folder, you will have to do something like this:
    `cd Downloads\wow-discord-rich-presence\script`

6. Go back to the command prompt while WoW is still open behind it, making sure none of the squares are being covered by the command prompt, and type this to run the wow.py script:
    `python wow.py`

7. Now, this is the tricky part. Your image viewer has opened and you will see something like this:

    ![Misaligned dots](https://github.com/wodim/wow-discord-rich-presence/raw/master/images/misaligned-squares.png)

    That's really bad! Every one of the white dots has to be right at the centre of every one of the squares.

8. Open wow.py with a text editor. You will see a variable called `MY_WIDTH` at the top. You have to tweak it and run the wow.py script again (remember, using `python wow.py`) until all the dots are aligned. Most likely you will have to use decimals. In the end, it will look like this:

    ![Aligned dots](https://github.com/wodim/wow-discord-rich-presence/raw/master/images/aligned-squares.png)

    That's so much better. Also, if you look in the command prompt, you will see the text has been read correctly by the script:
    `Read: This is just a test I'm making to make sure my Python script can read the squares that appear in my World of Warcraft window. :-)`

9. Edit the wow.py file again, this time change `DEBUG = 1` to `DEBUG = 0`.

From now on, you can double-click the wow.py file and it will work by itself. Your rich presence will be updated automatically as long as the script is kept running. You can just create a shortcut to this script on your Desktop and open it every time you open WoW.

## Licence

Both the addon and the wow.py script are in the public domain.
The rpc.py file is from [this repo](https://github.com/suclearnub/python-discord-rpc) and it's [MIT licenced](https://raw.githubusercontent.com/wodim/wow-discord-rich-presence/master/script/rcp.py-LICENSE).
