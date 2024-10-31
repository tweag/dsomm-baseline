import subprocess
import json

# Required Github permissions: "Contents" repository permissions (read)
# Rule: L3.1 (Code Signing): Check if the last commit is signed
# Ideas: Check if the main branch has required_signatures enabled (Prevent merging unsigned commits)
#        Check if the last x commits are signed (Ensure that signed commits are being used in the past)
def check_l3_1_code_signing(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/commits'],
            capture_output=True, text=True, check=True
        )
        commits = json.loads(result.stdout)
        if commits[0]['commit']['verification']['verified']:
            return "Enabled" 
        else:
            return "Not detected"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"