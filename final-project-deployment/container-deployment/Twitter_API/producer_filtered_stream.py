import requests
import os
import json
from kafka import KafkaProducer

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMquWwEAAAAArG%2BMVN%2BizU8VfbZHFxl7KFxgWIo%3D0wmW4dzYlxcbUJnDBYk2DN09Xfj8xWM41LHqasRvGtPs3LRQTM"
producer = KafkaProducer (bootstrap_servers="129.114.25.83:30000", value_serializer=lambda v: v.encode('utf-8'))

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


def set_rules(delete):
    import search_converter
    sample_rules = []
    for rule in search_converter.convertToRule():
        sample_rules.append({"value": rule, "tag": "in followers"})
    sample_rules.append({"value": "stock OR stocks", "tag": "sample words"})

    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:

            json_response = json.loads(response_line)
            textonly = json_response["data"]["text"]
            dict = {'text' : json_response["data"]["text"]}
            json_dict = json.dumps(dict)
            producer.send('tweetdata', textonly)
            print(json_dict)
            producer.flush ()



def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)
    producer.close()


if __name__ == "__main__":
    main()