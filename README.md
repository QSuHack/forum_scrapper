# forum_scrapper

## It's forum scrapper build for https://hoffpolitics.forumpolish.com
With it you can create backups. 
But it can work for other forum which based on same template. Hoffpolitics is created at [Forumotion](https://forumotion.com).

Authorized access to `hoffpolitics` is required. 
Place your `LOGIN` and `PASSWORD` in `.env` in main catalog.
Serialization structure is in `ForumModel.proto`.
In `deserialization.py` variable `forum_from_backup` store Forum object like in proto file. 
Required packages:
BeautifulSoup4, dotenv(only to import data from `.env`), requests.
