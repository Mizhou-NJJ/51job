from sock.sock import get_task
from tool.tool import OocFile
from config import PC
from tool.tool import Log as log
import os
from job51 import Job51
from proxy.proxyip import ProxyIP
from multiprocessing import Process,Queue
from threading import Thread
from entity.entity import CMD


PID = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
       'Q','R','S','T','U','V','W','X','Y','Z']
# ja
def start(pid,queue):
    task = init(pid,queue)
    if task is not None:
        if task.status == '000':
            # log.success('无待处理任务---进程:'+pid)
            cmd = CMD()
            cmd.type=log.SUCCESS
            cmd.msg = '无待处理任务---进程:'+pid
            queue.put(cmd)
            cmd = CMD()
            cmd.type = log.EXIT
            queue.put(cmd)
        elif task.status == '200':
            job51 = Job51(queue=queue)
            proxy = {
                "https": "223.82.106.253:3128"
            }
            job51.start(task=task,proxies=None)


def init(pid,queue):
    # 初始化本地任务
    of = OocFile()
    if os.path.exists(PC.tasksaveas+pid+'.txt'):
        task = of.read_localtask(pid=pid)
        task.pid = pid
        if task.status == '000':  # 本地任务已经完成
            task= get_task(queue)  # 从服务器拉去任务 task is Task
            task.pid = pid
            if task.status =='200':
                of.save_task_status(task)  # 跟新本地任务
        elif task.status == '200':  # 使用本地任务
            # _+_+_+_+_=_=
            pass
        return task
    else:
        task = get_task(queue)
        task.pid = pid
        of.save_task_status(task=task)
        return task


def fork_and_start(queue,processCount = 5):
    ps = []
    for i in  range(0,processCount):
        newp = Process(target=start, args=(PID[i], queue))
        ps.append(newp)
    for p in ps:
        p.start()

def loop_queue(queue,pcount):
    overp = 0
    while True:
        cmd = queue.get(True)
        if cmd.type == log.EXIT:
            overp = overp + 1
            if overp >= pcount: # 本轮任务已完成
                return None

        elif cmd.type == log.POWER_EXIT:  #  强制退出
            return None
        elif cmd.type == log.TASKSTART:
            log.taskstart(cmd.msg)
        elif cmd.type == log.NOMAL:
            log.normal(cmd.msg)
        elif cmd.type == log.SUCCESS:
            log.success(cmd.msg)
        elif cmd.type == log.WARNING:
            log.warning(cmd.msg)
        elif cmd.type == log.ERROR:
            log.error(cmd.msg)


def main():
    # pip = ProxyIP()
    # ips = pip.get_xila_ips(save=False)
    max_task = 100
    now_task = 0
    #############################################################
    process_count = 5      #       一次任务开启的进程数         #
    ##############################################################
    queue = Queue()
    fork_and_start(queue, processCount=process_count)
    while now_task < max_task:
        now_task = now_task +1
        th = Thread(target=loop_queue, args=(queue, process_count))
        th.start()
        th.join()
        fork_and_start(queue=queue,processCount=process_count)


if __name__ == '__main__':
    main()
 