import boto3
import botocore
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
def cli():
    """Paco manages instnaces"""

@cli.group('snapshots')
def snapshots():
    """commands for sbnapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project tag project:<name>")
def list_snapshots(project):
    "List snapshots of an Instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(','.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

@cli.group('volumes')
def volumes():
    """commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help="Only instances for project tag project:<name>")
def list_volumes(project):
    "List volumes of an Instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(','.join((
                v.id,
                i.id,
                str(v.size) + 'GiB',
                v.state,
                v.encrypted and 'Encrypted' or 'Not Encrypted'
            )))
    return


@cli.group('instances')
def instances():
    """manages instances"""

@instances.command('snapshot')
@click.option('--project', default=None, help="only create snapshots of instances for tag project:<name>")
def create_snapshot(project):

    instances = filter_instances(project)

    for i in instances:
        print("Stopping ... {0}".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print(" Creating a snapshot of ...{0}".format(v.id))
            v.create_snapshot(Description="Created by paco  automated bot")

        print("Starting ...{0}".format(i.id))
        i.start()
        i.wait_until_running()

    print("Jobs done!")
    return


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
        print("Stopping instance {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop instance {0}. ".format(i.id) + str(e))
            continue

    return

# user stop instances tag=Project: <tag_value>
@instances.command('start')
@click.option('--project', default=None, help="Only instances for project tag project:<name>")
def stop_instances(project):
    "start EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting instance {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start instance {0}. ".format(i.id) + str(e))
            continue

    return

if __name__ == '__main__':
    cli()


# user instances create-snapshot

# user list volumes

# user start instances --project = <tag_value>