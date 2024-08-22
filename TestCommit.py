import os
import subprocess

# Path to the file where we save the last processed commit ID
LAST_COMMIT_FILE = 'last_processed_commit.txt'

def get_last_processed_commit():
    # Read the last processed commit ID from the file, if it exists
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.readline().strip()
    return None

def save_last_processed_commit(commit_sha):
    # Save the current commit ID to the file
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(commit_sha + "\n")

def get_changed_files_since_commit(last_commit_sha):
    if last_commit_sha:
        try:
            # Run the git command to get changed files since the last commit
            result = subprocess.check_output(
                ['git', 'diff', '--name-only', last_commit_sha],
                universal_newlines=True
            )
            changed_files = result.strip().split('\n')
            return changed_files
        except subprocess.CalledProcessError as e:
            print(f"Error running git diff: {e}")
            return None
    else:
        print("No previous successful commit found.")
        return None

def filter_c_files(files):
    # Filter for .c files
    return [file for file in files if file.endswith('.c')]

if __name__ == "__main__":
    # Get the last successful commit from Jenkins environment variable
    current_commit_sha = os.getenv('GIT_PREVIOUS_SUCCESSFUL_COMMIT')

    # Get the last processed commit
    last_processed_commit_sha = get_last_processed_commit()

    # Check if this commit has already been processed
    if current_commit_sha == last_processed_commit_sha:
        print(f"Commit {current_commit_sha} has already been processed.")
    else:
        # Get the list of changed files since the last successful commit
        changed_files = get_changed_files_since_commit(last_processed_commit_sha)

        if changed_files:
            c_files = filter_c_files(changed_files)

            if c_files:
                # Save the current commit ID as the last processed commit
                save_last_processed_commit(current_commit_sha)

                # Output only the .c files
                for file in c_files:
                    print(file)
            else:
                print("No .c files to process.")
        else:
            print("No changed files found.")
