from aqt import qt, mw, utils

def update():
    utils.showInfo("This addon does't do anything yet")

update_action = qt.QAction("Update Beeminder", mw)
update_action.triggered.connect(update)
mw.form.menuTools.addAction(update_action)
