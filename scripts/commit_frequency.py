"""Count reachable non-merge commits by committer time in a UTC interval."""

import subprocess
from datetime import UTC, datetime, timedelta


def summarize(entries, end, days=7):
    start = end - timedelta(days=days)
    commits = [sha for sha, timestamp in entries if start.timestamp() < timestamp <= end.timestamp()]
    return {
        "source": "git log",
        "collection": "automatic",
        "period_start_exclusive": start.isoformat(),
        "period_end_inclusive": end.isoformat(),
        "days": days,
        "count": len(commits),
        "commits_per_day": round(len(commits) / days, 4),
        "commits": commits,
        "time_basis": "committer timestamp",
        "merges": "excluded",
    }


def collect_frequency(revision, end=None):
    shallow = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"], text=True
    ).strip()
    if shallow != "false":
        raise ValueError("Commit frequency requires full history (fetch-depth: 0)")
    resolved = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{revision}^{{commit}}"], text=True
    ).strip()
    output = subprocess.check_output(
        ["git", "log", "--no-merges", "--format=%H %ct", resolved], text=True
    )
    entries = [(line.split()[0], int(line.split()[1])) for line in output.splitlines()]
    result = summarize(entries, end or datetime.now(UTC))
    result["revision"] = resolved
    return result
