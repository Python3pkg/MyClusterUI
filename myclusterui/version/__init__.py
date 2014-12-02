# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

__all__ = ("get_git_version")

from subprocess import Popen, PIPE
import os
from pkg_resources import Requirement, resource_filename

def call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--tags', '--exact-match'],
                  stdout=PIPE, stderr=PIPE)
        return_code = p.wait()
        p.stderr.close()
        line = p.stdout.readlines()[0]
        if return_code == 0:
            return line.strip()
        else:
            p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            line = p.stdout.readlines()[0] 
            return line.strip()

    except:
        return None


def read_release_version():
    try:
        filename = resource_filename(Requirement.parse("MyClusterUI"),"share/MyClusterUI/RELEASE-VERSION")
        if os.path.isfile(filename):
            f = open(filename, 'r')
        else:
            filename = resource_filename(Requirement.parse("MyClusterUI"),"RELEASE-VERSION")
            f = open(filename, 'r')
        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=4):
    # Read in the version that's currently in RELEASE-VERSION.

    release_version = read_release_version()

    # First try to get the current version using “git describe”.

    version = call_git_describe(abbrev)

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.

    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.

    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.

    if version != release_version:
        write_release_version(version)

    # Finally, return the current version.

    return version


if __name__ == "__main__":
    print get_git_version()
