import requests

def getWhoThisUserFollows(userid):
    # HTTP Endpoint to request from twitter API
    url = "https://api.twitter.com/2/users/{}/following".format(userid)
    payload={}
    headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMquWwEAAAAArG%2BMVN%2BizU8VfbZHFxl7KFxgWIo%3D0wmW4dzYlxcbUJnDBYk2DN09Xfj8xWM41LHqasRvGtPs3LRQTM',
    'Cookie': 'guest_id_marketing=v1%3A163939297214435099; guest_id_ads=v1%3A163939297214435099; guest_id=v1%3A163939297214435099; personalization_id="v1_G9Xf/PuwcHMS9OJsngFHpg=="'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    resp = response.json()["data"]
    collection = []
    for user in resp:
        collection.append(user["username"])
    return collection

def getUserID(username):
    url = "https://api.twitter.com/2/users/by/username/{}".format(username)

    payload={}
    headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMquWwEAAAAArG%2BMVN%2BizU8VfbZHFxl7KFxgWIo%3D0wmW4dzYlxcbUJnDBYk2DN09Xfj8xWM41LHqasRvGtPs3LRQTM',
    'Cookie': 'guest_id_marketing=v1%3A163939297214435099; guest_id_ads=v1%3A163939297214435099; guest_id=v1%3A163939297214435099; personalization_id="v1_G9Xf/PuwcHMS9OJsngFHpg=="'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["data"]["id"]