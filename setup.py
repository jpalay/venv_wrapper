#!/usr/bin/env python
import os
import shutil

HOME = os.environ['HOME']


def create_dir(dir_path):
    """
    Create a directory, or don't if it already exists.  Fail if there's a
    file there instead.
    """
    print 'Creating directory {0}...'.format(dir_path),
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print 'done'
    elif os.path.isdir(dir_path):
        print 'directory already exists, skipping'
        return
    else:  # if file exists called dir_path
        print 'ERROR: {0} exists and is a file - aborting now'.format(dir_path)
        exit()


def copy_file(src, dst):
    """
    Copies file from src to dst, or doesn't if a file already exists at dst
    """
    print 'Copying file {0} to {1}...'.format(src, dst),
    if os.path.exists(dst):
        print 'file already exists, skipping'
        return
    else:
        shutil.copy(src, dst)
        print 'file copy successful'


def edit_bash_profile(add_path_dir):
    """
    Edits ~/.bash_profile to provide support for virtualenv wrapper.
    Adds ~/bin to system path if it's not there already, adds alias to make
    'activate' work properly, and provides support for autocomplete for
    the wrapper.
    """
    bash_profile = HOME + '/.bash_profile'

    bin_lines = ('\n# Adding ~/bin/ to PATH\n'
                 'PATH=$HOME/bin:$PATH\n')

    activate_lines = ('\n# Added for virtualenv wrapper\n'
                      'alias activate="source activate"\n'
                      'source ~/etc/activate-completion.bash\n')

    # Get contents of bash_profile, if it exists
    f = open(bash_profile, "a")
    contents = ''
    if os.path.exists(bash_profile):
        file_read = open(bash_profile, 'r')
        contents = file_read.read()
        file_read.close()

    # Add ~/bin/ to system path
    print 'Adding {0} to system path...'.format(add_path_dir),
    path = os.environ['PATH'].split(':')
    if (add_path_dir in path) or (bin_lines in contents):
        print '{0} already in system path, skipping this step'.format(
            add_path_dir)
    else:
        f.write(bin_lines)
        print 'done'

    # Add lines to support venv wrapper
    print 'Adding lines to {0} to support venv wrapper...'.format(bash_profile),
    if activate_lines in contents:
        print 'lines are already there!'
    else:
        f.write(activate_lines)
        print 'done'
    f.close()


def main():
    bin_dir = HOME + '/bin/'
    etc_dir = HOME + '/etc/'
    venvs_dir = HOME + '/venvs/'

    # Create directories
    create_dir(bin_dir)
    create_dir(etc_dir)
    create_dir(venvs_dir)

    # Copy files
    copy_file('mkvenv', bin_dir + 'mkvenv')
    copy_file('lsvenv', bin_dir + 'lsvenv')
    copy_file('rmvenv', bin_dir + 'rmvenv')
    copy_file('activate', bin_dir + 'activate')
    copy_file('activate-completion.bash', etc_dir + 'activate-completion.bash')

    # Make files executable
    os.chmod(bin_dir + 'mkvenv', 0755)
    os.chmod(bin_dir + 'lsvenv', 0755)
    os.chmod(bin_dir + 'rmvenv', 0755)
    os.chmod(bin_dir + 'activate', 0755)

    # Update bash_profile
    edit_bash_profile(bin_dir)
    print 'Success! Open a new terminal window to start using virtualenvs!'

if __name__ == '__main__':
    main()
