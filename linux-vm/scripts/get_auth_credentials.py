#!/usr/env/bin python

import subprocess
import os

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


ENV_VARS = os.environ.copy()
ENV_VARS['VAULT_ADDR'] = inputs.get('VAULT_ADDR')
ENV_VARS['VAULT_TOKEN'] = inputs.get('VAULT_TOKEN')


def _run_cmd(command):
    return subprocess.check_output(
        command,
        shell=True,
        env=ENV_VARS, 
        stderr=subprocess.STDOUT
    ).decode('utf-8')


echo_addr = _run_cmd(
    "echo $VAULT_ADDR"
)
echo_token = _run_cmd(
    "echo $VAULT_TOKEN"
)

ctx.logger.debug("VAULT_ADDR: {}".format(echo_addr))
ctx.logger.debug("VAULT_TOKEN: {}".format(echo_token))

arm_subscription_id = _run_cmd(
    "vault kv get -format=json 'secret/ARM_SUBSCRIPTION_ID'|jq -r .data.data[]"
)
arm_tenant_id = _run_cmd(
    "vault kv get -format=json 'secret/ARM_TENANT_ID'|jq -r .data.data[]"
)
local_admin_passwd = _run_cmd(
    "vault kv get -format=json 'secret/local_admin_passwd'|jq -r .data.data[]"
)
storage_account_key = _run_cmd(
    "vault kv get -format=json 'secret/storage_account_key'|jq -r .data.data[]"
)

ctx.instance.runtime_properties.update({
    'arm_subscription_id': arm_subscription_id,
    'arm_tenant_id': arm_tenant_id,
    'local_admin_passwd': local_admin_passwd,
    'storage_account_key': storage_account_key
})

ctx.logger.info(
    "Authentication credentials were successfully retrieved from the Vault.")