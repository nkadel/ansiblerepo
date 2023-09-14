#
# Makefile - build wrapper for Ansible RPMs
#

#REOBASEE=http://localhost
REPOBASE=file://$(PWD)

# EPEL buildable packages

#ANSIBLEPKGS+=ansible-openstack-modules-srpm
#ANSIBLEPKGS+=pyflakes-srpm
ANSIBLEPKGS+=ansible-collection-netcommon-srpm
ANSIBLEPKGS+=ansible-collections-openstack-srpm
ANSIBLEPKGS+=ansible-packaging-srpm
ANSIBLEPKGS+=pyproject-rpm-macros-srpm
ANSIBLEPKGS+=python3.11-babel-srpm
ANSIBLEPKGS+=python3.11-coverage-srpm
# Ansible repo based packages
ANSIBLEPKGS+=python3.11-markupsafe-srpm
ANSIBLEPKGS+=python3.11-resolvelib-srpm
ANSIBLEPKGS+=python3.11-ruamel-yaml-clib-srpm
ANSIBLEPKGS+=python3.11-unittest2-srpm

# Remaining packages require ansiblerepo
#ANSIBLEPKGS+=ansible-freeipa-srpm

ANSIBLEPKGS+=python3.11-pytz-srpm
# RHEL 3 and 9 lack this with python3.11
ANSIBLEPKGS+=python3.11-setuptools_scm-srpm
ANSIBLEPKGS+=python3.11-toml-srpm

# Build testing requirements
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
ANSIBLEPKGS+=ansible-core-2.15.x-srpm

# Needed for jmespath
ANSIBLEPKGS+=python3.11-nose-srpm

# Requires nose
ANSIBLEPKGS+=python3.11-jmespath-srpm

# Restrict to latest version
ANSIBLEPKGS+=ansible-8.x-srpm

# Alternate names for 'ansible' packages, better indicates their content
ANSIBLEPKGS+=ansible_collections-8.x-srpm

## python3.11
ANSIBLEPKGS+=python3.11-ruamel-yaml-srpm

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

ANSIBLEPKGS+=ansible-collection-netbox-netbox-srpm
ANSIBLEPKGS+=ansible-pcp-srpm

# Requires ruamel, not yet portable to older OS
# Requires rubygem modules
#ANSIBLEPKGS+=ansible-collection-microsoft-sql-srpm

# Has built-in ansible bundle reuirement
ANSIBLEPKGS+=ansible-inventory-grapher-srpm

REPOS+=ansiblerepo/el/8
REPOS+=ansiblerepo/el/9
REPOS+=ansiblerepo/fedora/38
REPOS+=ansiblerepo/amazon/2023

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

CFGS+=ansiblerepo-8-x86_64.cfg
CFGS+=ansiblerepo-9-x86_64.cfg
CFGS+=ansiblerepo-f38-x86_64.cfg
# Amazon 2 023config
CFGS+=ansiblerepo-amz2023-x86_64.cfg

# /etc/mock version lacks python3.11 modules
CFGS+=centos-stream+epel-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg
MOCKCFGS+=fedora-38-x86_64.cfg
MOCKCFGS+=amazonlinux-2023-x86_64.cfg

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
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@

# packages-microsoft-com-prod added for /bin/pwsh
ansiblerepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
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

ansiblerepo-amz2023-x86_64.cfg: /etc/mock/amazonlinux-2023-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'ansiblerepo-amz2023-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/amazon/2023/x86_64/' | tee -a $@
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
