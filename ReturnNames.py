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

def filter_c_files(files):
    # Filter for .c files
    return [file for file in files if file.endswith('.c')]

if __name__ == "__main__":
    # Get the list of changed files since the last successful commit
    changed_files = get_changed_files_since_commit(last_commit_sha)
    
    if changed_files:
        c_files = filter_c_files(changed_files)
        
        if c_files:
            for file in c_files:
                print(file)  # Output only the .c files
        else:
            print("No .c files to process.")
    else:
        print("No changed files found.")
