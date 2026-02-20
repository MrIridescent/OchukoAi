import github
import random
import time
import json
import os
from datetime import datetime

# CONFIGURATION
TOKEN = 'YOUR_GITHUB_PAT_HERE'
LOG_FILE = 'github_bot_log.json'

# SAFETY THRESHOLDS
MIN_DELAY = 45
MAX_DELAY = 90
DAILY_ACTION_LIMIT = 20

# THE NICHED SEARCH QUERY
# Targets Good First Issues in Security, AI, Web Dev, and Red Teaming
SEARCH_QUERY = 'is:issue is:open label:"good first issue" security OR hacking OR pentest OR web OR python OR ai OR cryptography OR redteam OR sql OR docker OR kubernetes'

class NicheGitHubBot:
    def __init__(self, token):
        self.g = github.Github(token)
        self.load_state()
        
    def load_state(self):
        """Load previous activity log."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'last_action': 0,
                'daily_count': 0,
                'stared': [],
                'forked': [],
                'commented': []
            }

    def save_state(self):
        """Save current state."""
        with open(LOG_FILE, 'w') as f:
            json.dump(self.state, f)

    def wait_human(self):
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

    def generate_contextual_comment(self, issue):
        """
        Analyzes the issue content and generates a tailored comment.
        """
        title = issue.title.lower()
        body = issue.body.lower() if issue.body else ""
        
        # Check for specific keywords to tailor the comment
        if any(word in title or word in body for word in ['sql', 'injection', 'database', 'db']):
            return "I have experience with SQL injection testing and database security. I'd love to help secure this."
        
        if any(word in title or word in body for word in ['xss', 'csrf', 'web', 'http', 'security']):
            return "I'm familiar with web application security. I'll take a look at this vulnerability."
        
        if any(word in title or word in body for word in ['prompt', 'llm', 'gpt', 'ai', 'machine learning']):
            return "This looks like a prompt engineering or AI model optimization task. I'm interested in contributing."
            
        if any(word in title or word in body for word in ['docker', 'kubernetes', 'container', 'infra']):
            return "I work with containerization and DevOps. I'll look into this infrastructure issue."
            
        # Default generic comment for unknown topics
        return "I'm new to this project but I'd love to take a look at this issue and contribute."

    def star_repo(self, repo):
        repo_name = repo.full_name
        if self.is_safe_to_act(repo_name):
            try:
                repo.star()
                print(f"✅ Starred: {repo_name}")
                self.state['stared'][repo_name] = [datetime.now().isoformat()]
                self.state['daily_count'] += 1
                self.save_state()
                return True
            except Exception as e:
                print(f"❌ Error: {e}")
        return False

    def comment_on_issue(self, issue):
        repo_name = issue.repository.full_name
        issue_number = issue.number
        
        # Check if we already commented on this specific issue to avoid spam
        if f"{repo_name}-{issue_number}" in self.state['commented']:
            return False

        try:
            # Generate a tailored comment based on the issue content
            comment_text = self.generate_contextual_comment(issue)
            
            issue.create_comment(comment_text)
            print(f"💬 Commented on issue #{issue_number} in {repo_name}")
            
            # Mark this specific issue as commented to prevent spam
            self.state['commented'].append(f"{repo_name}-{issue_number}")
            self.state['daily_count'] += 1
            self.save_state()
            return True
        except Exception as e:
            print(f"❌ Error commenting: {e}")
            return False

    def fork_repo(self, repo):
        """
        Fork a repository. 
        Note: Forking consumes a lot of API rate limits, so we do it sparingly.
        """
        repo_name = repo.full_name
        
        # Safety: Only fork if we haven't forked it yet
        if repo_name in self.state['forked']:
            return False
            
        try:
            # Create the fork
            fork = repo.create_fork()
            print(f"🍴 Forked: {repo_name}")
            
            # Track the fork
            self.state['forked'].append(repo_name)
            self.state['daily_count'] += 1
            self.save_state()
            return True
        except github.GithubException as e:
            # Sometimes you can't fork if you already have too many forks or the repo is private
            if e.status == 403:
                print(f"⚠️  Cannot fork {repo_name} (Permission denied or limit reached).")
            else:
                print(f"❌ Error forking: {e}")
            return False

    def check_rate_limit(self):
        """Check remaining API requests."""
        rate = self.g.rate_limiting
        remaining = rate[0]
        reset = datetime.fromtimestamp(rate[1])
        
        print(f"\n📊 API Status: {remaining} requests remaining.")
        if remaining < 10:
            wait_seconds = reset - datetime.now()
            print(f"⚠️  Low on requests. Waiting until {reset} ({wait_seconds.total_seconds():.0f} seconds)...")
            time.sleep(wait_seconds.total_seconds())

def main():
    print(f"🚀 Starting Niche GitHub Growth Bot at {datetime.now()}")
    
    # Initialize Bot
    bot = NicheGitHubBot(TOKEN)
    
    # Initial Safety Check
    bot.check_rate_limit()
    
    # Search for "Good First Issue" repos in specific niches
    print(f"🔍 Searching for: {SEARCH_QUERY}")
    try:
        query = bot.g.search_issues(SEARCH_QUERY)
        total_count = query.totalCount
        print(f"Found {total_count} issues to process.\n")
        
        for issue in query:
            print(f"--- Processing: {issue.repository.full_name} ---")
            
            # 1. Star the repo (Visibility)
            if bot.star_repo(issue.repository):
                bot.wait_human()
            
            # 2. Fork the repo (Badge: Forker) - Only if not already forked
            if issue.repository.full_name not in bot.state['forked']:
                if bot.fork_repo(issue.repository):
                    bot.wait_human()
            
            # 3. Comment on the issue (Engagement)
            if bot.comment_on_issue(issue):
                bot.wait_human()
                
            # Safety Break: Stop after 100 issues or if rate limit is low
            if bot.state['daily_count'] >= 100:
                print("Reached daily action limit. Stopping.")
                break
                
    except Exception as e:
        print(f"💥 Fatal Error: {e}")

if __name__ == "__main__":
    main()
