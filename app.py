import json
from random import choice
from urllib.parse import urlparse

from flask import Flask, make_response, redirect, render_template, request, url_for
from yaml import safe_load

app = Flask(__name__)

VARS = {
    "keywords": "webring, writing, fediverse",
    "description": "A webring for creative people",
    "title": "Writers of the Fediverse!",
    "version": "0.0.3",
}


class NotAMemberError(Exception):
    pass


@app.route("/")
def root():
    return render_template("index.html", members=get_members(), **VARS)


@app.route("/feeds.xml")
def feeds_xml():
    response = make_response(
        render_template("feeds.xml", members=get_members(), **VARS)
    )
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route("/next")
def hoop_next():
    return hoop_inc(request)


@app.route("/prev")
def hoop_prev():
    return hoop_inc(request, -1, -1)


@app.route("/random")
def hoop_random():
    go = randomUrl(get_members(), request.referrer)
    return redirect(go)


@app.route("/members")
def hoop_members():
    members = get_members()
    response = make_response(json.dumps(members))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/code-of-content")
def code_of_content():
    return render_template("code-of-content.html", **VARS)


def get_members():
    with open("data/members.yaml") as f:
        members = safe_load(f)
    return members


def randomUrl(lst, url=None):
    u = urlparse(choice(lst)["href"])
    if url is not None:
        while u.netloc == urlparse(url).netloc:
            u = urlparse(choice(lst)["href"])

    return u.geturl()


def incUrl(url, lst, dir=1, defi=0):
    url = urlparse(url)
    if url.netloc == "":
        url = url.path
    else:
        url = url.netloc

    for i, member in enumerate(lst):
        u = urlparse(member["href"])
        if url == u.netloc or url == u.netloc + u.path:
            try:
                ret = lst[i + dir]["href"]
            except IndexError:
                ret = lst[defi]["href"]

            print(ret)
            return ret

    raise NotAMemberError


def hoop_inc(req, dir=1, defi=0):
    go = url_for("hoop_random")

    ref = request.args.get("from", default=req.referrer or "example.com")

    members = get_members()
    try:
        go = incUrl(ref, members, dir, defi)
        return redirect(go)
    except NotAMemberError:
        pass

    return redirect(go)


if __name__ == "__main__":
    app.run()
