# A script for Jellyfin-Featured Banner (https://github.com/BobHasNoSoul/jellyfin-featured/).
# it gets all movies and shows.series ID (not seasons/episodes) selects user specified amount or Rand ids
# and y (num_newest_items) LastSavedMedia of the db of both Movies.Movie & Tv.Series, and makes a list of them
# to be the banners list.txt, num_newest_items in the db will be first on the list.

import os
import sqlite3
import random
import platform

NUM_NEWEST_ITEMS = 2  # Number of newest items in list
RANDOM_IDS = 4 # Num Rands in list


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
        DateLastMediaAdded,
        CleanName
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

while True:
    parsed_image_ids = []
    try:
        for ind, row in enumerate(results):
            ParsedImageID = parse_images(row[2])
            if ParsedImageID:
                parsed_image_ids.append({
                    'ParsedImageID': ParsedImageID,
                    'DateCreated': row[3],
                    'DateLastMediaAdded': row[4] if row[4] is not None else row[3]
                })
                # print(f"TypedBaseItem: {row[0]}, PresentationUniqueKey: {row[1]}, ParsedImageID: {ParsedImageID}, DateCreated: {row[3]}, DateLastMediaAdded: {row[4]}")
        break
    except AttributeError as e:
        print(e, f"\nItem {row} in db has No Image data yet (likely Jellyfin un-scanned): Skipping X item ")
        results.pop(ind)
        parsed_image_ids.clear()

# Select the newest items based on DateCreated and DateLastMediaAdded
newest_items = sorted(parsed_image_ids, key=lambda x: x['DateLastMediaAdded'], reverse=True)[:NUM_NEWEST_ITEMS]

remaining_items = [item for item in parsed_image_ids if item not in newest_items]

# Select x random ParsedImageIDs
# (ImageIds is the easiest way to get the ID as series hs a unique key and not one just for the parent Series)
# good tool to access dbs (https://sqlitebrowser.org/)
num_random_items = RANDOM_IDS
random_sample = random.sample(remaining_items, num_random_items) if len(remaining_items) >= num_random_items else remaining_items

all_items = newest_items + random_sample

parsed_image_id_strings = [item['ParsedImageID'] for item in all_items]

# # Uncomment the print block to test rather than saving a file every time
# for item in all_items:
#     print(item['ParsedImageID'] + '\n')

# Write the ParsedImageIDs to the file
with open(output_path, 'w') as file:
    file.write('\n'.join(parsed_image_id_strings))

print(f"ParsedImageIDs have been saved to {os.path.abspath(output_path)}")

path_reminder()
