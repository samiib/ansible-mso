#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Sabari Jaganathan (@sajagana) <sajagana@cisco.com>

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}

DOCUMENTATION = r"""
---
module: ndo_l3out_template
short_description: Manage L3Outs on Cisco Nexus Dashboard Orchestrator (NDO).
description:
- Manage L3Outs on Cisco Nexus Dashboard Orchestrator (NDO).
author:
- Sabari Jaganathan (@sajagana)
options:
  template:
    description:
    - The name of the L3Out template.
    type: str
    aliases: [ l3out_template ]
    required: true
  name:
    description:
    - The name of the L3Out.
    type: str
  uuid:
    description:
    - The UUID of the L3Out.
    - This parameter is required when the L3Out needs to be updated.
    type: str
  description:
    description:
    - The description of the L3Out.
    type: str
  vrf:
    description:
    - The VRF associated with the L3Out.
    type: dict
    suboptions:
      name:
        description:
        - The name of the VRF.
        required: true
        type: str
      schema:
        description:
        - The name of the schema.
        required: true
        type: str
      template:
        description:
        - The name of the template.
        required: true
        type: str
  l3_domain:
    description:
    - The name of the L3 Domain.
    type: str
  target_dscp:
    description:
    - The DSCP Level of the L3Out.
    type: str
    choices:
      - af11
      - af12
      - af13
      - af21
      - af22
      - af23
      - af31
      - af32
      - af33
      - af41
      - af42
      - af43
      - cs0
      - cs1
      - cs2
      - cs3
      - cs4
      - cs5
      - cs6
      - cs7
      - expedited_forwarding
      - unspecified
      - voice_admit
  pim:
    description:
    - The protocol independent multicast (PIM) flag of the L3Out.
    - By default, PIM is disabled. To enable the PIM, Layer 3 Multicast must be enabled on the O(vrf).
    type: bool
  interleak:
    description:
    - The name of the Route Map Policy for Route Control that needs to be associated with Interleak route map.
    type: str
  static_route_redistribution:
    description:
    - The name of the Route Map Policy for Route Control that needs to be associated with Static Route Redistribution route map.
    type: str
    aliases: [ static_route ]
  connected_route_redistribution:
    description:
    - The name of the Route Map Policy for Route Control that needs to be associated with Connected Route Redistribution route map.
    type: str
    aliases: [ connected_route ]
  attached_host_route_redistribution:
    description:
    - The name of the Route Map Policy for Route Control that needs to be associated with Attached Host Route Redistribution route map.
    type: str
    aliases: [ attached_host_route ]
  bgp:
    description:
    - The BGP routing protocol configuration of the L3Out.
    - Use empty dict ({}) to clear the complete BGP configuration.
    - Use empty string ("") to clear the BGP sub options configuration.
    type: dict
    suboptions:
      inbound_route_map:
        description:
        - The name of the Route Map Policy for Route Control that needs to be associated with inbound route map.
        type: str
        aliases: [ import_route, inbound_route ]
      outbound_route_map:
        description:
        - The name of the Route Map Policy for Route Control that needs to be associated with outbound route map.
        type: str
        aliases: [ export_route, outbound_route ]
      route_dampening_ipv4:
        description:
        - The name of the Route Map Policy for Route Control that needs to be associated with Route Dampening IPv4 route map.
        type: str
        aliases: [ dampening_ipv4 ]
      route_dampening_ipv6:
        description:
        - The name of the Route Map Policy for Route Control that needs to be associated with Route Dampening IPv6 route map.
        type: str
        aliases: [ dampening_ipv6 ]
  ospf:
    description:
    - The OSPF routing protocol configuration of the L3Out.
    - Use empty dict ({}) to clear the complete OSPF configuration.
    - Use empty string ("") to clear the OSPF sub options configuration.
    type: dict
    suboptions:
      area_id:
        description:
        - The area id of the OSPF area.
        type: str
        required: true
      area_type:
        description:
        - The area type of the OSPF area.
        type: str
        choices: [regular, stub, nssa]
        required: true
      cost:
        description:
        - The cost of the OSPF area.
        type: int
        required: true
      originate_summary_lsa:
        description:
        - This option is for OSPF NSSA (not-so-stubby area) or Stub area.
        - When this option is disabled, not only Type 4 and 5, but also Type 3 LSAs are not sent into the NSSA or Stub area by the border leaf.
        - Instead, the border leaf creates and sends a default route to the area.
        - If there is no Type 3 LSA in this area in the first place, a default route is not created.
        type: bool
        aliases: [ originate_lsa ]
      send_redistributed_lsas:
        description:
        - This option is for the OSPF NSSA (not-so-stubby area).
        - When this option is disabled, the redistributed routes are not sent into this NSSA area from the border leaf.
        - This is typically used when the O(ospf.originate_summary_lsa=false).
        - Because disabling the O(ospf.originate_summary_lsa) option creates and sends a default route to the NSSA or Stub area.
        type: bool
        aliases: [ redistributed_lsas ]
      suppress_forwarding_addr_translated_lsa:
        description:
        - This option is for OSPF NSSA (not-so-stubby area).
        - When an OSPF NSSA ABR (Area Border Router) translates a Type-7 LSA into a Type-5 LSA to send it across non-NSSA areas.
        - It typically includes the IP address of the originator ASBR (Autonomous System Boundary Router) as a forwarding address.
        - However, if an OSPF router receiving the Type-5 LSA lacks a route to this forwarding address.
        - The route may not be installed in the router's route table.
        - Enabling this option prevents the ABR from adding a forwarding address during the Type-7 to Type-5 translation, thereby avoiding this issue.
        type: bool
        aliases: [ suppress_fa_lsa ]
      originate_default_route:
        description:
        - The Originate Default Route option in an L3Out configuration allows the ACI fabric to advertise a default route (0.0.0.0/0) to external networks.
        - Use C("") to clear the Originate Default Route option.
        type: str
        choices: [ only, in_addition, "" ]
      originate_default_route_always:
        description:
        - This option is applicable only if OSPF is configured on the L3Out.
        type: bool
        aliases: [ always ]
  state:
    description:
    - Use C(absent) for removing.
    - Use C(query) for listing an object or multiple objects.
    - Use C(present) for creating or updating.
    type: str
    choices: [ absent, query, present ]
    default: query
notes:
- The O(template) must exist before using this module in your playbook.
  Use M(cisco.mso.ndo_template) to create the L3Out template.
- The O(vrf) must exist before using this module in your playbook.
  Use M(cisco.mso.mso_schema_template_vrf) to create the VRF.
- The O(l3_domain) must exist before using this module in your playbook.
  Use M(cisco.mso.ndo_l3_domain) to create the L3Out domain.
seealso:
- module: cisco.mso.mso_schema_template_vrf
- module: cisco.mso.ndo_template
- module: cisco.mso.ndo_l3_domain
extends_documentation_fragment: cisco.mso.modules
"""

EXAMPLES = r"""
- name: Create a new L3Out object
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    name: "l3out_1"
    vrf:
      name: "VRF1"
      schema: "Schema1"
      template: "Template1"
    state: "present"

- name: Update a L3Out object with UUID
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    uuid: "uuid"
    description: "updated description"
    state: "present"

- name: Create a new L3Out object with routing protocols
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    name: "l3out_1"
    vrf:
      name: "VRF1"
      schema: "Schema1"
      template: "Template1"
    bgp:
      inbound_route_map: "ans_route_map"
      outbound_route_map: "ans_route_map"
      route_dampening_ipv4: "ans_route_map"
      route_dampening_ipv6: "ans_route_map"
    ospf:
      area_id: "0.0.0.1"
      area_type: "regular"
      cost: 1
      send_redistributed_lsas: true
      originate_summary_lsa: true
      suppress_forwarding_addr_translated_lsa: true
      originate_default_route: "only"
      originate_default_route_always: false
    interleak: "ans_route_map"
    static_route_redistribution: "ans_route_map"
    connected_route_redistribution: "ans_route_map"
    attached_host_route_redistribution: "ans_route_map"
    state: "present"

- name: Clear an OSPF routing protocol from the existing L3Out with UUID
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    uuid: "uuid"
    ospf: {}
    state: "present"

- name: Query a L3Out object with name
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    name: "l3out_1"
    state: "query"
  register: query_l3out_name

- name: Query a L3Out object with UUID
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    uuid: "uuid"
    state: "query"
  register: query_l3out_uuid

- name: Query all L3Out objects
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    state: "query"
  register: query_all_l3out

- name: Delete a L3Out object with UUID
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    uuid: "uuid"
    state: "absent"

- name: Delete a L3Out object with name
  cisco.mso.ndo_l3out_template:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    l3out_template: l3out_template
    name: "l3out_1"
    state: "absent"
"""

RETURN = r"""
"""

import copy
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.mso.plugins.module_utils.mso import MSOModule, mso_argument_spec
from ansible_collections.cisco.mso.plugins.module_utils.template import MSOTemplate, KVPair
from ansible_collections.cisco.mso.plugins.module_utils.constants import TARGET_DSCP_MAP, ORIGINATE_DEFAULT_ROUTE


def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(
        template=dict(type="str", required=True, aliases=["l3out_template"]),
        name=dict(type="str"),
        uuid=dict(type="str"),
        description=dict(type="str"),
        vrf=dict(
            type="dict",
            options=dict(
                name=dict(type="str", required=True),
                schema=dict(type="str", required=True),
                template=dict(type="str", required=True),
            ),
        ),
        l3_domain=dict(type="str"),
        target_dscp=dict(type="str", choices=list(TARGET_DSCP_MAP)),
        pim=dict(type="bool"),
        interleak=dict(type="str"),
        static_route_redistribution=dict(type="str", aliases=["static_route"]),
        connected_route_redistribution=dict(type="str", aliases=["connected_route"]),
        attached_host_route_redistribution=dict(type="str", aliases=["attached_host_route"]),
        ospf=dict(
            type="dict",
            options=dict(
                area_id=dict(type="str", required=True),
                area_type=dict(type="str", choices=["regular", "stub", "nssa"], required=True),
                cost=dict(type="int", required=True),
                send_redistributed_lsas=dict(type="bool", aliases=["redistributed_lsas"]),
                originate_summary_lsa=dict(type="bool", aliases=["originate_lsa"]),
                suppress_forwarding_addr_translated_lsa=dict(type="bool", aliases=["suppress_fa_lsa"]),
                originate_default_route=dict(type="str", choices=list(ORIGINATE_DEFAULT_ROUTE)),
                originate_default_route_always=dict(type="bool", aliases=["always"]),
            ),
        ),
        bgp=dict(
            type="dict",
            options=dict(
                inbound_route_map=dict(type="str", aliases=["import_route", "inbound_route"]),
                outbound_route_map=dict(type="str", aliases=["export_route", "outbound_route"]),
                route_dampening_ipv4=dict(type="str", aliases=["dampening_ipv4"]),
                route_dampening_ipv6=dict(type="str", aliases=["dampening_ipv6"]),
            ),
        ),
        state=dict(type="str", default="query", choices=["absent", "query", "present"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ["state", "absent", ["name", "uuid"], True],
            ["state", "present", ["vrf", "uuid"], True],
            ["state", "present", ["name", "uuid"], True],
        ],
    )

    mso = MSOModule(module)

    l3out_template = module.params.get("l3out_template")
    name = module.params.get("name")
    uuid = module.params.get("uuid")
    description = module.params.get("description")
    l3_domain = module.params.get("l3_domain")
    pim = module.params.get("pim")
    interleak = module.params.get("interleak")
    static_route_redistribution = module.params.get("static_route_redistribution")
    connected_route_redistribution = module.params.get("connected_route_redistribution")
    attached_host_route_redistribution = module.params.get("attached_host_route_redistribution")
    target_dscp = TARGET_DSCP_MAP.get(module.params.get("target_dscp"))
    vrf_dict = module.params.get("vrf") if module.params.get("vrf") else {}
    ospf = module.params.get("ospf") if module.params.get("ospf") else {}
    bgp = module.params.get("bgp") if module.params.get("bgp") else {}
    state = module.params.get("state")

    l3out_identifier = None
    if state in ["absent", "present"]:
        l3out_identifier = "Name: {0}".format(name) if name is not None else "UUID: {0}".format(uuid)

    l3out_template_object = MSOTemplate(mso, "l3out", l3out_template)
    l3out_template_object.validate_template("l3out")

    tenant_id = l3out_template_object.template_summary.get("tenantId")
    tenant_name = l3out_template_object.template_summary.get("tenantName")

    l3outs = l3out_template_object.template.get("l3outTemplate", {}).get("l3outs", [])

    if state in ["query", "absent"] and l3outs == []:
        mso.exit_json()
    elif state == "query" and not (name or uuid):
        mso.existing = l3outs

    l3out_object = (None, None)
    if l3outs and (name or uuid):
        l3out_kv_list = []

        if uuid:
            l3out_kv_list = [KVPair("uuid", uuid)]
        else:
            l3out_kv_list = [KVPair("name", name)]

        l3out_object = l3out_template_object.get_object_from_list(l3outs, l3out_kv_list)

    l3out_object_index = None
    if l3out_object[0]:
        l3out_object_index = l3out_object[0].index

        if not uuid:
            uuid = l3out_object[0].details.get("uuid")

        if not name:
            name = l3out_object[0].details.get("name")

        mso.existing = copy.deepcopy(l3out_object[0].details)
        mso.previous = copy.deepcopy(l3out_object[0].details)
        proposed_payload = copy.deepcopy(l3out_object[0].details)

    ops = []

    if state == "present":
        if uuid and not mso.existing:
            mso.fail_json(msg="L3Out with the uuid: '{0}' not found".format(uuid))

        templates_objects_path = "templates/objects"
        route_map_params = {"type": "routeMap", "tenant-id": tenant_id}
        route_map_path = l3out_template_object.generate_api_endpoint(templates_objects_path, **route_map_params)
        route_map_objects = mso.query_objs(route_map_path)

        vrf_ref = None
        if vrf_dict:
            vrf_object = l3out_template_object.get_vrf_object(vrf_dict, tenant_id, templates_objects_path)
            if pim and vrf_object.details.get("l3MCast") is False:
                mso.fail_json(
                    msg="Invalid configuration in L3Out '{0}', 'PIM' cannot be enabled while using the VRF '{1}' with L3 Multicast disabled".format(
                        l3out_identifier, vrf_dict.get("name")
                    )
                )
            vrf_ref = vrf_object.details.get("uuid")

        routing_protocols = ""  # Initially routing_protocols="" during the create

        if mso.existing:  # During the update routing_protocols=None to identify the valid change
            routing_protocols = None

        if bgp and ospf:
            routing_protocols = "bgpOspf"
        elif bgp and ospf == {}:
            routing_protocols = "bgp"
        elif bgp == {} and ospf:
            routing_protocols = "ospf"

        if not mso.existing and name:
            payload = dict(name=name)

            payload["vrfRef"] = vrf_ref

            if description:
                payload["description"] = description

            if l3_domain:
                payload["l3domain"] = l3_domain

            if target_dscp:
                payload["targetDscp"] = target_dscp

            if pim is not None:
                payload["pim"] = pim

            if routing_protocols:
                payload["routingProtocol"] = routing_protocols

            outer_route_maps = dict()
            if interleak:
                outer_route_maps["interleakRef"] = l3out_template_object.get_route_map(
                    "interleak",
                    tenant_id,
                    tenant_name,
                    interleak,
                    route_map_objects,
                ).get("uuid", "")

            if static_route_redistribution:
                outer_route_maps["staticRouteRedistRef"] = l3out_template_object.get_route_map(
                    "static_route_redistribution",
                    tenant_id,
                    tenant_name,
                    static_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

            if connected_route_redistribution:
                outer_route_maps["connectedRouteRedistRef"] = l3out_template_object.get_route_map(
                    "connected_route_redistribution",
                    tenant_id,
                    tenant_name,
                    connected_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

            if attached_host_route_redistribution:
                outer_route_maps["attachedHostRouteRedistRef"] = l3out_template_object.get_route_map(
                    "attached_host_route_redistribution",
                    tenant_id,
                    tenant_name,
                    attached_host_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

            if outer_route_maps:
                payload["advancedRouteMapRefs"] = outer_route_maps

            if bgp:
                if bgp.get("inbound_route_map"):
                    payload["importRouteMapRef"] = l3out_template_object.get_route_map(
                        "inbound_route_map",
                        tenant_id,
                        tenant_name,
                        bgp.get("inbound_route_map"),
                        route_map_objects,
                    ).get("uuid", "")

                payload["importRouteControl"] = True if payload.get("importRouteMapRef") else False

                if bgp.get("outbound_route_map"):
                    payload["exportRouteMapRef"] = l3out_template_object.get_route_map(
                        "outbound_route_map",
                        tenant_id,
                        tenant_name,
                        bgp.get("outbound_route_map"),
                        route_map_objects,
                    ).get("uuid", "")

                if bgp.get("route_dampening_ipv4"):
                    payload["advancedRouteMapRefs"]["routeDampeningV4Ref"] = l3out_template_object.get_route_map(
                        "route_dampening_ipv4",
                        tenant_id,
                        tenant_name,
                        bgp.get("route_dampening_ipv4"),
                        route_map_objects,
                    ).get("uuid", "")

                if bgp.get("route_dampening_ipv6"):
                    payload["advancedRouteMapRefs"]["routeDampeningV6Ref"] = l3out_template_object.get_route_map(
                        "route_dampening_ipv6",
                        tenant_id,
                        tenant_name,
                        bgp.get("route_dampening_ipv6"),
                        route_map_objects,
                    ).get("uuid", "")

            if ospf:
                payload["ospfAreaConfig"] = dict(
                    cost=ospf.get("cost"),
                    id=ospf.get("area_id"),
                    areaType=ospf.get("area_type"),
                )

                default_route_leak = dict()
                if ospf.get("originate_default_route"):
                    default_route_leak["originateDefaultRoute"] = ORIGINATE_DEFAULT_ROUTE.get(ospf.get("originate_default_route"))

                if ospf.get("originate_default_route_always") is not None:
                    default_route_leak["always"] = ospf.get("originate_default_route_always")

                if default_route_leak:
                    payload["defaultRouteLeak"] = default_route_leak

                redistribute = ospf.get("send_redistributed_lsas")
                originate = ospf.get("originate_summary_lsa")
                suppress_fa = ospf.get("suppress_forwarding_addr_translated_lsa")

                control = dict()
                if redistribute is not None:
                    control["redistribute"] = redistribute

                if originate is not None:
                    control["originate"] = originate

                if suppress_fa is not None:
                    control["suppressFA"] = suppress_fa

                if control:
                    payload["ospfAreaConfig"]["control"] = control

            mso.sanitize(payload)
            ops = [dict(op="add", path="/l3outTemplate/l3outs/-", value=payload)]
        elif mso.existing:
            update_ops = []
            l3out_attrs_path = "/l3outTemplate/l3outs/{0}".format(l3out_object_index)

            if name is not None and mso.existing.get("name") != name:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/name", value=name))
                proposed_payload["name"] = name

            if vrf_ref is not None and mso.existing.get("vrfRef") != vrf_ref:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/vrfRef", value=vrf_ref))
                proposed_payload["vrfRef"] = vrf_ref

            if description is not None and mso.existing.get("description") != description:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/description", value=description))
                proposed_payload["description"] = description

            if l3_domain is not None and mso.existing.get("l3domain") != l3_domain:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/l3domain", value=l3_domain))
                proposed_payload["l3domain"] = l3_domain

            if target_dscp is not None and mso.existing.get("targetDscp") != target_dscp:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/targetDscp", value=target_dscp))
                proposed_payload["targetDscp"] = target_dscp

            if pim is not None and mso.existing.get("pim") != pim:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/pim", value=pim))
                proposed_payload["pim"] = pim

            if routing_protocols is not None and routing_protocols != "" and mso.existing.get("routingProtocol") != routing_protocols:
                update_ops.append(dict(op="replace", path=l3out_attrs_path + "/routingProtocol", value=routing_protocols))
                proposed_payload["routingProtocol"] = routing_protocols

            if (
                interleak is not None
                or static_route_redistribution is not None
                or connected_route_redistribution is not None
                or attached_host_route_redistribution is not None
            ) and not mso.existing.get("advancedRouteMapRefs"):
                update_ops.append(dict(op="add", path=l3out_attrs_path + "/advancedRouteMapRefs", value=dict()))
                proposed_payload["advancedRouteMapRefs"] = dict()

            outer_route_maps = dict()

            if interleak is not None:
                interleak_ref = l3out_template_object.get_route_map(
                    "interleak",
                    tenant_id,
                    tenant_name,
                    interleak,
                    route_map_objects,
                ).get("uuid", "")

                if interleak_ref and mso.existing.get("advancedRouteMapRefs", {}).get("interleakRef") != interleak_ref:
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/advancedRouteMapRefs/interleakRef", value=interleak_ref))
                    outer_route_maps["interleakRef"] = interleak_ref

            if static_route_redistribution is not None:
                static_route_redistribution_ref = l3out_template_object.get_route_map(
                    "static_route_redistribution",
                    tenant_id,
                    tenant_name,
                    static_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

                if (
                    static_route_redistribution_ref
                    and mso.existing.get("advancedRouteMapRefs", {}).get("staticRouteRedistRef") != static_route_redistribution_ref
                ):
                    update_ops.append(
                        dict(op="replace", path=l3out_attrs_path + "/advancedRouteMapRefs/staticRouteRedistRef", value=static_route_redistribution_ref)
                    )
                    outer_route_maps["staticRouteRedistRef"] = static_route_redistribution_ref

            if connected_route_redistribution is not None:
                connected_route_redistribution_ref = l3out_template_object.get_route_map(
                    "connected_route_redistribution",
                    tenant_id,
                    tenant_name,
                    connected_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

                if (
                    connected_route_redistribution_ref
                    and mso.existing.get("advancedRouteMapRefs", {}).get("connectedRouteRedistRef") != connected_route_redistribution_ref
                ):
                    update_ops.append(
                        dict(op="replace", path=l3out_attrs_path + "/advancedRouteMapRefs/connectedRouteRedistRef", value=connected_route_redistribution_ref)
                    )
                    outer_route_maps["connectedRouteRedistRef"] = connected_route_redistribution_ref

            if attached_host_route_redistribution is not None:
                attached_host_route_redistribution_ref = l3out_template_object.get_route_map(
                    "attached_host_route_redistribution",
                    tenant_id,
                    tenant_name,
                    attached_host_route_redistribution,
                    route_map_objects,
                ).get("uuid", "")

                if (
                    attached_host_route_redistribution_ref
                    and mso.existing.get("advancedRouteMapRefs", {}).get("attachedHostRouteRedistRef") != attached_host_route_redistribution_ref
                ):
                    update_ops.append(
                        dict(
                            op="replace",
                            path=l3out_attrs_path + "/advancedRouteMapRefs/attachedHostRouteRedistRef",
                            value=attached_host_route_redistribution_ref,
                        )
                    )
                    outer_route_maps["attachedHostRouteRedistRef"] = attached_host_route_redistribution_ref

            proposed_payload["advancedRouteMapRefs"] = outer_route_maps

            if bgp:
                if bgp.get("inbound_route_map") is not None:
                    inbound_route_map_ref = l3out_template_object.get_route_map(
                        "inbound_route_map",
                        tenant_id,
                        tenant_name,
                        bgp.get("inbound_route_map"),
                        route_map_objects,
                    ).get("uuid", "")

                    if inbound_route_map_ref and mso.existing.get("importRouteMapRef") != inbound_route_map_ref:
                        update_ops.append(dict(op="replace", path=l3out_attrs_path + "/importRouteMapRef", value=inbound_route_map_ref))
                        update_ops.append(dict(op="replace", path=l3out_attrs_path + "/importRouteControl", value=True if inbound_route_map_ref else False))
                        proposed_payload["importRouteMapRef"] = inbound_route_map_ref
                        proposed_payload["importRouteControl"] = True if inbound_route_map_ref else False

                if bgp.get("outbound_route_map") is not None:
                    outbound_route_map_ref = l3out_template_object.get_route_map(
                        "outbound_route_map",
                        tenant_id,
                        tenant_name,
                        bgp.get("outbound_route_map"),
                        route_map_objects,
                    ).get("uuid", "")

                    if outbound_route_map_ref and mso.existing.get("exportRouteMapRef") != outbound_route_map_ref:
                        update_ops.append(dict(op="replace", path=l3out_attrs_path + "/exportRouteMapRef", value=outbound_route_map_ref))
                        proposed_payload["exportRouteMapRef"] = outbound_route_map_ref

                if bgp.get("route_dampening_ipv4") is not None:
                    route_dampening_ipv4_ref = l3out_template_object.get_route_map(
                        "route_dampening_ipv4",
                        tenant_id,
                        tenant_name,
                        bgp.get("route_dampening_ipv4"),
                        route_map_objects,
                    ).get("uuid", "")

                    if route_dampening_ipv4_ref and mso.existing.get("advancedRouteMapRefs", {}).get("routeDampeningV4Ref") != route_dampening_ipv4_ref:
                        update_ops.append(
                            dict(op="replace", path=l3out_attrs_path + "/advancedRouteMapRefs/routeDampeningV4Ref", value=route_dampening_ipv4_ref)
                        )
                        proposed_payload["advancedRouteMapRefs"]["routeDampeningV4Ref"] = route_dampening_ipv4_ref

                if bgp.get("route_dampening_ipv6") is not None:
                    route_dampening_ipv6_ref = l3out_template_object.get_route_map(
                        "route_dampening_ipv6",
                        tenant_id,
                        tenant_name,
                        bgp.get("route_dampening_ipv6"),
                        route_map_objects,
                    ).get("uuid", "")

                    if route_dampening_ipv6_ref and mso.existing.get("advancedRouteMapRefs", {}).get("routeDampeningV6Ref") != route_dampening_ipv6_ref:
                        update_ops.append(
                            dict(op="replace", path=l3out_attrs_path + "/advancedRouteMapRefs/routeDampeningV6Ref", value=route_dampening_ipv6_ref)
                        )
                        proposed_payload["advancedRouteMapRefs"]["routeDampeningV6Ref"] = route_dampening_ipv6_ref

            if ospf:
                originate_default_route = ORIGINATE_DEFAULT_ROUTE.get(ospf.get("originate_default_route"))
                originate_default_route_always = ospf.get("originate_default_route_always")

                if originate_default_route is not None and originate_default_route != "":
                    if not mso.existing.get("defaultRouteLeak"):
                        update_ops.append(dict(op="replace", path=l3out_attrs_path + "/defaultRouteLeak", value=dict()))
                        proposed_payload["defaultRouteLeak"] = dict()

                    if originate_default_route != mso.existing.get("defaultRouteLeak", {}).get("originateDefaultRoute"):
                        update_ops.append(
                            dict(
                                op="replace",
                                path=l3out_attrs_path + "/defaultRouteLeak/originateDefaultRoute",
                                value=originate_default_route,
                            )
                        )
                        proposed_payload["defaultRouteLeak"]["originateDefaultRoute"] = originate_default_route

                    if originate_default_route_always is not None and originate_default_route_always != mso.existing.get("defaultRouteLeak", {}).get("always"):
                        update_ops.append(dict(op="replace", path=l3out_attrs_path + "/defaultRouteLeak/always", value=originate_default_route_always))
                        proposed_payload["defaultRouteLeak"]["always"] = originate_default_route_always

                elif mso.existing.get("defaultRouteLeak") and originate_default_route == "":
                    update_ops.append(dict(op="remove", path=l3out_attrs_path + "/defaultRouteLeak"))
                    del proposed_payload["defaultRouteLeak"]
                    del mso.existing["defaultRouteLeak"]

                if not mso.existing.get("ospfAreaConfig"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig", value=dict()))
                    proposed_payload["ospfAreaConfig"] = dict()

                if ospf.get("cost") != mso.existing.get("ospfAreaConfig", {}).get("cost"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/cost", value=ospf.get("cost")))
                    proposed_payload["ospfAreaConfig"]["cost"] = ospf.get("cost")

                if ospf.get("area_id") != mso.existing.get("ospfAreaConfig", {}).get("id"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/id", value=ospf.get("area_id")))
                    proposed_payload["ospfAreaConfig"]["id"] = ospf.get("area_id")

                if ospf.get("area_type") != mso.existing.get("ospfAreaConfig", {}).get("areaType"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/areaType", value=ospf.get("area_type")))
                    proposed_payload["ospfAreaConfig"]["areaType"] = ospf.get("area_type")

                redistribute = ospf.get("send_redistributed_lsas")
                originate = ospf.get("originate_summary_lsa")
                suppress_fa = ospf.get("suppress_forwarding_addr_translated_lsa")

                if (redistribute is not None or originate is not None or suppress_fa is not None) and not mso.existing.get("ospfAreaConfig", {}).get(
                    "control"
                ):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/control", value=dict()))
                    proposed_payload["ospfAreaConfig"]["control"] = dict()

                if redistribute is not None and redistribute != mso.existing.get("ospfAreaConfig", {}).get("control", {}).get("redistribute"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/control/redistribute", value=redistribute))
                    proposed_payload["ospfAreaConfig"]["control"]["redistribute"] = redistribute

                if originate is not None and originate != mso.existing.get("ospfAreaConfig", {}).get("control", {}).get("originate"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/control/originate", value=originate))
                    proposed_payload["ospfAreaConfig"]["control"]["originate"] = originate

                if suppress_fa is not None and suppress_fa != mso.existing.get("ospfAreaConfig", {}).get("control", {}).get("suppressFA"):
                    update_ops.append(dict(op="replace", path=l3out_attrs_path + "/ospfAreaConfig/control/suppressFA", value=suppress_fa))
                    proposed_payload["ospfAreaConfig"]["control"]["suppressFA"] = suppress_fa

            elif mso.existing.get("ospfAreaConfig") and not ospf:
                update_ops.append(dict(op="remove", path=l3out_attrs_path + "/ospfAreaConfig"))
                del proposed_payload["ospfAreaConfig"]
                del mso.existing["ospfAreaConfig"]

            mso.sanitize(proposed_payload, collate=True)
            ops = update_ops

        mso.existing = mso.proposed

    elif state == "absent":
        if mso.existing:
            ops = [dict(op="remove", path="/l3outTemplate/l3outs/{0}".format(l3out_object_index))]
        mso.existing = {}

    if not module.check_mode and ops:
        l3out_template_path = "{0}/{1}".format(l3out_template_object.templates_path, l3out_template_object.template_id)
        mso.request(l3out_template_path, method="PATCH", data=ops)

    mso.exit_json()


if __name__ == "__main__":
    main()