ansiblerepo
==========-

Wrapper for SRPM building tools for ansible 6.x and ansible-core 2.13
using python3. CentOS 7 has ansible from before it was split
ansible_collecitons, which is deliberately mislabeled as "ansible",
and ansible-core. This provides an RPM based update path.

Stop installing ansible package
-------------------------------

Ehe ansible package is now pointless. It contains roughly 100 distinct
ansible_collections, takes up half a gig of disk to provide only a few
modules that an ansible server might actually use. Those modules are
better provided by installing ansible-core and using the "ansible
galaxy" tool to install them as needed.

Modules in ansible
------------------

The actual list of ansible collection modules in the ansible tarball
is in the release specific file of the ansible-build-date git repo,
for example:

* https://github.com/ansible-community/ansible-build-data/blob/main/6/ansible-6.6.0.deps

Python 3.8 compatibility split
==============================

ansible-core 2.13.x and the matching ansible-6.x now require python
3.8 or better, and are not supportable yet for RHEL 7 or 8. So the
older ansible-core 2.11.x and ansible-4.x are being built in parallel
until further notice.

ansible-core 2.13 requires jinja2 > 3.0.0, which creates dependencies
on sphinx more recent than RHEL provides. Therefore only the Fedora
versions of ansible-core 2.13 will provide the sphinx generated
documentation.

RHEL dnf modularity breakage
============================

The dnf modularity of RHEL 8 has completely broken dnf based
installation of both build components and of dependencies to build
ansible-core. The multiple versions of python38-pytest and
python38-markupsafe, combined with the need for updated versions of
python38-jinja2 for ansible-core-2.13, mean that, make it impossible to build these tools with "mock" until further notice.

Building ansible
===============

Ideally, install "mock" and use that to build for both RHEL 6 and RHEL

* make getsrc # Get source tarvalls for all SRPMs

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
for locally built components. Generating GPG signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

ansible_collections Rather Than ansible Package
===============================================

There are tools here to build an "ansible_collections" package rather
than ansible, more consistently named and deployed than the ansible
package itself but with precisely the same ansible collections modules.

		Nico Kadel-Garcia <nkadel@gmail.com>
