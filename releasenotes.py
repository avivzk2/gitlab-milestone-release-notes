"""
Release Notes Generator
-----------------------

Creates release notes based on a milestone.

"""
import gitlab
import argparse
from typing import Any


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Gitlab Release Notes')
    parser.add_argument('group', type=str, help='Name of the Gitlab group (lower case)')
    parser.add_argument('milestone', type=str, help='Name of the milestone (lower case)')
    parser.add_argument('--server', type=str, help="Server's host (e.g. https://gitlab.com)")
    parser.add_argument('--token', type=str, help="Server\'s private token")
    return parser.parse_args()


def get_connection(server: str, token: str) -> gitlab.Gitlab:
    return gitlab.Gitlab(server, private_token=token)


def get_milestone(gl: gitlab.Gitlab, group: str, milestone: str) -> Any:
    groups = gl.groups.list(all=True, get_all=True)
    name2group = {group.name.lower(): group for group in groups}
    group = name2group[group]
    milestones = group.milestones.list(all=True, get_all=True)
    name2milestone = {milestone.title.lower(): milestone for milestone in milestones}
    return name2milestone[milestone.lower()]


def get_assignee_str(assignee: dict) -> str:
    return f"@{assignee['username']}" if assignee else 'none'


def get_issues(milestone: Any) -> dict:
    issues = {'opened': [], 'closed': []}
    for issue in milestone.issues(all=True, get_all=True):
        assignee = get_assignee_str(issue.assignee)
        issue_str = f" - {issue.title} ([#{issue.iid}]({issue.web_url})) ({assignee})"
        issues[issue.state].append(issue_str)
    return issues


def get_mrs(milestone: Any) -> dict:
    mrs = {'opened': [], 'closed': [], 'merged': []}
    for mr in milestone.merge_requests(all=True, get_all=True):
        assignee = get_assignee_str(mr.assignee)
        mr_str = f" - {mr.title} ([#{mr.iid}]({mr.web_url})) ({assignee})"
        mrs[mr.state].append(mr_str)
    return mrs


def generate_release_notes(milestone: Any) -> str:
    issues = get_issues(milestone)
    mrs = get_mrs(milestone)

    release_notes = [
        f"## {milestone.title}",
        "\n",
        f"{milestone.description}",
        "\n",
    ]
    if issues['opened']:
        release_notes.append("### Open Issues")
        release_notes.extend(issues['opened'])
        release_notes.append("\n")
    if issues['closed']:
        release_notes.append("### Closed Issues")
        release_notes.extend(issues['closed'])
        release_notes.append("\n")

    if mrs['opened']:
        release_notes.append("### Open MRs")
        release_notes.extend(mrs['opened'])
        release_notes.append("\n")
    if mrs['closed']:
        release_notes.append("### Closed MRs")
        release_notes.extend(mrs['closed'])
        release_notes.append("\n")
    if mrs['merged']:
        release_notes.append("### Merged MRs")
        release_notes.extend(mrs['merged'])
        release_notes.append("\n")

    return '\n'.join(release_notes)


if __name__ == '__main__':
    args = get_args()
    # print(args)

    gl = get_connection(args.server, args.token)
    milestone = get_milestone(gl, args.group, args.milestone)

    release_notes = generate_release_notes(milestone)
    print(release_notes)

