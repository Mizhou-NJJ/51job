import os
from config import Config
from config import PC
from entity.entity import Task
IS_DEBUG = True
IS_LOOP_QUEUE =True


class OocFile:
    def __init__(self):
        pass

    def judge_and_create(self, strPath, cfile=False):
        # '''
        #  创建文件或文件夹
        #  如果文件不存在则创建
        # :param strPath: 文件路径 例如:d:\\xx\xx\xx.x
        # :cfile 是否创建文件 例如：路径中包含xx.x的文件，是否传教，默认只创建文件夹
        # :return:
        # '''
        if strPath == None and strPath != '':
            raise Exception('无效路径')
            return
        ps = None
        if '/' in strPath:
            ps = strPath.split('/')
        if '\\' in strPath:
            ps = strPath.split('\\')
        fullPath = ''
        for pa in ps:
            if fullPath == '':
                fullPath = pa
            else:
                fullPath = fullPath + "\\" + pa
            if '.' not in pa:
                if not os.path.exists(fullPath):
                    os.makedirs(fullPath)
            else:
                if not os.path.exists(fullPath) and cfile:
                    open(fullPath, 'w')
        if cfile:
            return fullPath
        else:
            pat = ''
            for i in range(0, len(ps)):
                if pat == '':
                    pat = ps[i]
                else:
                    pat = pat + '\\' + ps[i]
            return pat

    def save_task_status(self, task=None):
        '''

        :param modelkey:
        :param key:
        :param city:
        :param pageno:
        :return:
        '''
        if task is None:
            raise Exception('task is None')
        else:
            path = PC.tasksaveas+task.pid+'.txt'
            self.judge_and_create(strPath=path)
            with open(path, 'w+',encoding='utf8') as f:
                f.writelines('status=' + task.status + '\n')
                f.writelines('modelkey=' + task.modelkey + '\n')
                f.writelines('key=' + task.key + '\n')
                f.writelines('citycode=' + task.citycode + '\n')
                f.writelines('cityname=' + task.cityname + '\n')
                f.writelines('pageno=' + str(task.pageno) + '\n')

    def read_localtask(self,pid):
        '''
        读取本地任务信息, status == 000 无本地任务
        status == 200 有本地任务
        :return: 本地任务信息
        '''
        task = Task()
        with open(PC.tasksaveas+pid+'.txt', 'r+',encoding='utf-8') as f:
            task.status = f.readline().split('=')[1].replace('\n', '')
            task.modelkey = f.readline().split('=')[1].replace('\n', '')
            task.key = f.readline().split('=')[1].replace('\n', '')
            task.citycode = f.readline().split('=')[1].replace('\n', '')
            task.cityname = f.readline().split('=')[1].replace('\n', '')
            task.pageno = int(f.readline().split('=')[1].replace('\n', ''))
        return task


class Log:
    NOMAL = 0x00
    WARNING = 0x01
    SUCCESS = 0x02
    ERROR = 0x03
    TASKSTART = 0x04
    EXIT = 0xEA
    POWER_EXIT = 0xFF
    def normal(log=None):
        if IS_DEBUG:
            # print('\033[1;37;40m' , end='')
            print(log)
            # print('wocao')
            # print('\033[0m')
            # print('haha')

    def warning(log=None):
        if IS_DEBUG:
            print('\033[1;33;40m', end='')
            print(log)
            print('\033[0m', end='')

    def success(log=None):
        if IS_DEBUG:
            print('\033[0;32;40m', end='')
            print(log)
            print('\033[0m', end='')

    def error(log=None):
        if IS_DEBUG:
            print('\033[0;31;40m', end='')
            print(log)
            print('\033[0m', end='')

    def taskstart(log=None):
        if IS_DEBUG:
            print('\033[0;34;40m', end='')
            print(log)
            print('\033[0m', end='')

