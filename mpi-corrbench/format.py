#!/usr/bin/env python3

import os
import subprocess
import re
import sys

FORMAT_TIMEOUT = 15

def apply_clang_format(file):
    try:
        subprocess.check_output(
            f'clang-format -style=\'{{ColumnLimit: 100000,'
            f'AllowAllArgumentsOnNextLine: false, '
            f'AllowShortFunctionsOnASingleLine: false, '
            f'AllowShortLoopsOnASingleLine: false, '
            f'AllowShortCaseLabelsOnASingleLine: false, '
            f'BreakBeforeBraces: Allman, '
            f'BinPackArguments: true, '
            f'PenaltyBreakBeforeFirstCallParameter: 100000 }}\' -i {file}',
            stderr=subprocess.DEVNULL, shell=True, text=True, timeout=FORMAT_TIMEOUT
        )
        
        result = subprocess.check_output(
            f'gcc -fpreprocessed -dD -E {file}',
            stderr=subprocess.DEVNULL, shell=True, text=True, timeout=FORMAT_TIMEOUT
        )
        
        pattern = r"^#\ \d+\ \".*\""
        lines = result.splitlines(keepends=True)[0:]
        lines = [line if not re.match(pattern, line) else "\n" for line in lines]
        lines.insert(0, '# 1 "{}"'.format(file))


        with open(file, 'w') as f:
            f.writelines(lines)

    except subprocess.CalledProcessError as e:
        print(f"Error applying clang-format to '{file}': {e}")
    except subprocess.TimeoutExpired:
        print(f"Timeout while formatting '{file}'")

def main(directory_path):
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory path.")
        return

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx')):
                file_path = os.path.abspath(os.path.join(root, file))
                apply_clang_format(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
      sys.exit("No directory argument!")
    directory_path = str(sys.argv[1])
    main(os.path.abspath(directory_path))

