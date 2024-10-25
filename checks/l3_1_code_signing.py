import subprocess
import json

def check_l3_1_code_signing(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/commits'],
            capture_output=True, text=True, check=True
        )
        commits = json.loads(result.stdout)
        if commits and 'verification' in commits[0]:
            if commits[0]['verification']['verified']:
                return "Enabled"
            else:
                return "Not detected"
        return "Not detected"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return f"Error: {str(e)}"
