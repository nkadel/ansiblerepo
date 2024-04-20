#
# Makefile - build wrapper for Ansible RPMs
#

#REOBASEE=http://localhost
REPOBASE=file://$(PWD)

# EPEL buildable packages

#ANSIBLEPKGS+=ansible-openstack-modules-srpm
ANSIBLEPKGS+=ansible-collection-azure-azcollection-srpm
ANSIBLEPKGS+=ansible-collection-netcommon-srpm
ANSIBLEPKGS+=ansible-collections-openstack-srpm
ANSIBLEPKGS+=ansible-packaging-srpm

#ANSIBLEPKGS+=doctest-srpm

ANSIBLEPKGS+=python3.12-babel-srpm
ANSIBLEPKGS+=python3.12-coverage-srpm
ANSIBLEPKGS+=python3.12-gast-srpm
ANSIBLEPKGS+=python3.12-jmespath-srpm
ANSIBLEPKGS+=python3.12-pytz-srpm
ANSIBLEPKGS+=python3.12-six-srpm

# Ansible repo based packages
ANSIBLEPKGS+=python3.12-markupsafe-srpm
ANSIBLEPKGS+=python3.12-resolvelib-srpm

# Remaining packages require ansiblerepo
# Requires six
ANSIBLEPKGS+=python3.12-unittest2-srpm

ANSIBLEPKGS+=ansible-freeipa-srpm

# Requires babel and markupsafe
ANSIBLEPKGS+=python3.12-jinja2-srpm

# RHEL 8 and 9 lack this with python3.12
ANSIBLEPKGS+=python3.12-setuptools_scm-srpm
ANSIBLEPKGS+=python3.12-toml-srpm

# Build testing requirements
##ANSIBLEPKGS+=antsibull-core-srpm
##ANSIBLEPKGS+=antsibull-default-srpm
##ANSIBLEPKGS+=antsibull-docs-srpm
##ANSIBLEPKGS+=antsibull-srpm

# Incompatible with RHEL
##ANSIBLEPKGS+=ansible-lint-srpm

# Requires six and unittest2
ANSIBLEPKGS+=python3.12-mock-srpm

# Requires jinj2 and mock
ANSIBLEPKGS+=ansible-core-srpm

# Restrict to latest version
ANSIBLEPKGS+=ansible-srpm

# Alternate names for 'ansible' packages, better indicates their content
#ANSIBLEPKGS+=ansible_collections-srpm

## Requires ruamel-yaml-glibc if not in bootstrap
ANSIBLEPKGS+=python3.12-ruamel-yaml-srpm
# Requires ruamel-yaml
ANSIBLEPKGS+=python3.12-ruamel-yaml-clib-srpm

#
ANSIBLEPKGS+=ansible-collection-ansible-netcommon-srpm
# Updated in EPEL
#ANSIBLEPKGS+=ansible-collection-ansible-posix-srpm
#ANSIBLEPKGS+=ansible-collection-ansible-utils-srpm
#ANSIBLEPKGS+=ansible-collection-chocolatey-chocolatey-srpm
#ANSIBLEPKGS+=ansible-collection-community-general-srpm

ANSIBLEPKGS+=ansible-collection-community-kubernetes-srpm
ANSIBLEPKGS+=ansible-collection-community-mysql-srpm
# Requires jinja2
ANSIBLEPKGS+=ansible-collection-containers-podman-srpm
ANSIBLEPKGS+=ansible-collection-google-cloud-srpm

ANSIBLEPKGS+=ansible-collection-netbox-netbox-srpm
ANSIBLEPKGS+=ansible-pcp-srpm

# Requires ruamel-yaml
ANSIBLEPKGS+=ansible-collection-microsoft-sql-srpm

# Has built-in ansible bundle reuirement
ANSIBLEPKGS+=ansible-inventory-grapher-srpm

REPOS+=ansiblerepo/el/8
REPOS+=ansiblerepo/el/9
REPOS+=ansiblerepo/fedora/40
REPOS+=ansiblerepo/amazon/2023

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

CFGS+=ansiblerepo-8-x86_64.cfg
CFGS+=ansiblerepo-9-x86_64.cfg
CFGS+=ansiblerepo-f40-x86_64.cfg
# Amazon 2 023config
CFGS+=ansiblerepo-amz2023-x86_64.cfg

# /etc/mock version lacks python3.12 modules
MOCKCFGS+=centos-stream+epel-next-8-x86_64.cfg
MOCKCFGS+=centos-stream+epel-next-9-x86_64.cfg
MOCKCFGS+=fedora-40-x86_64.cfg
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
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@

# packages-microsoft-com-prod added for /bin/pwsh
ansiblerepo-8-x86_64.cfg: ./centos-stream+epel-next-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'ansiblerepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
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
ansiblerepo-9-x86_64.cfg: centos-stream+epel-next-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
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

ansiblerepo-f40-x86_64.cfg: ./fedora-40-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['root'] = 'ansiblerepo-f{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[ansiblerepo]' | tee -a $@
	@echo 'name=ansiblerepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/fedora/40/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

ansiblerepo-rawhide-x86_64.cfg: ./fedora-rawhide-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
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

ansiblerepo-amz2023-x86_64.cfg: ./amazonlinux-2023-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
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
