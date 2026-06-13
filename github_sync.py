import os
import requests
import base64
from dotenv import load_dotenv

# .env file load karein
load_dotenv()

# Environment variables se token extract karein
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

GITHUB_USERNAME = "hammas-shani" # Apna GitHub username yahan dalen
DATASET_DIR = "dataset"


# Headers for API request (Token dalne se API block nahi hogi agar repos zyada hain)
headers = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

def ensure_dir_exists():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)

def fetch_all_repos():
    print(f"Fetching repositories for {GITHUB_USERNAME}...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repos: {response.status_code}")
        return []

def fetch_and_save_readme(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/readme"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # GitHub README ko Base64 encode kar ke bhejta hai, isko decode karna lazmi hai
        readme_content = base64.b64decode(data['content']).decode('utf-8')
        
        file_path = os.path.join(DATASET_DIR, f"{repo_name}_readme.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"✅ Saved README for: {repo_name}")
    else:
        print(f"⚠️ No README found for: {repo_name}")

def sync_github_data():
    ensure_dir_exists()
    repos = fetch_all_repos()
    
    for repo in repos:
        repo_name = repo['name']
        fetch_and_save_readme(repo_name)
        
    print("\n🎉 Sync Complete! Sara data 'dataset' folder mein agaya hai.")

if __name__ == "__main__":
    sync_github_data()



