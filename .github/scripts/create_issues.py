import re
from pathlib import Path
from github import Github
import os

def parse_markdown(path: Path):
    issues = []
    content = path.read_text(encoding="utf-8")
    blocks = re.split(r"###\s+", content)

    for block in blocks:
        if "**Labels:**" in block:
            lines = block.strip().splitlines()
            title = lines[0].strip()
            label_line = next((line for line in lines if line.startswith("**Labels:**")), "")
            description_lines = [line for line in lines if not line.startswith("**Labels:**")]
            description = "\n".join(description_lines[1:]).strip()

            # Extraer etiquetas
            labels_match = re.search(r"\*\*Labels:\*\*\s*`(.+?)`", label_line)
            if labels_match:
                labels = re.findall(r"`(.*?)`", label_line)
            else:
                labels = []

            issues.append((title, description, labels))
    return issues

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
    existing_titles = {i.title.strip() for i in repo.get_issues(state="all")}

    for title, body, labels in issues_to_create:
        if title not in existing_titles:
            print(f"✅ Creating issue: {title}")
            repo.create_issue(title=title, body=body, labels=labels)
        else:
            print(f"⚠️ Issue already exists: {title}")

if __name__ == "__main__":
    main()
