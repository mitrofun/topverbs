import shutil
from git import Repo

from console import colored_print


def clone_to_dir(git_url, repo_dir):
    repo = Repo.clone_from(git_url, repo_dir)
    colored_print(f"Repository cloned to path: {repo.common_dir.strip('.git')}")


def delete_created_repo_dir(repo_dir):
    shutil.rmtree(repo_dir)
    colored_print(f"Remove temporary dir: {repo_dir}")
