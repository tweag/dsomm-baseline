import subprocess
import json

def check_l5_1_artifact_sigining(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/artifacts'],
            capture_output=True, text=True, check=True
        )
        artifacts = json.loads(result.stdout)
        signed_artifacts = [a for a in artifacts['artifacts'] if 'signature' in a.get('name', '').lower()]
        if signed_artifacts:
            return f"Detected ({len(signed_artifacts)})"
        return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
