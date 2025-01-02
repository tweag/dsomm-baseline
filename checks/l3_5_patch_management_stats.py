import subprocess
import json

# Required Github permissions: "Contents" and "Pull requests" repository permissions (read)
# Rule: Generation of Patch Management Statistics
# Ideas: Check for pull requests related to dependency updates and security patches
#        Could be extended to analyze merge frequency and patch application time

def check_l3_5_patch_management_stats(repo):
    try:
        # Check for dependency update PRs
        dependency_prs = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/pulls?state=all&per_page=100'],
            capture_output=True, text=True
        )
        
        if dependency_prs.returncode == 0:
            prs = json.loads(dependency_prs.stdout)
            update_prs = [pr for pr in prs if 'dependency' in pr['title'].lower() or 'update' in pr['title'].lower()]
            
            # Check for security patch PRs
            security_prs = [pr for pr in prs if 'security' in pr['title'].lower() or 'patch' in pr['title'].lower()]
            
            if update_prs or security_prs:
                stats = f"Detected ({len(update_prs)} dependency updates, {len(security_prs)} security patches)"
                return stats
        
        return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
