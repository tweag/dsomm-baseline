import subprocess
import json

# Required Github permissions: "Contents" repository permissions (read)
# Rule: L1.2 (Versioning): Check if the repository uses versioning
# Ideas: Check for common version files, tags, and releases
#        Could be extended to check for version patterns in commit messages or branch names

def check_l1_2_versioning(repo):
    try:
        # Check for common version files
        version_files = ['VERSION', 'version.txt', 'package.json', 'setup.py', 'pom.xml']
        for file in version_files:
            # Use GitHub CLI to check if each version file exists
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"Detected (file: {file})"

        # Check for tags
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/tags?per_page=1'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            tags = json.loads(result.stdout)
            if tags:
                return f"Detected (latest tag: {tags[0]['name']})"

        # Check for releases
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/releases?per_page=1'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            releases = json.loads(result.stdout)
            if releases:
                return f"Detected (latest release: {releases[0]['tag_name']})"

        return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return "Error exception"
