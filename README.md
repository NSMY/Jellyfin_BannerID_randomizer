# A random ID script for [Jellyfin-Featured Banner](https://github.com/BobHasNoSoul/jellyfin-featured/) From [BobHasNoSoul](https://github.com/BobHasNoSoul) ![Screenshot 2023-11-11 090503](https://github.com/BobHasNoSoul/jellyfin-featured/assets/23018412/be19e601-da6f-4428-ba66-0c8179b2dd55) 
## Windows Or Linux Compatible
it gets all movies.movie and shows.series ID (Images; MetadataPath ID) from your [Jellyfin DB](https://jellyfin.org/) (not seasons/episodes) selects X random and or y Latest Non Duplicates (Movies or TvSeries) of the db, and makes a list of them
to be the banners list.txt to make a Random Featured list, NewestItemSaved in the db will be 0 on the list.
- Remember to alter the [get_rand_jellyfin_ids.py](https://github.com/NSMY/Jellyfin_BannerID_randomizer/blob/main/get_rand_jellyfin_ids.py) files Paths and Variables for your personal choices

jellyfin-featured was found From the list of Jellyfin addons/plugins/mods & utils found HERE: https://github.com/awesome-jellyfin/awesome-jellyfin

all you need is the [get_rand_jellyfin_ids.py](https://github.com/NSMY/Jellyfin_BannerID_randomizer/blob/main/get_rand_jellyfin_ids.py) open with a text editor and edit <ins>**YOUR**</ins> Paths in to the file then Run via the command prompt it will auto gen the list.txt
> if on Linux and default install you will need perms to place in correct path so instead it will save list.txt in Curr Dir (editable) then you can sudo mv it to destination, there will be a print statement when completed of the whole command if needed[Current list path and DEFAULT jellyfin web/avatars path]

> Or (linux) you can sudo crontab -e and open the roots crontab and make scheduled job to do whenever.
> - EG of making a new random list each night at 12:01 is:
> - 1 0 * * * cd /path/to/get_rand_jellyfin_ids.py/file/ && python3 get_rand_jellyfin_ids.py && mv list.txt /path/to/YOUR/jellyfin/web/avatars/dir
> - (default linux path is /usr/share/jellyfin/web/avatars/)

# Prerequisite [Python Installed](https://www.python.org/downloads/)

## Download the Script

You can directly download the `get_rand_jellyfin_ids.py` script:

**Right-click the link and select "Save Link As..." to download the file.**

[![Download get_rand_jellyfin_ids.py](https://img.shields.io/badge/Download-get__rand__jellyfin__ids.py-blue?style=for-the-badge&logo=download&logoColor=white)](https://raw.githubusercontent.com/NSMY/Jellyfin_BannerID_randomizer/refs/heads/main/get_rand_jellyfin_ids.py)
