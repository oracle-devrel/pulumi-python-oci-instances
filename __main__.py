from pulumi import Config
from resources.instances import instance
from resources.network import network
from resources.policies import policies
from resources.outputs import outputs


""" Load common pulumi config """
config = Config()

"""OCI Policies"""
policies_object = policies()
pulumi_devops_policies = policies_object.create_policies(config)


""" VCN Creation """
vcn = network().create_vcn(config)

""" Service Gateway for instance """
service_gateway = network().create_service_gateway(config,vcn)
""" Nat gateway for instance  """
nat_gateway = network().create_natgateway(config,vcn)
""" Internget gateway for instance  """
internet_gateway = network().create_internet_gateway(config,vcn)

""" Security list for instance nodes """
node_security_list = network().create_node_securitylist(config,vcn)


""" Route table for instance Node """
instance_node_route_table=network().create_node_routetable(config,vcn,service_gateway,nat_gateway)

""" Subnet for instance node """
node_subnet = network().create_node_subnet(config,vcn,instance_node_route_table,node_security_list)

"""Create a OL instance"""
oci_instance = instance().create_instaces(config,node_subnet)

"""Final outputs """
outputs(oci_instance)



