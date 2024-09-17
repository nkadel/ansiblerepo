ansiblerepo
==========-

Wrapper for SRPM building tools for ansibl9 8.x and ansible-core 2.16
using python3.11. Alma 7 does not have python3.11 easily available,
so it's no longer supported here for Ansible servers.

Pre-install ansible-packaging for mock compilation
--------------------------------------------------

'make getsrc' relies on macros from ansible-packaging


Stop installing 'ansible' package
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

Python 3.12 or later required
=============================

ansible-core and the matching ansible now require python
3.12 or better.

ansible-core 2.15 requires importlib-resources, which is built into
python 3.12

Building ansible
===============

Ideally, install "mock" and use that to build for both RHEL and up,
through 9 and Fedora 40. Run these commands at the top directory.

* make getsrc # Get source tarvalls for all SRPMs

* make cfgs # Create local .cfg configs for "mock".
* * alma+epel-8-x86_64.cfg # Used for some Makefiles
* * alma+epel-9-x86_64.cfg # Used for some Makefiles
* * fedora-40-x86_64.cfg # Used for some Makefiles
* * ansiblerepo-8-x86_64.cfg
* * ansiblerepo-9-x86_64.cfg
* * ansiblerepo-f40-x86_64.cfg

* make repos # Creates local local yum repositories in $PWD/ansiblerepo
* * ansiblerepo/el/8
* * ansiblerepo/el/9
* * ansiblerepo/fedora/40

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
