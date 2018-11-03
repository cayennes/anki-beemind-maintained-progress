from aqt import qt, mw, utils

def get_maintained_progress():
    return len(mw.col.findCards("-is:suspended -is:new -is:due -is:buried"))

def update():
    info_string = ("This addon doesn't connect to beeminder yet.\n\n"
                   "Your maintained progress is %s") % get_maintained_progress()
    utils.showInfo(info_string)

update_action = qt.QAction("Update Beeminder", mw)
update_action.triggered.connect(update)
mw.form.menuTools.addAction(update_action)
