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

    # Get the list of labels applied to the pull request
    labels = [label.name for label in pr.labels]

    # Check if the "Checklist-Passed" label is already applied
    checklist_passed = 'Checklist-Passed' in labels

    # Update the status of the "Checklist-Passed" label accordingly
    if all_checked and not checklist_passed:
        pr.add_to_labels('Checklist-Passed')
    elif not all_checked and checklist_passed:
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

    all_checked = True

    # Check if all checklist items are checked
    for item in checklist_items:
        regex = re.compile(rf'\[ \] {re.escape(item)}')
        if regex.search(body):
            all_checked = False
            break

    # Comment on the PR accordingly
    if all_checked:
        pr.create_issue_comment("All checklist items are checked! You can merge this pull request.")
        set_checklist_status(github, pr_number, 'success')
    else:
        pr.create_issue_comment("Not all checklist items are checked. Please complete the checklist before merging.")
        set_checklist_status(github, pr_number, 'failure')

if __name__ == "__main__":
    main()
