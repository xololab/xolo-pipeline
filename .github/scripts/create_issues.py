import re
from pathlib import Path
from github import Github
import os

def parse_markdown(path: Path):
    issues = []
    content = path.read_text(encoding="utf-8")
    sections = re.split(r"##+ ", content)
    for sec in sections:
        if sec.strip().startswith("Issue:"):
            lines = sec.splitlines()
            title = lines[0].replace("Issue:", "").strip()
            description = "\n".join(lines[2:]).strip()
            issues.append((title, description))
    return issues

def main():
    token = os.getenv("TOKEN_PAT")
    repo_name = "xololab/xolo-pipeline"

    if not token:
        print("Error: GITHUB_TOKEN_PAT environment variable not set.")
        return

    gh = Github(token)
    repo = gh.get_repo(repo_name)

    md_path = Path(".github/project-plan.md")
    if not md_path.exists():
        print(f"ERROR: File not found: {md_path}")
        return

    issues_to_create = parse_markdown(md_path)
    existing_issues = list(repo.get_issues(state="all"))

    for title, body in issues_to_create:
        if not any(i.title.strip() == title.strip() for i in existing_issues):
            print(f"Creating issue: {title}")
            repo.create_issue(title=title, body=body)
        else:
            print(f"Issue already exists: {title}")

if __name__ == "__main__":
    main()
