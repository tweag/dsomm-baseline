import subprocess
import json

# Required Github permissions: "Actions" repository permissions (read)
# Rule: L2.1 (Pinning of artifacts): Check if there are any pinned artifacts in the repository
# Ideas: Check for artifacts with no expiration date
#        Could be extended to check for specific types of pinned artifacts or their usage in workflows

def check_l2_1_artifact_pinning(repo):
    try:
        # Use GitHub CLI to fetch information about artifacts in the repository
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/artifacts'],
            capture_output=True, text=True, check=True
        )

        # Parse the JSON output into a Python object
        artifacts = json.loads(result.stdout)

        # Filter for pinned artifacts (those with no expiration date)
        pinned_artifacts = [a for a in artifacts['artifacts'] if a['expires_at'] is None]

        if pinned_artifacts:
            return f"Enabled ({len(pinned_artifacts)})"
        return "Not enabled"

    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
