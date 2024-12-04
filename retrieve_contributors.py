import datetime
import json
import time

import polars as pl
import requests

repos = pl.read_parquet("commits.parquet").get_column("repo_name").unique().to_list()

# "https://api.github.com/repos/schochastics/schochastics-net/contributors"
api = "https://api.github.com/repos/"

try:
    with open("credentials1.json") as f:
        credentials = json.load(f)
    headers = {"Authorization": "Bearer " + credentials["github_token"]}
except:
    headers = None

results = {r: None for r in repos}
print("Fetching contributors")
for repo in repos:
    r = requests.get(api + repo + "/contributors", headers=headers)
    results[repo] = r.json()
    if int(r.headers["X-RateLimit-Remaining"]) == 0:
        print("Waiting for rate limit ", end="")
        reset_time = datetime.datetime.fromtimestamp(
            int(r.headers["X-RateLimit-Reset"])
        )
        while reset_time > datetime.datetime.now():
            print(".", end="")
            time.sleep(1)
        time.sleep(5)
        print("")

with open("contributors.json", "w") as f:
    json.dump(results, f)