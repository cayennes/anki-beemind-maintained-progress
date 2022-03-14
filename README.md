# Anki addon: beemind maintained progress

## Quickstart

### Requirements

* An [Anki](https://apps.ankiweb.net/) installation.
* A [Beeminder](https://www.beeminder.com/) account. (You do _not_, as of February 2022, need an Infinibee account; the free one will work fine.

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

This is an [Anki](https://apps.ankiweb.net/) addon to track maintained progress with [Beeminder](https://www.beeminder.com).

Specifically it tracks [_rotestock_](https://forum.beeminder.com/t/anki-addon-maintained-progress/5062/26), the number of cards in the database right now that are *not* currently in `New`, `Due` or `Learning`.

So:
- If a card you've never seen before is in the leftmost `New` column on the Anki start screen, and you have never reviewed it before, it is _not_ in your rotestock.
- If you review the card, but not enough to move it out of the middle `Learning` column, it is still _not_ in your rotestock.
- If the card is in the left `Due` column, it has _fallen out_ of your rotestock, and you need to review it again to add it back in.
- If you review the card enough that it is in _none_ of the 3 columns, then it **is** in your rotestock. It has been reviewed recently enough that you're not being prompted to review it again today.

Simply put: If Anki won't show you the card without you studying ahead, it counts. If it's a bit confusing now, try it for a few days - it will make much more sense with practice.

## Why rotestock? Why not just reviews per day?

Simply put, it's a better metric.

Tracking reviews per day is easier to understand, but rotestock gives a bonus of sorts to mature cards. If you review a mature card that won't be due again for another 4 months, it will stay in rotestock for 4 months. Compare this to reviewing a new card which will show up tomorrow - it will only be added to the rotestock odometer for today, but then tomorrow, you'll have to review it again to re-add it to the rotestock count.

Rotestock is therefore especially useful when you're trying to work down a backlog of due items. If you fall off Anki reviews for a few weeks, install this, and then start to work through the dumptruck of mature cards that collected during that time, the rotestock card count will decrease far slower over time than if you were doing all new cards.

Rotestock is better for what you're actually trying to _do_ with SRS: create durable, long-term memory by using active recall and the spacing effect.

## Why does it have to be an Odometer goal, not a Do More goal?

An Odometer goal is similar to a Do More goal with one difference: You send the _total_ to Beeminder, rather than _today's difference_. A Do More goal with datapoints `100, 100, 100, 100, 100` starting from `0` produces the same kind of graph as an Odometer goal starting from `0` with datapoints `100, 200, 300, 400, 500`.

Simply put, this is an Odometer goal because _cards can both fall into and out of rotestock_. It's much more straightforward to just count up however many cards are currently in rotestock and send that to Beeminder. You're just trying to count the number of cards in the database right now that are not currently in `New`, `Due` or `Learning`.

## What should my Beeminder goal be?

There are a few ways to decide on this.

If you want a braindead approach - start with 50. Add 10% at the end of the week if you want more. Subtract 10% if you want less.

If you want to think more long-term - your Beeminder goal should be set to the number of _new_ cards you want to review on average to create a _maintainable_ number of reviews per day, though you might want to temporarily start out with it higher if you are starting to beemind anki at a time when you have a large backlog of due cards. (So, if you want to get into the swing of adding and reviewing 100 new cards a day per day - try 100.)

If you do not want to need to absolutely study every day - set your number of new cards to something higher in Anki, get a bit ahead, and then you won't need to do all your reviews and new cards every day. If you get behind, your rotestock will only gradually fall, and Beeminder will guide you to catch up gradually, unlike the overwhelming amount of due cards situation that happen when you fall behind without Beeminder.

Warning: if you want to take a break, you need to schedule a negative slope equal to at least as many cards become due.

## Features

* Supports multiple goals, each tracking cards filtered by deck, tag, card type, note type, or anything else you can express as a search in Anki.
* It can post precise pessimistic reports so that if you don't sync one day beeminder will have the number that it should have if you didn't do any reviewing. (Another benefit of an Odometer goal - this is easier to guess!)
* Updates Beeminder after syncing or exiting reviews (both of these are optional but on by default) or manually with a menu item

How to use it:
1. Make an odometer goal on beeminder (requires an infinibee plan)
2. Go to the addon config (tools menu -> addons -> select this addon -> config button) and read the instructions there to set it up

This addon on AnkiWeb: https://ankiweb.net/shared/info/1928083890

Install code: `1928083890`

# License and Copyright

This addon is available under the GNU Affero General Public License, the same as Anki.

Copyright Cayenne Geis 2019
