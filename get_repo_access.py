import requests
import os

def get_repo_collaborators(owner, repo, token):
    """Get the list of collaborators with access to the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return [collaborator['login'] for collaborator in response.json()]
    else:
        print(f"Error fetching collaborators: {response.status_code}, {response.text}")
        return []

def get_repo_teams(owner, repo, token):
    """Get the list of teams with access to the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/teams"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return [team['slug'] for team in response.json()]
    else:
        print(f"Error fetching teams: {response.status_code}, {response.text}")
        return []

def main():
    # Get the GITHUB_TOKEN and the full repo (owner/repo) from environment variables
    token = os.getenv('GITHUB_TOKEN')
    full_repo = os.getenv('GITHUB_REPOSITORY')  # This will be in the format 'owner/repo'

    # Split the 'owner/repo' into 'owner' and 'repo'
    if full_repo:
        owner, repo = full_repo.split('/')
    else:
        print("Error: GITHUB_REPOSITORY environment variable is not set.")
        return

    print(f"Processing repository: {owner}/{repo}")

    # Fetch collaborators and teams
    collaborators = [] #get_repo_collaborators(owner, repo, token)
    teams = get_repo_teams(owner, repo, token)

    # Write combined list of users to a file
    with open("access_report.txt", "w") as f:
        all_users = collaborators + teams
        for user in all_users:
            f.write(f"{user}\n")

    print("Access report generated successfully.")

if __name__ == "__main__":
    main()
