# DanhengServer_Tools
A program that parses the Handbook from DanghengServer and provides a convenient interface for composing commands.

## Features
- Creating relics with the desired affixes
- Easily search and give away various items
- Easily search and issue blessings and miracles of the virtual universe. They are sorted by universe type, rarity and path
- Issuing characters and customizing their properties
- Support for item names in any language supported by the game. Just specify your language in the server settings to create a Handbook in that language, and then give that Handbook to this program.
- Localization in English and Russian, but other languages can be added.

## Soon to be realized:
- Overlaying all effects, including character and food effects
- Smart subaffix generation for relics
- List of starting and frequently used commands, as well as a list of custom commands
- Execution of commands on the server if someone develops OpenCommand Plugin. I don't know C#.
- Mission Management
- Scenes management


## Running

It requires a Handbook, which can be found in the config folder of your server. This allows DanghengServer Tools to not need to be updated when a new version of the game is released, just give it a new Handbook and it will find the IDs of new items on its own. To work, just place `Handbook.txt` next to `DanghengServer_Tools.exe`. 

---
![image](https://github.com/user-attachments/assets/63c781cf-f30a-4ef6-8942-9daa71c1c269)

