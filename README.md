ansiblerepo
==========-

Wrapper for SRPM building tools for ansibl9 8.x and ansible-core 2.16
using python3.11. Almalinux 7 does not have python3.11 easily available,
so it's no longer supported here for Ansible servers.

Stop installing ansible package
-------------------------------

The "ansible" package itself is now pointless. It contains more than
100 distinct ansible_collections entries, takes up at least 300 Meg
gig of disk to provide only a few modules that an ansible server might
actually use. Those modules are better provided by installing
ansible-core and using the "ansible-galaxy" tool to install them as
needed.

Modules in ansible
------------------

The actual list of ansible collection modules in the ansible tarball
is in the release specific file of the ansible-build-date git repo,
for example:

* https://github.com/ansible-community/ansible-build-data/blob/main/8/ansible-8.0.0.deps

Python 3.11 or later required
=============================

ansible-core 2.14.x and the matching ansible-7.x now require python
3.8 or better, and are not supportable RHEL 7. So the older
ansible-core 2.11.x and ansible-4.x have been abandoned.

ansible-core 2.15 requires importlib-resources, which is built into
python 3.11

RHEL dnf modularity breakage
============================

The dnf modularity of RHEL 8 has repeatedly broken
installation of both build components and of dependencies to build
ansible-core. The updates to python3.11 have helped.

Building ansible
===============

Ideally, install "mock" and use that to build for both RHEL and up,
through 9 and Fedora 38. Run these commands at the top directory.

* make getsrc # Get source tarvalls for all SRPMs

* make cfgs # Create local .cfg configs for "mock".
* * almalinux+epel-8-x86_64.cfg # Used for some Makefiles
* * almalinux+epel-9-x86_64.cfg # Used for some Makefiles
* * fedora-38-x86_64.cfg # Used for some Makefiles
* * ansiblerepo-8-x86_64.cfg
* * ansiblerepo-9-x86_64.cfg
* * ansiblerepo-f38-x86_64.cfg

* make repos # Creates local local yum repositories in $PWD/ansiblerepo
* * ansiblerepo/el/8
* * ansiblerepo/el/9
* * ansiblerepo/fedora/38

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

ansible has strong dependencies on other python modules that may, or
may not, be available in a particular OS. These are listed in the
Makefile

Installing Ansible
=================

The relevant yum repository is built locally in ansiblereepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Ansible RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPG signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

ansible_collections Rather Than ansible Package
===============================================

There are tools here to build an "ansible_collections" package rather
than ansible, more consistently named and deployed than the ansible
package itself but with precisely the same ansible collections modules.

		Nico Kadel-Garcia <nkadel@gmail.com>
