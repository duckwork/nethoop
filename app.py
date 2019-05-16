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
    go = url_for("hoop_random")

    if request.referrer:
        referrer = request.referrer
    else:
        referrer = request.args.get("from", default="example.com")

    members = get_members()
    try:
        go = incUrl(referrer, members)
        return redirect(go)
    except NotAMemberError:
        pass

    return redirect(go)


@app.route("/prev")
def hoop_prev():
    go = url_for("hoop_random")

    if request.referrer:
        referrer = request.referrer
    else:
        referrer = request.args.get("from", default="example.com")

    members = get_members()
    try:
        go = incUrl(referrer, members, -1, -1)
        return redirect(go)
    except NotAMemberError:
        pass

    return redirect(go)


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
        if url == u.netloc:
            try:
                return lst[i + dir]["href"]
            except IndexError:
                return lst[defi]["href"]

    raise NotAMemberError


if __name__ == "__main__":
    app.run()
