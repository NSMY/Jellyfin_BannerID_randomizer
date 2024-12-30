# A script for Jellyfin-Featured Banner (https://github.com/BobHasNoSoul/jellyfin-featured/).
# it gets all movies and shows.series ID (not seasons/episodes) selects 5 (line 73) random
# and the LastSavedMedia of the db of either Movies/Series, and makes a list of them
# to be the banners list.txt, NewestItemSaved in the db will be 0 on the list.

import os
import sqlite3
import random
import platform


# If linux cd to where this file is saved,
# will need perms to place this in the right dir (defualt: /usr/share/jellyfin/web/avatars/)
# so this is just for reference if new.
# Comment out last line if you dont want this next def to print every run
def path_reminder():
    print(f'\n"sudo mv {os.path.abspath(output_path)} /usr/share/jellyfin/web/avatars/"')


# PATHS
if platform.system() == 'Windows':
    db_path = r'C:\path_to\jellyfin\library.db' # Path for Win db (generally same place as jellyfin.db)
    output_path = r'C:\path\to\output_of\list.txt'  # Output path for Windows for the list.txt
else:
    db_path = '/var/lib/jellyfin/data/library.db'  # Path for Linux library db
    output_path = 'list.txt'  # Output path for Linux
    # default path of where the file should be move to '/usr/share/jellyfin/web/avatars/list.txt'  # Output path for Linux


def parse_images(images_col):
    parts = images_col.split('/')
    return parts[3] if len(parts) > 3 else None


with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Query to get movies and TV series with DateCreated and DateLastMediaAdded columns
    query = """
    SELECT
        type,
        PresentationUniqueKey,
        Images,
        DateCreated,
        DateLastMediaAdded
    FROM
        TypedBaseItems
    WHERE
        type = 'MediaBrowser.Controller.Entities.Movies.Movie' OR
        type = 'MediaBrowser.Controller.Entities.TV.Series'
    ORDER BY
        DateCreated DESC, DateLastMediaAdded DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

parsed_image_ids = []

for row in results:
    ParsedImageID = parse_images(row[2])
    if ParsedImageID:
        parsed_image_ids.append({
            'ParsedImageID': ParsedImageID,
            'DateCreated': row[3],
            'DateLastMediaAdded': row[4] if row[4] is not None else row[3]
        })
        # print(f"TypedBaseItem: {row[0]}, PresentationUniqueKey: {row[1]}, ParsedImageID: {ParsedImageID}, DateCreated: {row[3]}, DateLastMediaAdded: {row[4]}")

# Select the newest item based on DateCreated and DateLastMediaAdded
newest_item = max(parsed_image_ids, key=lambda x: x['DateLastMediaAdded']) if parsed_image_ids else None

# Select 5 random ParsedImageIDs
# (ImageIds is the easiest way to get the ID as series hs a unique key and not one just for the parent Series)
# good tool to access dbs (https://sqlitebrowser.org/)
random_sample = random.sample(parsed_image_ids, 5) if len(parsed_image_ids) >= 5 else parsed_image_ids

if newest_item:
    all_items = [newest_item] + [item for item in random_sample if item != newest_item]
else:
    all_items = random_sample

parsed_image_id_strings = [item['ParsedImageID'] for item in all_items]


# # Uncomment the print block to test rather than saving a file every time
# for item in all_items:
#     print(item['ParsedImageID'] + '\n')

# Write the ParsedImageIDs to the file
with open(output_path, 'w') as file:
    file.write('\n'.join(parsed_image_id_strings))

print(f"ParsedImageIDs have been saved to {os.path.abspath(output_path)}")

path_reminder()
