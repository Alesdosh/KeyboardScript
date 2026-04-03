When I switched to Linux (Fedora 42 btw) I noticed that the LED activation on my generic keyboard stopped working.

So the key that normally turned on the keyboard LEDs didn’t do anything anymore, so I decided to try making a driver to get it working, which was actually a wrong idea since it wasn’t necessary to make a whole driver, just a script that would send the correct instructions when the corresponding key was pressed, so that’s what I did (with a bit of help from Claude to send the instructions).

## Scripts

- **main.py**  
  It was used to find the correct instructions that would turn on the LEDs.

- **index.py**  
  It’s the script used to turn on the LEDs by pressing the key.

## Execution

The command:

```bash
nohup python3 index.py > log.txt 2>&1 &
...
```

I use it to run the script in the background without needing to keep the terminal or the code editor open.
