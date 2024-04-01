import os,re
import random
import uuid
import logging,json

def get_info_from_install_cmd(installCommand):

    ACCESS_TOKEN_PATTERN = 'ACCESS_TOKEN=["]*([a-zA-Z0-9-_.]+)'
    REFRESH_TOKEN_PATTERN = 'REFRESH_TOKEN=["]*([a-zA-Z0-9-_.]+)'
    TENANT_NAME_PATTERN = 'NETWORK=["]*([a-zA-Z0-9]+)'

    p0 = re.compile(ACCESS_TOKEN_PATTERN)
    result0 = p0.search(installCommand)
    if result0:
        access_token = result0.group(1)
    
    p1 = re.compile(REFRESH_TOKEN_PATTERN)
    result1 = p1.search(installCommand)
    if result1:
        refresh_token = result1.group(1)

    p2 = re.compile(TENANT_NAME_PATTERN)
    result2 = p2.search(installCommand)
    if result2:
        tenant_name = result2.group(1)
    
    return tenant_name,access_token,refresh_token
