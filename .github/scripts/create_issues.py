import re
import os
from pathlib import Path
from github import Github


def parse_markdown(path: Path):
    issues = []
    content = path.read_text(encoding="utf-8")
    # Match markdown blocks: Title, Labels, optional Milestone, Description
    blocks = re.findall(
        r"### (.+?)\n\*\*Labels:\*\* (.+?)\n(?:\*\*Milestone:\*\* (.+?)\n)?(.*?)\n(?=\n###|\Z)",
        content,
        re.DOTALL
    )

    for title, label_str, milestone, description in blocks:
        labels = [lbl.strip(" `") for lbl in label_str.split(",")]
        milestone = milestone.strip() if milestone else None
        description = description.strip()
        issues.append((title.strip(), description, labels, milestone))
    return issues


def fetch_all_issues(repo):
    return list(repo.get_issues(state="all"))


def fetch_or_create_milestone(repo, milestone_title):
    for ms in repo.get_milestones(state="all"):
        if ms.title == milestone_title:
            return ms
    # Create milestone if not found
    print(f"🛠️  Creating milestone: {milestone_title}")
    return repo.create_milestone(title=milestone_title)


def main():
    token = os.getenv("TOKEN_PAT")
    repo_name = "xololab/xolo-pipeline"

    if not token:
        print("❌ Error: TOKEN_PAT environment variable not set.")
        return

    gh = Github(token)
    repo = gh.get_repo(repo_name)

    md_path = Path(".github/project-plan.md")
    if not md_path.exists():
        print(f"❌ ERROR: File not found: {md_path}")
        return

    issues_to_create = parse_markdown(md_path)
    existing_issues = fetch_all_issues(repo)

    for title, body, labels, milestone_name in issues_to_create:
        if any(i.title.strip() == title for i in existing_issues):
            print(f"⚠️  Issue already exists: {title}")
            continue

        print(f"✅ Creating issue: {title}")
        try:
            milestone = fetch_or_create_milestone(repo, milestone_name) if milestone_name else None
            repo.create_issue(title=title, body=body, labels=labels, milestone=milestone)
        except Exception as e:
            print(f"❌ Failed to create issue '{title}': {e}")


if __name__ == "__main__":
    main()
