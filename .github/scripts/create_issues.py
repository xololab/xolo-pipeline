import re
import os
from pathlib import Path
from github import Github


def parse_markdown(path: Path):
    issues = []
    content = path.read_text(encoding="utf-8")
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
    print(f"🛠️  Creating milestone: {milestone_title}")
    return repo.create_milestone(title=milestone_title)


def update_issue_if_needed(issue, new_body, new_labels, new_milestone):
    needs_update = False

    # Normalize label names
    current_labels = sorted([l.name for l in issue.labels])
    target_labels = sorted(new_labels)

    if issue.body.strip() != new_body.strip():
        needs_update = True

    if current_labels != target_labels:
        needs_update = True

    if new_milestone:
        if not issue.milestone or issue.milestone.title != new_milestone.title:
            needs_update = True
    else:
        if issue.milestone:
            needs_update = True

    if needs_update:
        print(f"🔄 Updating issue: {issue.title}")
        issue.edit(
            body=new_body,
            labels=new_labels,
            milestone=new_milestone
        )
    else:
        print(f"✅ Issue already up-to-date: {issue.title}")


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
        # Check if issue with same title already exists
        existing = next((i for i in existing_issues if i.title.strip() == title), None)

        milestone = fetch_or_create_milestone(repo, milestone_name) if milestone_name else None

        if existing:
            update_issue_if_needed(existing, body, labels, milestone)
        else:
            print(f"➕ Creating new issue: {title}")
            repo.create_issue(title=title, body=body, labels=labels, milestone=milestone)


if __name__ == "__main__":
    main()
