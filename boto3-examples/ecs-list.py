import boto3
import click

"""
create a list of intances from aws 
"""

session = boto3.Session(profile_name='paco')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instnaces"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project tag project:<name>")
def list_instances(project):
    "List EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project', '<no_project>')
        )))
    return

# user stop instances tag=Project: <tag_value>
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project tag project:<name>")
def stop_instances(project):
    "stop EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping instance {0} ...".format(i.id))
        i.stop()

    return

# user stop instances tag=Project: <tag_value>
@instances.command('start')
@click.option('--project', default=None, help="Only instances for project tag project:<name>")
def stop_instances(project):
    "start EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting instance {0} ...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    instances()


# user instances create-snapshot

# user list volumes

# user start instances --project = <tag_value>