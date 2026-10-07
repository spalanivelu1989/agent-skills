"""Scenes for this demo video — one function per "app" scene in scenes.json, same id.

Each function: set up the page, call mark() when the content to show is on
screen (the voice starts a moment later), then at("<cue phrase>") before each
action so it happens as the narration reaches those words.

Rules: find things by their visible text (point / reveal / find), not by pixels;
navigation clicks only — never click save, submit, accept, approve, delete or
anything that changes data. Hover over such buttons instead.
"""
import os

from demo import *  # noqa: F401,F403  hold, settle, glide, click, wheel, tab, still, find, reveal, point, hover_text, W, H

BASE_URL = os.environ.get("DEMO_URL", "http://localhost:3000")


def login(pg):
    """Sign in once; the recorder reuses the session for every scene. Delete the body if there is no login."""
    pg.goto(BASE_URL)
    settle(pg)
    # pg.fill("#username", os.environ["DEMO_USERNAME"])
    # pg.fill("#password", os.environ["DEMO_PASSWORD"])
    # pg.click('button:has-text("Sign in")')
    # pg.wait_for_url("**/dashboard")   # a URL only the signed-in app has: a loose pattern such as
    #                                    # r".*/demo.*" also matches the login page's "?next=/demo"


def s01_overview(pg, mark, at):
    pg.goto(BASE_URL + "/dashboard")
    settle(pg)
    mark()
    still(pg, "s01_overview")
    at("Revenue is up")
    point(pg, "Revenue")
    at("Below them")
    reveal(pg, "Trend")
    point(pg, "Trend", dy=120)


def s02_detail(pg, mark, at):
    pg.goto(BASE_URL + "/orders")
    settle(pg)
    mark()
    click(pg, pg.locator("table tbody tr").first)
    at("The detail panel")
    point(pg, "Customer", min_x=W * 0.6)          # min_x targets the right-hand panel
    at("why it was flagged")
    reveal(pg, "Flags", min_x=W * 0.6)
    point(pg, "Flags", min_x=W * 0.6)
