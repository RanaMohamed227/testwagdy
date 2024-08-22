import os
import subprocess

# File to store the last processed commit and the list of changed files
LAST_COMMIT_FILE = 'last_processed_commit.txt'
CHANGED_FILES_FILE = 'changed_files.txt'

def get_last_processed_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.readline().strip()
    return None

def save_last_processed_commit(commit_sha):
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(commit_sha + "\n")

def save_changed_files(changed_files):
    with open(CHANGED_FILES_FILE, 'w') as f:
        for file in changed_files:
            f.write(f"{file}\n")

def get_changed_files_since_commit(last_commit_sha):
    try:
        if last_commit_sha:
            # Get all commits since the last processed one and list changed files
            result = subprocess.check_output(
                ['git', 'diff', '--name-only', last_commit_sha + '..HEAD'],
                universal_newlines=True
            )
        else:
            # If no previous commit is found, get the changes from the initial commit
            result = subprocess.check_output(
                ['git', 'diff', '--name-only', 'HEAD'],
                universal_newlines=True
            )

        changed_files = result.strip().split('\n')
        return [file for file in changed_files if file.endswith('.c') or file.endswith('.h')]
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []

if __name__ == "__main__":
    current_commit_sha = os.getenv('GIT_COMMIT')

    last_processed_commit_sha = get_last_processed_commit()

    changed_files = get_changed_files_since_commit(last_processed_commit_sha)

    if changed_files:
        print("Changed .h and .c files since last processed commit:")
        for file in changed_files:
            print(file)

        # Save the current commit ID and the list of changed files
        save_last_processed_commit(current_commit_sha)
        save_changed_files(changed_files)
    else:
        print("No changed .c or .h files found.")
