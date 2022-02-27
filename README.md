# Anki addon: beemind maintained progress

## Quickstart

### Requirements

* An [Anki](https://apps.ankiweb.net/) installation.
* A [Beeminder](https://www.beeminder.com/).

### Setup

0. Open Anki, and go to `Tools -> Add-ons (Ctrl+Shift+A)`.
0. Add "Beemind maintaned progress" to Anki with install code `1928083890`.
0. Restart Anki.
0. Go back to `Tools -> Add-ons (Ctrl+Shift+A)`, select the add-on `Beemind maintained progress`, and hit the `Config` button on the left side. You should see JSON that looks roughly like this.
    ```json
    {
        "auth_token": "PUT_YOUR_BEEMINDER_AUTH_TOKEN_HERE",
        "goals": [
            {
                "beeminder_slug": "PUT_YOUR_BEEMINDER_GOAL_SHORT_NAME_HERE"
            }
        ],
        "pessimistic_reports": {
            "days_ahead": 0
        },
        "update_after": {
            "finishing_reviews": true,
            "syncing": true
        }
    }
    ```
    You will be editing this by hand to get synchronization working, so leave it open.
0. First we need the `auth_token`.
  0. Go to your [Beeminder account settings](https://www.beeminder.com/settings/account); under "Apps & API" you should be able to find a "Personal Auth Token".
  0. Copy and paste this into the "auth_token" field in the Anki `Config` JSON.
0. Now we need a `beeminder_slug` to actually send the data to.
  0. [Create an "Odometer" goal in Beeminder](https://www.beeminder.com/new) (**not** a "Do More") with a descriptive `goal_name` such as `anki_rotestock` or `anki_maintained_progress`.
    * Beeminder lets you immediately delete goals in their first week under the "Stop/Pause" tab. Remember you can do this and start over easily if you make a mistake.
    * If this is your first time messing with the APIs and auth tokens directly, consider checking "Start this goal with extra leeway" as well.
  0. Copy and paste the `goal_name` into the "beeminder_slug" field in the Anki `Config` JSON.

### Testing

0. Open your Beeminder goal and go to the "Data" tab.
0. Open Anki.
0. Review a few cards.
0. Leave reviewing; do an Anki sync if possible.
0. Refresh the Beeminder page on the "Data" tab.
0. If a new line has been added, congratulations - it's working!

## Information

This is an [anki](https://apps.ankiweb.net/) addon to track maintained progress with [beeminder](https://www.beeminder.com).

Specifically it tracks _rotestock_: the number of cards that you have started studying and are caught up on reviewing; that is, they are not currently due. This number encapsulates both adding new things and staying on top of reviewing. This is the number that represents real progress; if you only track the number you've started, then when you fall behind on reviewing your number stays high but you might have actually forgotten everything and not made any true progress. This number is also useful when you're trying to work down a backlog of due items, since it's measuring the increase in caught up cards. Using this allows some flexibility without sacrificing overall progress.

Your beeminder goal should be set to the number of new cards you want add on average to create a maintainable number of reviews per day, though you might want to temporarily start out with it higher if you are starting to beemind anki at a time when you have a large backlog of due cards. If you do not want to need to absolutely study every day, you can set your number of new cards to something higher in anki, get a bit ahead, and not need to do all your reviews and new cards every day - and if you get behind beeminder will guide you to catch up gradually, unlike the overwhelming amount of due cards situation that happen when you fall behind without beeminder.

Warning: if you want to take a break, you need to schedule a negative slope equal to at least as many cards become due.

Features:
* Supports multiple goals, each tracking cards filtered by deck, tag, card type, note type, or anything else you can express as a search
* It can post precise pessimistic reports so that if you don't sync one day beeminder will have the number that it should have if you didn't do any reviewing
* Updates beeminder after syncing or exiting reviews (both of these are optional but on by default) or manually with a menu item

How to use it:
1. Make an odometer goal on beeminder (requires an infinibee plan)
2. Go to the addon config (tools menu -> addons -> select this addon -> config button) and read the instructions there to set it up

This addon on AnkiWeb: https://ankiweb.net/shared/info/1928083890

Install code: `1928083890`

# License and Copyright

This addon is available under the GNU Affero General Public License, the same as Anki.

Copyright Cayenne Geis 2019
