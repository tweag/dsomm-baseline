import subprocess
import base64

# Required Github permissions: "Contents" repository permissions (read)
# Rule: L4.1 (.gitignore): Check for the presence and content of a .gitignore file
# Ideas: Check if .gitignore exists and count the number of active rules
#        Could be extended to analyze specific rules or patterns in the .gitignore file

def check_l4_1_gitignore(repo):
    try:
        # Use GitHub CLI to check if .gitignore exists in the repository
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/contents/.gitignore'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            gitignore_content = result.stdout
            
            # Use jq to extract the content field from the JSON response
            content_json = subprocess.run(
                ['jq', '-r', '.content'],
                input=gitignore_content,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            if content_json:
                # Decode the base64 encoded content of the .gitignore file
                decoded_content = base64.b64decode(content_json).decode('utf-8')
                
                # Split the content into lines and filter out empty lines and comments
                lines = decoded_content.split('\n')
                non_empty_lines = [line for line in lines if line.strip() and not line.startswith('#')]
                
                return f"Detected ({len(non_empty_lines)} rules)"
            else:
                return "Not detected"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except Exception as e:
        return "Error exception"
