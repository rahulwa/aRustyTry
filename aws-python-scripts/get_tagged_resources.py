import boto3
import csv
import argparse

def elasticache_tagged(tag_key, tag_found=True):
    nodes = []
    data = {}
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec_client = boto3.client('elasticache')
    region_name = ec_client.meta.region_name
    paginator = ec_client.get_paginator('describe_cache_clusters')
    pages = paginator.paginate()
    for page in pages:
        nodes.extend(page['CacheClusters'])
    for node in nodes:
        arn = format("arn:aws:elasticache:{}:{}:cluster:{}".format(
            region_name, account_id, node["CacheClusterId"]))
        tags_list = ec_client.list_tags_for_resource(ResourceName=arn).get('TagList', [])
        if tags_list:
            tags = {}
            for tag_dicts in tags_list:
                tags.update({
                    tag_dicts['Key']: tag_dicts['Value']
                })
                data.update({ 
                    node['CacheClusterId'] : tags 
                    for k,v in tag_dicts.items() 
                    if k == 'Key' and ( not tag_found or v == tag_key )
                })
    return data


def sqs_tagged(tag_key, tag_found=True):
    data = {}
    sqs_client = boto3.client('sqs')
    queues = sqs_client.list_queues()
    for queue_url in queues['QueueUrls']:
        tags = sqs_client.list_queue_tags(QueueUrl=queue_url).get('Tags', None)
        if tags:
            data.update({ 
                queue_url : tags 
                for k, v in tags.items() 
                if k == tag_key or not tag_found
            })
    return data


def take_inputs():
    text = '''
    This is a python script that writes AWS resources based on tagging to a file
    '''
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument(
        "-v", "--version",
        help="show help", action="store_true",
    )
    parser.add_argument(
        "--file", "-f",
        help="set output file path", 
        action='store', type=str, required=True,
    )
    parser.add_argument(
        "--tag", "-t",
        help="filter resources based on this tag",
        action='store', type=str,
        default="ProductDomain"
    )
    parser.add_argument(
        "--resource-type", "-rt",
        help="Type of AWS resource type to be run on",
        action='store', type=str, required=True,
        choices=('elasticache', 'sqs'),
    )
    parser.add_argument(
        "--tag-present", "-p",
        help="Output the resources matching input tag if it is passed else resources not having gived tag will be the output",
        action='store_false',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = take_inputs()
    with open(args.file, 'w') as csvfile:
        if args.resource_type == 'elasticache':
            resources = elasticache_tagged(args.tag, args.tag_present)
            fieldnames = ['node', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k, v in resources.items():
                writer.writerow({'node': k, 'tags': str(v)})
        elif args.resource_type == 'sqs':
            resources = sqs_tagged(args.tag, args.tag_present)
            fieldnames = ['queue', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k, v in resources.items():
                writer.writerow({'queue': k.split('/')[-1], 'tags': str(v)})