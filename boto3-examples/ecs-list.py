import boto3
import click

"""
create a list of intances from aws 
"""

session = boto3.Session(profile_name='paco')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List EC2 Instances"
    for i in ec2.instances.all():
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['name'],
            i.public_dns_name
        )))
    return


if __name__ == '__main__':
    print(sys.argv)
    list_instances()

# user list instances

# user instances create-snapshot

# user list volumes

# user stop instances tag=Project: <tag_value>

# user start instances --project = <tag_value>