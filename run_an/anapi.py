#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-27  上午9:08
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: anapi.py
# @SoftWare	: PyCharm
import os
from bt2.settings import BASE_DIR
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.playbook import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.config.manager import namedtuple
from ansible import constants

class Common_inventory_vars(object):
    def __init__(self):
        self.dataloader=DataLoader()
        self.inventory_file=os.path.join(BASE_DIR,'run_an/aninfo/hosts')
        self.inventory=InventoryManager(loader=self.dataloader,sources=[self.inventory_file])
        self.varobj=VariableManager(loader=self.dataloader,inventory=self.inventory)
        self.hostip=None
    def check_host(self,chip):
        self.hostip=chip
        if self.inventory.get_host(self.hostip):
            return True
        else: return False
    def add_host(self,add_to_group):
        self.inventory.add_host(host=self.hostip,group=add_to_group)
    def check_group(self,groupname):
        inventory_file_all_groups=self.inventory.groups
        if groupname in inventory_file_all_groups:  return True
        else:   return False
    def add_group(self,add_groupname):
        self.inventory.add_group(add_groupname)

class Adhoc_callback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(Adhoc_callback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result._result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result._result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result._result

class Playbook_callback(CallbackBase):
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(Playbook_callback, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }

class Run_ansible(object):
    def __init__(self):
        self.commonobj=Common_inventory_vars()
        self.options=None
        self.passwords=dict(sshpass=None, becomepass=None)
        self.callback=None
    def init_ansible(self):
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=True)

    def adhoc_run(self,hostip,module_name,module_args):
        self.callback = Adhoc_callback()
        play_source = dict(
            name="Ansible adhoc Play",
            hosts=hostip,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args,))]
        )

        play = Play().load(play_source, variable_manager=self.commonobj.varobj, loader=self.commonobj.dataloader)
        tqm = None
        # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
        # else:self.callback = ModelResultsCollector()
        # self.callback = ModelResultsCollector()
        import traceback
        try:
            tqm = TaskQueueManager(
                inventory=self.commonobj.inventory,
                variable_manager=self.commonobj.varobj,
                loader=self.commonobj.dataloader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback,
            )
            # tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            tqm.run(play)
        except Exception as err:
            print traceback.print_exc()
            # DsRedis.OpsAnsibleModel.lpush(self.redisKey,data=err)
            # if self.logId:AnsibleSaveResult.Model.insert(self.logId, err)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def playbook_run(self, playbook_path,extra_vars=None):
        try:
            # if self.redisKey:self.callback = PlayBookResultsCollectorToSave(self.redisKey,self.logId)
            self.callback = Playbook_callback()
            if extra_vars:
                self.commonobj.varobj.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path],
                inventory=self.commonobj.inventory,
                variable_manager=self.commonobj.varobj,
                loader=self.commonobj.dataloader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            executor.run()
        except Exception as err:
            return False

    def get_adhoc_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['success'][hostvisiable] = result

        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['failed'][hostvisiable] = result

        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['unreachable'][hostvisiable] = result

        # return json.dumps(self.results_raw)
        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result._result['stdout_lines']

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        # for host, result in self.callback.task_changed.items():
        #     self.results_raw['changed'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result
        return self.results_raw

# Ip='192.168.0.81'
# ll=Run_ansible()
# ll.init_ansible()
# common=Common_inventory_vars()
# if common.check_host(Ip):
#     ll.adhoc_run(Ip,'shell','hostname')
#     print(ll.get_model_result())
#     print(ll.get_model_result()['success'] == {})
# else:
#     print('ip not in inventory file')

# ip='192.168.0.212'
# ymlfile=os.path.join(BASE_DIR,'run_an/yaml/find_service/java.yml')
# pp=Run_ansible()
# pp.init_ansible()
# pp.playbook_run(ymlfile,{'Hosts':ip})
# res=pp.get_playbook_result()
# print(res)
# print(res['ok'][ip])