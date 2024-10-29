import subprocess
import json

def check_l2_6_test_libyear(repo):
    try:
        libyear_indicators = []

        # Check for libyear-related files
        libyear_files = [
            'libyear.json',
            'libyear-config.js',
            'libyear.config.js',
            '.libyearrc'
        ]

        for file in libyear_files:
            result = subprocess.run(
                ['gh', 'api', f'/repos/{repo}/contents/{file}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                libyear_indicators.append(f"Config file: {file}")

        # Check for GitHub Actions using libyear
        actions_result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/actions/workflows'],
            capture_output=True, text=True
        )

        if actions_result.returncode == 0:
            workflows = json.loads(actions_result.stdout)
            for workflow in workflows['workflows']:
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
