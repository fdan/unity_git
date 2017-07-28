

Using Git for Unity3d projects requires usage of Git LFS (large file storage).  Files to be tracked as LFS can be defined using either paths or extensions, and this is stored in the .gitattributes file.

However a problem with this is that it's not very artist friendly - git defaults to assuming no files are LFS, and the user has to opt-in to tell Git when a file is LFS.  Considering many CG artists are not familiar with version control, this is not a good idea.

This provides a git pre-commit hook, that tracks any file type not whitelisted as LFS.  This means artists cannot accidentally commit large media files as not-LFS, and the onus is on developers to whitelist any source code files they want to add.

setup_osx.sh and setup_windows.bat provide os native setup scripts, which will install the pre-commit hook after the repository is cloned.  The pre-commit hook is a simple bash script that executes pre-commit.py, so any changes made to pre-commit.py will be applied at the pre-commit stage.  
