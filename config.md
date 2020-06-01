`auth_token`: Your beeminder auth token. You can find it in the "Apps and API" tab of your account settings on beeminder.

`goals`: Your beeminder goals. Goals can track maintained progress of your whole collection, or you can filter by deck, tag, note type, or anything else that you can search for. Examples:

Just one goal for your whole collection:

    {"auth_token": "tHis1sAf4keT0ken",
     "goals": [{"beeminder_slug": "anki-maintained-progress"}]}

Several goals, for different things:

    {"auth_token": "tHis1sAf4keT0ken",
     "goals": [{"beeminder_slug": "japanese-maintained-progress",
                "filter": "deck:Japanese"},
               {"beeminder_slug": "n4-maintained-progress",
                "filter": "tag:n4"},
               {"beeminder_slug": "kanji-maintained-progress",
                "filter": "card:kanji"}]}

`update_after`: Indicate whether or not you want the addon to update beeminder after syncing and/or finishing reviews.

    {"auth_token": "tHis1sAf4keT0ken",
     "goals": [{"beeminder_slug": "anki-maintained-progress"}],
     "update_after": {"syncing": true,
                      "finishing_reviews": true}}

`pessimistic_reports`: If this is set to a number greater than 0, the addon will post pessimistic predictions for future days, so the goal will default to what your numbers would be if you don't do any reviews. The addon will automatically update these. The `days_ahead` value will indicate how many days of pessimistic reports to post.

This will produce pessimistic reports for the 14 days that a beeminder graph shows ahead:

    {"auth_token": "tHis1sAf4keT0ken",
     "goals": [{"beeminder_slug": "anki-maintained-progress"}],
     "pessimistic_reports": {"days_ahead": 14}}
     
This will turn them off:

    {"auth_token": "tHis1sAf4keT0ken",
     "goals": [{"beeminder_slug": "anki-maintained-progress"}]
     "pessimistic_reports": {"days_ahead": 0}}
