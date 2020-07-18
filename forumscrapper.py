from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

import ForumDateModel

import _pb2

load_dotenv()
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
root_url = "https://hoffpolitics.forumpolish.com"
form = {"username": login, "password": password, "autologin": "on", "redirect": '', "query": '', "login": "Zaloguj"}
with  requests.Session() as session_:
    request = session_.post("https://hoffpolitics.forumpolish.com/login", data=form)
    #   print(req.content)
    response = session_.get(root_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_forum = ForumDateModel.Forum()
    sub_forum = None
    for forum_ in soup.find_all("a", class_="forumtitle"):
        sub_forum = ForumDateModel.SubForum()
        soup1 = BeautifulSoup(session_.get(root_url + forum_['href']).content, 'html.parser')
        for row_ in soup1.find_all(class_="row"):
            if row_ is not None:
                title_div = row_.find(class_="topictitle")
                if title_div is not None:
                    title = title_div.contents[0]
                    theard_link = title_div['href']
                    theard_author = row_.find(class_="topic-author").find("a").contents[0]
                    posts = row_.find(class_="posts").contents[0]
                    views = row_.find(class_="views").contents[0]
                    last_user = row_.find(class_="gensmall").contents[0]
                    last_date = row_.find(class_="lastpost").contents[0].contents[6]
                    theard_to_add = ForumDateModel.Theard(title, theard_link, theard_author,
                                                          views, posts, last_user, last_date)
                    if theard_to_add is not None:
                        sub_forum.add_theard(theard_to_add)
        for theard in sub_forum.list_of_theard:
            soup2 = BeautifulSoup(session_.get(root_url + theard.link).content, 'html.parser')
            pages = list(set([x.parent.contents[3]['href'] for x in soup2.find_all(class_="page-sep")]))
            pages.insert(0, theard.link)
            for page_link in pages:
                soup3 = BeautifulSoup(session_.get(root_url + page_link).content, 'html.parser')
                for c_post in soup3.find_all(class_="post"):
                    poster = c_post.find(class_="postprofile-name").findChild().contents[0]
                    post_content = c_post.find(class_="content").findChild().text
                    if c_post.find(class_="vote-bar-desc") is not None:
                        post_rep = c_post.find(class_="vote-bar-desc").text
                    else:
                        post_rep = None
                    try:
                        post_date = c_post.find(class_="topic-date").text[3:11] + "20"
                        post_time = c_post.find(class_="topic-date").text[12:17]
                    except IndexError:
                        post_date = None
                        post_time = None
                    cp = ForumDateModel.Post(poster, post_content, post_date, post_time, post_rep)
                    theard.add_post(cp)

        main_forum.add_subforum(sub_forum)
    # for subforum in main_forum.subforum:
    #     for theard in subforum.list_of_theard:
    #         theard.text_form()
    #         for post in theard.list_of_post:
    #             print(str(post))

    forum_backup = _pb2.Forum()
    for subforum in main_forum.subforum:
        s = forum_backup.Sb.add()
        for theard in subforum.list_of_theard:
            th = s.theards.add()
            th.title = str(theard.title)
            th.author = str(theard.author)
            th.views = int(theard.views)
            th.replies = int(theard.replies)
            th.link = str(theard.link)
            th.hot = theard.is_hot
            th.lock = theard.locked
            th.recent_date = str(theard.recent_date)
            th.last_poster = str(theard.last_poster)
            for post in theard.list_of_post:
                ps = th.posts.add()
                ps.author = str(post.author)
                ps.content = str(post.content)
                ps.publication_date = str(post.date)
                ps.publication_time = str(post.time)
                ps.reputation = str(post.post_reputation)
    with open("backup", mode="wb+") as backup:
        backup.write(forum_backup.SerializeToString())
