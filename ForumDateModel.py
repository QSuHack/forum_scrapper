class User:
    def __init__(self, name, join_date, posts: int, rep: int):
        self.name = name
        self.join_date = join_date
        self.number_of_posts = posts
        self.user_reputation = rep

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


#class UserSecretInformation(User):
#   raise NotImplementedError


class Post:
    def __init__(self, author: User, content: str, date: str,time:str, reputation: int):
        self.time = time
        self.author = author
        self.content = content
        self.date = date
        self.post_reputation = reputation
    def __str__(self):
        return str(self.author)+"\n"+ self.date + self.time + "rep:" + str(self.post_reputation) + "\n" + self.content + "\n"

class Theard:
    def __init__(self, title:str, link:str,theard_author: User, views:int, replies:int,last_poster, recent_date, is_hot=False, is_locked=False):
        self.recent_date = recent_date
        self.last_poster = last_poster
        self.link = link
        self.title = title
        self.views = views
        self.replies = replies
        self.author = theard_author
        self.list_of_post = list()
        self.is_hot = is_hot
        self.locked = is_locked

    def add_post(self, new_post: Post):
        self.list_of_post.append(new_post)

    def text_form(self):
        return self.link + self.title + str(self.views) + str(self.replies) + str(self.author) + "\n"


class SubForum:
    def __init__(self):
        self.list_of_theard = list()

    def add_theard(self, new_theard: Theard):
        self.list_of_theard.append(new_theard)


class Forum:
    def __init__(self):
        self.users = list()
        self.subforum = list()

    def add_subforum(self, new_subforum: SubForum):
        self.subforum.append(new_subforum)

    def add_user(self, user:User):
        self.users.append(user)