import requests

api_url = "https://www.beeminder.com/api/v1/"

def add_datapoint(auth_token, slug, value):
    url = api_url + "users/me/goals/" + slug + "/datapoints.json"
    res = requests.post(url, data={"value": value,
                                   "auth_token": auth_token})
    if res.status_code == 200:
        return {"success?": True}
    else:
        return {"success?": False,
                "error_message": ("Goal: %s\nStatus: %s\nResponse: %s" %
                                  (slug, res.status_code, res.text))}
