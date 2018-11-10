import time
from anki import hooks, sync
from aqt import qt, mw, utils
from . import beeminder


projection_comment = "PESSIMISTIC PROJECTION (update from anki after doing reviews)"

day_in_seconds = 24 * 60 * 60


def get_maintained_progress(col, projection_days=0):
    search_string = ("-is:suspended -is:new -is:buried -prop:due<=%s"
                     % projection_days)
    return len(col.findCards(search_string))


def time_after_days(days):
    return time.time() + days * day_in_seconds


def update(col, show_info=False):
    config = mw.addonManager.getConfig(__name__)
    auth_token = config["auth_token"]
    goal_slug = config["goal"]["slug"]
    days_ahead = config["pessemistic_reports"]["days_ahead"]

    datapoints = [beeminder.as_datapoint(get_maintained_progress(col, day),
                                         time_after_days(day),
                                         "" if day == 0 else projection_comment)
                  for day in range(days_ahead+1)]

    beeminder_result = beeminder.add_datapoints(auth_token,
                                                goal_slug,
                                                datapoints)

    if show_info:
        if beeminder_result["success?"]:
            info_string = ("Updated beeminder goal %s "
                        "with %s cards of maintained progress" %
                        (goal_slug, datapoints[0]["value"]))
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

