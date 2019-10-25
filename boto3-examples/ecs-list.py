import boto3

"""
create a list of intances from aws 
"""

if __name__ == '__main__':
    session = boto3.Session(profile_name='paco')
    ec2 = session.resource('ec2')

    for i in ec2.instances.all():
        print(i)

