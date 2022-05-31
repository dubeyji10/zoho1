#!/usr/bin/env python3

import json
import sys
import requests


def get_secrets():
    j = json.loads(open("secrets.json").read())
    return (j["client_id"], j["client_secret"])


def request_auth(code):
    base_accounts_url = "accounts.zoho.com"
    client_id, client_secret = get_secrets()
    url = f"https://{base_accounts_url}/oauth/v2/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&access_type=offline"

    resp = requests.post(url)
    return resp.json()


def refresh_auth(auth):
    base_accounts_url = "accounts.zoho.com"
    client_id, client_secret = get_secrets()
    refresh_token = auth["refresh_token"]
    url = f"https://{base_accounts_url}/oauth/v2/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&access_type=offline"

    resp = requests.post(url)
    resp_j = resp.json()
    resp_j["refresh_token"] = refresh_token
    return resp_j


def read_report(auth, path):
    token = auth["access_token"]

    url = f"https://creator.zoho.com/api/v2/USER/APP/report/{path}"
    headers = { "Authorization":  f"Zoho-oauthtoken {token}" }

    resp = requests.get(url, headers=headers)
    resp_j = resp.json()

    return resp_j


if __name__ == "__main__":

    # if new code on cmd line, generate auth
    if len(sys.argv) > 1:
        auth = request_auth(sys.argv[1])
        if auth is not None and "access_token" in auth:
            open("auth.json", "w").write(json.dumps(auth))

    # get saved auth
    auth = json.loads(open("auth.json", "r").read())

    # refresh auth if required
    try:
        read_report(auth, "All_Items")["data"]
    except KeyError:
        auth = refresh_auth(auth)
        if auth is not None and "access_token" in auth:
            open("auth.json", "w").write(json.dumps(auth))

    # some test
    resp_j = read_report(auth, "All_Items")
    print(json.dumps(resp_j, indent=1))