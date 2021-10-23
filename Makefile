#
# Makefile - build wrapper for Ansible RPMs
#

#REOBASEE=http://localhost
REPOBASE=file://$(PWD)

ANSIBLEPKGS+=python-lark-parser-srpm
ANSIBLEPKGS+=python-commentjson-srpm

ANSIBLEPKGS+=python-entrypoints-srpm
ANSIBLEPKGS+=pyflakes-srpm
ANSIBLEPKGS+=python-flake8-srpm
ANSIBLEPKGS+=python-resolvelib-srpm

ANSIBLEPKGS+=ansible-core-srpm

ANSIBLEPKGS+=ansible-collections-openstack-srpm

ANSIBLEPKGS+=ansible-srpm

REPOS+=ansiblerepo/el/7
REPOS+=ansiblerepo/el/8
REPOS+=ansiblerepo/fedora/34
REPOS+=ansiblerepo/amz/2

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

CFGS+=ansiblerepo-7-x86_64.cfg
CFGS+=ansiblerepo-8-x86_64.cfg
CFGS+=ansiblerepo-f34-x86_64.cfg
# Amazon 2 config
CFGS+=ansiblerepo-amz2-x86_64.cfg

# /et/cmock version lacks EPEL
CFGS+=epel-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-7-x86_64.cfg
MOCKCFGS+=epel-8-x86_64.cfg
MOCKCFGS+=fedora-34-x86_64.cfg
#MOCKCFGS+=amazonlinux-2-x86_64.cfg

all:: install

install:: $(CFGS)
install:: $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(ANSIBLEPKGS)

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

python-commentjson-srpm:: python-lark-parser-srpm
python-entrypoints-srpm:: python-commentjson-srpm

python-flake8-srpm:: pyflakes-srpm

python-resolvelib-srpm:: python-flake8-srpm
python-resolvelib-srpm:: python-commentjson-srpm

ansible-core-srpm:: python-resolvelib-srpm
ansible-srpm:: ansible-core-srpm

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

epel-8-x86_64.cfg:: /etc/mock/epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@echo >> $@
	@echo '# epel-8 configs lack EPEL, added here' >> $@
	@echo "include('templates/epel-8.tpl')" >> $@

ansiblerepo-7-x86_64.cfg: /etc/mock/epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/ansiblerepo-7-x86_64/g' $@
	@echo >> $@
	@echo "Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[ansiblerepo]' >> $@
	@echo 'name=ansiblerepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1s' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=20' >> $@
	@echo '"""' >> $@

# packages-microsoft-com-prod added for /bin/pwsh
ansiblerepo-8-x86_64.cfg: epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-8-x86_64/ansiblerepo-8-x86_64/g' $@
	@echo >> $@
	@echo "Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[ansiblerepo]' >> $@
	@echo 'name=ansiblerepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1s' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=20' >> $@
	@echo '' >> $@
	@echo '[packages-microsoft-com-prod]' >> $@
	@echo 'name=packages-microsoft-com-prod' >> $@
	@echo 'baseurl=https://packages.microsoft.com/rhel/8/prod/' >> $@
	@echo 'enabled=1' >> $@
	@echo 'gpgcheck=1' >> $@
	@echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' >> $@
	@echo '"""' >> $@

ansiblerepo-f34-x86_64.cfg: /etc/mock/fedora-34-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-34-x86_64/ansiblerepo-f34-x86_64/g' $@
	@echo >> $@
	@echo "Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[ansiblerepo]' >> $@
	@echo 'name=ansiblerepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/fedora/34/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1s' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=20' >> $@
	@echo '"""' >> $@

ansiblerepo-rawhide-x86_64.cfg: /etc/mock/fedora-rawhide-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-rawhide-x86_64/ansiblerepo-rawhide-x86_64/g' $@
	@echo >> $@
	@echo "Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[ansiblerepo]' >> $@
	@echo 'name=ansiblerepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/fedora/rawhide/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1s' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=20' >> $@
	@echo '"""' >> $@

ansiblerepo-amz2-x86_64.cfg: /etc/mock/amazonlinux-2-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/amz-2-x86_64/ansiblerepo-amz2-x86_64/g' $@
	@echo >> $@
	@echo "Disabling 'best=' for $@"
	@sed -i '/^best=/d' $@
	@echo "best=0" >> $@
	@echo "config_opts['dnf.conf'] += \"\"\"" >> $@
	@echo '[ansiblerepo]' >> $@
	@echo 'name=ansiblerepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/ansiblerepo/amz/2/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1s' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo 'priority=20' >> $@
	@echo '"""' >> $@

$(MOCKCFGS)::
	ln -sf /etc/mock/$@ $@

repo: ansiblerepo.repo
ansiblerepo.repo:: Makefile ansiblerepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
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


