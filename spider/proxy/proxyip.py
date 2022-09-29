from bs4 import BeautifulSoup
import requests
from config import IPConfig
from tool.tool import Log as log
from tool.tool import OocFile
from threading import Thread, Lock


class ProxyIP:
    def __init__(self):
        self.availableips = []  # 可以使用的ip列表
        self.checking = 0  # 正在
        self.checkingcount = 0  # 一次检查多少个，及开辟几个线程
        self.taskcount = 0  # 总任务 一个ip一个任务
        self.lock = Lock()
        self.befips = None
        self.isChecking = False

    def get_89free_ips(self, save=True):
        '''
         获取 89免费代理的 代理ip列表
         保存至本地文件时，为覆盖方式
        :param save: 是否保存至本地 保存路径在 config.py中
        :return:
        '''
        ips = []
        api = IPConfig._89_FREE_PROXY['api']
        log.taskstart('开始获取代理ip api=' + api + '...')
        rep = requests.get(api)
        if rep.status_code == 200:
            bs4 = BeautifulSoup(rep.content, 'lxml')
            # print(bs4.prettify())
            div = bs4.find_all('div', 'fly-panel')[0]
            tgdiv = None
            for t in div.contents:
                if t.name == 'div':
                    tgdiv = t
            for t in tgdiv.contents:
                if t.string is not None and 'ip' not in t.string:
                    v = t.string.replace(' ', '')
                    ips.append(v)
            # save as path
            if save:
                sp = IPConfig._89_FREE_PROXY['saveas']
                OocFile.judge_and_create(strPath=sp)
                with open(sp, 'w+') as f:
                    for i in range(1, len(ips)):
                        f.write(ips[i] + '\n')
                log.success('代理ip获取成功...已保存至' + sp)
        else:
            log.error('代理ip获取失败' + rep.status_code)
        log.success('ip获取成功...')
        return ips

    def get_xila_ips(self, save=True):
        '''
         从西拉免费代理ip获取
         同上
        :param save: 是否保存至本地
        :return: ip列表
        '''
        ips = []
        api = IPConfig.XL_FREE_PROXY['api']
        log.taskstart('开始获取代理ip...')
        rep = requests.get(api)
        if rep.status_code == 200:
            bs4 = BeautifulSoup(rep.content, 'lxml')
            tbody = bs4.find_all(name='tbody')[0]
            trs = tbody.contents
            for t in trs:
                if t.name == 'tr':
                    tds = t.contents
                    ip = tds[1].string
                    ip = ip.replace(' ', '')
                    ip = ip.replace('\r\n', '')
                    ips.append(ip)
            # write
            if save:
                ipf = IPConfig.XL_FREE_PROXY['saveas']
                OocFile.judge_and_create(strPath=ipf)
                with open(ipf, 'w+') as f:
                    for ip in ips:
                        f.write(ip + '\n')
                log.success('代理ip获取成功...已保存至' + ipf)
        else:
            log.error('代理ip获取失败' + rep.status_code)
        log.success('ip获取成功...')
        return ips

    def is_ip_available(self, ip=None):
        '''
        检查 ip是否可用
        :param ip:
        :return:
        '''

        if ip == None or len(ip) == 0:
            raise Exception('ip不能为空')
            return
        status_code = 0
        try:
            rep = requests.get('http://' + ip, timeout=5)
            if rep is not None:
                status_code = rep.status_code
        except:
            pass
        return self.on_ipchecked(True, ip) if status_code == 200 else self.on_ipchecked(False, None)
        # if status_code == 200:
        #     log.success(ip)

    def check_ips(self, ips=None, checkingcount=3):
        if ips == None or len(ips) == 0:
            raise Exception('ip列表为空 ips=None')
            return
        log.taskstart('正在检测ip....')
        self.befips = ips
        self.checkingcount = checkingcount
        self.taskcount = len(ips)
        #     开启 3 个线程检测
        theads = []
        for _ in range(0, checkingcount):
            t = Thread(target=self.is_ip_available, args=(self.befips[self.taskcount - 1],))
            self.taskcount = self.taskcount - 1
            theads.append(t)
        for t in theads:
            t.start()
        self.isChecking = True
        while (self.isChecking):
            pass
        log.success('ip检测完成...')
        log.normal(self.availableips)
        return self.availableips

    def on_ipchecked(self, result, ip):
        '''
         ip检测完成后的回调方法,此方法保证了 在任务充足时 总会有 {@self.checkingcout} 个线程在运行
        :param result: ip 检测结果
        :param ip: 可用的ip
        :return: None
        '''
        if result:
            self.availableips.append(ip)
        self.lock.acquire()  # --------------Lock------------------------------------------------
        self.checkingcount = self.checkingcount - 1
        self.taskcount = self.taskcount - 1
        if self.taskcount >= 0:
            self.checkingcount = self.checkingcount + 1
            Thread(target=self.is_ip_available, args=(self.befips[self.taskcount],)).start()
        if self.checkingcount <= 0:
            self.isChecking = False
        self.lock.release()  # ---------------------------Release Lock ---------------------------------------


# if __name__ == '__main__':
#     pip = ProxyIP()
#     # ips = pip.get_89free_ips(save=False)
#     ips = pip.get_xila_ips(save=False)
#     avips = pip.check_ips(ips=ips)
#     print(avips)
    # pip.get_ips()
