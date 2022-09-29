
class Task:
    modelkey = None
    key = None
    citycode = None
    cityname = None
    pageno = None
    status = None
    msg = None
    pid = None #
    def __init__(self):
        pass


class AbstractJob:
    jobarea = None
    degree = None
    jodid = None
    coid = None
    salary = None
    workyear = None
    jobtype = None
    def __init__(self):
        pass


class Job:
    jobid = None
    jobname = None
    coid = None
    coname = None  # 公司名
    jobnum = None  #  需求人数
    workyear = None  #几年经验
    degree = None  # 学历
    cityname = None
    welfare = None  # 待遇 例如：五险一金...
    jobtag = None  # 职位标签
    salary = None  #  薪资
    cotype = None   # 公司类型
    jobinfo = None  # 职位要求

class CMD:
    type = None
    msg = None

