from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os


import ForumDateModel


def pr(form: ForumDateModel.Theard):
    return form.text_form()


load_dotenv()
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
root_url = "https://hoffpolitics.forumpolish.com"
form = {"username": login, "password": password, "autologin": "on", "redirect": '', "query": '', "login": "Zaloguj"}
with  requests.Session() as s:
    req = s.post("https://hoffpolitics.forumpolish.com/login", data=form)
    #   print(req.content)
    res = s.get(root_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    main_forum = ForumDateModel.Forum()
    n = None
    for forum_ in soup.find_all("a", class_="forumtitle"):
        n = ForumDateModel.SubForum()
        s1 = BeautifulSoup(s.get(root_url + forum_['href']).content, 'html.parser')
        for row_ in s1.find_all(class_="row"):
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
                        n.add_theard(theard_to_add)
        for th in n.list_of_theard:
            s2 = BeautifulSoup(s.get(root_url+ th.link).content, 'html.parser')
            pages =list(set([x.parent.contents[3]['href'] for x in s2.find_all(class_ = "page-sep")]))
            pages.insert(0,th.link)
            for page_link in pages:
                s3 = BeautifulSoup(s.get(root_url + page_link).content, 'html.parser')
                for c_post in s3.find_all(class_="post"):
                    poster = c_post.find(class_="postprofile-name").findChild().contents[0]
                    post_content =c_post.find(class_="content").findChild().text
                    if c_post.find(class_="vote-bar-desc") is not None:
                        post_rep = c_post.find(class_="vote-bar-desc").text
                    else:
                        post_rep = None
                    try:
                        post_date = c_post.find(class_="topic-date").text[3:11]+"20"
                        post_time = c_post.find(class_="topic-date").text[12:17]
                    except IndexError:
                        post_date = None
                        post_time = None
                    cp = ForumDateModel.Post(poster,post_content,post_date,post_time,post_rep)
                    th.add_post(cp)

        main_forum.add_subforum(n)
    for sub in main_forum.subforum:
        for th in sub.list_of_theard:
            th.text_form()
            for ps in th.list_of_post:
                print(str(ps))
