import re
import os
import tempfile
import shutil
import sys
from MBIutils import *

import subprocess

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

        #lines = result.splitlines(keepends=True)[1:]
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

class Tool(AbstractTool):
    def identify(self):
        return "MPI-Arg-Tracer"

    def ensure_image(self):
        pass

    def build(self, rootdir, cached=True):
        pass


    def run(self, execcmd, filename, binary, id, timeout, batchinfo):
        cachefile = f'{binary}_{id}'
        os.environ["MPI_ARG_TRACE_FILE_TARGET"] = filename
        os.environ["LD_PRELOAD"] = os.environ["MPI_ARG_TRACER_LIB"]
        
        execcmd = re.sub("mpirun", f'mpirun --oversubscribe', execcmd) # FIXME: oversubcribe for CI
        execcmd = re.sub('\${EXE}', f'./{binary}', execcmd)
        execcmd = re.sub('\$zero_buffer', "", execcmd)
        execcmd = re.sub('\$infty_buffer', "", execcmd)

        buildcmd=f"OMPI_CC=clang mpicc {filename} -g -o {binary}"

        temp_file = filename + "-mpi-args-trace.tmp"
        with open(filename, 'rb') as src_file, open(temp_file, 'wb') as dst_file:
            shutil.copyfileobj(src_file, dst_file)

        apply_clang_format(os.path.abspath(filename))

        ran = run_cmd(
                buildcmd=buildcmd,
                execcmd=execcmd,
                cachefile=cachefile,
                filename=filename,
                binary=binary,
                timeout=timeout,
                batchinfo=batchinfo)

        with open(temp_file, 'rb') as src_file, open(filename, 'wb') as dst_file:
            shutil.copyfileobj(src_file, dst_file)
        os.remove(temp_file)


    def parse(self, cachefile):
        return 'OK'

    def is_correct_diagnostic(self, test_id, res_category, expected, detail):
        return True
