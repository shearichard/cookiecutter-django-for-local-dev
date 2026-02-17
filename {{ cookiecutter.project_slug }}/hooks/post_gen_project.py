import os
import subprocess
import sys
from pathlib import Path

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
WORK_DIR = "{{ cookiecutter.work_dir }}"
CREATE_VENV = "{{ cookiecutter.create_virtualenv }}".lower() in ("y", "yes", "true", "1")

def run(cmd, cwd=None):
    print(f"==> {cmd}")
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}: {cmd}")
        sys.exit(e.returncode)


def main():
    # Resolve working directory
    work_dir = Path(WORK_DIR).expanduser()
    if not work_dir.is_absolute():
        work_dir = Path.cwd().joinpath(work_dir)

    # Create directory if necessary
    work_dir.mkdir(parents=True, exist_ok=True)
    print(f"Using work directory: {work_dir}")

    # Move generated project into work_dir if we aren't already there
    project_root = Path.cwd()
    target_root = work_dir.joinpath(PROJECT_SLUG)

    if project_root != target_root:
        # Ensure target_root parent exists
        target_root.parent.mkdir(parents=True, exist_ok=True)
        print(f"Moving project from {project_root} to {target_root}")
        # On the filesystem, move the entire tree
        import shutil
        shutil.move(str(project_root), str(target_root))
        project_root = target_root

    # Change into the working directory / project directory
    os.chdir(project_root)
    print(f"Changed directory to: {project_root}")

    if not CREATE_VENV:
        print("Skipping Pipenv environment creation (create_virtualenv != y).")
        return

    # Initialise pipenv, install dependencies
    # This assumes `pipenv` is on PATH
    run("pipenv --python python") # or specify a version, e.g. pipenv --python 3.12
    run(
        "pipenv install "
        "django "
        {{ cookiecutter.project_slug }}/hooks/post_gen_project.py
        "django-environ "
        "django-extensions "
        "django-easy-logging "
        "flake8 "
        "black"
    )

    print("\nEnvironment ready.")
    print("To activate the virtualenv, run:\n")
    print(" cd {}".format(project_root))
    print(" pipenv shell\n")


if __name__ == "__main__":
    main()
