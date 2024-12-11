import requests
import datetime
import time
import json

# https://api.github.com/search/commits?q=author:schochastics+committer-date:%3E=2022-03-01&sort=author-date&&order=asc&page=1

def search_commits(username: str, date_range: str, page: int = 1) -> list[dict]:
    results = []
    api = "https://api.github.com/search/commits"
    # the query parameters should not be escaped, but "requests" automatically
    # escapes all parameter characters (e.g., "+"). So we use this workaround
    query = f"?q=author:{username}+committer-date:{date_range}&sort=author-date&order=asc&page={page}"
    r = requests.get(api + query)
    print("Got total of", r.json()["total_count"], "results")
    results += r.json()["items"]
    next_link = [l for l in r.headers["Link"].split(", ") if 'rel="next"' in l]
    while len(next_link) > 0:
        url = next_link[0].split(";")[0][1:-1]
        r = requests.get(url)
        results += r.json()["items"]
        next_link = [l for l in r.headers["Link"].split(", ") if 'rel="next"' in l]
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
    return results


# the api doesn't like too many results at once,
# so we query by date ranges (should be less than 1000 hits each)
date_ranges = [
    "2022-03-01..2022-12-31",
    "2023-01-01..2023-06-30",
    "2023-07-01..2023-12-31",
    "2024-01-01..2024-12-01",
]

data = []
for d in date_ranges:
    print(d)
    data += search_commits("schochastics", d)


with open("results.json", "w") as f:
    json.dump(data, f)
