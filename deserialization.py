import _pb2

with open("backup", mode="rb") as backup:
    forum_from_backup = _pb2.Forum()
    forum_from_backup.ParseFromString(backup.read())
    print(forum_from_backup)
    for subforum in forum_from_backup.Sb:
        for theard in subforum.theards:
            print(theard.title)
            # Here next 'for' for post and you can get each property of post and use it, print or write it.
    with open("backup.txt", mode="w+", encoding="utf-8") as b:
        b.write(str(forum_from_backup)) # Not writing properly Polish characters, but it can be fixed by long version above.
