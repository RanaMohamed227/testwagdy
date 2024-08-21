import os
import subprocess

# Get the last successful commit from Jenkins environment variable
last_commit_sha = os.getenv('GIT_PREVIOUS_SUCCESSFUL_COMMIT')

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

def filter_files(files, extensions):
    # Filter files that match the given extensions
    return [file for file in files if any(file.endswith(ext) for ext in extensions)]

if __name__ == "__main__":
    # Get the list of changed files since the last successful commit
    changed_files = get_changed_files_since_commit(last_commit_sha)
    
    if changed_files:
        # Filter for .h and .c files only
        filtered_files = filter_files(changed_files, ['.h', '.c'])

        if filtered_files:
            print("Changed .h and .c files since last successful commit:")
            for file in filtered_files:
                print(file)
        else:
            print("No .h or .c files found.")
    else:
        print("No changed files found.")
