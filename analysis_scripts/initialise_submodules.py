import subprocess
from loguru import logger

def run(*args):
    return subprocess.check_call(['git'] + list(args))

def commit(message):
    run("add", ".")
    run("commit", "-m", message)
    run("push", "origin", "master")


def branch(branch_name):

    run("checkout", "-b", f'analysis_{branch_name}')
    run("push", "-u", "origin", f'analysis_{branch_name}')


def add_submodule(repo_name, branch='master', user='dezeraecox-experiments', local_path='experimental_data/'):
    subprocess.Popen(['git', 'submodule', 'add', '-b', branch, f'https://github.com/{user}/{repo_name}.git', f'{local_path}{repo_name}'])


def add_submodule_branches(branch_name):
    run('submodule', "foreach", "git", "checkout",
        "-b", f'analysis_{branch_name}')
    run('submodule', "foreach", "git", "push",
        "-u", "origin", f'analysis_{branch_name}')


def create_submodules(repositories, branch_name):

    for repository in repositories:
        try:
            repo, branch = repository.split(':')
        except:
            branch = 'master'
        add_submodule(repo_name=repository, branch=branch)

    commit("Adding submodules")
    add_submodule_branches(branch_name)

    logger.info(f'Submodules created and set to branch {branch_name}')

"""--------------------------------------------------------------------"""
"""
Automate the process of collecting experiments as submodules into an analysis folder, then create a new branch for the combined analysis.

To specify specific branch for submodules to be collected, include repo:branch in list else each repo will be added from the master branch.
"""

repositories = [
    'experiment'
]

branch_name = 'test'

create_submodules(repositories, branch_name)
