#!/usr/bin/env python

import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

get_result={'status':None,'data':None}
hostfile=os.path.join(os.path.dirname(os.path.abspath(__file__)),'aninfo/hosts')

class ops_ip():
    def __init__(self,IP,Group):
        self.IP=IP
        self.Group=Group
    def add_ip(self):
        keyword = str(self.Group)+']'
        i = '\n'+str(self.IP)
        try:
            file = open(hostfile, 'r')
            content = file.read()
            post = content.find(keyword)
            if post != -1:
                content = content[:post + len(keyword)] + i + content[post + len(keyword):]
                file = open(hostfile, 'w')
                file.write(content)
            file.close()
        except Exception as e:
            print(e)
            return 0
        return 1
    def check_ip(self):
        try:
            file = open(hostfile, 'r')
            content = file.read()
            post = content.find(self.IP)
            file.close()
            if post != -1:
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            return 0
    def del_ip(self):
        keyword='\n'+str(self.IP)
        try:
            file = open(hostfile, 'r')
            content = file.read()
            post = content.find(keyword)
            if post != -1:
                content = content[:post] + content[post + len(keyword):]
                file = open(hostfile, 'w')
                file.write(content)
            file.close()
        except Exception as e:
            print(e)
            return 0
        return 1
class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        global get_result
        get_result['status']='ok'
        get_result['data']=result._result
    # def v2_runner_on_unreachable(self, result):
    #     global get_result
    #     get_result=result._result['msg']
    def v2_runner_on_failed(self, result, ignore_errors=False):
        global get_result
        get_result['status'] = 'failed'
        get_result['data'] = result._result
def an_shell(IP,cmd,Module='shell'):
    r=ops_ip(IP,'kaifa')
    if not r.check_ip():
        r.add_ip()
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    # initialize needed objects
    loader = DataLoader()
    options = Options(connection='paramiko', module_path='', forks=100, become=None, become_method=None, become_user=None, check=False,
                      diff=False)
    passwords = dict(vault_pass='')

    # Instantiate our ResultCallback for handling results as they come in
    results_callback = ResultCallback()

    # create inventory and pass to var manager
    inventory = InventoryManager(loader=loader, sources=[hostfile])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create play with tasks
    play_source =  dict(
            name = "Ansible adhoc Play",
            hosts = IP,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=Module, args=cmd), register='shell_out'),
             ]
        )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                  passwords=passwords,
                  stdout_callback=results_callback,
              )
        tqm.run(play)

        return get_result
    finally:
        if tqm is not None:
            tqm.cleanup()
#r=an_shell('192.168.0.212','','setup')


class Get_setup_info(object):
    def __init__(self,IP):
        self.IP=IP
        self.result=None
    def give_result(self):
        data=an_shell(self.IP,'','setup')
        self.result=data['data']['ansible_facts']
    def diskinfo(self):
        d=[{i['mount']:{"total":str(i['size_total']/ 1024 / 1024),"free":str(i['size_available']/ 1024 / 1024)}} for i in self.result['ansible_mounts']]
        return d
    def meminfo(self):
        mem={'total':str(self.result['ansible_memory_mb']['real']['total']),'used':str(self.result['ansible_memory_mb']['nocache']['used']),'free':str(self.result['ansible_memory_mb']['nocache']['free']),'swap':self.result['ansible_memory_mb']['swap']}
        return mem
    def hostnameinfo(self):
        hname=self.result['ansible_hostname']
        return hname
    def kernelinfo(self):
        k=self.result['ansible_lsb']['description'] + ' '+self.result['ansible_machine'] +' '+ self.result['ansible_kernel']
        return k
    def networkinfo(self):
        tmp=self.result
        info=[{tmp['ansible_facts']['ansible_'+i]['device']:{'ip':tmp['ansible_facts']['ansible_'+i]['ipv4']['address'],'mac':tmp['ansible_facts']['ansible_'+i]['macaddress']}} for i in tmp['ansible_facts']['ansible_interfaces'] if i != "lo"]
        return info
    def cpunumberinfo(self):
        num=self.result['ansible_processor_count']
        return num
class shell_info(object):
    def __init__(self,IP,cmd,Module):
        self.IP=IP
        self.result=None
        self.Module=Module
        self.cmd=cmd
    def give_result(self):
        self.result=an_shell(self.IP,self.cmd,self.Module)
    def get_info(self):
        data=None
        if self.result['status'] == 'ok':
            data=self.result['data']['stdout']
        elif self.result['status'] == 'failed':
            data = self.result['data']['stderr_lines']
        return data


# r=Get_setup_info('192.168.0.211')
# r.give_result()
# print(r.hostnameinfo())