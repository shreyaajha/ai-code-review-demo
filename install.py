import os
import subprocess
import sys


def run(command):
    subprocess.run(command, check=True)


def main():

    print("Installing AI Code Reviewer...\n")

    if not os.path.exists(".git"):
        print("Error: Not inside a Git repository.")
        sys.exit(1)

    run(["git", "config", "core.hooksPath", "hooks"])

    hook = "hooks/pre-push"

    if os.path.exists(hook):
        run(["chmod", "+x", hook])

    print("Git hook installed successfully.")
    print("AI Code Reviewer is ready.")


if __name__ == "__main__":
    main()