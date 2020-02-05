# Seed_Raid_Bot
 A python script useful to softreset Pokémon SwSh Raids
 
# Warning
 I won't be liable if your Switch get damaged or banned. Use at your own risk.
 
 # Features
* Sofreset for a good Den Seed (perfect IVs, shiny at low frame, etc.)
* Softreset for event raids
* Softreset for rare beam raids
 
# Requirements
* CFW
* Internet Connection
* sys-botbase(https://github.com/olliz0r/sys-botbase)
* ldn_mitm(https://github.com/spacemeowx2/ldn_mitm)

# Usage
* Connect your Switch to Interet
* Start sys-botbase and ldn_mitm
* Go to System Settings, check your Switch IP and write it in the script
* Set game text speed to normal
* Save in front of an empty Den, get its watts if they're avaiable. You must have at least one Wishing Piece in your bag
* Start the bot with game closed and selection square over it

# Research Filters
* r.Ability == '1'/'2'/'H'
* r.Nature == 'NATURE'
* r.ShinyType = 'None'/'Star'/'Square'
* r.IVs == spread_name (spread_name = [x,x,x,x,x,x])

# Credits:
* spacemeowx2 for his livesafer sys-module. It avoids Switch to disconnect from wifi once game is opened
* olliz0r for his amazing sys-module
* wwwwwwzx for [G8RNG](https://github.com/wwwwwwzx/raidtool) code
* Admiral-Fish for cleaning G8RNG code
* zaksabeast for [CaptureSight](https://github.com/zaksabeast/CaptureSight/) (all addresses/checks are taken from there)
