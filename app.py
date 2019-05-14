from urllib.parse import urlparse

from flask import Flask, make_response, redirect, render_template, request
from yaml import safe_load

app = Flask(__name__)

VARS = {"title": "Writers of the Fediverse!", "version": "0.0.3"}


class NotAMemberError(Exception):
    pass


@app.route("/")
def root():
    return render_template("index.html", members=hoop_members(), **VARS)


@app.route("/feeds.xml")
def feeds_xml():
    response = make_response(
        render_template("feeds.xml", members=hoop_members(), **VARS)
    )
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route("/next")
def hoop_next():
    if request.referrer:
        members = hoop_members()
        try:
            return redirect(nextUrl(request.referrer, members))
        except NotAMemberError:
            return "Not a member!"


@app.route("/prev")
def hoop_prev():
    if request.referrer:
        members = hoop_members()
        try:
            return redirect(prevUrl(request.referrer, members))
        except NotAMemberError:
            return "Not a member!"


def hoop_members():
    with open("data/members.yaml") as f:
        members = safe_load(f)
    return members


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
