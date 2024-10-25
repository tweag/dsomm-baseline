import subprocess
import json
from datetime import datetime, timedelta

def check_l2_3_automated_pr_merges(repo):
    try:
        # Check merged PRs from the last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            automated_merges = [
                pr for pr in prs 
                if pr['merged_at'] and pr['merged_by']['type'] == 'Bot' 
                and datetime.fromisoformat(pr['merged_at'].rstrip('Z')) > datetime.fromisoformat(thirty_days_ago)
            ]
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
        return f"Error: {str(e)}"
