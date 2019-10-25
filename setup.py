from setuptools import setup

setup(
    name="AWS-Snapshooter",
    version="0.1",
    author="Francisco Laguna",
    author_email="emanuelaguna@gmail.com",
    description="AWS-Snapshooter is a tool to manage and create AWS snapshot for your instances",
    license="GPLv3+",
    packages=['snapshotty'],
    url='https://github.com/emanuelaguna/aws-acg-py-automate',
    install_requires=[
        'click',
        'boto3',
    ],
    entry_points='''
        [console_scripts]
        snapshotty = snapshotty.ecslist:cli
    '''
)