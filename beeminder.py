import json
import requests


api_url = "https://www.beeminder.com/api/v1/"


def _result_dict(res):
    if res.status_code == 200:
        return {"success?": True}
    else:
        return {"success?": False,
                "error_message": ("Status: %s\nResponse: %s" %
                                  (res.status_code, res.text))}


def add_datapoint(auth_token, slug, value):
    url = api_url + "users/me/goals/" + slug + "/datapoints.json"
    res = requests.post(url, data={"value": value,
                                   "auth_token": auth_token})
    return _result_dict(res)


def as_datapoint(value, date, comment=None):
    if comment is None:
        comment = ""
    return {"value": value,
            "daystamp": date,
            "comment": comment,
            "requestid": date}


def add_datapoints(auth_token, goal_slug, datapoints):
    """post a list of datapoints to beeminder

    each datapoint is a map containing
    * "daystamp" a string representing the date
    * "value"
    * "comment"
    * optional "requestid"
    """
    url = api_url + "users/me/goals/" + goal_slug + "/datapoints/create_all.json"
    res = requests.post(url, data={"datapoints": json.dumps(datapoints),
                                   "auth_token": auth_token})
    return _result_dict(res)


def get_goal_details(auth_token, goal_name):
    url = api_url + "users/me/goals/" + goal_name + ".json"
    params = {"auth_token": auth_token}
    res = requests.get(url, params=params)
    return res.json()


def doesnt_autosum(auth_token, goal_name):
    goal_details = get_goal_details(auth_token, goal_name)
    return goal_details["kyoom"] == False


def modify_goal(auth_token, goal_name, new_attributes):
    url = api_url + "users/me/goals/" + goal_name + ".json"
    data = new_attributes
    data["auth_token"] = auth_token
    res = requests.put(url, data=data)
    return _result_dict(res)


def configure_api_goal(auth_token, goal_name):
    """sets odom to False and datasource to API

    This is what we want because this is an API source and zeroes are zeroes, not odometer resets."""
    return modify_goal(auth_token, goal_name, {"odom": False, "datasource": "api"})
