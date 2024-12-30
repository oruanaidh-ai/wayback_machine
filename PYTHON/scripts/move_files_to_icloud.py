import traceback
import os
import sys
import shutil
import subprocess
import time
import pickle
from pathlib import Path
import numpy as np
from operator import itemgetter


def mycopy(src, dst):

    subprocess.call(["rsync", "-aur", src, dst])

class Counter:

    def __init__(self, root):
        self.memo = {}
        self.dirs = {}
        self.root = os.path.abspath(root)

        if os.path.exists('memo.pkl') and os.path.exists('dirs.pkl'):
            with open('memo.pkl', 'rb') as fp:
                self.memo = pickle.load(fp)
            with open('dirs.pkl', 'rb') as fp:
                self.dirs = pickle.load(fp)
        else:
            self.countOnDisk()
            with open('memo.pkl', 'wb') as fp:
                pickle.dump(self.memo, fp)
            with open('dirs.pkl', 'wb') as fp:
                pickle.dump(self.dirs, fp)


    def countOnDisk(self, f=None):

        if f is None: f = self.root

        fullpath = str(os.path.abspath(f))
        if fullpath in self.memo:
            return self.memo[(fullpath)]

        if os.path.isdir(fullpath):
            self.dirs[fullpath] = 1
            size = np.sum([self.countOnDisk(os.path.join(fullpath, sub)) for sub in os.listdir(f)])
        else:
            size = os.stat(fullpath).st_size

        self.memo[fullpath] = size
        if len(self.memo) % 1000 == 0:
            print( f'{len(self.memo)} files' )
            sys.stdout.flush()

        return size

    def countInMemo(self, f=None):
        if f is None: f = self.root

        fullpath = str(os.path.abspath(f))
        if fullpath in self.memo:
            return self.memo[(fullpath)]

        if os.path.isdir(fullpath):
            size = np.sum([self.memo.get(os.path.join(fullpath, sub), 0) for sub in os.listdir(f) if os.path.join(fullpath, sub) in self.memo])
        else:
            size = self.memo.get(fullpath, 0)

        return size

        

    @staticmethod
    def parent(f):
        return str(Path(f).parent.absolute())


    def pre_dir(self, f):
        fullpath = str(os.path.abspath(f))
        if self.root in fullpath:
            return fullpath[len(self.root)+1:]
        else:
            raise ValueError(f'{f} is not a subdirectory of {self.root}')
                             


    def remove(self, f):

        fullpath = os.path.abspath(f)
        if fullpath not in self.memo:
            print(f'{fullpath} is not recorded')
            return

        
        if os.path.isdir(fullpath):
            for x in  os.listdir(fullpath):
                path = os.path.join(fullpath, x)
                if path in self.memo: self.remove(path)
        else:
            delta = self.memo[fullpath]

            parent = Counter.parent(fullpath)
            while parent != self.root:
                self.memo[parent] -= delta
                parent = Counter.parent(parent)
            else:
                self.memo[self.root] -= delta

        del self.memo[fullpath]
        if fullpath in self.dirs: del self.dirs[fullpath]


    def total(self, f=None):
        if f is None: f = self.root
        return self.memo[f]


    def directories(self):
        # Sort into order by filesize
        tuples = sorted(count_filesize.memo.items(), key=itemgetter(1))

        return [(d, v) for (d, v) in tuples if d in self.dirs]


def test1():
    #count_filesize = Counter('/Volumes/My Book')
    count_filesize = Counter('/Users/oruanaidh/Downloads2')

    print
    print(f'Before = {count_filesize.total()}')

    dir = '/Users/oruanaidh/Downloads2/DaisyDisk.app/Contents'
    print(f'Decrement = {count_filesize.total(dir)}')
    count_filesize.remove(dir)
    print(f'After = {count_filesize.total()}')

    print(count_filesize.pre_dir('/Users/oruanaidh/Downloads2/tvnjviewer-2/nossh'))
    print(Counter.parent('/Users/oruanaidh/Downloads2/tvnjviewer-2/nossh'))
    print(Counter.parent(Counter.parent('/Users/oruanaidh/Downloads2/DaisyDisk.app/Content')))


if __name__=='__main__':
    count_filesize = Counter('/Volumes/Elements')
    #count_filesize = Counter('/Users/oruanaidh/Downloads2')
    thresh = 1e7
    tgtdir = '/Users/oruanaidh/iCloud/Archives/Elements'
    content = 0
    while True:
        directories = count_filesize.directories()
        indx, *_ = np.where([x[1] > thresh for x in directories])
        if len(indx) == 0: break
        d, _ = directories[indx[0]]
        prefix = count_filesize.pre_dir(d)
        target =  os.path.join(tgtdir, prefix)
        print(f'Selected {d} to go to {target}')
        sys.stdout.flush()
        content += count_filesize.total(d)
        try:
            os.mkdirs(target)
        except:
            pass

        for attempt in range(10):
            try:
                shutil.copytree(d,  target, copy_function=mycopy, ignore_dangling_symlinks=True, dirs_exist_ok=True)
                break
            except:
                pass #traceback.print_exc()
        else:
            print (f'Multiple attempts failed at copying {d} to {target}')
        
        count_filesize.remove(d)
        try:
            shutil.rmtree(d)
        except FileNotFoundError:
            traceback.print_exc()

        print(f'Removed {d}')
        if content > thresh:
            print('Sleep')
            time.sleep(content/thresh*10)
            content = 0

        

