<div align="center">

<h3>PttAlert</h3>

A "gentle" reminder to press push-to-talk ;)

<img src="https://i.imgur.com/RCiSvU4.png"><img/>

</div>

### Installation for noobs:

1. Click "Code" => Download zip => Extract
2. Create a shortcut to `dist/PttAlert.exe`
3. Right click your new shortcut => properties
4. Add an integer after the target string to specify a required abstract threshold for the microphone input (0 or 1) is a good starting point (ex. `C:\path\to\PttAlert.exe` => `C:\path\to\PttAlert.exe 1`
5. Stick the shortcut somewhere convenient and run PttAlert
6. For now, you'll need to tell PttAlert which key you use for Discord when the program starts. The first key you press on the keyboard after PttAlert starts will register that key with the program.
7. If the microphone level is above the threshold and the Ptt Key isn't depressed, we'll see a friendly reminder appear center-screen.