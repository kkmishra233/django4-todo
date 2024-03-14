import os
import re
from github import Github, GithubException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def set_checklist_status(github, pr_number, all_checked):
    # Get the repository and pull request
    repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr = repo.get_pull(int(pr_number))

    # Check if the "Checklist-Passed" label is already applied
    checklist_passed = 'Checklist-Passed' in [label.name for label in pr.labels]

    # Update the status of the "Checklist-Passed" label accordingly
    if all_checked:
        if not checklist_passed:
            pr.add_to_labels('Checklist-Passed')
    else:
        if checklist_passed:
            pr.remove_from_labels('Checklist-Passed')

def main():
    # Initialize GitHub client
    github_token = os.getenv('GITHUB_TOKEN')
    github = Github(github_token)

    # Get the PR number from the context
    pr_number = os.getenv('PR_NUMBER')

    # Define checklist items
    checklist_items = [
        "Tests have been added or updated",
        "Documentation has been updated",
        "Code follows the coding style guidelines"
        # Add more checklist items as needed
    ]

    # Get the PR object
    repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr = repo.get_pull(int(pr_number))

    # Get the body of the PR
    body = pr.body

    all_checked = all(re.search(rf'\[x\] {re.escape(item)}', body) for item in checklist_items)

    # Comment on the PR accordingly
    if all_checked:
        pr.create_issue_comment("All checklist items are checked! You can merge this pull request.")
    else:
        pr.create_issue_comment("Not all checklist items are checked. Please complete the checklist before merging.")

    # Set the status of the "Checklist-Passed" label
    set_checklist_status(github, pr_number, all_checked)

    # Return appropriate exit code
    if all_checked:
        exit(0)  # Success
    else:
        exit(1)  # Failure

if __name__ == "__main__":
    main()
