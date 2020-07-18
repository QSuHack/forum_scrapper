import _pb2

with open("backup", mode="rb") as backup:
    forum_from_backup = _pb2.Forum()
    forum_from_backup.ParseFromString(backup.read())
    print(forum_from_backup)
    for s in forum_from_backup.Sb:
        for t in s.theards:
            print(t.title)
    with open("backup.txt", mode="w+", encoding="utf-8") as b:
        b.write(str(forum_from_backup))