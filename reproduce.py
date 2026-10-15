"""Run the complete synthetic lab without external network access."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent


def run(repo, module, *args, expected=0):
    result = subprocess.run([sys.executable, str(ROOT / repo / module), *map(str, args)],
                            capture_output=True, text=True, timeout=30)
    if result.returncode != expected:
        raise RuntimeError(f"{repo}: expected exit {expected}, got {result.returncode}: {result.stderr}")
    return json.loads(result.stdout)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    auth = run("ghostlayer-authwatch", "authwatch.py", ROOT / "ghostlayer-authwatch/examples/events.jsonl")
    require(auth["event_count"] == 9 and auth["alert_count"] == 3, "unexpected authentication result")
    require({a["rule"] for a in auth["alerts"]} == {"repeated_failures", "success_after_failures", "multiple_accounts_targeted"}, "unexpected authentication rules")
    weak = run("ghostlayer-headercheck", "headercheck.py", "--headers", ROOT / "ghostlayer-headercheck/examples/weak.txt")
    hardened = run("ghostlayer-headercheck", "headercheck.py", "--headers", ROOT / "ghostlayer-headercheck/examples/hardened.txt")
    require(weak["finding_count"] == 5 and hardened["finding_count"] == 0, "unexpected header results")
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        site = directory / "site"
        shutil.copytree(ROOT / "ghostlayer-integrity/examples/site", site)
        manifest = directory / "baseline.json"
        run("ghostlayer-integrity", "integrity.py", "baseline", site, manifest)
        clean = run("ghostlayer-integrity", "integrity.py", "check", site, manifest)
        require(not any(clean[k] for k in ("added", "removed", "modified")), "fresh tree is not clean")
        with (site / "index.html").open("a", encoding="utf-8") as stream:
            stream.write("\n<!-- known training change -->\n")
        changed = run("ghostlayer-integrity", "integrity.py", "check", site, manifest, expected=1)
        require(changed["modified"] == ["index.html"], "known modification was not identified")
    print("Lab passed: 9 events, 3 alerts, 5 weak-header findings, 0 hardened-header findings, 1 integrity modification.")


if __name__ == "__main__":
    main()
