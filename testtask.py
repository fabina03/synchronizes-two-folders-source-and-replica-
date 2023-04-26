import os
import filecmp
import shutil

class Files:
    def __init__(self, name=''):
        self.name = name
        self.file_list = []
        self.file_copied_count = 0
        self.folder_copied_count = 0

    def add_file(self, file):
        self.file_list.append(file)

    def copy_file(self):
        fileListLength = len(self.file_list)
        for file in self.file_list:
            if self.file_list.index(file) < len(self.file_list) - 1: 
                file2 = self.file_list[self.file_list.index(file) + 1]
                print( '\nCopy from Folder 1 '+ ' to Folder 2:')
                self._compare_directories(file.root_path, file2.root_path)
    
    def _compare_directories(self, left, right):
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self._compare_directories(os.path.join(left, d), os.path.join(right, d))
        if comparison.left_only:
            self._copy(comparison.left_only, left, right)
        if comparison.right_only:
            self._copy(comparison.right_only, right, left)
        left_newer = []
        right_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                l_modified = os.stat(os.path.join(left, d)).st_mtime
                r_modified = os.stat(os.path.join(right, d)).st_mtime
                if l_modified > r_modified:
                    left_newer.append(d)
                else:
                    right_newer.append(d)
        self._copy(left_newer, left, right)
        self._copy(right_newer, right, left)

    def _copy(self, file_list, src, dest):
        for f in file_list:
            srcpath = os.path.join(src, os.path.basename(f))
            if os.path.isdir(srcpath):
                shutil.copytree(srcpath, os.path.join(dest, os.path.basename(f)))
                self.folder_copied_count = self.folder_copied_count + 1
                print( 'Copied directory \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
            else:
                shutil.copy2(srcpath, dest)
                self.file_copied_count = self.file_copied_count + 1
                print( 'Copied \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')


class Node: 
    def __init__(self, path, name=''):
        self.name = name
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)


if __name__ == "__main__":
    my_dispatch = Files(' ')
    folder1 = Node('C:/Users/Puf/Desktop/source', 'folder1')
    folder2 = Node('C:/Users/Puf/Desktop/replica', 'folder2')
    my_dispatch.add_file(folder1)
    my_dispatch.add_file(folder2)
    my_dispatch.copy_file()
    print( 'Total files copied ' + str(my_dispatch.file_copied_count))
    print( 'Total folders copied ' + str(my_dispatch.folder_copied_count))