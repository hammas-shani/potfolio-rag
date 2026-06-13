import os
import time
import requests
import base64
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ab humein GITHUB_USERNAME ki zaroorat hi nahi hai
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_all_repositories():
    """GitHub se user ki tamam repositories fetch karta hai"""
    print("📦 Fetching all repositories...")
    url = "https://api.github.com/user/repos?type=owner&per_page=100"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repos = response.json()
        # Yahan hum direct 'full_name' utha rahe hain (e.g., 'hammas-shani/ai-trainer-')
        return [repo['full_name'] for repo in repos]
    else:
        print(f"❌ Error fetching repositories: {response.json()}")
        return []

def get_repo_context(repo_full_name):
    """Repo ki details aur files structure fetch karta hai"""
    repo_url = f"https://api.github.com/repos/{repo_full_name}"
    repo_res = requests.get(repo_url, headers=HEADERS)
    
    if repo_res.status_code != 200:
        return None
    
    repo_data = repo_res.json()
    description = repo_data.get("description") or "No description provided."
    language = repo_data.get("language") or "Unknown"
    
    contents_url = f"https://api.github.com/repos/{repo_full_name}/contents"
    contents_res = requests.get(contents_url, headers=HEADERS)
    files = []
    if contents_res.status_code == 200:
        files = [item['name'] for item in contents_res.json() if item['type'] == 'file']
    
    repo_short_name = repo_full_name.split('/')[-1]
    
    return {
        "full_name": repo_full_name,
        "name": repo_short_name,
        "description": description,
        "language": language,
        "files": ", ".join(files)
    }

def generate_readme(context):
    """Groq se README banwata hai"""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant", # Naya model yahan update kiya
        temperature=0.3
    )

    system_prompt = (
        "You are Hammas Shahzad Shani, an AI/ML Engineer. Write a highly technical, professional README.md "
        "for the following GitHub repository based on its name, description, language, and file structure. "
        "Include: Project Overview, Features, Tech Stack, and Architecture. "
        "Return ONLY the markdown format."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Repo: {context['name']}\nDescription: {context['description']}\nLanguage: {context['language']}\nFiles: {context['files']}")
    ])

    chain = prompt | llm
    response = chain.invoke({})
    return response.content

def update_github_readme(repo_full_name, new_readme_content):
    """Updated README ko direct GitHub pe commit karta hai"""
    file_path = "README.md"
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
    
    get_res = requests.get(url, headers=HEADERS)
    sha = None
    if get_res.status_code == 200:
        sha = get_res.json()['sha'] 
        
    encoded_content = base64.b64encode(new_readme_content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": "docs: Automated README generation via AI Agent",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha 
        
    put_res = requests.put(url, headers=HEADERS, json=data)
    
    if put_res.status_code in [200, 201]:
        print(f"✅ Successfully updated README for: {repo_full_name.split('/')[-1]}")
    else:
        print(f"❌ Failed to update {repo_full_name.split('/')[-1]}")

def run_bulk_updater():
    print("\n🚀 Starting Full Automation RAG Updater...")
    repos = get_all_repositories()
    
    if not repos:
        print("No repositories found.")
        return

    print(f"Total Repositories Found: {len(repos)}\n")

    for index, repo_full_name in enumerate(repos):
        repo_short_name = repo_full_name.split('/')[-1]
        print(f"[{index + 1}/{len(repos)}] Processing '{repo_short_name}'...")
        
        context = get_repo_context(repo_full_name)
        if context:
            readme_content = generate_readme(context)
            update_github_readme(repo_full_name, readme_content)
        else:
            print(f"⚠️ Skipping {repo_short_name} (Could not fetch context)")
            
        time.sleep(2)

if __name__ == "__main__":
    run_bulk_updater()