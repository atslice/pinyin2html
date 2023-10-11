import os
import shutil
from zipfile import ZipFile


from pathlib import Path
import re
import errno

def makedirs(_dir):
    """
        make dirs if _dir not exists
    """
    if not os.path.exists(_dir):
        os.makedirs(_dir)

def dump_str(_file, _str):
    """dump str to file"""
    with open(_file, 'w') as writer:
        writer.write(_str)

class Files():
    """
        methods for files operation
    """

    @staticmethod
    def append_file(file_write, file_read):  #  把一个文件追加到另一个文件末尾
        """
            the content of file_read will be added to the end of file_write
        """
        with open(file_write, 'ab') as f:
            f.write(open(file_read, 'rb').read())

    @staticmethod
    def remove_dirs(_dir):
        """
            _dir can be non-empty
        """
        # Delete everything reachable from the directory named in 'top',
        # assuming there are no symbolic links.
        # CAUTION:  This is dangerous!  For example, if top == '/', it
        # could delete all your disk files.
        import os
        top = _dir
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        try:
        # if Directory not empty, exception occurs
            os.removedirs(_dir)
        except BaseException as e:
            logs = 'Fial to remove dir = %s, %s' %(_dir, format(e))
            print(logs)
    


    @staticmethod
    def merge(outfile, infiles):
        """
            Args:
                outfile: str, the path to the output file
                infiles: list, files in order to be merged into one file
        """
        if not type(infiles) is list:
            raise TypeError('infiles must be list type.')
        with open(outfile, 'wb') as output:
            for infile in infiles:
                if not os.path.exists(infile):
                    raise ValueError('The element in list must be file.')
                # print('appending %s' % infile)
                with open(infile, 'rb') as reader:
                    output.write(reader.read())

    @staticmethod
    def get_files(path):
        """
            get files list in the first level depth of the path
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files]


    @staticmethod
    def get_zipfiles(path):
        """
            get files list in the first level depth of the path, with filter: "the extension is zip"
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 4 and re.match(r'[Zz][Ii][Pp]', Path(_file).suffix[1:]))]

    @staticmethod
    def get_mobi_files(path):
        """
            get files list in the first level depth of the path, with filter: "the extension is mobi"
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 5 and re.match(r'[Mm][Oo][Bb][Ii]', Path(_file).suffix[1:]))]

    @staticmethod
    def get_html_files(path):
        """
            get files list in the first level depth of the path, with filter: "the extension is html"
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 5 and re.match(r'[Hh][Tt][Mm][Ll]', Path(_file).suffix[1:]))]
            
    @staticmethod
    def get_html_files_filter(path, pattern):
        """
            get files list in the first level depth of the path, with filter: "the extension is html" and filter: pattern of basename
            if nothing matched, return empty list
            Args:
                path: str, the path to directory
                pattern: str, the re pattern for basename
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 5 and re.match(r'[Hh][Tt][Mm][Ll]', Path(_file).suffix[1:]) and (pattern in os.path.basename(_file)))]            

    @staticmethod
    def get_zip_files(path):
        """
            get files list in the first level depth of the path, with filter: "the extension is zip"
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 4 and re.match(r'[Zz][Ii][Pp]', Path(_file).suffix[1:]))]

    @staticmethod
    def rude_move_files(files, dest_path):
        """
            BE CAREFUL, source files would be removed anyway
            Move files to dest_path, not overwritten destination files, remove source files anyway
            Args:
                files: list, which elements is the path to file
                dest_path: str
        """
        for _file in files:
            try:
                print('moving file %s to %s' % (_file, dest_path))
                shutil.move(_file, dest_path)
            except BaseException:  # if destination file already exists, remove source file directly
                os.remove(_file)

    @staticmethod
    def move_files(src_path, dest_path):
        """
            Move files from src_path to dest_path
            Args:
                src_path: str
                dest_path: str
        """
        files =  Files.get_files(src_path)
        Files.rude_move_files(files, dest_path)

    @staticmethod
    def move_mobi_files(src_path, dest_path):
        """
            Move mobi files from src_path to dest_path
            Args:
                src_path: str
                dest_path: str
        """
        files =  Files.get_mobi_files(src_path)
        Files.rude_move_files(files, dest_path)

    @staticmethod
    def move_html_files(src_path, dest_path):
        """
            Move html files from src_path to dest_path
            Args:
                src_path: str
                dest_path: str
        """
        files =  Files.get_html_files(src_path)
        Files.rude_move_files(files, dest_path)

    @staticmethod
    def move_zip_files(src_path, dest_path):
        """
            Move zip files from src_path to dest_path
            Args:
                src_path: str
                dest_path: str
        """
        files =  Files.get_zip_files(src_path)
        Files.rude_move_files(files, dest_path)

    @staticmethod
    def get_splited_files(path):
        """
            get files list in the first level depth of the path, with filter: "the extension is three-digits"
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (len(Path(_file).suffix) == 4 and re.match(r'[0-9][0-9][0-9]', Path(_file).suffix[1:]))]
        """
                nfiles = []
                for _file in files:
                    nfile = os.path.join(root, _file)
                    # filter here
                    print(nfile)
                    suffix = Path(nfile).suffix  # with leading dot .
                    # print(Path(nfile).suffix)
                    if re.match(r'[0-9][0-9][0-9]', suffix[1:]):  # only three digits from 000 to 999
                        print('match: %s' % suffix[1:])
                        nfiles.append(nfile)
                return nfiles
        """

    @staticmethod
    def get_all_lv1_files(path):
        """
            get files list in the first level depth of the path
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files]

    @staticmethod
    def get_lv1_files(path, suffix):
        """
            get files list in the first level depth of the path, with filter: "the suffix of the file is the same with parameter suffix"
            Args:
                path: str, the directory to search
                suffix: str, the suffix, only files with the exact suffix will be returned
            if nothing matched, return empty list
        """

        for rdf in os.walk(path):
            root = rdf[0]
            # dirs = rdf[1]
            files = rdf[2]
            if root == path:
                # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
                return [os.path.join(root, _file) for _file in files if (Path(_file).suffix == suffix)]
 

    @staticmethod
    def get_lv2_files(path):
        """
            get files list in the second level depth of the path
            if nothing matched, return empty list
            Return:
                dict, lv1_dir_basename as key, files list within as value
        """
        # print('path = %s' % path)
        name_files = {}

        for rdf in os.walk(path):
            root = rdf[0]
            dirs = rdf[1]
            files = rdf[2]
            # print('\r\nroot = %s, dirs = %s , files = %s ' %(root, dirs, files))
            #if '/' in root:
            #    print('root contains /')
            #if root == path:
            #    continue # skip first level
            dir_basename = os.path.basename(root)
            # print('dir_basename = %s' % dir_basename)
            join_name = os.path.join(path, dir_basename)
            # print('join_name = %s' % join_name)
            # print('root = %s' % root)
            if join_name == root:
                # print('lv1 basename %s' % dir_basename)
                files_abspath = [os.path.abspath(os.path.join(root, _file)) for _file in files]
                name_files[dir_basename] = files_abspath
        return name_files

    @staticmethod
    def groupfiles(files):
        """
            group files list if they have the same file name without extension, and sort them by extension
            Args:
                files: list, files list
            Return:
                a list, which elements are a dict, {'filename': str, 'files': list}
                if len(files) == 0, return empty list
        """
        # sort list
        # find the first unmatch
        if not type(files) is list:
            raise TypeError('Param files must be list.')
        if len(files) == 0:
            return []
        sfiles = files[:] # make a copy
        sfiles.sort()  # sorts the list ascending by default
        groups = [] # list to return
        common_name = ''
        onefile = []
        for sfile in sfiles:
            basename = Path(sfile).stem
            print('groupfiles(): %s' % os.path.basename(sfile))
            if common_name == '':
                common_name = basename
                onefile = []
            if basename == common_name:
                onefile.append(sfile)
            else:
                onedict = {'filename': common_name, 'files': onefile}
                groups.append(onedict)
                common_name = basename
                onefile = [sfile]
        onedict = {'filename': common_name, 'files': onefile}
        groups.append(onedict)
        return groups

    @staticmethod
    def unzip(_file, _dir):
        """
            Args:
                _file: str, path to the zip file
                _dir: str, the local directory to place the unziped files/directories
            Return:
                boolean: True if no exception, otherwise False
        """
        try:
            with ZipFile(_file, 'r') as zip_ref:
                zip_ref.extractall(_dir)
        except BaseException as err:
            print('unzip file %s error: %s' % (_file, format(err)))
            return False
        else:
            return True

    @staticmethod
    def delete(_file):
        """
            delete a file
        """
        try:
            os.remove(_file)
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

    @staticmethod
    def deletes(files):
        """
            delete files in list
        """
        for _file in files:
            Files.delete(_file)

    @staticmethod
    def mkdir(path):
        path = path.strip()
        path = path.rstrip("/")
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False

    @staticmethod
    def removetrees(path):
        """
            empty the directory but remains the directory itself
        """
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def main():
    pass

if __name__ == "__main__":
    main()
