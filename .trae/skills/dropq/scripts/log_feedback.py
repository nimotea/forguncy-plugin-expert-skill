import argparse
import json
import datetime
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Log feedback to a JSONL file.')
    # Changed nargs to '+' to handle cases where shell splits the JSON string by spaces
    parser.add_argument('data', nargs='+', help='JSON string or path to a JSON file')
    parser.add_argument('--log-file', default='feedback_logs.jsonl', help='Name of the log file (default: feedback_logs.jsonl)')
    
    args = parser.parse_args()
    
    json_str = ""
    
    # Strategy 1: Check if the first argument is a valid file path
    # (Only if only one argument is provided, to avoid ambiguity)
    if len(args.data) == 1 and os.path.isfile(args.data[0]):
        try:
            with open(args.data[0], 'r', encoding='utf-8') as f:
                json_str = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)
    else:
        # Strategy 2: Treat arguments as a split JSON string
        # Join them back with spaces (this approximates the original string if shell split by space)
        json_str = " ".join(args.data)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw input was: {json_str}")
        print("Tip: For complex JSON, consider writing it to a temporary file and passing the file path instead.")
        sys.exit(1)

    # Add timestamp
    data['timestamp'] = datetime.datetime.now().isoformat()
    
    # Define log file path (workspace root)
    # Current script: .trae/skills/dropQ/scripts/log_feedback.py
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    log_file_path = os.path.join(workspace_root, args.log_file)
    
    # Append to file
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
        print(f"Successfully logged feedback to {log_file_path}")
    except Exception as e:
        print(f"Error writing to log file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
