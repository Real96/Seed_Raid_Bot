# Seed_Raid_Bot
 A python script useful to softreset Pokémon SwSh Raids
 
# Requirements
* sys-botbase(https://github.com/olliz0r/sys-botbase)

# Features
* Sofreset for a good Den Seed (perfect IVs, shiny at low frame, etc.)
* Softreset for event raids
* Softreset for rare beam raids

# Usage
* Set game text speed to slow
* Save in front of a Den. You must have at least one Wishing Piece in your bag
* Start the bot with game closed and selection square over it
* Den Seed address: "peek 0xaddress 8" (address = 0x4298FA70 + (0xden_id) * 0x18)) Example: 0x4298FB78 Den 11
* Rare beam flag byte address = "peek 0xaddress 1" (address = 0x4298FA7A + (0xden_id) * 0x18) Example: 0x4298FB82 Den 11
* Event flag byte address = "peek 0xaddress 1" (address = (0x4298FA7B + (0xden_id) * 0x18)) Example: 0x4298FB83 Den 11

# Credits:
* olliz0r for his amazing sys-module
* wwwwwwzx for [G8RNG](https://github.com/wwwwwwzx/raidtool) code
* Admiral-Fish for cleaning G8RNG code
* zaksabeast for [CaptureSight](https://github.com/zaksabeast/CaptureSight/) (all addresses/checks are taken from there)
 
 
