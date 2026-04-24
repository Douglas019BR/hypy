"""
Printer module. Formats messages to be printed in command line.
"""
from datetime import timedelta
from fnmatch import fnmatch

from hypy.modules.snaptree import create_tree

STATES = {3: 'off',
          2: 'running',
          9: 'paused',
          6: 'saved'}
ADJ = {'index': 3,
       'state': 7,
       'name': 30,
       'ip': 15}


def print_vm_switch(switch_json: dict):
    """
    Print virtual machine's current virtual network switch.

    Args:
        switch_json: Dict containing current switch information.
    """
    if isinstance(switch_json, dict):
        switch_json = [switch_json]

    print("{} {}".format("VMName".ljust(ADJ['name']), "SwitchName"))
    for switch in switch_json:
        print("{} {}".format(str(switch['VMName']).ljust(ADJ['name']), switch['SwitchName']))


def print_switches(switches_json: dict):
    """
    Print a list of virtual network switches.

    Args:
        switches_json: Dict containing the table of switches.
    """
    print("-- Virtual network switches --")

    # Listing
    for switch in switches_json:
        print(switch['Name'])


def print_vm_snaps(snaps_json: dict, vm_name: str, current_snap: str):
    """
    Print ascii tree of checkpoints.

    Args:
        snaps_json: Dict containing the table of checkpoints.
        vm_name: Vm name to be shown as root of the tree.
    """
    if snaps_json:
        # If there is only one element, make it a list
        if isinstance(snaps_json, dict):
            snaps_json = [snaps_json]

        t_snaps = create_tree(snaps_json,
                              vm_name,
                              mark=current_snap,
                              f_pid="ParentSnapshotId",
                              f_id="Id",
                              f_label="Name",
                              f_ctime="CreationTime",
                              v_none=None)
        print("-- Virtual Machine Snapshots --")
        print(t_snaps)
    else:
        print("{} has no snapshots".format(vm_name))


def print_list_vms(vms_json: dict, filter_vms: str, show_ip: bool = False):
    """
    Print list of virtual machines.

    Args:
        vms_json: Dict containing the table of vms.
        filter_vms: Filter to be applied at the output. Only the vms whose name
            matches the filter will be shown.
        show_ip: Whether to show IP addresses column.
    """
    # Listing
    # print("-- Hyper-V Virtual Machine Listing --")

    # Header
    header = "{} {} {}".format("Index".rjust(ADJ['index']),
                               "State".ljust(ADJ['state']),
                               "Name".ljust(ADJ['name']))
    if show_ip:
        header += " {}".format("IP Address".ljust(ADJ['ip']))
    header += " Uptime"
    print(header)

    if filter_vms:
        vms_show = [vm for vm in vms_json if fnmatch(vm['Name'], filter_vms)]
    else:
        vms_show = vms_json

    # Listing
    for vm in vms_show:
        index = str(vms_json.index(vm)).rjust(ADJ['index'])
        state = STATES.get(vm['State'], "unknown").ljust(ADJ['state'])
        name = str(vm['Name']).ljust(ADJ['name'])

        row = "[{}] {} {}".format(index, state, name)

        if show_ip:
            ip_addr = vm.get('IPAddress', 'N/A')
            if ip_addr is None:
                ip_addr = 'N/A'
            row += " {}".format(str(ip_addr).ljust(ADJ['ip']))

        uptime = str(timedelta(hours=vm['Uptime']['TotalHours']))
        row += " {}".format(uptime)

        print(row)
