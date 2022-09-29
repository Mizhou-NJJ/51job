import socket
from config import PC
from entity.entity import Task,CMD
from tool.tool import Log as log
def get_task(queue):

    # log.taskstart('拉取任务...')
    cmd = CMD()
    cmd.type=log.TASKSTART
    cmd.msg = '拉取任务...'
    queue.put(cmd)
    s = socket.socket()
    host = PC.host
    port = PC.port
    data = None
    try:
        s.connect((host, port))
        s.settimeout(10)
        s.send(('code:PULL_TASK&id:' + PC.uid).encode('utf-8'))
        data = s.recv(1024)
        s.close()
        #  处理响应体
        # print(data.decode('gbk'))

    except:
        cmd = CMD()
        cmd.type =log.EXIT
        queue.put(cmd)
    else:
        data = data.decode('utf-8')
        # data = data.encode('utf-8')
        k_v = data.split('&')
        kv = {}
        for item in k_v:
            ox02 = item.split(':')
            kv[ox02[0]] = ox02[1]
        task = Task()
        task.status = kv['status']
        if task.status == '000':
            task.msg = kv['msg']
            task.modelkey = 'NULL'
            task.key = 'NULL'
            task.citycode = 'NULL'
            task.cityname = 'NULL'
            task.pageno = 0
        else:
            task.modelkey = kv['modelkey']
            task.key = kv['key']
            task.citycode = kv['citycode']
            task.cityname = kv['cityname']
            task.msg = kv['msg']
            task.pageno = 0
    # s.connect((host, port))
    # s.settimeout(5)
    # s.send(('code:PULL_TASK&id:' + PC.uid).encode('utf-8'))
    # data = s.recv(1024)
    # s.close()
    # #  处理响应体
    # # print(data.decode('gbk'))
    # data = data.decode('utf-8')
    # # data = data.encode('utf-8')
    # k_v = data.split('&')
    # kv = {}
    # for item in k_v:
    #     ox02 = item.split(':')
    #     kv[ox02[0]] = ox02[1]
    # task = Task()
    # task.status = kv['status']
    # if task.status =='000':
    #     task.msg = kv['msg']
    #     task.modelkey = 'NULL'
    #     task.key = 'NULL'
    #     task.citycode = 'NULL'
    #     task.cityname = 'NULL'
    #     task.pageno = 0
    # else:
    #     task.modelkey = kv['modelkey']
    #     task.key = kv['key']
    #     task.citycode = kv['citycode']
    #     task.cityname = kv['cityname']
    #     task.msg = kv['msg']
    #     task.pageno = 0

    return task