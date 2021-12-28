import functools
import os
from secrets import token_urlsafe

import hikari
import verox
from quart import Quart, redirect, request, session, url_for

from dashboard.http import *

app = Quart(__name__)
app.secret_key = os.environ["APP_SECRET"]
client = verox.Client(os.environ["APP_SECRET"])
rest = hikari.RESTApp()


@app.route("/")
async def home() -> str:
    if not session.get("token"):
        session["state"] = token_urlsafe(20)
        return redirect(url_for("login"))

    async with rest.acquire(session["token"]) as rest_client:
        guilds = await rest_client.fetch_my_guilds()

    bot_guilds = await client.request("get_guild_ids")

    guilds = [
        g.name
        for g in guilds
        if g.my_permissions & hikari.Permissions.MANAGE_GUILD and g.id in bot_guilds
    ]

    return "\n".join(guilds)


@app.route("/login")
async def login():
    redirect_url = get_redirect_url(state=session["state"])

    return redirect(redirect_url)


@app.route("/callback")
async def callback():
    state = request.args.get("state")
    code = request.args.get("code")
    if state != session["state"]:
        return "Authorization failed", 403

    token = await get_user_token(code=code)

    session["token"] = token

    return redirect(url_for("home"))


def run():
    app.run(debug=True)
