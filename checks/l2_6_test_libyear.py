import subprocess
import json

# Required Github permissions: "Contents" and "Actions" repository permissions (read)
# Rule: L2.6 (Test libyear): Check for implementation of libyear testing
# Ideas: Check for libyear configuration files and GitHub Actions workflows related to libyear
#        Could be extended to analyze libyear results or check for specific libyear thresholds

def check_l2_6_test_libyear(repo):
    try:
        libyear_indicators = []

        # Check for libyear-related configuration files
        libyear_files = [
            'libyear.json',
            'libyear-config.js',
            'libyear.config.js',
            '.libyearrc'
        ]

        # Use GitHub CLI to check for the existence of each libyear config file
        for file in libyear_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                libyear_indicators.append(f"Config file: {file}")

        # Check for GitHub Actions workflows related to libyear
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            # Parse the JSON output of workflows
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
                # Check if 'libyear' is mentioned in the workflow name
                if 'libyear' in workflow['name'].lower():
                    libyear_indicators.append(f"GitHub Action: {workflow['name']}")

        if libyear_indicators:
            return f"Libyear testing implemented: {', '.join(libyear_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
