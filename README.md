# Anki addon: beemind maintained progress

This is an [anki](https://apps.ankiweb.net/) addon to track maintained progress with [beeminder](https://www.beeminder.com).

The number tracked is the number of cards that you have started studying and are caught up on reviewing; that is, they are not currently due. This number encapsulates both adding new things and staying on top of reviewing. This is the number that represents real progress; if you only track the number you've started, then when you fall behind on reviewing your number stays high but you might have actually forgotten everything and not made any true progress. This number is also useful when you're trying to work down a backlog of due items, since it's measuring the increase in caught up cards. Using this allows some flexibility without sacrificing overall progress.

Your beeminder goal should be set to the number of new cards you want add on average to create a maintainable number of reviews per day, though you might want to temporarily start out with it higher if you are starting to beemind anki at a time when you have a large backlog of due cards. If you do not want to need to absolutely study every day, you can set your number of new cards to something higher in anki, get a bit ahead, and not need to do all your reviews and new cards every day - and if you get behind beeminder will guide you to catch up gradually, unlike the overwhelming amount of due cards situation that happen when you fall behind without beeminder.

Features:
* Supports multiple goals, each tracking cards filtered by deck, tag, card type, note type, or anything else you can express as a search
* It can post precise pessimistic reports so that if you don't sync one day beeminder will have the number that it should have if you didn't do any reviewing
* Updates beeminder after syncing or exiting reviews (both of these are optional but on by default) or manually with a menu item

How to use it:
1. Make an odometer goal on beeminder (requires an infinibe plan)
2. Go to the addon config (tools menu -> addons -> select this addon -> config button) and read the instructions there to set it up

This addon on AnkiWeb: https://ankiweb.net/shared/info/1928083890

Install code: 1928083890
