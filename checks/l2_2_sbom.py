import subprocess
import json

def check_l2_2_sbom(repo):
    try:
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/dependency-graph/sbom'],
            capture_output=True, text=True, check=True
        )
        if result.returncode == 0:
            sbom_data = json.loads(result.stdout)
            package_count = len(sbom_data['sbom'].get('packages', []))
            return f"Yes ({package_count} packages)"
        else:
            return "Not detected"
    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error"
    except Exception as e:
        return f"Error: {str(e)}"
