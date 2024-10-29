import subprocess
import base64

def check_l4_1_gitignore(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/contents/.gitignore'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            gitignore_content = result.stdout
            content_json = subprocess.run(
                ['jq', '-r', '.content'],
                input=gitignore_content,
                capture_output=True,
                text=True
            ).stdout.strip()
            
            if content_json:
                decoded_content = base64.b64decode(content_json).decode('utf-8')
                lines = decoded_content.split('\n')
                non_empty_lines = [line for line in lines if line.strip() and not line.startswith('#')]
                return f"Found ({len(non_empty_lines)} rules)"
            else:
                return "Not detected"
        else:
            return "Not detected"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except Exception as e:
        #return f"Error: {str(e)}"
        return "Error exception"
