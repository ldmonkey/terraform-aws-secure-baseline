import json
import os

REGIONS = [
    'ap-northeast-1',
    'ap-northeast-2',
    'ap-northeast-3',
    'ap-south-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1',
    'eu-central-1',
    'eu-north-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'sa-east-1',
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2'
]

REGIONAL_MODULES = [
    'analyzer_baseline',
    'config_baseline',
    'ebs_baseline',
    'guardduty_baseline',
    'securityhub_baseline',
    'vpc_baseline'
]

MODULES = [
    'cloudtrail_baseline',
    'alarm_baseline'
]


def main():
    prefix = 'module.secure_baseline.'
    resources = list_resources(prefix)
    rename_modules(prefix, resources)


def list_resources(prefix):
    resources = os.popen('terraform state list').read().split('\n')
    return [resource for resource in resources if resource.startswith(prefix)]


def contains_module(resources, module):
    for resource in resources:
        if resource.startswith(module):
            return True

    return False


def rename_modules(prefix, resources):
    candidates = list(MODULES)

    for mod in REGIONAL_MODULES:
        for region in REGIONS:
            candidates.append(f'{mod}_{region}.')

    to_rename = [f'{prefix}module.{candidate}' for candidate in candidates if contains_module(
        resources, f'{prefix}module.{candidate}')]

    for mod in to_rename:
        os.system(f'terraform state mv "{mod}" "{mod}[0]"')


if __name__ == '__main__':
    main()
