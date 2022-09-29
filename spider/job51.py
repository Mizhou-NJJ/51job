"""
前程无忧 51job
"""
import requests
import xml.dom.minidom as md
from pubdate import KW_PREFIX, KW_OUTER
from xls import XLS
from config import Config
from tool.tool import Log as log
from tool.tool import OocFile
from  entity.entity import AbstractJob,Job,Task,CMD

class Job51:
    queue = None
    STA_OK = 200
    STA_NOT_FOUND = 404
    STA_ERROR = 500
    PARTNER = '722c9d11cdb268775790fffbca28914c'
    UUID = '6c77e7936e40b8cc1758999f5be9ed88'
    GUDI = '89eef0d82320e918ab4dde0ccd98e3ca'
    headers = {
        "Accept-Encoding": "gzip",
        "Host": "appapi.51job.com",
        "User-Agent": "51job-android-client"
    }
    parames = {
        "postchannel": "0000",
        "keyword": "",
        "keywordtype": "all",
        "jobarea": "",
        "famoustype": "",
        "iswangshen": "",
        "pageno": "",
        "pagesize": "50",
        "pagecode": "search|search|searchlist",
        "accountid": "",
        "key": "",
        "productname": "51job",
        "partner": PARTNER,
        "uuid": UUID,
        "version": "9.6.6",
        "guid": GUDI
    }
    KW_URL = "https://appapi.51job.com/api/job/associate_keyword.php"
    DETAIL_URL = "https://appapi.51job.com/api/job/get_job_info.php"
    DETAIL_PARAMES = {
        'jobid': '',
        'accountid': '',
        'key': '',
        'jobtype': '',
        'pagecode': 'search|search|searchlist',
        'productname': '51job',
        'partner': PARTNER,
        'uuid': UUID,
        'version': '9.7.0'
    }
    KW_PARAMS = {
        "keyword": "",
        "keywordtype": "",
        "productname": "51job",
        "partner": PARTNER,
        "uuid": UUID,
        "version": "9.6.6",
        "guid": GUDI
    }

    def __init__(self, url = 'https://appapi.51job.com/api/2/job/search_job_list.php',queue = None):
        self.ssn = requests.session()
        self.queue = queue
        if url is None or len(url) == 0:
            raise Exception("url不能为空")
        else:
            self.url = url

    def login(self):
        pass

    def start_spider(self):
        pass
    def spider_joblist(self, task=None, proxy=None):
        self.parames['keyword'] = task.key
        self.parames['pageno'] = str(task.pageno)
        self.parames['jobarea'] = task.citycode
        rep = None
        try:
            rep = self.ssn.get(self.url, headers=self.headers, params=self.parames, proxies=proxy)
        except Exception:
            # log.error('爬取joblist失败了,要更换代理了---进程:'+task.pid)
            cmd = CMD()
            cmd.type = log.ERROR
            cmd.msg = '爬取joblist失败了,要更换代理了---进程:'+task.pid
            self.queue.put(cmd)
            oocf = OocFile()
            task.status = '200'
            oocf.save_task_status(task=task)
            # log.success('任务状态已保存!---进程:'+task.pid)
            cmd = CMD()
            cmd.type = log.WARNING
            cmd.msg = '任务状态已更新!---进程:'+task.pid
            self.queue.put(cmd)
            cmd = CMD()
            cmd.type =log.POWER_EXIT
            self.queue.put(cmd)
            return None
        else:
            rep = rep.json()
            # print(rep)
            result = rep['result']
            status = rep['status']
            resultbody = rep['resultbody']
            maxpage = resultbody['maxapplynum']
            items = resultbody['joblist']['items']
            # print(items)
            joblists = []
            if result == '1' and status == '1':
                if len(items) > 0:
                    for item in items:
                        abjob = AbstractJob()
                        abjob.jobarea = item['jobarea']
                        abjob.degree = item['degree']
                        abjob.jodid = item['jobid']
                        abjob.salary = item['providesalary']
                        abjob.workyear = item['workyear']
                        abjob.jobtype = item['jobtype']
                        joblists.append(abjob)
                        # print('地址:' + item['cddr'])
                        # print('coid:' + item['coid'])
                        # print('公司名:' + item['coname'])
                        # print('类型:' + item['cotype'])
                        # print('需要学历:' + item['degree'])
                        # print('地区:' + item['jobarea'])
                        # print('id:' + item['jobid'])
                        # print('岗位名称:' + item['jobname'])
                        # print('jobType:' + item['jobtype'])
                        # print('薪资:' + item['providesalary'])
                        # print('工作经验:' + item['workyear'])
                        # print('\n\n')
                else:
                    # log.success('modelkey='+task.modelkey+" cityname="+task.cityname+' keyword='+task.key+' 的职位列表爬取完成---进程:'+task.pid)
                    oocf = OocFile()
                    task.status = '000'
                    oocf.save_task_status(task=task)
                    # log.success('任务状态已保存!---进程:'+task.pid)
                    cmd = CMD()
                    cmd.type = log.WARNING
                    cmd.msg = '任务状态已更新!---进程:'+task.pid
                    self.queue.put(cmd)
                    return 0
            return joblists
    def start(self,task, proxies = None):
        jobmaps = {}
        filename = task.cityname + task.modelkey + '.xls'
        modelkey = task.modelkey
        cityname = task.cityname
        # log.taskstart('开始爬取 modelkey='+task.modelkey+' cityname='+task.cityname+' keyword='+task.key+' 的数据...---进程:'+task.pid)
        cmd = CMD()
        cmd.type = log.TASKSTART
        cmd.msg = '开始爬取 modelkey='+task.modelkey+' cityname='+task.cityname+' keyword='+task.key+' 的数据...---进程:'+task.pid
        self.queue.put(cmd)
        while(True):
            results = self.spider_joblist(task=task,proxy=proxies);
            # print(task.pageno)
            task.pageno = task.pageno + 1
            if results == 0:  # 该城市信息爬取完成,保存了city+modelkey.xls
                xls = XLS()
                jobms = xls.read_job(filename, modelkey)
                if jobms is None:  # 说明没有文件直接写入即可
                    # log.taskstart('正在写入xls...'+filename+"...---进程:"+task.pid)
                    cmd = CMD()
                    cmd.type=log.TASKSTART
                    cmd.msg ='正在写入xls...'+filename+"...---进程:"+task.pid
                    self.queue.put(cmd)
                    xls.write_job(jobmaps, filename, modelkey, cityname)
                    # log.success('写入完成..'+filename+"---进程:"+task.pid)
                    cmd = CMD()
                    cmd.type = log.SUCCESS
                    cmd.msg = '写入完成..'+filename+"---进程:"+task.pid
                    self.queue.put(cmd)
                else:  # 已有文件存在
                    # log.taskstart('正在合并文件...---进程:'+task.pid)
                    cmd = CMD()
                    cmd.type = log.TASKSTART
                    cmd.msg = '正在合并文件...---进程:'+task.pid
                    self.queue.put(cmd)
                    jobmaps.update(jobms)
                    # log.success('合并完成!')
                    cmd = CMD()
                    cmd.type = log.SUCCESS
                    cmd.msg = '合并完成!'
                    self.queue.put(cmd)
                    # 重新写入
                    # log.taskstart('正在重新写入 ' + filename + '...---进程:'+task.pid)
                    cmd = CMD()
                    cmd.type = log.TASKSTART
                    cmd.msg = '正在重新写入 ' + filename + '...---进程:'+task.pid
                    self.queue.put(cmd)
                    xls.write_job(jobmaps, filename, modelkey, cityname)
                    # log.success('写入完成' + filename + '!---进程:'+task.pid)
                    cmd = CMD()
                    cmd.type = log.SUCCESS
                    cmd.msg = '写入完成' + filename + '!---进程:'+task.pid
                    self.queue.put(cmd)

                # log.success('********************爬取完成 modelkey='+task.modelkey+' cityname='+task.cityname+' keyword='+task.key+"**************---进程:"+task.pid)
                cmd = CMD()
                cmd.type = log.SUCCESS
                cmd.msg = '********************爬取完成 modelkey='+task.modelkey+' cityname='+task.cityname+' keyword='+task.key+"**************---进程:"+task.pid
                self.queue.put(cmd)
                ocmd = CMD()
                ocmd.type = log.EXIT
                self.queue.put(ocmd)
                break
            elif results is not None:  # 如果仍然有joblist
                for j in results:
                    job = self.detail_by_abjob(abjob=j, proxy=proxies,task =task)
                    if job is not None:
                        jobmaps[job.jobid] = job
            elif results is None:
                break


    def detail_by_abjob(self, abjob = None, task = None, proxy=None):
        '''
        获取职位介绍...更详细的信息
        :param abjob:
        :param proxy:
        :return:
        '''
        self.DETAIL_PARAMES['jobid'] = abjob.jodid
        self.DETAIL_PARAMES['jobtype'] = abjob.jobtype
        rep = None
        try:
            rep = self.ssn.get(self.DETAIL_URL, headers=self.headers, params=self.DETAIL_PARAMES, proxies=proxy)
        except Exception:
            # log.error('爬取Job失败了,要更换代理了...Process:'+task.pid)
            cmd = CMD()
            cmd.type = log.ERROR
            cmd.msg = '爬取Job失败了,要更换代理了...Process:'+task.pid
            self.queue.put(cmd)
            cmd = CMD()
            cmd.type = log.POWER_EXIT
            self.queue.put(cmd)
            oocf = OocFile()
            task.status = '200'
            oocf.save_task_status(task=task)
            # log.success('任务状态已保存...Process:'+task.pid)
            cmd = CMD()
            cmd.type = log.SUCCESS
            cmd.msg = '任务状态已保存...进程:'+task.pid
            self.queue.put(cmd)
            return None
        else:
            content = rep.content
            doms = md.parseString(content).documentElement
            result = doms.getElementsByTagName('result')[-1].childNodes[0].data
            status = doms.getElementsByTagName('result')[-1].childNodes[0].data
            job = None
            if result == '1' and status == '1':
                rb = doms.getElementsByTagName('resultbody')[-1]
                job = Job()
                job.jobid = (self.itr_rdxml(rb, 'jobid') + abjob.jobtype)
                job.jobname = self.itr_rdxml(rb, 'jobname')
                job.coid = self.itr_rdxml(rb, 'coid')
                job.coname = self.itr_rdxml(rb, 'coname')  # 公司名
                # jobmaps['issuedate'] = self.itr_rdxml(rb, 'issuedate')  # 发布日期
                job.jobnum = self.itr_rdxml(rb, 'jobnum')  # 需求人数
                job.workyear = self.itr_rdxml(rb, 'workyear')  # 几年经验
                job.degree = self.itr_rdxml(rb, 'degree')  # 文凭
                job.cityname = self.itr_rdxml(rb, 'cityname')
                # jobmaps['funtypecode'] = self.itr_rdxml(rb, 'funtypecode')
                # jobmaps['funtypename'] = self.itr_rdxml(rb, 'funtypename')
                # jobmaps['workyearcode'] = self.itr_rdxml(rb, 'workyearcode')
                # jobmaps['degreecode'] = self.itr_rdxml(rb, 'degreecode')
                # jobmaps['address'] = self.itr_rdxml(rb, 'address')
                job.welfare = self.itr_rdxml(rb, 'welfare')  # 例如： 五险一金 绩效奖金等
                job.jobtag = self.itr_rdxml(rb, 'jobtag')  # 该职位的标签 例如 java、软件工程师...
                job.salary = self.itr_rdxml(rb, 'providesalary')  # 工资
                job.cotype = self.itr_rdxml(rb, 'cotype')  # 公司类型 是民营 还是..
                # jobmaps['cosize'] = self.itr_rdxml(rb, 'cosize')  # 公司人数范围
                # jobmaps['jobterm'] = self.itr_rdxml(rb, 'jobterm')  # ? 全职....
                job.jobinfo = self.itr_rdxml(rb, 'jobinfo')  # 需要的技能有哪些
        return job

    def itr_rdxml(self, resultbody, tagname):
        '''
         取出 resultbody 中子节点的 tagname的值
        :param resultbody:
        :param targetname:
        :return:
        '''
        rz = resultbody.getElementsByTagName(tagname)[0]
        v = ''
        if len(rz.childNodes) > 0:
            v = rz.childNodes[0].data
        return v

    def get_keywords(self, prefix="a", kwtype='all'):
        """
        获取职位关键字
        :param prefix: 关键字前缀
        :param kwtype: 关键字类型,就是职业的信息.例如 软件工程..等 默认搜索所有
        :return: 返回一个关键字列表
        """
        self.KW_PARAMS['keyword'] = prefix
        self.KW_PARAMS['keywordtype'] = kwtype
        rep = self.ssn.get(self.KW_URL, headers=self.headers, params=self.KW_PARAMS)
        if rep.status_code != self.STA_OK:
            raise Exception("获取关键字失败! 错误码"
                            ": " + rep.status_code)
            return None
        else:
            # okeys={'',} # 去除OUTKEY 的关键字
            keys = set()  # 所有关键字集合
            # outkyes={'',} #关键字key
            doms = md.parseString(rep.content).documentElement
            items = doms.getElementsByTagName('item')
            for item in items:
                # print(item.getElementsByTagName('keyword')[0].childNodes[0].data)
                key = item.getElementsByTagName('keyword')[0].childNodes[0].data
                tag = True
                # 去除一些不要的关键字
                for ok in KW_OUTER:
                    if ok in key:
                        tag = False
                if tag:
                    keys.add(key)
        return keys


    def ite_key_by_prelist(self):
        '''
        :return:
        '''
        # log.taskstart('开始获取关键字...')
        cmd =CMD()
        cmd.type = log.TASKSTART
        cmd.msg = '开始获取关键字...'
        self.queue.put(cmd)
        allkeys = set()  # =
        modelkeys = {}
        for modelkey in KW_PREFIX.keys():
            modelkeys[modelkey] = set()
            prekeys = KW_PREFIX.get(modelkey)
            for prekey in prekeys:
                keys = self.get_keywords(prekey)
                if keys != None:
                    for key in keys:
                        modelkeys[modelkey].add(key)
                    allkeys = allkeys.union(keys)

        # modelkeys的格式是什么呢?
        # {模块关键字:{关键字A,keyB,keyC....}}
        txtpath = Config.FILE_DIR_KEYWORD + '\\keyword.txt'
        # 写入xls
        xls = XLS()
        xls.write_keys(data=allkeys)
        # 写入txt
        with open(txtpath, 'w+') as f:
            for mk  in modelkeys.keys():
                f.write(mk+':')
                for key in modelkeys[mk]:
                    f.write(key+'&')
                f.write('\n')
        # log.success('关键字获取成功...已写入到'+Config.FILE_DIR_KEYWORD)
        cmd = CMD()
        cmd.type = log.SUCCESS
        cmd.msg = '关键字获取成功...已写入到'+Config.FILE_DIR_KEYWORD
        self.queue.put(cmd)


# if __name__ == '__main__':
#     job51 = Job51()
#     # job51.java_kunMing("java")
#     # jobmaps = job51.detail_by_jobid('120936554', '0100')
#     # for key in jobmaps.keys():
#     #     print(jobmaps[key])
#     proxy = {
#         'http': '122.224.65.197:3128',
#         'https': '122.224.65.197:3128'
#     }
#     task = Task()
#     task.key='java'
#     task.pageno=10
#     task.citycode = '250200'
#     task.cityname = '昆明'
#     task.modelkey = 'java'
#     job51.start(task)
    # print(len(abjoblist))
    # job51.get_keywords(prefix='php')
    # job51.ite_key_by_prelist()
    # rep = requests.get('http://www.httpbin.org/ip=49.235.49.118:8080')
    # print(rep.content)