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
    if request.referrer:
        members = get_members()
        try:
            go = nextUrl(request.referrer, members)
            return redirect(go)
        except NotAMemberError:
            go = url_for("hoop_random")
            return redirect(go)


@app.route("/prev")
def hoop_prev():
    if request.referrer:
        members = get_members()
        try:
            go = prevUrl(request.referrer, members)
            return redirect(go)
        except NotAMemberError:
            go = url_for("hoop_random")
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


def nextUrl(url, lst):
    for i, member in enumerate(lst):
        u = urlparse(member["href"])
        if urlparse(url).netloc == u.netloc:
            try:
                return lst[i + 1]["href"]
            except IndexError:
                return lst[0]["href"]

    raise NotAMemberError


def prevUrl(url, lst):
    for i, member in enumerate(lst):
        u = urlparse(member["href"])
        if urlparse(url).netloc == u.netloc:
            try:
                return lst[i - 1]["href"]
            except IndexError:
                return lst[-1]["href"]

    raise NotAMemberError


if __name__ == "__main__":
    app.run()
