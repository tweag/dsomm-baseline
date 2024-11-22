import subprocess
import json

# Required Github permissions: "Dependency graph" repository permissions (read)
# Rule: L2.2 (SBOM of components): Check if a Software Bill of Materials (SBOM) is available for the repository
# Ideas: Check for the existence of an SBOM and count the number of packages
#        Could be extended to analyze specific package types or versions

def check_l2_2_sbom(repo):
    try:
        # Use GitHub CLI to fetch the SBOM (Software Bill of Materials) for the repository
        result = subprocess.run(
            ['gh', 'api', f'/repos/{repo}/dependency-graph/sbom'],
            capture_output=True, text=True, check=True
        )

        if result.returncode == 0:
            # Parse the JSON output into a Python object
            sbom_data = json.loads(result.stdout)

            # Count the number of packages in the SBOM
            package_count = len(sbom_data['sbom'].get('packages', []))
            return f"Detected ({package_count} packages)"
        else:
            return "Not detected"

    except subprocess.CalledProcessError:
        return "Unable to check"
    except json.JSONDecodeError:
        return "Error parsing data"
    except Exception as e:
        return "Error exception"
