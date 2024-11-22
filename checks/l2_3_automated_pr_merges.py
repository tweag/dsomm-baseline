import subprocess
import json
from datetime import datetime, timedelta

# Required Github permissions: "Pull requests" repository permissions (read)
# Rule: L2.3 (Automated merge of automated PRs): Check for automatically merged pull requests
# Ideas: Check for PRs merged by bot accounts in the last 30 days
#        Could be extended to analyze specific bot names or PR characteristics

def check_l2_3_automated_pr_merges(repo):
    try:
        # Calculate the date 30 days ago from now
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

        # Use GitHub CLI to fetch closed pull requests, sorted by update time
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            # Parse the JSON output into a Python object
            prs = json.loads(result.stdout)
            automated_merges = []

            # Iterate through the pull requests
            for pr in prs:
                if pr.get('merged_at'):
                    # Convert merged_at time to datetime object
                    merged_at = datetime.fromisoformat(pr['merged_at'].rstrip('Z'))
                    
                    # Check if the PR was merged within the last 30 days
                    if merged_at > datetime.fromisoformat(thirty_days_ago):
                        merged_by = pr.get('merged_by', {})
                        # Check if the PR was merged by a bot
                        if merged_by and merged_by.get('type') == 'Bot':
                            automated_merges.append(pr)

            if automated_merges:
                return f"Detected ({len(automated_merges)} in last 30 days)"
            else:
                return "Not detected"
        else:
            return "Unable to check"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
