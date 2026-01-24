import argparse
import json
import datetime
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Log feedback to a JSONL file.')
    # Changed nargs to '*' to handle cases where shell splits the JSON string by spaces, or no args (stdin)
    parser.add_argument('data', nargs='*', help='JSON string, path to a JSON file, or empty for stdin')
    # parser.add_argument('--log-file', default='feedback_logs.jsonl', help='Name of the log file (default: feedback_logs.jsonl)')
    parser.add_argument('--project-root', help='Absolute path to the project root directory where logs should be saved')
    parser.add_argument('--delete', action='store_true', help='Delete the input file after successful logging (only if input is a file)')
    
    args = parser.parse_args()
    
    log_filename = 'feedback_logs.jsonl'
    input_is_file = False
    input_file_path = None
    
    json_str = ""
    
    # Strategy 0: Check Stdin if no args
    if not args.data:
        if not sys.stdin.isatty():
            try:
                # Force stdin to use utf-8 in Windows
                if sys.platform == 'win32':
                    sys.stdin.reconfigure(encoding='utf-8')
                json_str = sys.stdin.read()
                
                # Handle BOM if present (PowerShell might add it)
                if json_str.startswith('\ufeff'):
                    json_str = json_str[1:]
            except Exception as e:
                print(f"Error reading from stdin: {e}")
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
    # Strategy 1: Check if the first argument is a valid file path
    # (Only if only one argument is provided, to avoid ambiguity)
    elif len(args.data) == 1 and os.path.isfile(args.data[0]):
        input_is_file = True
        input_file_path = args.data[0]
        print(f"Reading input from file: {input_file_path}")
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                json_str = f.read()
                if not json_str.strip():
                    print("Error: Input file is empty.")
                    sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)
    else:
        # Strategy 2: Treat arguments as a split JSON string
        # Join them back with spaces (this approximates the original string if shell split by space)
        json_str = " ".join(args.data)

    if not json_str.strip():
        print("Error: Input JSON is empty.")
        sys.exit(1)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Truncate raw input if too long
        display_str = json_str if len(json_str) < 200 else json_str[:200] + "..."
        print(f"Raw input was: {display_str}")
        print("Tip: For complex JSON, consider writing it to a temporary file and passing the file path instead.")
        sys.exit(1)

    # Add timestamp
    data['timestamp'] = datetime.datetime.now().isoformat()
    
    # Define log file path
    # Priority 1: Use provided --project-root
    if args.project_root:
        workspace_root = os.path.abspath(args.project_root)
        if not os.path.exists(workspace_root):
            print(f"Warning: Provided project root does not exist: {workspace_root}")
    else:
        # Priority 2: Use Current Working Directory (CWD) as the workspace root
        # This assumes the user/agent is running the command from the project root, which is the standard practice.
        workspace_root = os.getcwd()
        
    log_file_path = os.path.join(workspace_root, log_filename)
    print(f"Target log file path: {log_file_path}")
    
    # Append to file
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
        print(f"Successfully logged feedback to {log_file_path}")
        
        # Auto-delete input file if requested
        if input_is_file and args.delete and input_file_path:
            try:
                os.remove(input_file_path)
                print(f"Deleted input file: {input_file_path}")
            except Exception as e:
                print(f"Warning: Failed to delete input file: {e}")
                
    except Exception as e:
        print(f"Error writing to log file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
