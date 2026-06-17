import requests
import os

# Aapka GitHub Username
GITHUB_USERNAME = "hammas-shani"
PORTFOLIO_PATH = "dataset/portfolio.md"

def fetch_recent_repos():
    print(f"Fetching repositories for {GITHUB_USERNAME}...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=5"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from GitHub API.")
        return []
    
    return response.json()

def update_portfolio(repos):
    if not os.path.exists(PORTFOLIO_PATH):
        print(f"Error: {PORTFOLIO_PATH} not found!")
        return

    # File ka mojooda data read karein
    with open(PORTFOLIO_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_projects_added = False
    added_content = "\n\n### Auto-Fetched GitHub Repositories\n"

    for repo in repos:
        # Check karein ke repo pehle se toh nahi likhi hui (taake duplicate na ho)
        if repo['name'] not in content:
            name = repo['name'].replace("-", " ").title()
            desc = repo['description'] if repo['description'] else "No description provided."
            url = repo['html_url']
            lang = repo['language'] if repo['language'] else "Multiple Technologies"
            
            # Markdown format mein project ki details
            added_content += f"#### {name}\n"
            added_content += f"- **Description:** {desc}\n"
            added_content += f"- **Primary Technology:** {lang}\n"
            added_content += f"- **GitHub Link:** {url}\n\n"
            new_projects_added = True
            print(f"➕ Added new project: {name}")

    # Agar nayi repo mili hai, toh file update kar dein
    if new_projects_added:
        with open(PORTFOLIO_PATH, "a", encoding="utf-8") as f:
            f.write(added_content)
        print("✅ portfolio.md updated successfully!")
    else:
        print("ℹ️ No new repositories to add.")

if __name__ == "__main__":
    repos = fetch_recent_repos()
    if repos:
        update_portfolio(repos)