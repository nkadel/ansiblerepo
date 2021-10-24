# Created by pyp2rpm-3.3.7
%global pypi_name ansible
%global pypi_version 4.7.0

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

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
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

%doc ansible_collections/amazon/aws/README.md ansible_collections/ansible/netcommon/README.md ansible_collections/ansible/posix/.azure-pipelines/README.md ansible_collections/ansible/posix/README.md ansible_collections/ansible/utils/README.md ansible_collections/ansible/windows/README.md ansible_collections/ansible/windows/tests/integration/targets/win_copy/files-different/vault/readme.txt ansible_collections/arista/eos/README.md
%doc ansible_collections/awx/awx/README.md ansible_collections/awx/awx/tools/roles/template_galaxy/templates/README.md.j2 ansible_collections/azure/azcollection/README.md ansible_collections/check_point/mgmt/README.md ansible_collections/chocolatey/chocolatey/README.md
%doc ansible_collections/chocolatey/chocolatey/plugins/README.md
%doc  ansible_collections/cisco/aci/.pytest_cache/README.md ansible_collections/cisco/aci/README.md ansible_collections/cisco/aci/tests/unit/module_utils/.pytest_cache/README.md ansible_collections/cisco/asa/README.md ansible_collections/cisco/intersight/README.md ansible_collections/cisco/intersight/misc/README.md ansible_collections/cisco/intersight/plugins/README.md ansible_collections/cisco/ios/README.md ansible_collections/cisco/iosxr/README.md ansible_collections/cisco/meraki/README.md ansible_collections/cisco/mso/README.md ansible_collections/cisco/nso/README.md ansible_collections/cisco/nxos/README.md ansible_collections/cisco/ucs/README.md ansible_collections/cisco/ucs/misc/README.md ansible_collections/cisco/ucs/plugins/README.md ansible_collections/cisco/ucs/releases/README.md ansible_collections/cloudscale_ch/cloud/README.md ansible_collections/community/aws/README.md
%doc  ansible_collections/community/aws/tests/integration/targets/connection_aws_ssm/aws_ssm_integration_test_setup/README.md ansible_collections/community/aws/tests/integration/targets/connection_aws_ssm/aws_ssm_integration_test_teardown/README.md ansible_collections/community/azure/README.md ansible_collections/community/crypto/.azure-pipelines/README.md ansible_collections/community/crypto/README.md ansible_collections/community/digitalocean/README.md ansible_collections/community/docker/.azure-pipelines/README.md ansible_collections/community/docker/README.md ansible_collections/community/fortios/README.md ansible_collections/community/general/.azure-pipelines/README.md ansible_collections/community/general/README.md ansible_collections/community/general/tests/integration/targets/setup_flatpak_remote/README.md ansible_collections/community/google/README.md ansible_collections/community/grafana/README.md ansible_collections/community/hashi_vault/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_cert_content/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_localenv_docker/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_localenv_gha/README.md
%doc ansible_collections/community/hashi_vault/tests/integration/targets/setup_tinyproxy_server/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_legacy/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server_cert/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_server_download/README.md ansible_collections/community/hashi_vault/tests/integration/targets/setup_vault_test_plugins/README.md ansible_collections/community/hrobot/README.md
%doc ansible_collections/community/kubernetes/README.md ansible_collections/community/kubernetes/tests/integration/targets/kubernetes/README.md ansible_collections/community/kubernetes/tests/integration/targets/kubernetes/library/README.md ansible_collections/community/kubevirt/README.md ansible_collections/community/kubevirt/plugins/README.md ansible_collections/community/libvirt/.azure-pipelines/README.md ansible_collections/community/libvirt/README.md ansible_collections/community/mongodb/README.md ansible_collections/community/mongodb/roles/mongodb_auth/README.md ansible_collections/community/mongodb/roles/mongodb_config/README.md ansible_collections/community/mongodb/roles/mongodb_install/README.md ansible_collections/community/mongodb/roles/mongodb_linux/README.md ansible_collections/community/mongodb/roles/mongodb_mongod/README.md ansible_collections/community/mongodb/roles/mongodb_mongos/README.md ansible_collections/community/mongodb/roles/mongodb_repository/README.md ansible_collections/community/mongodb/roles/mongodb_selinux/README.md
%doc  ansible_collections/community/mysql/README.md ansible_collections/community/mysql/plugins/README.md ansible_collections/community/network/.azure-pipelines/README.md
%doc  ansible_collections/community/network/README.md ansible_collections/community/network/tests/integration/targets/cnos_backup/README.md ansible_collections/community/network/tests/integration/targets/cnos_bgp/README.md ansible_collections/community/network/tests/integration/targets/cnos_command/README.md ansible_collections/community/network/tests/integration/targets/cnos_conditional_command/README.md ansible_collections/community/network/tests/integration/targets/cnos_conditional_template/README.md ansible_collections/community/network/tests/integration/targets/cnos_config/README.md ansible_collections/community/network/tests/integration/targets/cnos_facts/README.md ansible_collections/community/network/tests/integration/targets/cnos_image/README.md ansible_collections/community/network/tests/integration/targets/cnos_rollback/README.md ansible_collections/community/network/tests/integration/targets/cnos_save/README.md ansible_collections/community/network/tests/integration/targets/cnos_showrun/README.md ansible_collections/community/network/tests/integration/targets/cnos_template/README.md ansible_collections/community/network/tests/integration/targets/cnos_vlag/README.md ansible_collections/community/network/tests/integration/targets/enos_command/README.md ansible_collections/community/network/tests/integration/targets/enos_config/README.md ansible_collections/community/network/tests/integration/targets/enos_facts/README.md
%doc  ansible_collections/community/okd/README.md ansible_collections/community/okd/molecule/default/README.md ansible_collections/community/postgresql/.azure-pipelines/README.md ansible_collections/community/postgresql/README.md ansible_collections/community/proxysql/README.md ansible_collections/community/proxysql/plugins/README.md ansible_collections/community/proxysql/roles/proxysql/README.md ansible_collections/community/rabbitmq/.azure-pipelines/README.md ansible_collections/community/rabbitmq/README.md ansible_collections/community/routeros/README.md ansible_collections/community/skydive/README.md ansible_collections/community/sops/README.md ansible_collections/community/sops/tests/integration/targets/var_sops/README.md ansible_collections/community/vmware/README.md ansible_collections/community/windows/README.md ansible_collections/community/windows/tests/integration/targets/win_lineinfile/files/expectations/99_README.md
%doc ansible_collections/community/zabbix/README.md ansible_collections/community/zabbix/roles/zabbix_agent/README.md ansible_collections/community/zabbix/roles/zabbix_javagateway/README.md ansible_collections/community/zabbix/roles/zabbix_proxy/README.md ansible_collections/community/zabbix/roles/zabbix_server/README.md ansible_collections/community/zabbix/roles/zabbix_web/README.md ansible_collections/containers/podman/README.md ansible_collections/cyberark/conjur/README.md ansible_collections/cyberark/conjur/project/roles/testrole/README.md ansible_collections/cyberark/conjur/roles/conjur_host_identity/README.md ansible_collections/cyberark/conjur/roles/conjur_host_identity/tests/.pytest_cache/README.md ansible_collections/cyberark/conjur/tests/conjur_variable/.pytest_cache/README.md ansible_collections/cyberark/pas/README.md ansible_collections/cyberark/pas/custom-cred-types/cyberark-pas-restapi/README.md
%doc  ansible_collections/dellemc/enterprise_sonic/README.md ansible_collections/dellemc/openmanage/README.md ansible_collections/dellemc/openmanage/plugins/README.md ansible_collections/dellemc/openmanage/tests/README.md
%doc ansible_collections/dellemc/os10/README.md ansible_collections/dellemc/os10/playbooks/clos_fabric_ebgp/README.md ansible_collections/dellemc/os10/playbooks/vxlan_evpn/README.md ansible_collections/dellemc/os10/roles/os10_aaa/README.md ansible_collections/dellemc/os10/roles/os10_acl/README.md ansible_collections/dellemc/os10/roles/os10_bfd/README.md ansible_collections/dellemc/os10/roles/os10_bgp/README.md ansible_collections/dellemc/os10/roles/os10_copy_config/README.md ansible_collections/dellemc/os10/roles/os10_dns/README.md ansible_collections/dellemc/os10/roles/os10_ecmp/README.md ansible_collections/dellemc/os10/roles/os10_fabric_summary/README.md ansible_collections/dellemc/os10/roles/os10_flow_monitor/README.md ansible_collections/dellemc/os10/roles/os10_image_upgrade/README.md ansible_collections/dellemc/os10/roles/os10_interface/README.md ansible_collections/dellemc/os10/roles/os10_lag/README.md ansible_collections/dellemc/os10/roles/os10_lldp/README.md ansible_collections/dellemc/os10/roles/os10_logging/README.md ansible_collections/dellemc/os10/roles/os10_network_validation/README.md ansible_collections/dellemc/os10/roles/os10_ntp/README.md ansible_collections/dellemc/os10/roles/os10_prefix_list/README.md ansible_collections/dellemc/os10/roles/os10_qos/README.md ansible_collections/dellemc/os10/roles/os10_raguard/README.md ansible_collections/dellemc/os10/roles/os10_route_map/README.md ansible_collections/dellemc/os10/roles/os10_snmp/README.md ansible_collections/dellemc/os10/roles/os10_system/README.md ansible_collections/dellemc/os10/roles/os10_template/README.md ansible_collections/dellemc/os10/roles/os10_uplink/README.md ansible_collections/dellemc/os10/roles/os10_users/README.md ansible_collections/dellemc/os10/roles/os10_vlan/README.md ansible_collections/dellemc/os10/roles/os10_vlt/README.md ansible_collections/dellemc/os10/roles/os10_vrf/README.md ansible_collections/dellemc/os10/roles/os10_vrrp/README.md ansible_collections/dellemc/os10/roles/os10_vxlan/README.md ansible_collections/dellemc/os10/roles/os10_xstp/README.md ansible_collections/dellemc/os6/README.md ansible_collections/dellemc/os6/playbooks/ibgp/README.md ansible_collections/dellemc/os6/roles/os6_aaa/README.md ansible_collections/dellemc/os6/roles/os6_acl/README.md ansible_collections/dellemc/os6/roles/os6_bgp/README.md ansible_collections/dellemc/os6/roles/os6_interface/README.md ansible_collections/dellemc/os6/roles/os6_lag/README.md ansible_collections/dellemc/os6/roles/os6_lldp/README.md ansible_collections/dellemc/os6/roles/os6_logging/README.md ansible_collections/dellemc/os6/roles/os6_ntp/README.md ansible_collections/dellemc/os6/roles/os6_qos/README.md ansible_collections/dellemc/os6/roles/os6_snmp/README.md ansible_collections/dellemc/os6/roles/os6_system/README.md ansible_collections/dellemc/os6/roles/os6_users/README.md ansible_collections/dellemc/os6/roles/os6_vlan/README.md ansible_collections/dellemc/os6/roles/os6_vrrp/README.md ansible_collections/dellemc/os6/roles/os6_xstp/README.md ansible_collections/dellemc/os9/README.md ansible_collections/dellemc/os9/playbooks/clos_fabric_ebgp/README.md ansible_collections/dellemc/os9/roles/os9_aaa/README.md ansible_collections/dellemc/os9/roles/os9_acl/README.md ansible_collections/dellemc/os9/roles/os9_bgp/README.md ansible_collections/dellemc/os9/roles/os9_copy_config/README.md ansible_collections/dellemc/os9/roles/os9_dcb/README.md ansible_collections/dellemc/os9/roles/os9_dns/README.md ansible_collections/dellemc/os9/roles/os9_ecmp/README.md ansible_collections/dellemc/os9/roles/os9_interface/README.md ansible_collections/dellemc/os9/roles/os9_lag/README.md ansible_collections/dellemc/os9/roles/os9_lldp/README.md ansible_collections/dellemc/os9/roles/os9_logging/README.md ansible_collections/dellemc/os9/roles/os9_ntp/README.md ansible_collections/dellemc/os9/roles/os9_prefix_list/README.md ansible_collections/dellemc/os9/roles/os9_sflow/README.md ansible_collections/dellemc/os9/roles/os9_snmp/README.md ansible_collections/dellemc/os9/roles/os9_system/README.md ansible_collections/dellemc/os9/roles/os9_users/README.md ansible_collections/dellemc/os9/roles/os9_vlan/README.md ansible_collections/dellemc/os9/roles/os9_vlt/README.md ansible_collections/dellemc/os9/roles/os9_vrf/README.md ansible_collections/dellemc/os9/roles/os9_vrrp/README.md ansible_collections/dellemc/os9/roles/os9_xstp/README.md
#%%doc  ansible_collections/f5networks/f5_modules/README.md
#%%doc  ansible_collections/fortinet/fortimanager/README.md
#%%doc  ansible_collections/fortinet/fortimanager/plugins/README.md
#%%doc  ansible_collections/fortinet/fortios/README.md
#%%doc  ansible_collections/frr/frr/README.md
#%%doc  ansible_collections/gluster/gluster/README.md
#%%doc  ansible_collections/google/cloud/README.md
#%%doc  ansible_collections/google/cloud/plugins/README.md
#%%doc  ansible_collections/google/cloud/roles/gcloud/README.md
#%%doc  ansible_collections/google/cloud/roles/gcp_http_lb/README.md
#%%doc  ansible_collections/google/cloud/roles/gcsfuse/README.md
#%%doc  ansible_collections/google/cloud/roles/stackdriver_logging/README.md
#%%doc  ansible_collections/google/cloud/roles/stackdriver_monitoring/README.md
#%%doc  ansible_collections/hetzner/hcloud/.azure-pipelines/README.md
#%%doc  ansible_collections/hetzner/hcloud/README.md
#%%doc  ansible_collections/hpe/nimble/README.md
#%%doc  ansible_collections/ibm/qradar/README.md
#%%doc  ansible_collections/infinidat/infinibox/README.md
#%%doc  ansible_collections/infinidat/infinibox/docs/DEV_README.md
#%%doc  ansible_collections/inspur/sm/README.md
#%%doc  ansible_collections/junipernetworks/junos/README.md
#%%doc  ansible_collections/kubernetes/core/README.md
#%%doc  ansible_collections/kubernetes/core/tests/integration/targets/kubernetes/README.md
#%%doc  ansible_collections/kubernetes/core/tests/integration/targets/kubernetes/library/README.md
#%%doc  ansible_collections/mellanox/onyx/.pytest_cache/README.md
#%%doc  ansible_collections/mellanox/onyx/README.md
#%%doc  ansible_collections/netapp/aws/README.md
#%%doc  ansible_collections/netapp/azure/README.md
#%%doc  ansible_collections/netapp/cloudmanager/README.md
#%%doc  ansible_collections/netapp/cloudmanager/plugins/README.md
#%%doc  ansible_collections/netapp/elementsw/README.md
#%%doc  ansible_collections/netapp/ontap/README.md
#%%doc  ansible_collections/netapp/ontap/playbooks/examples/README.md
#%%doc  ansible_collections/netapp/ontap/playbooks/examples/json_query/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_cluster_config/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_nas_create/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_san_create/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_snapmirror_create/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_vserver_create/README.md
#%%doc  ansible_collections/netapp/ontap/roles/na_ontap_vserver_delete/README.md
#%%doc  ansible_collections/netapp/um_info/README.md
#%%doc  ansible_collections/netapp_eseries/santricity/README.md
#%%doc  ansible_collections/netapp_eseries/santricity/roles/nar_santricity_common/README.md
#%%doc  ansible_collections/netapp_eseries/santricity/roles/nar_santricity_host/README.md
#%%doc  ansible_collections/netapp_eseries/santricity/roles/nar_santricity_management/README.md
#%%doc  ansible_collections/netbox/netbox/README.md
#%%doc  ansible_collections/ngine_io/cloudstack/README.md
#%%doc  ansible_collections/ngine_io/exoscale/README.md
#%%doc  ansible_collections/ngine_io/vultr/README.md
#%%doc  ansible_collections/openstack/cloud/README.md
#%%doc  ansible_collections/openvswitch/openvswitch/README.md
#%%doc  ansible_collections/ovirt/ovirt/README-developers.md
#%%doc  ansible_collections/ovirt/ovirt/README.md
#%%doc  ansible_collections/ovirt/ovirt/automation/README.md
#%%doc  ansible_collections/ovirt/ovirt/changelogs/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/cluster_upgrade/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/disaster_recovery/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/engine_setup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/after_add_host/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/after_setup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/enginevm_after_engine_setup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/hosted_engine_setup/hooks/enginevm_before_engine_setup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/image_template/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/aaa_jdbc/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/clusters/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/datacenter_cleanup/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/datacenters/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/external_providers/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/hosts/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/mac_pools/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/networks/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/permissions/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/infra/roles/storages/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/manageiq/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/remove_stale_lun/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/repositories/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/shutdown_env/README.md
#%%doc  ansible_collections/ovirt/ovirt/roles/vm_infra/README.md
#%%doc  ansible_collections/purestorage/flasharray/README.md
#%%doc  ansible_collections/purestorage/flashblade/README.md
#%%doc  ansible_collections/sensu/sensu_go/README.md
#%%doc  ansible_collections/sensu/sensu_go/roles/agent/README.md
#%%doc  ansible_collections/sensu/sensu_go/roles/backend/README.md
#%%doc  ansible_collections/sensu/sensu_go/roles/install/README.md
#%%doc  ansible_collections/servicenow/servicenow/README.md
#%%doc  ansible_collections/servicenow/servicenow/update_sets/README.md
#%%doc  ansible_collections/splunk/es/README.md
#%%doc  ansible_collections/t_systems_mms/icinga_director/README.md
#%%doc  ansible_collections/t_systems_mms/icinga_director/roles/ansible_icinga/README.md
#%%doc  ansible_collections/theforeman/foreman/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/activation_keys/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/content_credentials/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/content_rhel/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/content_view_version_cleanup/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/content_views/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/hostgroups/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/lifecycle_environments/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/manifest/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/organizations/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/repositories/README.md
#%%doc  ansible_collections/theforeman/foreman/roles/sync_plans/README.md
#%%doc  ansible_collections/vyos/vyos/README.md
#%%doc  ansible_collections/wti/remote/README.md

%{python3_sitelib}/ansible_collections
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n %{pypi_name}-doc
%if %{with docs}
%doc html
%endif

%license ansible_collections/ansible/netcommon/LICENSE ansible_collections/ansible/utils/LICENSE ansible_collections/arista/eos/LICENSE ansible_collections/awx/awx/plugins/modules/license.py ansible_collections/awx/awx/plugins/modules/tower_license.py ansible_collections/azure/azcollection/LICENSE ansible_collections/chocolatey/chocolatey/LICENSE
%license ansible_collections/cisco/aci/LICENSE ansible_collections/cisco/asa/LICENSE ansible_collections/cisco/intersight/LICENSE.txt ansible_collections/cisco/ios/LICENSE ansible_collections/cisco/iosxr/LICENSE ansible_collections/cisco/mso/LICENSE ansible_collections/cisco/nso/LICENSE ansible_collections/cisco/nxos/LICENSE ansible_collections/cisco/ucs/LICENSE.txt
%license ansible_collections/community/fortios/LICENSE ansible_collections/community/google/LICENSE ansible_collections/community/grafana/LICENSE ansible_collections/community/hashi_vault/LICENSE ansible_collections/community/kubernetes/LICENSE ansible_collections/community/kubevirt/LICENSE ansible_collections/community/libvirt/LICENSE ansible_collections/community/okd/LICENSE ansible_collections/community/proxysql/LICENSE ansible_collections/community/skydive/LICENSE ansible_collections/community/vmware/LICENSE ansible_collections/community/vmware/docs/community.vmware.vcenter_license_module.rst ansible_collections/community/vmware/plugins/modules/vcenter_license.py ansible_collections/community/zabbix/LICENSE
%license ansible_collections/cyberark/conjur/LICENSE ansible_collections/cyberark/pas/LICENSE ansible_collections/dellemc/enterprise_sonic/LICENSE ansible_collections/dellemc/os10/LICENSE ansible_collections/dellemc/os10/roles/os10_aaa/LICENSE ansible_collections/dellemc/os10/roles/os10_acl/LICENSE ansible_collections/dellemc/os10/roles/os10_bfd/LICENSE ansible_collections/dellemc/os10/roles/os10_bgp/LICENSE ansible_collections/dellemc/os10/roles/os10_copy_config/LICENSE ansible_collections/dellemc/os10/roles/os10_dns/LICENSE ansible_collections/dellemc/os10/roles/os10_ecmp/LICENSE ansible_collections/dellemc/os10/roles/os10_fabric_summary/LICENSE ansible_collections/dellemc/os10/roles/os10_flow_monitor/LICENSE ansible_collections/dellemc/os10/roles/os10_image_upgrade/LICENSE ansible_collections/dellemc/os10/roles/os10_interface/LICENSE ansible_collections/dellemc/os10/roles/os10_lag/LICENSE ansible_collections/dellemc/os10/roles/os10_lldp/LICENSE ansible_collections/dellemc/os10/roles/os10_logging/LICENSE ansible_collections/dellemc/os10/roles/os10_network_validation/LICENSE ansible_collections/dellemc/os10/roles/os10_ntp/LICENSE ansible_collections/dellemc/os10/roles/os10_prefix_list/LICENSE ansible_collections/dellemc/os10/roles/os10_qos/LICENSE ansible_collections/dellemc/os10/roles/os10_raguard/LICENSE ansible_collections/dellemc/os10/roles/os10_route_map/LICENSE ansible_collections/dellemc/os10/roles/os10_snmp/LICENSE ansible_collections/dellemc/os10/roles/os10_system/LICENSE ansible_collections/dellemc/os10/roles/os10_template/LICENSE ansible_collections/dellemc/os10/roles/os10_uplink/LICENSE ansible_collections/dellemc/os10/roles/os10_users/LICENSE ansible_collections/dellemc/os10/roles/os10_vlan/LICENSE ansible_collections/dellemc/os10/roles/os10_vlt/LICENSE ansible_collections/dellemc/os10/roles/os10_vrf/LICENSE ansible_collections/dellemc/os10/roles/os10_vrrp/LICENSE ansible_collections/dellemc/os10/roles/os10_vxlan/LICENSE ansible_collections/dellemc/os10/roles/os10_xstp/LICENSE ansible_collections/dellemc/os6/LICENSE ansible_collections/dellemc/os6/roles/os6_aaa/LICENSE ansible_collections/dellemc/os6/roles/os6_acl/LICENSE ansible_collections/dellemc/os6/roles/os6_bgp/LICENSE ansible_collections/dellemc/os6/roles/os6_interface/LICENSE ansible_collections/dellemc/os6/roles/os6_lag/LICENSE ansible_collections/dellemc/os6/roles/os6_lldp/LICENSE ansible_collections/dellemc/os6/roles/os6_logging/LICENSE ansible_collections/dellemc/os6/roles/os6_ntp/LICENSE ansible_collections/dellemc/os6/roles/os6_qos/LICENSE ansible_collections/dellemc/os6/roles/os6_snmp/LICENSE ansible_collections/dellemc/os6/roles/os6_system/LICENSE ansible_collections/dellemc/os6/roles/os6_users/LICENSE ansible_collections/dellemc/os6/roles/os6_vlan/LICENSE ansible_collections/dellemc/os6/roles/os6_vrrp/LICENSE ansible_collections/dellemc/os6/roles/os6_xstp/LICENSE ansible_collections/dellemc/os9/LICENSE ansible_collections/dellemc/os9/roles/os9_aaa/LICENSE ansible_collections/dellemc/os9/roles/os9_acl/LICENSE ansible_collections/dellemc/os9/roles/os9_bgp/LICENSE ansible_collections/dellemc/os9/roles/os9_copy_config/LICENSE ansible_collections/dellemc/os9/roles/os9_dcb/LICENSE ansible_collections/dellemc/os9/roles/os9_dns/LICENSE ansible_collections/dellemc/os9/roles/os9_ecmp/LICENSE ansible_collections/dellemc/os9/roles/os9_interface/LICENSE ansible_collections/dellemc/os9/roles/os9_lag/LICENSE ansible_collections/dellemc/os9/roles/os9_lldp/LICENSE ansible_collections/dellemc/os9/roles/os9_logging/LICENSE ansible_collections/dellemc/os9/roles/os9_ntp/LICENSE ansible_collections/dellemc/os9/roles/os9_prefix_list/LICENSE ansible_collections/dellemc/os9/roles/os9_sflow/LICENSE ansible_collections/dellemc/os9/roles/os9_snmp/LICENSE ansible_collections/dellemc/os9/roles/os9_system/LICENSE ansible_collections/dellemc/os9/roles/os9_users/LICENSE ansible_collections/dellemc/os9/roles/os9_vlan/LICENSE ansible_collections/dellemc/os9/roles/os9_vlt/LICENSE ansible_collections/dellemc/os9/roles/os9_vrf/LICENSE ansible_collections/dellemc/os9/roles/os9_vrrp/LICENSE ansible_collections/dellemc/os9/roles/os9_xstp/LICENSE ansible_collections/f5networks/f5_modules/plugins/lookup/bigiq_license.py
%license ansible_collections/f5networks/f5_modules/plugins/lookup/license_hopper.py ansible_collections/f5networks/f5_modules/plugins/modules/bigip_device_license.py ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_regkey_license.py ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_regkey_license_assignment.py ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_utility_license.py ansible_collections/f5networks/f5_modules/plugins/modules/bigiq_utility_license_assignment.py ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_license_pool.json ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_license_pool_members.json ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_regkey_license_key.json ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/fixtures/load_regkey_license_pool.json ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigip_device_license.py ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_regkey_license.py ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_regkey_license_assignment.py ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_utility_license.py ansible_collections/f5networks/f5_modules/tests/unit/modules/network/f5/test_bigiq_utility_license_assignment.py
%license ansible_collections/frr/frr/LICENSE ansible_collections/gluster/gluster/LICENSE ansible_collections/google/cloud/LICENSE ansible_collections/google/cloud/roles/gcloud/LICENSE ansible_collections/ibm/qradar/LICENSE ansible_collections/infinidat/infinibox/LICENSE ansible_collections/inspur/sm/LICENSE ansible_collections/junipernetworks/junos/LICENSE ansible_collections/kubernetes/core/LICENSE ansible_collections/mellanox/onyx/LICENSE
%license ansible_collections/netapp/ontap/plugins/modules/na_ontap_license.py ansible_collections/netapp/ontap/roles/na_ontap_cluster_config/LICENSE ansible_collections/netapp/ontap/roles/na_ontap_nas_create/LICENSE ansible_collections/netapp/ontap/roles/na_ontap_san_create/LICENSE ansible_collections/netapp/ontap/roles/na_ontap_vserver_create/LICENSE ansible_collections/netbox/netbox/LICENSE ansible_collections/openvswitch/openvswitch/LICENSE ansible_collections/ovirt/ovirt/licenses/Apache-license.txt ansible_collections/ovirt/ovirt/licenses/GPL-license.txt ansible_collections/splunk/es/LICENSE ansible_collections/t_systems_mms/icinga_director/LICENSE ansible_collections/theforeman/foreman/LICENSE ansible_collections/vyos/vyos/LICENSE ansible_collections/dellemc/openmanage/COPYING.md

%changelog
* Sat Oct 23 2021 Nico Kadel-Garcia - 4.7.0-1
- Initial package.
- Split up excessively long %%doc and %%license lines
- Add more BuildRequires
- Add 'with docs' and 'with checks' to enable only after bugs resolved
