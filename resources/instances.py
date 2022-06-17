import os
import pulumi_oci as oci

class instance:
    def create_instaces(self,config,node_subnet):
        try:
            get_ad_name = oci.identity.get_availability_domain(compartment_id=os.environ['TF_VAR_tenancy_ocid'],ad_number=1)
            ssh_pub_key=open(config.require('path_ssh_pubkey'),"r").read()
            node_image = oci.core.get_images(compartment_id=config.get('compartment_ocid'),
                                             operating_system=config.get('instance_node_operating_system'),
                                             operating_system_version=config.get('instance_operating_system_version'),
                                             shape=config.get('instance_node_shape'),
                                             sort_by="TIMECREATED",
                                             sort_order="DESC")

            instance_oraclelinux = oci.core.Instance("instance_oraclelinux",
                                                     agent_config=oci.core.InstanceAgentConfigArgs(
                                                         plugins_configs=[
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_vulnerability'),
                                                                 name="Vulnerability Scanning",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_javamgmtsvc'),
                                                                 name="Oracle Java Management Service",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_osmgmtsvc'),
                                                                 name="OS Management Service Agent",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_mgmt'),
                                                                 name="Management Agent",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_customlogs'),
                                                                 name="Custom Logs Monitoring",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_comptinstance'),
                                                                 name="Compute Instance Run Command",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_comptinstancemonitoring'),
                                                                 name="Compute Instance Monitoring",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_blkvolume'),
                                                                 name="Block Volume Management",
                                                             ),
                                                             oci.core.InstanceAgentConfigPluginsConfigArgs(
                                                                 desired_state=config.require('oci_agent_bastion'),
                                                                 name="Bastion",
                                                             ),
                                                         ],
                                                     ),

                                                     availability_domain=get_ad_name.__dict__['name'],
                                                     compartment_id=config.get('compartment_ocid'),
                                                     create_vnic_details=oci.core.InstanceCreateVnicDetailsArgs(
                                                         display_name=config.require('instance_name'),
                                                         subnet_id=node_subnet.id,
                                                     ),
                                                     display_name=config.require('instance_name'),
                                                     fault_domain="FAULT-DOMAIN-1",

                                                     metadata={
                                                         "ssh_authorized_keys": ssh_pub_key,
                                                     },
                                                     shape=config.require('instance_node_shape'),
                                                     shape_config=oci.core.InstanceShapeConfigArgs(
                                                         memory_in_gbs=config.require('instance_node_memory_in_gbs'),
                                                         ocpus=config.require('instance_node_ocpus'),
                                                     ),
                                                     source_details=oci.core.InstanceSourceDetailsArgs(
                                                         boot_volume_size_in_gbs=config.require('instance_bootvolume_size_gb'),
                                                         source_id=node_image.images[0]['id'],
                                                         source_type="image",
                                                     ),)


            return instance_oraclelinux
        except Exception as error:
            print("Instance creation failed " + str(error))