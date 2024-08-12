import json
import os
import sys
import time
from typing import Dict, List, Any

def parse_directory(directory: Dict[str, Any], show_hidden: bool = False, long_format: bool = False, reverse: bool = False, sort_by_time: bool = False, filter_option: str = None) -> List[Dict[str, Any]]:
    contents = directory.get("contents", [])
    
    if filter_option:
        if filter_option == "file":
            contents = [item for item in contents if "contents" not in item]
        elif filter_option == "dir":
            contents = [item for item in contents if "contents" in item]
        else:
            print(f"error: '{filter_option}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
            sys.exit(1)
    
    if not show_hidden:
        contents = [item for item in contents if not item.get("name","").startswith(".")]
    
    if sort_by_time:
        import pdb;pdb.set_trace()
        contents.sort(key=lambda x: x.get("time_modified",""))
    
    if reverse:
        contents.reverse()
    
    return contents

def print_directory_contents(contents: List[Dict[str, Any]], long_format: bool = False, human_readable: bool = False):
    for item in contents:
        if long_format:
            size = item.get("size",0)
            if human_readable:
                for unit in ['B', 'K', 'M', 'G']:
                    if size < 1024:
                        break
                    size /= 1024
                size_str = f"{size:.1f}{unit}"
            else:
                size_str = str(size)
            time_str = time.strftime('%b %d %H:%M', time.localtime(item.get("time_modified")))
            print(f"{item.get('permissions','')} {size_str:>4} {time_str} {item.get('name')}")
        else:
            print(item.get("name",""), end=" ")
    if not long_format:
        print()

def pyls(json_file: str, path: str = ".", show_hidden: bool = False, long_format: bool = False, reverse: bool = False, sort_by_time: bool = False, filter_option: str = None, human_readable: bool = False):
    with open(json_file, 'r') as file:
        directory = json.load(file)
    
    current_directory = directory
    
    if path != ".":
        parts = path.split(os.sep)
        for part in parts:
            found = False
            for item in current_directory["contents"]:
                if item["name"] == part:
                    current_directory = item
                    found = True
                    break
            if not found:
                print(f"error: cannot access '{path}': No such file or directory")
                return
    
    contents = parse_directory(current_directory, show_hidden, long_format, reverse, sort_by_time, filter_option)
    print_directory_contents(contents, long_format, human_readable)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Python implementation of the 'ls' command.")
    parser.add_argument("path", nargs="?", default=".", help="Directory or file to list.")
    parser.add_argument("-A", action="store_true", help="Do not ignore entries starting with .")
    parser.add_argument("-l", action="store_true", help="Use a long listing format")
    parser.add_argument("-r", action="store_true", help="Reverse order while sorting")
    parser.add_argument("-t", action="store_true", help="Sort by modification time")
    parser.add_argument("--filter", choices=["file", "dir"], help="Filter the results to show only files or directories")
    parser.add_argument("-H", "--human-readable", action="store_true", help="With -l, print sizes in human-readable format (e.g., 1K 234M 2G)")
    parser.add_argument("json_file", help="JSON file containing the directory structure.")
    
    args = parser.parse_args()
    
    pyls(args.json_file, args.path, args.A, args.l, args.r, args.t, args.filter, args.human_readable)

if __name__ == "__main__":
    main()
