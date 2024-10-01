# IntegrateFlatpak

Flatpaks naturally store all their information (including `config`, `cache`, and `data`) in their own sequestered folder. For simpler backups and an easier way to find _all_ installed program config folders, lets put them all in `XDG_CONFIG_HOME`  instead of individal `com.name.app/config/truename` folders.

## Usage 
1. Download `integrateFlatpaks.py` and `truenames.toml` to the same folder.
2. Add to the "run" section of `truenames.toml` any flatpak names and truenames. Truenames of flatpaks being the name they are given when placed in xdg homes and follow the pattern `com.name.app/config/truename`.
3. Run the program:


```python integrateFlatpaks.py [flatpaktoxdg|xdgtoflatpak] ```
Parameters | Description
---|---
flatpaktoxdg | Move flatpak files to xdg locations then place link in flatpak folder.
xdgtoflatpak | Delete empty flatpak file folders and replace with link to xdg location.
--flatpaks | Limit to certain flatpaks that are listed afterwards instead of all installed.
--noconfig | Do not alter config dirs.
--nodata | Do not alter data dirs.
--nocache | Do not alter cache dirs.