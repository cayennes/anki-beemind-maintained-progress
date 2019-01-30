import datetime
from anki import hooks, sync
from aqt import qt, mw, utils
from . import beeminder


projection_comment = "PESSIMISTIC PROJECTION (update from anki after doing reviews)"

day_in_seconds = 24 * 60 * 60


def get_maintained_progress(col, projection_days, search_filter):
    search_string = ("-is:suspended -is:new -is:due -is:buried -prop:due<=%s %s"
                     % (projection_days, search_filter))
    return len(col.findCards(search_string))


def datestamp_in_days(col, days):
    """Returns a string representing the date in a number of days

    Uses anki's notion of what day it is, taking the day start preference into account"""
    # this is based on code in anki preferences. number of hours past midnight.
    rollover = col.conf.get("rollover", datetime.datetime.fromtimestamp(col.crt).hour)
    if datetime.datetime.now().hour >= rollover:
        today = datetime.date.today()
    else:
        today = datetime.date.today() - datetime.timedelta(1)
    the_day = today + datetime.timedelta(days)
    return str(the_day)


def update(col, show_info=False):
    config = mw.addonManager.getConfig(__name__)
    auth_token = config["auth_token"]
    days_ahead = config["pessemistic_reports"]["days_ahead"]

    for goal in config["goals"]:
        goal_slug = goal["beeminder_slug"]
        search_filter = goal.get("filter", "")

        datapoints = [beeminder.as_datapoint(get_maintained_progress(col, day, search_filter),
                                             datestamp_in_days(col, day),
                                             "" if day == 0 else projection_comment)
                      for day in range(days_ahead+1)]

        beeminder_result = beeminder.add_datapoints(auth_token,
                                                    goal_slug,
                                                    datapoints)

        if show_info:
            if beeminder_result["success?"]:
                filter_string = " in " + search_filter if search_filter else ""
                info_string = ("Updated beeminder goal %s "
                               "with %s cards of maintained progress"
                               "%s" %
                               (goal_slug, datapoints[0]["value"], filter_string))
            else:
                info_string = ("There was a problem updating beeminder:\n\n"
                            + beeminder_result["error_message"])

            utils.showInfo(info_string)


def menu_update():
    update(mw.col, True)


# menu item
update_action = qt.QAction("Update Beeminder", mw)
update_action.triggered.connect(menu_update)
mw.form.menuTools.addAction(update_action)


# optionally update after syncing or doing reviews
def should_update(config_key):
    config = mw.addonManager.getConfig(__name__)
    return config["update_after"][config_key]


def on_review_cleanup():
    if should_update("finishing_reviews"):
        update(mw.col)


hooks.addHook("reviewCleanup", on_review_cleanup)


orig_sync = sync.Syncer.sync


def new_sync(self):
    ret = orig_sync(self)
    if should_update("syncing"):
        update(self.col)
    return ret


sync.Syncer.sync = new_sync

