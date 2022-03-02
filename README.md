ansiblerepo
==========-

Wrapper for SRPM building tools for ansible 5.x and ansible-core 2.12
using python3. CentOs 7 has a working version published via EPEL, but
it's out of date, so this provides an RPM based upgrade path.

Modules in ansible
==================

The actual list of modules in the ansible tarball is in the release
specific file of the ansible-build-date git repo, for example:

* https://github.com/ansible-community/ansible-build-data/blob/main/5/ansible-5.4.0.deps

Upstream renaming
=================

The ansible maintainers decided to replace the ansible named module
with a bundle of dozens of ansible_collection modules, and fragment
off the primary ansible repo package as ansible-core. This makes
ansible require both, and makes it at least 20 times as large overall.

Python 3.8 compatibility split
==============================

ansible-core 2.12.x and the matching ansible-5.x now require python
3.8 or better, and are not supportable yet for RHEL 7 or 8. So the
older ansible-core 2.11.x and ansible-4.x are being built in parallel
until further notice.

Building ansible
===============

Ideally, install "mock" and use that to build for both RHEL 6 and RHEL

* make cfgs # Create local .cfg configs for "mock".
* * epel-7-x86_64.cfg # Used for some Makefiles

* make repos # Creates local local yum repositories in $PWD/ansiblerepo
* * ansiblerepo/el/7

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

ansible has strong dependencies on other python modules that may, or may not,
be available in a particular OS. These are listed in the Makefile

Installing Ansible
=================

The relevant yum repository is built locally in ansiblereepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Ansible RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPF signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

ansible_collections Rather Than ansible Package
===============================================

There are tools here to build an "ansible_collections" package rather
than ansible, more consistently named and deployed than the ansible
package itself but with precise the same ansible collections modules.


		Nico Kadel-Garcia <nkadel@gmail.com>
