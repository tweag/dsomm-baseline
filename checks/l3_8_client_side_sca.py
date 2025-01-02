import subprocess
import json

# Required Github permissions: "Contents" repository permissions (read)
# Rule: Software Composition Analysis (client side)
# Ideas: Check for client-side SCA tool configurations and related GitHub Actions workflows
#        Could be extended to analyze specific tool outputs or integration methods

def check_l3_8_client_side_sca(repo):
    try:
        sca_indicators = []

        # Check for common client-side SCA tool config files
        config_files = [
            'package.json',  # npm audit
            'yarn.lock',     # yarn audit
            'bower.json',    # Bower
            'Gemfile.lock',  # Bundle audit
            'requirements.txt'  # Safety for Python
        ]

        for file in config_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                sca_indicators.append(f"Config file: {file}")

        # Check for GitHub Actions workflows related to client-side SCA
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
                if any(keyword in workflow['name'].lower() for keyword in ['npm audit', 'yarn audit', 'bundle audit', 'safety check']):
                    sca_indicators.append(f"GitHub Action: {workflow['name']}")

        if sca_indicators:
            return f"Client-side SCA detected: {', '.join(sca_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
