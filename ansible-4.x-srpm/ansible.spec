# Created by pyp2rpm-3.3.7
%global pypi_name ansible
%global pypi_version 4.8.0

#
# If we should enable docs building
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with docs

#
# If we should enable checks
# Currently we cannot until we get a stack of needed packages added and a few bugs fixed
#
%bcond_with checks

# Disable debugionfo package, the submodule generation mishandles this
%define debug_package %{nil}

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Radically simple IT automation

License:        GPLv3+
URL:            https://ansible.com/
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz

BuildRequires:  ansible-core < 2.12
BuildRequires:  ansible-core >= 2.11.6
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
# manually added
BuildRequires:  python%{python3_pkgversion}-cryptography
BuildRequires:  python%{python3_pkgversion}-resolvelib
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

%description
|PyPI version| |Docs badge| |Chat badge| |Build Status| |Code Of Conduct|
|Mailing Lists| |License|**************Ansible is a radically simple IT
automation system. It handles configuration management, application deployment,
cloud provisioning, ad-hoc task execution, network automation, and multi-node
orchestration. Ansible makes complex changes like zero-downtime rolling updates
with load...

Requires:       ansible-core < 2.12
Requires:       ansible-core >= 2.11.6

%package -n %{pypi_name}-doc
Summary:        ansible documentation
%description -n %{pypi_name}-doc
Documentation for ansible

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

grep -rl '#!/usr/bin/env python$' . | grep '\.py$' | while read name; do
    echo Fixing bare '#!/usr/bin/env python' in: $name
    sed -i "s|#!/usr/bin/env python$|#!/usr/bin/env python3|g" "$name"
done

grep -rl '#!/usr/bin/python$' . | grep '\.py$' | while read name; do
    echo Fixing bare '#!/usr/bin/env python' in: $name
    sed -i "s|#!/usr/bin/python$|#!/usr/bin/python3|g" "$name"
done

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build-%{python3_version} ansible_collections/sensu/sensu_go/docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%if %{with checks}
%check
%{__python3} setup.py test
%endif

%files
%doc README.rst
%doc ansible_collections/amazon/aws/README.md
%doc ansible_collections/ansible/netcommon/README.md
%doc ansible_collections/ansible/posix/.azure-pipelines/README.md
%doc ansible_collections/ansible/posix/README.md
%doc ansible_collections/ansible/utils/README.md
%doc ansible_collections/ansible/windows/README.md
%doc ansible_collections/ansible/windows/tests/integration/targets/win_copy/files-different/vault/readme.txt
%doc ansible_collections/arista/eos/README.md
%doc ansible_collections/awx/awx/README.md
%doc ansible_collections/awx/awx/tools/roles/template_galaxy/templates/README.md.j2
%doc ansible_collections/azure/azcollection/README.md
%doc ansible_collections/check_point/mgmt/README.md
%doc ansible_collections/chocolatey/chocolatey/README.md
%doc ansible_collections/chocolatey/chocolatey/plugins/README.md
%doc ansible_collections/cisco/aci/.pytest_cache/README.md
%doc ansible_collections/cisco/aci/README.md
%doc ansible_collections/cisco/aci/tests/unit/module_utils/.pytest_cache/README.md
%doc ansible_collections/cisco/asa/README.md
%doc ansible_collections/cisco/intersight/README.md
%doc ansible_collections/cisco/intersight/misc/README.md
%doc ansible_collections/cisco/intersight/plugins/README.md
%doc ansible_collections/cisco/ios/README.md
%doc ansible_collections/cisco/iosxr/README.md
%doc ansible_collections/cisco/meraki/README.md
%doc ansible_collections/cisco/mso/README.md
%doc ansible_collections/cisco/nso/README.md
%doc ansible_collections/cisco/nxos/README.md
%doc ansible_collections/cisco/ucs/README.md
%doc ansible_collections/cisco/ucs/misc/README.md
%doc ansible_collections/cisco/ucs/plugins/README.md
%doc ansible_collections/cisco/ucs/releases/README.md
%doc ansible_collections/cloudscale_ch/cloud/README.md
%doc ansible_collections/community/aws/README.md
%doc ansible_collections/community/aws/tests/integration/targets/connection_aws_ssm/aws_ssm_integration_test_setup/README.md
%doc ansible_collections/community/aws/tests/integration/targets/connection_aws_ssm/aws_ssm_integration_test_teardown/README.md
%doc ansible_collections/community/azure/.azure-pipelines/README.md
%doc ansible_collections/community/azure/README.md
%doc ansible_collections/community/crypto/.azure-pipelines/README.md
%doc ansible_collections/community/crypto/README.md
%doc ansible_collections/community/digitalocean/README.md
%doc ansible_collections/community/docker/.azure-pipelines/README.md
%doc ansible_collections/community/docker/README.md
%doc ansible_collections/community/fortios/README.md
%doc ansible_collections/community/general/.azure-pipelines/README.md
%doc ansible_collections/community/general/README.md
%doc ansible_collections/community/general/tests/integration/targets/setup_flatpak_remote/README.md
%doc ansible_collections/community/google/README.md
%doc ansible_collections/community/grafana/README.md
%doc ansible_collections/community/hashi_vault/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_cert_content/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_localenv_docker/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_localenv_gha/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_tinyproxy_server/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_configure/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_legacy/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server_cert/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server_download/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_test_plugins/README.md
%doc ansible_collections/community/hrobot/README.md
%doc ansible_collections/community/kubernetes/README.md
%doc ansible_collections/community/kubernetes/tests/integration/targets/kubernetes/README.md
%doc ansible_collections/community/kubernetes/tests/integration/targets/kubernetes/library/README.md
%doc ansible_collections/community/kubevirt/README.md
%doc ansible_collections/community/kubevirt/plugins/README.md
%doc ansible_collections/community/libvirt/.azure-pipelines/README.md
%doc ansible_collections/community/libvirt/README.md
%doc ansible_collections/community/mongodb/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_auth/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_config/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_install/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_linux/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_mongod/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_mongos/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_repository/README.md
%doc ansible_collections/community/mongodb/roles/mongodb_selinux/README.md
%doc ansible_collections/community/mysql/README.md
%doc ansible_collections/community/mysql/plugins/README.md
%doc ansible_collections/community/network/.azure-pipelines/README.md
%doc ansible_collections/community/network/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_backup/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_bgp/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_command/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_conditional_command/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_conditional_template/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_config/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_facts/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_image/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_rollback/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_save/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_showrun/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_template/README.md
%doc ansible_collections/community/network/tests/integration/targets/cnos_vlag/README.md
%doc ansible_collections/community/network/tests/integration/targets/enos_command/README.md
%doc ansible_collections/community/network/tests/integration/targets/enos_config/README.md
%doc ansible_collections/community/network/tests/integration/targets/enos_facts/README.md
%doc ansible_collections/community/okd/README.md
%doc ansible_collections/community/okd/molecule/default/README.md
%doc ansible_collections/community/postgresql/.azure-pipelines/README.md
%doc ansible_collections/community/postgresql/README.md
%doc ansible_collections/community/proxysql/README.md
%doc ansible_collections/community/proxysql/plugins/README.md
%doc ansible_collections/community/proxysql/roles/proxysql/README.md
%doc ansible_collections/community/rabbitmq/.azure-pipelines/README.md
%doc ansible_collections/community/rabbitmq/README.md
%doc ansible_collections/community/routeros/README.md
%doc ansible_collections/community/skydive/README.md
%doc ansible_collections/community/sops/README.md
%doc ansible_collections/community/sops/tests/integration/targets/var_sops/README.md
%doc ansible_collections/community/vmware/README.md
%doc ansible_collections/community/windows/README.md
%doc ansible_collections/community/windows/tests/integration/targets/win_lineinfile/files/expectations/99_README.md
%doc ansible_collections/community/zabbix/README.md
%doc ansible_collections/community/zabbix/roles/zabbix_agent/README.md
%doc ansible_collections/community/zabbix/roles/zabbix_javagateway/README.md
%doc ansible_collections/community/zabbix/roles/zabbix_proxy/README.md
%doc ansible_collections/community/zabbix/roles/zabbix_server/README.md
%doc ansible_collections/community/zabbix/roles/zabbix_web/README.md
%doc ansible_collections/containers/podman/README.md
%doc ansible_collections/cyberark/conjur/README.md
%doc ansible_collections/cyberark/conjur/project/roles/testrole/README.md
%doc ansible_collections/cyberark/conjur/roles/conjur_host_identity/README.md
%doc ansible_collections/cyberark/conjur/roles/conjur_host_identity/tests/.pytest_cache/README.md
%doc ansible_collections/cyberark/conjur/tests/conjur_variable/.pytest_cache/README.md
%doc ansible_collections/cyberark/pas/README.md
%doc ansible_collections/cyberark/pas/custom-cred-types/cyberark-pas-restapi/README.md
%doc ansible_collections/dellemc/enterprise_sonic/README.md
%doc ansible_collections/dellemc/openmanage/README.md
%doc ansible_collections/dellemc/openmanage/plugins/README.md
%doc ansible_collections/dellemc/openmanage/tests/README.md
%doc ansible_collections/dellemc/os10/README.md
%doc ansible_collections/dellemc/os10/playbooks/clos_fabric_ebgp/README.md
%doc ansible_collections/dellemc/os10/playbooks/vxlan_evpn/README.md
%doc ansible_collections/dellemc/os10/roles/os10_aaa/README.md
%doc ansible_collections/dellemc/os10/roles/os10_acl/README.md
%doc ansible_collections/dellemc/os10/roles/os10_bfd/README.md
%doc ansible_collections/dellemc/os10/roles/os10_bgp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_copy_config/README.md
%doc ansible_collections/dellemc/os10/roles/os10_dns/README.md
%doc ansible_collections/dellemc/os10/roles/os10_ecmp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_fabric_summary/README.md
%doc ansible_collections/dellemc/os10/roles/os10_flow_monitor/README.md
%doc ansible_collections/dellemc/os10/roles/os10_image_upgrade/README.md
%doc ansible_collections/dellemc/os10/roles/os10_interface/README.md
%doc ansible_collections/dellemc/os10/roles/os10_lag/README.md
%doc ansible_collections/dellemc/os10/roles/os10_lldp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_logging/README.md
%doc ansible_collections/dellemc/os10/roles/os10_network_validation/README.md
%doc ansible_collections/dellemc/os10/roles/os10_ntp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_prefix_list/README.md
%doc ansible_collections/dellemc/os10/roles/os10_qos/README.md
%doc ansible_collections/dellemc/os10/roles/os10_raguard/README.md
%doc ansible_collections/dellemc/os10/roles/os10_route_map/README.md
%doc ansible_collections/dellemc/os10/roles/os10_snmp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_system/README.md
%doc ansible_collections/dellemc/os10/roles/os10_template/README.md
%doc ansible_collections/dellemc/os10/roles/os10_uplink/README.md
%doc ansible_collections/dellemc/os10/roles/os10_users/README.md
%doc ansible_collections/dellemc/os10/roles/os10_vlan/README.md
%doc ansible_collections/dellemc/os10/roles/os10_vlt/README.md
%doc ansible_collections/dellemc/os10/roles/os10_vrf/README.md
%doc ansible_collections/dellemc/os10/roles/os10_vrrp/README.md
%doc ansible_collections/dellemc/os10/roles/os10_vxlan/README.md
%doc ansible_collections/dellemc/os10/roles/os10_xstp/README.md
%doc ansible_collections/dellemc/os6/README.md
%doc ansible_collections/dellemc/os6/playbooks/ibgp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_aaa/README.md
%doc ansible_collections/dellemc/os6/roles/os6_acl/README.md
%doc ansible_collections/dellemc/os6/roles/os6_bgp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_interface/README.md
%doc ansible_collections/dellemc/os6/roles/os6_lag/README.md
%doc ansible_collections/dellemc/os6/roles/os6_lldp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_logging/README.md
%doc ansible_collections/dellemc/os6/roles/os6_ntp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_qos/README.md
%doc ansible_collections/dellemc/os6/roles/os6_snmp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_system/README.md
%doc ansible_collections/dellemc/os6/roles/os6_users/README.md
%doc ansible_collections/dellemc/os6/roles/os6_vlan/README.md
%doc ansible_collections/dellemc/os6/roles/os6_vrrp/README.md
%doc ansible_collections/dellemc/os6/roles/os6_xstp/README.md
%doc ansible_collections/dellemc/os9/README.md
%doc ansible_collections/dellemc/os9/playbooks/clos_fabric_ebgp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_aaa/README.md
%doc ansible_collections/dellemc/os9/roles/os9_acl/README.md
%doc ansible_collections/dellemc/os9/roles/os9_bgp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_copy_config/README.md
%doc ansible_collections/dellemc/os9/roles/os9_dcb/README.md
%doc ansible_collections/dellemc/os9/roles/os9_dns/README.md
%doc ansible_collections/dellemc/os9/roles/os9_ecmp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_interface/README.md
%doc ansible_collections/dellemc/os9/roles/os9_lag/README.md
%doc ansible_collections/dellemc/os9/roles/os9_lldp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_logging/README.md
%doc ansible_collections/dellemc/os9/roles/os9_ntp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_prefix_list/README.md
%doc ansible_collections/dellemc/os9/roles/os9_sflow/README.md
%doc ansible_collections/dellemc/os9/roles/os9_snmp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_system/README.md
%doc ansible_collections/dellemc/os9/roles/os9_users/README.md
%doc ansible_collections/dellemc/os9/roles/os9_vlan/README.md
%doc ansible_collections/dellemc/os9/roles/os9_vlt/README.md
%doc ansible_collections/dellemc/os9/roles/os9_vrf/README.md
%doc ansible_collections/dellemc/os9/roles/os9_vrrp/README.md
%doc ansible_collections/dellemc/os9/roles/os9_xstp/README.md
%doc ansible_collections/f5networks/f5_modules/README.md
%doc ansible_collections/fortinet/fortimanager/README.md
%doc ansible_collections/fortinet/fortimanager/plugins/README.md
%doc ansible_collections/fortinet/fortios/README.md
%doc ansible_collections/frr/frr/README.md
%doc ansible_collections/gluster/gluster/README.md
%doc ansible_collections/google/cloud/README.md
%doc ansible_collections/google/cloud/plugins/README.md
%doc ansible_collections/google/cloud/roles/gcloud/README.md
%doc ansible_collections/google/cloud/roles/gcp_http_lb/README.md
%doc ansible_collections/google/cloud/roles/gcsfuse/README.md
%doc ansible_collections/google/cloud/roles/stackdriver_logging/README.md
%doc ansible_collections/google/cloud/roles/stackdriver_monitoring/README.md
%doc ansible_collections/hetzner/hcloud/.azure-pipelines/README.md
%doc ansible_collections/hetzner/hcloud/README.md
%doc ansible_collections/hpe/nimble/README.md
%doc ansible_collections/ibm/qradar/README.md
%doc ansible_collections/infinidat/infinibox/README.md
%doc ansible_collections/infinidat/infinibox/docs/DEV_README.md
%doc ansible_collections/inspur/sm/README.md
%doc ansible_collections/junipernetworks/junos/README.md
%doc ansible_collections/kubernetes/core/README.md
%doc ansible_collections/kubernetes/core/tests/integration/targets/kubernetes/README.md
%doc ansible_collections/kubernetes/core/tests/integration/targets/kubernetes/library/README.md
%doc ansible_collections/mellanox/onyx/.pytest_cache/README.md
%doc ansible_collections/mellanox/onyx/README.md
%doc ansible_collections/netapp/aws/README.md
%doc ansible_collections/netapp/azure/README.md
%doc ansible_collections/netapp/cloudmanager/README.md
%doc ansible_collections/netapp/cloudmanager/plugins/README.md
%doc ansible_collections/netapp/elementsw/README.md
%doc ansible_collections/netapp/ontap/README.md
%doc ansible_collections/netapp/ontap/playbooks/examples/README.md
%doc ansible_collections/netapp/ontap/playbooks/examples/json_query/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_cluster_config/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_nas_create/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_san_create/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_snapmirror_create/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_vserver_create/README.md
%doc ansible_collections/netapp/ontap/roles/na_ontap_vserver_delete/README.md
%doc ansible_collections/netapp/um_info/README.md
%doc ansible_collections/netapp_eseries/santricity/README.md
%doc ansible_collections/netapp_eseries/santricity/roles/nar_santricity_common/README.md
%doc ansible_collections/netapp_eseries/santricity/roles/nar_santricity_host/README.md
%doc ansible_collections/netapp_eseries/santricity/roles/nar_santricity_management/README.md
%doc ansible_collections/netbox/netbox/README.md
%doc ansible_collections/ngine_io/cloudstack/README.md
%doc ansible_collections/ngine_io/exoscale/README.md
%doc ansible_collections/ngine_io/vultr/README.md
%doc ansible_collections/openstack/cloud/README.md
%doc ansible_collections/openvswitch/openvswitch/README.md
%doc ansible_collections/ovirt/ovirt/README-developers.md
%doc ansible_collections/ovirt/ovirt/README.md
%doc ansible_collections/ovirt/ovirt/automation/README.md
%doc ansible_collections/ovirt/ovirt/changelogs/README.md
%doc ansible_collections/ovirt/ovirt/roles/cluster_upgrade/README.md
%doc ansible_collections/ovirt/ovirt/roles/disaster_recovery/README.md
%doc ansible_collections/ovirt/ovirt/roles/engine_setup/README.md
%doc ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/README.md
%doc ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/after_add_host/README.md
%doc ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/after_setup/README.md
%doc ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/enginevm_after_engine_setup/README.md
%doc ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/enginevm_before_engine_setup/README.md
%doc ansible_collections/ovirt/ovirt/roles/image_template/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/aaa_jdbc/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/clusters/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/datacenter_cleanup/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/datacenters/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/external_providers/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/hosts/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/mac_pools/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/networks/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/permissions/README.md
%doc ansible_collections/ovirt/ovirt/roles/infra/roles/storages/README.md
%doc ansible_collections/ovirt/ovirt/roles/manageiq/README.md
%doc ansible_collections/ovirt/ovirt/roles/remove_stale_lun/README.md
%doc ansible_collections/ovirt/ovirt/roles/repositories/README.md
%doc ansible_collections/ovirt/ovirt/roles/shutdown_env/README.md
%doc ansible_collections/ovirt/ovirt/roles/vm_infra/README.md
%doc ansible_collections/purestorage/flasharray/README.md
%doc ansible_collections/purestorage/flashblade/README.md
%doc ansible_collections/sensu/sensu_go/README.md
%doc ansible_collections/sensu/sensu_go/roles/agent/README.md
%doc ansible_collections/sensu/sensu_go/roles/backend/README.md
%doc ansible_collections/sensu/sensu_go/roles/install/README.md
%doc ansible_collections/servicenow/servicenow/README.md
%doc ansible_collections/servicenow/servicenow/update_sets/README.md
%doc ansible_collections/splunk/es/README.md
%doc ansible_collections/t_systems_mms/icinga_director/README.md
%doc ansible_collections/t_systems_mms/icinga_director/roles/ansible_icinga/README.md
%doc ansible_collections/theforeman/foreman/README.md
%doc ansible_collections/theforeman/foreman/roles/activation_keys/README.md
%doc ansible_collections/theforeman/foreman/roles/content_credentials/README.md
%doc ansible_collections/theforeman/foreman/roles/content_rhel/README.md
%doc ansible_collections/theforeman/foreman/roles/content_view_version_cleanup/README.md
%doc ansible_collections/theforeman/foreman/roles/content_views/README.md
%doc ansible_collections/theforeman/foreman/roles/hostgroups/README.md
%doc ansible_collections/theforeman/foreman/roles/lifecycle_environments/README.md
%doc ansible_collections/theforeman/foreman/roles/manifest/README.md
%doc ansible_collections/theforeman/foreman/roles/organizations/README.md
%doc ansible_collections/theforeman/foreman/roles/repositories/README.md
%doc ansible_collections/theforeman/foreman/roles/sync_plans/README.md
%doc ansible_collections/vyos/vyos/README.md
%doc ansible_collections/wti/remote/README.md
%{python3_sitelib}/ansible_collections
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n %{pypi_name}-doc
%if %{with docs}
%doc html
%license ansible_collections/ansible/netcommon/LICENSE 
%license ansible_collections/ansible/utils/LICENSE 
%license ansible_collections/arista/eos/LICENSE 
%license ansible_collections/awx/awx/plugins/modules/license.py 
%license ansible_collections/awx/awx/plugins/modules/tower_license.py 
%license ansible_collections/azure/azcollection/LICENSE 
%license ansible_collections/chocolatey/chocolatey/LICENSE 
%license ansible_collections/cisco/aci/LICENSE 
%license ansible_collections/cisco/asa/LICENSE 
%license ansible_collections/cisco/intersight/LICENSE.txt 
%license ansible_collections/cisco/ios/LICENSE 
%license ansible_collections/cisco/iosxr/LICENSE 
%license ansible_collections/cisco/mso/LICENSE 
%license ansible_collections/cisco/nso/LICENSE 
%license ansible_collections/cisco/nxos/LICENSE 
%license ansible_collections/cisco/ucs/LICENSE.txt 
%license ansible_collections/community/fortios/LICENSE 
%license ansible_collections/community/google/LICENSE 
%license ansible_collections/community/grafana/LICENSE 
%license ansible_collections/community/hashi_vault/LICENSE 
%license ansible_collections/community/kubernetes/LICENSE 
%license ansible_collections/community/kubevirt/LICENSE 
%license ansible_collections/community/libvirt/LICENSE 
%license ansible_collections/community/okd/LICENSE 
%license ansible_collections/community/proxysql/LICENSE 
%license ansible_collections/community/skydive/LICENSE 
%license ansible_collections/community/vmware/LICENSE 
%license ansible_collections/community/vmware/docs/community.vmware.vcenter_license_module.rst 
%license ansible_collections/community/vmware/plugins/modules/vcenter_license.py 
%license ansible_collections/community/zabbix/LICENSE 
%license ansible_collections/cyberark/conjur/LICENSE 
%license ansible_collections/cyberark/pas/LICENSE 
%license ansible_collections/dellemc/enterprise_sonic/LICENSE 
%license ansible_collections/dellemc/os10/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_aaa/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_acl/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_bfd/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_bgp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_copy_config/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_dns/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_ecmp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_fabric_summary/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_flow_monitor/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_image_upgrade/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_interface/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_lag/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_lldp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_logging/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_network_validation/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_ntp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_prefix_list/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_qos/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_raguard/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_route_map/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_snmp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_system/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_template/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_uplink/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_users/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_vlan/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_vlt/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_vrf/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_vrrp/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_vxlan/LICENSE 
%license ansible_collections/dellemc/os10/roles/os10_xstp/LICENSE 
%license ansible_collections/dellemc/os6/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_aaa/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_acl/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_bgp/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_interface/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_lag/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_lldp/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_logging/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_ntp/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_qos/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_snmp/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_system/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_users/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_vlan/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_vrrp/LICENSE 
%license ansible_collections/dellemc/os6/roles/os6_xstp/LICENSE 
%license ansible_collections/dellemc/os9/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_aaa/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_acl/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_bgp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_copy_config/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_dcb/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_dns/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_ecmp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_interface/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_lag/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_lldp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_logging/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_ntp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_prefix_list/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_sflow/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_snmp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_system/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_users/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_vlan/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_vlt/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_vrf/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_vrrp/LICENSE 
%license ansible_collections/dellemc/os9/roles/os9_xstp/LICENSE 
%license ansible_collections/f5networks/f5_modules/plugins/lookup/bigiq_license.py 
%license ansible_collections/f5networks/f5_modules/plugins/lookup/license_hopper.py 
%license ansible_collections/f5networks/f5_modules/plugins/modules/bigip_device_license.py 
%license ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_regkey_license.py 
%license ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_regkey_license_assignment.py 
%license ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_utility_license.py 
%license ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_utility_license_assignment.py 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_license_pool.json 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_license_pool_members.json 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_regkey_license_key.json 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_regkey_license_pool.json 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigip_device_license.py 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_regkey_license.py 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_regkey_license_assignment.py 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_utility_license.py 
%license ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_utility_license_assignment.py 
%license ansible_collections/frr/frr/LICENSE 
%license ansible_collections/gluster/gluster/LICENSE 
%license ansible_collections/google/cloud/LICENSE 
%license ansible_collections/google/cloud/roles/gcloud/LICENSE 
%license ansible_collections/ibm/qradar/LICENSE 
%license ansible_collections/infinidat/infinibox/LICENSE 
%license ansible_collections/inspur/sm/LICENSE 
%license ansible_collections/junipernetworks/junos/LICENSE 
%license ansible_collections/kubernetes/core/LICENSE 
%license ansible_collections/mellanox/onyx/LICENSE 
%license ansible_collections/netapp/ontap/plugins/modules/na_ontap_license.py 
%license ansible_collections/netapp/ontap/roles/na_ontap_cluster_config/LICENSE 
%license ansible_collections/netapp/ontap/roles/na_ontap_nas_create/LICENSE 
%license ansible_collections/netapp/ontap/roles/na_ontap_san_create/LICENSE 
%license ansible_collections/netapp/ontap/roles/na_ontap_vserver_create/LICENSE 
%license ansible_collections/netbox/netbox/LICENSE 
%license ansible_collections/openvswitch/openvswitch/LICENSE 
%license ansible_collections/ovirt/ovirt/licenses/Apache-license.txt 
%license ansible_collections/ovirt/ovirt/licenses/GPL-license.txt 
%license ansible_collections/splunk/es/LICENSE 
%license ansible_collections/t_systems_mms/icinga_director/LICENSE 
%license ansible_collections/theforeman/foreman/LICENSE 
%license ansible_collections/vyos/vyos/LICENSE 
%license ansible_collections/dellemc/openmanage/COPYING.md
%endif

%changelog
* Sat Nov 6 2021 Nico Kadel-Garcia - 4.8.0
- Initial package.
- Split up excessively long %%doc and %%license lines
- Add more BuildRequires
- Add 'with docs' and 'with checks' to enable only after bugs resolved
