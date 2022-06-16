import os
import pulumi_oci as oci

class policies:

    def create_policies(self,config,):
        try:
            user_group = oci.identity.Group("user_group",
                                            compartment_id=os.environ['TF_VAR_tenancy_ocid'],
                                            description=config.require('usergroup_description'),
                                            name=f"{config.require('usergroup_name')}_{config.require('app_name_prefix')}")


            user_group_membership = oci.identity.UserGroupMembership("user_group_membership",
                                                                          group_id=user_group.id,
                                                                          user_id=os.environ['TF_VAR_user_ocid'])


            pulumi_instance_policies = oci.identity.Policy("pulumi_instance_policies",
                                                         compartment_id=config.get('compartment_ocid'),
                                                         description=config.get('policies_description'),
                                                         name=f"{config.get('policies_name')}",
                                                         statements=[
                                                             f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to manage all-resources in compartment id {config.get('compartment_ocid')}",
                                                            #  f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to manage instance-family in compartment id {config.get('compartment_ocid')}",
                                                            #  f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to manage  all-resources in compartment id {config.get('compartment_ocid')}",
                                                            # f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to use virtual-network-family in compartment id {config.get('compartment_ocid')}",
                                                            # f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to read app-catalog-listing in compartment id {config.get('compartment_ocid')}",
                                                            # f"Allow group {config.require('usergroup_name')}_{config.require('app_name_prefix')} to use volume-family in compartment id {config.get('compartment_ocid')}"
                                                         ],
                                                         )
            return pulumi_instance_policies

        except Exception as error:
            print("Policies Creation failed " + str(error))