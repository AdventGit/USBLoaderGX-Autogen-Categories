# USBLoaderGX-Autogen-Categories
A poorly coded python script to auto-generate game categories from a WiiTDB.xml file

## Dependencies
Python 3: `pip install --upgrade lxml untangle`

## How to use
- Obtain a copy of `wiitdb.xml` from USBLoaderGX. This can be done by going to it's settings menu, navigating to `Update` on page 3, and clicking `WiiTDB.xml`.
- Mount your drive with the HomeBrew Channel `apps` folder on it into your computer and copy `..\apps\usbloader_gx\wiitdb.xml` into the same folder as the script, run the script, and copy over the newly created `GXGameCategories.xml` to `..\apps\usbloader_gx` and overwrite.
- Unmount and re-insert your drive into the Wii and boot into USBLoaderGX
- For best layout (Hover on the icons within USBLoaderGX for tooltips if you can't find the buttons I'm referencing)
  - Change view to Custom Selection
  - Change Game Sources to Wii, Gamecube, and NAND and/or EmuNAND
  - Sort By Rank
- That's it! Use the Game Categories button to filter games.

<br/>You now have categories for:
```txt
All
Wii
WiiWare
GameCube
Programs
Third-Party

VC-Arcade
VC-Commodore 64
VC-MSX
VC-N64
VC-NeoGeo
VC-NES
VC-Sega Genesis
VC-SEGA Master System
VC-SNES
VC-Turbo Grafx 1.6

Region-None
Region-NTSC
Region-PAL

Players-(1)
Players-(2)
Players-(3)
Players-(4)
Players-(5-8)
Players-(9-32)

ReqInput-Normal
ReqInput-Nunchuk
ReqInput-Gamecube
ReqInput-Classic
ReqInput-Exotic
```
