import datetime

from aqt import gui_hooks, mw, qt, utils

from . import beeminder

placeholder_slug = "PUT_YOUR_BEEMINDER_GOAL_SHORT_NAME_HERE"


day_in_seconds = 24 * 60 * 60


# when errors occur during the sync during loading, we need to queue them to
# display once it is possible
mw_loaded = False
queued_errors = []


# manage the goals


# these things are checked the first time that a goal is updated each time anki
# is launched both because it is quicker to implement this way than storing it
# persistently, and we do want to recheck every so often for the unlikely case
# that it has changed.
checked_goals = {}


def check_goals():
    valid_goals = []
    invalid_goals = []
    config = mw.addonManager.getConfig(__name__)
    for config_goal in config["goals"]:
        goal = config_goal.copy()
        goal_slug = goal["beeminder_slug"]
        if goal_slug not in checked_goals:
            if goal["beeminder_slug"] == placeholder_slug:
                pass
            elif beeminder.doesnt_autosum(config["auth_token"], goal_slug):
                res = beeminder.configure_api_goal(config["auth_token"], goal_slug)
                if res["success?"]:
                    valid_goals.append(goal)
                else:
                    goal["error"] = "Error configuring goal on beeminder: " + res["error_message"] + ". If you think this is resolved, restart anki and try again."
                    invalid_goals.append(goal)
            else:
                goal["error"] = "This goal autosums data, which is not compatible with the data this addon produces. Create an odometer type goal."
                invalid_goals.append(goal)
            checked_goals["goal_slug"] = goal
        elif checked_goals[goal_slug]:
            valid_goals.append(goal)
        else:
            checked_goal = checked_goals[goal_slug]
            if "error" in checked_goals:
                invalid_goals.append(checked_goal)
            else:
                valid_goals.append(checked_goal)

    return {"valid": valid_goals, "invalid": invalid_goals}


# update the goal


def get_maintained_progress(col, projection_days, search_filter):
    search_string = ("-is:suspended -is:new -is:due -prop:due<=%s %s"
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
    days_ahead = config.get("pessimistic_reports", {}).get("days_ahead", 0)

    def projection_comment(day):
        if day == 0:
            return ""
        else:
            return "{}-day PESSIMISTIC PROJECTION (will be updated by anki addon)".format(day)

    goals = check_goals()

    for goal in goals["invalid"]:
        info_string = ("Can't update goal %s: %s" % (goal["beeminder_slug"], goal["error"]))
        if mw_loaded:
            utils.showInfo(info_string)
        else:
            queued_errors.append(info_string)

    for goal in goals["valid"]:
        goal_slug = goal["beeminder_slug"]
        search_filter = goal.get("filter", "")

        datapoints = [beeminder.as_datapoint(get_maintained_progress(col, day, search_filter),
                                             datestamp_in_days(col, day),
                                             projection_comment(day))
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


# deal with displaying queued errors after we have a mw


def on_profile_loaded():
    while queued_errors:
        msg = queued_errors.pop(0)
        utils.showInfo(msg)
    mw_loaded = True

gui_hooks.profile_did_open.append(on_profile_loaded)


# menu item

def menu_update():
    update(mw.col, True)


# Create a shortcut for updating Beeminder
shortcut = "Ctrl+Shift+B"  # Qt will automatically map Ctrl to Cmd on macOS
update_action = qt.QAction("Update Beeminder", mw)
update_action.setShortcut(qt.QKeySequence(shortcut))
update_action.triggered.connect(menu_update)
mw.form.menuTools.addAction(update_action)


# optionally update after syncing or doing reviews
def should_update(config_key):
    config = mw.addonManager.getConfig(__name__)
    return config["update_after"].get(config_key, False)


def on_review_cleanup():
    if should_update("finishing_reviews"):
        update(mw.col)

gui_hooks.reviewer_will_end.append(on_review_cleanup)


def on_sync_did_finish():
    if should_update("syncing"):
        update(mw.col)

gui_hooks.sync_did_finish.append(on_sync_did_finish)
