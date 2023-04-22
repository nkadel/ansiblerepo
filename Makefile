#
# Makefile - build wrapper for Ansible RPMs
#

#REOBASEE=http://localhost
REPOBASE=file://$(PWD)

#ANSIBLEPKGS+=ansible-openstack-modules-srpm

# EPEL based packages
#ANSIBLEPKGS+=ansible-freeipa-srpm
#ANSIBLEPKGS+=pyflakes-srpm
ANSIBLEPKGS+=pyproject-rpm-macros-srpm
ANSIBLEPKGS+=ansible-collections-openstack-srpm
#ANSIBLEPKGS+=python39-ansible-generator-srpm
ANSIBLEPKGS+=python3.11-babel-srpm
ANSIBLEPKGS+=python3.11-coverage-srpm
#ANSIBLEPKGS+=python39-docutils-srpm
#ANSIBLEPKGS+=python39-invoke-srpm
#ANSIBLEPKGS+=python39-lark-parser-srpm
#ANSIBLEPKGS+=python39-pretend-srpm
ANSIBLEPKGS+=python3.11-pytz-srpm
ANSIBLEPKGS+=python3.11-resolvelib-srpm
#ANSIBLEPKGS+=python39-ruamel-yaml-clib-srpm
ANSIBLEPKGS+=python3.11-unittest2-srpm

# Ansible repo based packages
ANSIBLEPKGS+=python3.11-markupsafe-srpm
#ANSIBLEPKGS+=python39-progress-srpm

# Build testing requirements
##ANSIBLEPKGS+=python39-asyncio-pool-sprm
##ANSIBLEPKGS+=antsibull-core-srpm
##ANSIBLEPKGS+=antsibull-default-srpm
##ANSIBLEPKGS+=antsibull-docs-srpm
##ANSIBLEPKGS+=antsibull-srpm

# Requires babel and markupsafe
ANSIBLEPKGS+=python3.11-jinja2-srpm

# Incompatible with RHEL
##ANSIBLEPKGS+=ansible-lint-srpm
##ANSIBLEPKGS+=python-ansible-compat-srpm

ANSIBLEPKGS+=python3.11-mock-srpm
##ANSIBLEPKGS+=python39-packaging-srpm
ANSIBLEPKGS+=ansible-core-2.14.x-srpm
# Stop building 2.12.x or 2.13.x by default, no need for it
##ANSIBLEPKGS+=ansible-core-2.13.x-srpm
##ANSIBLEPKGS+=ansible-core-2.12.x-srpm

# For RHEL 7
##ANSIBLEPKGS+=ansible-core-2.11.x-srpm
##ANSIBLEPKGS+=ansible-4.x-srpm

# Requires coverage
# Needed for jmespath
ANSIBLEPKGS+=python3.11-nose-srpm
#ANSIBLEPKGS+=python39-pbr-srpm

ANSIBLEPKGS+=python3.11-jmespath-srpm

# Stop building by defult
##ANSIBLEPKGS+=ansible-5.x-srpm
##ANSIBLEPKGS+=ansible-6.x-srpm
#ANSIBLEPKGS+=ansible-7.x-srpm

# Alternate names for 'ansible' packages, better indicates their content
##ANSIBLEPKGS+=ansible_collections-4.x-srpm
# Stop building by defult
###ANSIBLEPKGS+=ansible_collections-5.x-srpm
###ANSIBLEPKGS+=ansible_collections-6.x-srpm
#ANSIBLEPKGS+=ansible_collections-7.x-srpm

## python3.11
#ANSIBLEPKGS+=python3.119-ruamel-yaml-srpm

##ANSIBLEPKGS+=python39-setuptools_scm-srpm
##ANSIBLEPKGS+=python39-unittest2-srpm

##ANSIBLEPKGS+=python39-commentjson-srpm
##ANSIBLEPKGS+=python39-flake8-srpm
#
##ANSIBLEPKGS+=python39-pytest-forked-srpm
##ANSIBLEPKGS+=python39-pytest-xdist-srpm
#
ANSIBLEPKGS+=ansible-collection-ansible-netcommon-srpm
ANSIBLEPKGS+=ansible-collection-ansible-posix-srpm
ANSIBLEPKGS+=ansible-collection-ansible-utils-srpm
ANSIBLEPKGS+=ansible-collection-chocolatey-chocolatey-srpm
ANSIBLEPKGS+=ansible-collection-community-general-srpm
ANSIBLEPKGS+=ansible-collection-community-kubernetes-srpm
ANSIBLEPKGS+=ansible-collection-community-mysql-srpm
ANSIBLEPKGS+=ansible-collection-containers-podman-srpm
ANSIBLEPKGS+=ansible-collection-google-cloud-srpm

# Requires ruamel, not yet portable to older OS
#ANSIBLEPKGS+=ansible-collection-microsoft-sql-srpm
#ANSIBLEPKGS+=ansible-collection-netbox-netbox-srpm
#
#ANSIBLEPKGS+=ansible-pcp-srpm
#
# Has built-in ansible bundle reuirement
#ANSIBLEPKGS+=ansible-inventory-grapher-srpm

REPOS+=ansiblerepo/el/7
REPOS+=ansiblerepo/el/8
REPOS+=ansiblerepo/el/9
REPOS+=ansiblerepo/fedora/38
REPOS+=ansiblerepo/amazon/2

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

CFGS+=ansiblerepo-7-x86_64.cfg
CFGS+=ansiblerepo-8-x86_64.cfg
CFGS+=ansiblerepo-9-x86_64.cfg
CFGS+=ansiblerepo-f38-x86_64.cfg
# Amazon 2 config
CFGS+=ansiblerepo-amz2-x86_64.cfg

# /etc/mock version lacks python39 modules
CFGS+=centos-stream+epel-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos+epel-7-x86_64.cfg
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg
MOCKCFGS+=fedora-38-x86_64.cfg
MOCKCFGS+=amazonlinux-2-x86_64.cfg

all:: install

install:: $(CFGS)
install:: $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(#ANSIBLEPKGS)

# Actually put all the modules in the local repo
.PHONY: install clean getsrc build srpm src.rpm
install clean getsrc build srpm src.rpm::
	@for name in $(ANSIBLEPKGS); do \
	     (cd $$name && $(MAKE) $(MFLAGS) $@); \
	done  

# Git submodule checkout operation
# For more recent versions of git, use "git checkout --recurse-submodules"
#*-srpm::
#	@[ -d $@/.git ] || \
#	     git submodule update --init $@

# Dependencies of libraries on other libraries for compilation

#python39-commentjson-srpm:: python39-lark-parser-srpm
#python39-entrypoints-srpm:: python39-commentjson-srpm
#
#python39-flake8-srpm:: pyflakes-srpm
#
#python39-resolvelib-srpm:: python39-flake8-srpm
#python39-resolvelib-srpm:: python39-commentjson-srpm
#
#ansible-core-2.11.x-srpm:: python39-resolvelib-srpm
##ansible-core-2.12.x-srpm:: python39-resolvelib-srpm
#ansible-core-2.13.x-srpm:: python39-resolvelib-srpm
#
#ansible-4.x-srpm:: ansible-core-2.11.x-srpm
##ansible-5.x-srpm:: ansible-core-2.12.x-srpm
#ansible-6.x-srpm:: ansible-core-2.13.x-srpm

# Actually build in directories
.PHONY: $(ANSIBLEPKGS)
$(ANSIBLEPKGS)::
	(cd $@ && $(MAKE) $(MLAGS) install)

repodirs: $(REPOS) $(REPODIRS)
repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo_c -q `dirname $@`

.PHONY: cfg
cfg:: cfgs

.PHONY: cfgs
cfgs:: $(CFGS)
cfgs:: $(MOCKCFGS)


$(MOCKCFGS)::
	@echo Generating $@ from $?
	@echo "include('/etc/mock/$@')" | tee $@

centos-stream+epel-8-x86_64.cfg:: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "# Enable python39 modules" | tee -a $@
	@echo "config_opts['module_setup_commands'] = [ ('enable', 'python39'), ('enable', 'python39-devel') ]" | tee -a $@
	@echo "# Disable best" | tee -a $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@

ansiblerepo-7-x86_64.cfg: /etc/mock/centos+epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['yum.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/el/7/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

# packages-microsoft-com-prod added for /bin/pwsh
ansiblerepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "# Enable python39 modules" | tee -a $@
	@echo "config_opts['module_setup_commands'] = [ ('enable', 'python39'), ('enable', 'python39-devel') ]" | tee -a $@
	@echo "# Disable best" | tee -a $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/el/8/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '' | tee -a $@
	@echo '[packages-microsoft-com-prod]' | tee -a $@
	@echo 'name=packages-microsoft-com-prod' | tee -a $@
	@echo 'baseurl=https://packages.microsoft.com/rhel/8/prod/' | tee -a $@
	@echo 'enabled=0' | tee -a $@
	@echo 'gpgcheck=1' | tee -a $@
	@echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' | tee -a $@
	@echo '"""' | tee -a $@

# packages-microsoft-com-prod added for /bin/pwsh
ansiblerepo-9-x86_64.cfg: centos-stream+epel-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/el/9/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '' | tee -a $@
	@echo '[packages-microsoft-com-prod]' | tee -a $@
	@echo 'name=packages-microsoft-com-prod' | tee -a $@
	@echo 'baseurl=https://packages.microsoft.com/rhel/9/prod/' | tee -a $@
	@echo 'enabled=0' | tee -a $@
	@echo 'gpgcheck=1' | tee -a $@
	@echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' | tee -a $@
	@echo '"""' | tee -a $@

ansiblerepo-f38-x86_64.cfg: /etc/mock/fedora-38-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/fedora/38/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

ansiblerepo-rawhide-x86_64.cfg: /etc/mock/fedora-rawhide-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-rawhide-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/fedora/rawhide/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

ansiblerepo-amz2-x86_64.cfg: /etc/mock/amazonlinux-2-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-amz2-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/amz/2/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

repo: ansiblerepo.repo
ansiblerepo.repo:: Makefile ansiblerepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" | tee $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" | tee $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

ansiblerepo.repo::
	@cmp -s $@ /etc/yum.repos.d/$@ || \
	    diff -u $@ /etc/yum.repos.d/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(ANSIBLEPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean: clean
	rm -rf $(REPOS)
	rm -rf ansiblerepo
	@for name in $(ANSIBLEPKGS); do \
	    (cd $$name; git clean -x -d -f); \
	done

maintainer-clean: distclean
	rm -rf $(ANSIBLEPKGS)
	@for name in $(ANSIBLEPKGS); do \
	    (cd $$name; git clean -x -d -f); \
	done
