"""run_all_corpus.py - Run the unchanged run_all.py pipeline on a separate corpus.

common.py hardcodes repos/, data/, reports/ and repos.txt, which hold the
already-analysed Corpus 2. This launcher points those paths at corpus-specific
siblings and then hands control to run_all.main(), so every phase runs exactly
as written and the existing folders are never read or written:

  repos_<corpus>.txt   repository list (input)
  repos_<corpus>/      clones
  data_<corpus>/       CSVs
  reports_<corpus>/    reports and charts/

The override works because each phase does ``from common import DATA_DIR, ...``
and run_all imports the phases lazily, so they bind the patched values; the
helpers iter_repo_dirs()/read_repo_list() read common's globals at call time.
Shared infrastructure (developer-tools/, tools/, .tmp/, .env) stays as is.

Examples:
    python scripts/run_all_corpus.py --corpus govbr
    python scripts/run_all_corpus.py --corpus govbr --only dataset,ml,report
"""
from __future__ import annotations

import argparse
import sys

import common


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run run_all.py with corpus-specific folders.")
    parser.add_argument("--corpus", required=True,
                        help="suffix of repos_<corpus>.txt and the output folders")
    args, run_all_args = parser.parse_known_args()

    root = common.ROOT
    repos_txt = root / f"repos_{args.corpus}.txt"
    if not repos_txt.exists():
        parser.error(f"{repos_txt.name} not found")

    common.REPOS_TXT = repos_txt
    common.REPOS_DIR = root / f"repos_{args.corpus}"
    common.DATA_DIR = root / f"data_{args.corpus}"
    common.REPORTS_DIR = root / f"reports_{args.corpus}"
    common.CHARTS_DIR = common.REPORTS_DIR / "charts"
    common.DB_PATH = root / f"metrics_{args.corpus}.db"
    for d in (common.REPOS_DIR, common.DATA_DIR, common.REPORTS_DIR,
              common.CHARTS_DIR):
        d.mkdir(parents=True, exist_ok=True)

    common.log.info("Corpus '%s': list=%s repos=%s data=%s reports=%s",
                    args.corpus, repos_txt.name, common.REPOS_DIR.name,
                    common.DATA_DIR.name, common.REPORTS_DIR.name)

    import run_all
    sys.argv = [run_all.__file__, *run_all_args]
    return run_all.main()


if __name__ == "__main__":
    sys.exit(main())
