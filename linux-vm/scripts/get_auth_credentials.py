#!/usr/env/bin python

import subprocess

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

arm_subrscription_id = subprocess.check_output(
    "vault kv get -format=json 'secret/ARM_SUBSCRIPTION_ID'|jq -r .data.data[]",
    shell=True
)

arm_tenant_id = subprocess.check_output(
    "vault kv get -format=json 'secret/ARM_TENANT_ID'|jq -r .data.data[]",
    shell=True
)

local_admin_passwd = subprocess.check_output(
    "vault kv get -format=json 'secret/local_admin_passwd'|jq -r .data.data[]",
    shell=True
)

storage_account_key = subprocess.check_output(
    "vault kv get -format=json 'secret/storage_account_key'|jq -r .data.data[]",
    shell=True
)

ctx.instance.runtime_properties.update(
    'arm_subscription_id': arm_subrscription_id,
    'arm_tenant_id': arm_tenant_id,
    'local_admin_passwd': local_admin_passwd,
    'storage_account_key': storage_account_key
)

ctx.logger.info(
    "Authentication credentials were successfully retrieved from the Vault.")