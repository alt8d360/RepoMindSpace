import sys
import os
import json
from utils.parser import LocalParser

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_parser.py <path_to_repo>")
        sys.exit(1)

    repo_path = sys.argv[1]
    print(f"Initializing parser for: {os.path.abspath(repo_path)}\n")

    parser = LocalParser(repo_path)
    parsed_data = parser.parse()

    print(f"Successfully parsed {len(parsed_data)} files.\n")
    
    print("Files extracted:")
    for f in parsed_data:
        print(f" - {f['path']} ({f['language']}, {f['size']} bytes)")

    # Save a sample to test_output.json for inspection
    output_file = "test_output.json"
    with open(output_file, "w", encoding="utf-8") as out:
        # Strip content for the summary JSON to keep it readable, just store lengths
        summary = [{"path": f["path"], "language": f["language"], "content_length": len(f["content"])} for f in parsed_data]
        json.dump(summary, out, indent=2)
    
    print(f"\nSaved summary to {output_file}")

if __name__ == "__main__":
    main()
