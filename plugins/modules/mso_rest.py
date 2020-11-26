#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Anvitha Jain (@anvitha-jain) <anvjain@cisco.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: mso_rest
short_description: Direct access to the Cisco MSO REST API
description:
- Enables the management of the Cisco MSO fabric through direct access to the Cisco MSO REST API.
- This module is not idempotent and does not report changes.
options:
  method:
    description:
    - The HTTP method of the request.
    - Using C(delete) is typically used for deleting objects.
    - Using C(get) is typically used for querying objects.
    - Using C(post) is typically used for modifying objects.
    - Using C(put) is typically used for modifying existing objects.
    - Using C(patch) is typically also used for modifying existing objects.
    type: str
    choices: [ delete, get, post, put, patch ]
    default: get
    aliases: [ action ]
  path:
    description:
    - URI being used to execute API calls.
    type: str
    required: yes
    aliases: [ uri ]
  content:
    description:
    - When used instead of C(src), sets the payload of the API request directly.
    - This may be convenient to template simple requests.
    - For anything complex use the C(template) lookup plugin (see examples)
      or the M(template) module with parameter C(src).
    type: raw
    aliases: [ payload ]
extends_documentation_fragment:
- cisco.mso.modules

notes:
- Most payloads are known not to be idempotent, so be careful when constructing payloads.
seealso:
- module: cisco.mso.mso_tenant
author:
- Anvitha Jain (@anvitha-jain)
'''

EXAMPLES = r'''
- name: Add schema (JSON)
  cisco.mso.mso_rest:
    host: mso
    username: admin
    password: SomeSecretPassword
    path: /mso/api/v1/schemas
    method: post
    content:
      {
          "displayName": "mso_schema",
          "templates": [{
              "name": "Template_1",
              "tenantId": "{{ add_tenant.jsondata.id }}",
              "displayName": "Template_1",
              "templateSubType": [],
              "templateType": "stretched-template",
              "anps": [],
              "contracts": [],
              "vrfs": [],
              "bds": [],
              "filters": [],
              "externalEpgs": [],
              "serviceGraphs": [],
              "intersiteL3outs": []
          }],
          "sites": [],
          "_updateVersion": 0
      }
  delegate_to: localhost

- name: Query schema
  cisco.mso.mso_rest:
    host: mso
    username: admin
    password: SomeSecretPassword
    path: /mso/api/v1/schemas
    method: get
  delegate_to: localhost

- name: Patch schema (YAML)
  cisco.mso.mso_rest:
    host: mso
    username: admin
    password: SomeSecretPassword
    path: "/mso/api/v1/schemas/{{ add_schema.jsondata.id }}"
    method: patch
    content:
      - op: add
        path: /templates/Template_1/anps/-
        value:
          name: AP2
          displayName: AP2
          epgs: []
        _updateVersion: 0
  delegate_to: localhost
'''

RETURN = r'''
'''

import json
import os

# Optional, only used for YAML validation
try:
    import yaml
    HAS_YAML = True
except Exception:
    HAS_YAML = False

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.mso.plugins.module_utils.mso import MSOModule, mso_argument_spec
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text


def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(
        path=dict(type='str', required=True, aliases=['uri']),
        method=dict(type='str', default='get', choices=['delete', 'get', 'post', 'put', 'patch'], aliases=['action']),
        content=dict(type='raw', aliases=['payload']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    content = module.params.get('content')
    path = module.params.get('path')

    mso = MSOModule(module)
    mso.result['status'] = -1  # Ensure we always return a status

    # Validate content/payload
    if content and (isinstance(content, dict) or isinstance(content, list)):
        # Validate inline YAML/JSON
        content = json.dumps(content)
    elif content and isinstance(content, str) and HAS_YAML:
        try:
            # Validate YAML/JSON string
            content = json.dumps(yaml.safe_load(content))
        except Exception as e:
            module.fail_json(msg='Failed to parse provided JSON/YAML payload: %s' % to_text(e), exception=to_text(e), payload=content)

    # Perform actual request using auth cookie (Same as mso.request())
    if 'port' in mso.params and mso.params.get('port') is not None:
        mso.url = '%(protocol)s://%(host)s:%(port)s/' % mso.params + path.lstrip('/')
    else:
        mso.url = '%(protocol)s://%(host)s/' % mso.params + path.lstrip('/')

    mso.method = mso.params.get('method').upper()

    # Perform request
    resp, info = fetch_url(module, mso.url,
                           data=content,
                           headers=mso.headers,
                           method=mso.method,
                           timeout=mso.params.get('timeout'),
                           use_proxy=mso.params.get('use_proxy'))

    mso.response = info.get('msg')
    mso.status = info.get('status')

    # Report failure
    if info.get('status') not in [200, 201, 202, 204]:
        try:
            # MSO error
            mso.response_json(info['body'])
            mso.fail_json(msg='MSO Error %(code)s: %(message)s' % mso.error)
        except KeyError:
            # Connection error
            mso.fail_json(msg='Connection failed for %(url)s. %(msg)s' % info)

    mso.response_json(resp.read())

    if mso.method != 'GET':
        mso.result['changed'] = True

    mso.result['jsondata'] = mso.jsondata

    # Report success
    mso.exit_json(**mso.result)


if __name__ == '__main__':
    main()
