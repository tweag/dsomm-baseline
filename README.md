# OWASP DevSecOps Maturity Model (DSOMM) Baseline Using GitHub API

This project provides a modular framework to check various OWASP DSOMM features on a specified GitHub repository using gh cli. The checks are organised as per [owasp dsomm](https://dsomm.owasp.org/) guidance and possible automated checks using github api.

### Level 1: Basic understanding of security practices
| DSOMM Baseline | Description  | 
| :------------ |:---------------|
| [automated_prs](./checks/l1_1_automated_prs.py) | Look for PRs that have been created by bots or specific tools commonly used for automated dependency updates, such as Dependabot. |
| [versioning](./checks/l1_2_versioning.py)        | Look for common versioning indicators such as version files, tags, or release information. |
| [test_stored_secrets](./checks/l1_3_test_stored_secrets.py) | Check if secret scanning alerts are enabled. |

### Level 2: Adoption of basic security practices
| DSOMM Baseline | Description  | 
| :------------ |:---------------|
| [artifact_pinning](./checks/l2_1_artifact_pinning.py)  |  Look if artifact pinning is enabled for a the repository.  |
| [sbom](./checks/l2_2_sbom.py)  |  Look for SBOM information for the repository  |
| [automated_pr_merges](./checks/l2_3_automated_pr_merges.py)  |  Look for PRs that have been created by bots or specific tools.  |
| [mfa](./checks/l2_4_mfa.py)  |  Look for repository owner's username and then check their MFA status  |
| [serverside_sca](./checks/l2_5_serverside_sca.py)  |  Look for SCA tool configuration files  |
| [test_libyear](./checks/l2_6_test_libyear.py)  |  Look for libyear-related files  |

### Level 3: High adoption of security practices
| DSOMM Baseline | Description  | 
| :------------ |:---------------|
| [code_signing](./checks/l3_1_code_signing.py) | Look for code signing by examining the verification status of the latest commit  |

### Level 4: Very high adoption of security practices
| DSOMM Baseline | Description  | 
| :------------ |:---------------|
| [gitignore](./checks/l4_1_gitignore.py) | Look for the presence of a .gitignore file |

### Level 5: Advanced deployment of security practices at scale
| DSOMM Baseline | Description  | 
| :------------ |:---------------|
| [artifact_sigining](./checks/l5_1_artifact_sigining.py) | Look for artifact siginature |

## Setup

- **[requirements.txt](./requirements.txt)**: Lists the Python dependencies required to run the project.
- **[main.py](./main.py)**: The main script to run selected checks for each dsomm level on specified repositories.
- **[checks/](./checks)**: Contains individual Python scripts for each check. Each script defines a function that performs a specific check.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ModusCreate-NFR/devsecops-maturity-model-baseline.git
   cd devsecops-maturity-model-baseline
   ```
2. **Install the required dependencies**:

   Make sure you have Python 3 installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install and authenticate GitHub CLI**:

   Follow the instructions at [GitHub CLI](https://cli.github.com/) to install and authenticate.

## Usage
**Run the main script**:

   Execute main.py to start the process:
   ```bash
   python main.py
   ```
It will be prompted with set of DCOMM Levels and Checks to choose to run for a given repo(s)
1. **Select checks**:

   You will be presented with a list of available checks grouped as per owasp dsomm levels.

   Enter the group names (e.g., Level1, Level2) or specific check numbers (e.g., 1, 5, 10) to select which checks to run.

2. **Enter repositories**:

   Provide a comma-separated list of repositories in the format owner/repo (e.g., Modus/testrepo).

3. **View results**:

   The script will output a table showing the results of each selected check for each repository.

   OWASP DSOMM Level statistics will be displayed, indicating the number of successful checks per group.
