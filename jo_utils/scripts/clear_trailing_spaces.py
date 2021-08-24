import os
import sys
import shutil
from tempfile import NamedTemporaryFile

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write(f'python {sys.argv[0]} filename\n')
        sys.exit(1)


    try:
        with NamedTemporaryFile(delete=False) as out_clean:
            with open(out_clean.name, 'w') as out:
                with open(sys.argv[1]) as fp:
                    for line in fp:
                        line = line.rstrip()
                        out.write(f'{line}\n')
        shutil.copy(out_clean.name, sys.argv[1])
    finally:
        os.unlink(out_clean.name)
