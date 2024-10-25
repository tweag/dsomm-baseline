import subprocess
import json

def check_l2_1_artifact_pinning(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/artifacts'],
            capture_output=True, text=True, check=True
        )
        artifacts = json.loads(result.stdout)
        pinned_artifacts = [a for a in artifacts['artifacts'] if a['expires_at'] is None]
        if pinned_artifacts:
            return f"Enabled ({len(pinned_artifacts)})"
        return "Not enabled"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
