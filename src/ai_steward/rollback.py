"""Git rollback utility for ai-steward.

Used by VERIFY when a change fails — restores a file to its last
committed state. V1 assumes the file existed at HEAD (guaranteed by
the clean-tree PRE-FLIGHT gate: IMPLEMENT can only modify tracked files).
"""

import subprocess
from pathlib import Path


def rollback_file(repo: Path, file: Path) -> None:
    """Restore a single file to its HEAD state via git checkout.

    Args:
        repo: Repository root (used as cwd for git).
        file: Path to the file to restore (absolute or relative to repo).

    Raises:
        subprocess.CalledProcessError: if git checkout fails (e.g. file
            has no committed version — should not happen given PRE-FLIGHT
            clean-tree gate, but surfaces clearly if it does).
    """
    try:
        rel = file.relative_to(repo)
    except ValueError:
        rel = file  # already relative — pass as-is

    subprocess.run(
        ["git", "checkout", "HEAD", "--", str(rel)],
        cwd=repo,
        check=True,
        capture_output=True,
    )
