import boto3

#Set Params here.
region=None
profile=None
vpc=None
owner_tag=None
print()

if region and profile and vpc and owner_tag is not None:
	creds = boto3.Session(profile_name=profile)
else:
	print("missing paramaters")
	exit(1)

#All Classes build here
class Tag_Create(object):
	def vpc_create_tag(region=None, profile=None, vpcid=None, owner_tag=None):
		creds = boto3.Session(profile_name=profile)
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.create_tags(Resources=[vpcid], Tags=[{'Key': 'Owner', 'Value': owner_tag}])

	def subnet_create_tag(region=None, profile=None, subnets=None, owner_tag=None):
		creds = boto3.Session(profile_name=profile)
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.create_tags(Resources=subnets, Tags=[{'Key': 'Owner', 'Value': owner_tag}])

	def ec2_create_tag(region=None, profile=None, ec2=None, owner_tag=None):
		creds = boto3.Session(profile_name=profile)
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.create_tags(Resources=ec2, Tags=[{'Key': 'Owner', 'Value': owner_tag}])

	def sg_create_tag(region=None, profile=None, sg=None, owner_tag=None):
		creds = boto3.Session(profile_name=profile)
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.create_tags(Resources=sg, Tags=[{'Key': 'Owner', 'Value': owner_tag}])

class Lookup(object):
	def subnetlookup(creds, region=None, vpcid=None):
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.describe_subnets(Filters=[{"Name": "vpc-id", "Values": ["{0}".format(vpcid)]}])

	def ec2lookup(creds, region=None, vpcid=None):
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.describe_instances(Filters=[{"Name": "vpc-id", "Values": ["{0}".format(vpcid)]}])

	def sglookup(creds, region=None, vpcid=None):
		ec2_call = creds.client('ec2', region_name=region)
		return ec2_call.describe_security_groups(Filters=[{"Name": "vpc-id", "Values": ["{0}".format(vpcid)]}])


# Start the Process of taggging the main VPC
print("Found the following VPC and tagging it", vpc)
Tag_Create.vpc_create_tag(region=region, profile=profile, vpcid=vpc, owner_tag=owner_tag)

# Tagging the Subnets
subnet_complete_list = []
subnet_list = Lookup.subnetlookup(creds=creds, region=region, vpcid=vpc)
for item in subnet_list['Subnets']:
	print("Found the following subnet and tagging it", item['SubnetId'])
	subnet_complete_list.append(item['SubnetId'])
Tag_Create.subnet_create_tag(region=region, profile=profile, subnets=subnet_complete_list, owner_tag=owner_tag)

# Process of tagging all EC2's that are apart of the VPC.
ec2_list = Lookup.ec2lookup(creds=creds, region=region, vpcid=vpc)
ec2_complete_list = []
for item in ec2_list['Reservations']:
	for instance in item['Instances']:
		print("Found the following instance and tagging it", instance['InstanceId'])
		ec2_complete_list.append(instance['InstanceId'])
Tag_Create.ec2_create_tag(region=region, profile=profile, ec2=ec2_complete_list, owner_tag=owner_tag)

# Process to tag Security Groups
sg_list = Lookup.sglookup(creds=creds, region=region, vpcid=vpc)
sg_complete_list = []
for item in sg_list['SecurityGroups']:
	print("Found the following Security Group and tagging it", item['GroupId'])
	sg_complete_list.append(item['GroupId'])
Tag_Create.sg_create_tag(region=region, profile=profile, sg=sg_complete_list, owner_tag=owner_tag)
print("ec2 function tagging has completed.")