import os
import subprocess

# Files to store the last processed commit and the list of changed files
LAST_COMMIT_FILE = 'last_processed_commit.txt'
CHANGED_FILES_FILE = 'changed_files.txt'

def get_last_processed_commit():
    # Check if the last commit file exists and read the commit SHA
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.readline().strip()
    return None

def save_last_processed_commit(commit_sha):
    # Save the latest commit SHA to the last processed commit file
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(commit_sha + "\n")

def save_changed_files(changed_files):
    # Save the list of changed files to the changed files text file
    with open(CHANGED_FILES_FILE, 'w') as f:
        for file in changed_files:
            f.write(f"{file}\n")

def get_changed_files_since_commit(last_commit_sha):
    try:
        # Get all commits since the last processed one and list changed files
        if last_commit_sha:
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

        # Filter the files to only include .c and .h files
        changed_files = result.strip().split('\n')
        return [file for file in changed_files if file.endswith('.c') or file.endswith('.h')]
    
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []

if __name__ == "__main__":
    # Get the current commit SHA from the environment
    current_commit_sha = os.getenv('GIT_COMMIT')

    # Get the last processed commit SHA from the file
    last_processed_commit_sha = get_last_processed_commit()

    # Get the changed .c and .h files since the last processed commit
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
