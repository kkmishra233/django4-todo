import os
import re
from github import Github, GithubException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize GitHub client
    github_token = os.getenv('GITHUB_TOKEN')
    github = Github(github_token)

    # Get the PR number from the context
    pr_number = os.getenv('PR_NUMBER')

    # Define checklist items
    checklist_items = [
        "Item 1",
        "Item 2",
        "Item 3"
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
        if not regex.search(body):
            all_checked = False
            break

    # Comment on the PR accordingly
    if all_checked:
        pr.create_issue_comment("All checklist items are checked! You can merge this pull request.")
    else:
        pr.create_issue_comment("Not all checklist items are checked. Please complete the checklist before merging.")

if __name__ == "__main__":
    main()
