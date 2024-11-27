import requests
import pandas as pd


# Function to get a user's repositories
def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code}, {response.text}")


# Function to get commits for a specific repository by the given user
def get_commits(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    params = {'author': username}  # Filter commits by this user
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []  # Return empty list if commits are not accessible


# Main function to collect commit messages
def get_commit_messages(username):
    try:
        repos = get_repositories(username)
        data = []
        for repo in repos:
            repo_name = repo['name']
            print(f"Fetching commits for repository: {repo_name}")
            commits = get_commits(username, repo_name)
            for commit in commits:
                commit_message = commit['commit']['message']
                commit_date = commit['commit']['author']['date']
                data.append({
                    "Repository": repo_name,
                    "Commit Message": commit_message,
                    "Commit Date": commit_date
                })
        # Create pandas DataFrame
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error


# Input username
if __name__ == "__main__":
    github_username = "schochastics"
    df = get_commit_messages(github_username)
    if not df.empty:
        print("Commit messages retrieved successfully!")
        print(df)
        # Save to CSV
        df.to_csv(f"{github_username}_commit_messages.csv", index=False)
        print(f"Data saved to {github_username}_commit_messages.csv")
    else:
        print("No commit messages found or error occurred.")
