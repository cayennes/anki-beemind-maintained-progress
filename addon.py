from anki import hooks, sync
from aqt import qt, mw, utils
from . import beeminder

def get_maintained_progress(col):
    caught_up = col.findCards("-is:suspended -is:new -is:due -is:buried")
    return len(caught_up)

def update(col, show_info=False):
    config = mw.addonManager.getConfig(__name__)
    auth_token = config["auth_token"]
    goal_slug = config["goal"]["slug"]

    maintained_progress = get_maintained_progress(col)

    beeminder_result = beeminder.add_datapoint(auth_token,
                                               goal_slug,
                                               maintained_progress)

    if show_info:
        if beeminder_result["success?"]:
            info_string = ("Updated beeminder goal %s "
                        "with %s cards of maintained progress" %
                        (goal_slug, maintained_progress))
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

