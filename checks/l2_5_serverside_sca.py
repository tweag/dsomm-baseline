import subprocess
import json

def check_l2_5_serverside_sca(repo):
    try:
        sca_indicators = []

        # Check for SCA configuration files, add more as needed
        sca_files = [
            'dependency-check.xml',  # OWASP Dependency-Check
            'sca-config.json',       # Generic SCA config
            '.snyk',                 # Snyk
        ]

        for file in sca_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                sca_indicators.append(f"Config file: {file}")

        # Check for GitHub Actions workflows related to SCA
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            # Add more keywords as needed
            sca_keywords = ['dependency', 'sca', 'composition', 'snyk']
            for workflow in workflows['workflows']:
                if any(keyword in workflow['name'].lower() for keyword in sca_keywords):
                    sca_indicators.append(f"GitHub Action: {workflow['name']}")

        if sca_indicators:
            return f"Server-side SCA detected: {', '.join(sca_indicators)}"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
