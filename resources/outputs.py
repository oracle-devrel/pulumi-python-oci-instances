import pulumi

def outputs(oci_instance):

    pulumi.export("Stack","OCI Instances with Pulumi")
    pulumi.export("Instance Hostname" ,oci_instance.display_name)
    pulumi.export("Instance PublicIP" ,oci_instance.public_ip)
    pulumi.export("Authors","Made with \u2764 by Oracle Developers")