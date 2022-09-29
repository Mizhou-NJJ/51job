class Config:
    FILE_NAMES = {
        '51jobkw': '\\51jobkeywords',
        'keyword': '\\keyword'
    }
    # -------------------------------
    SHEET_NAME_51JOB = "51job职位关键字"
    # --------------------------
    FILE_DIR = 'c:\\bs'
    FILE_DATE_DIR = 'c:\\bs\\date'
    FILE_DIR_KEYWORD = "c:\\bs\\keyword"
    FILE_JOB51_DIR = FILE_DIR + '\\51job'



class IPConfig:
    _89_FREE_PROXY = {
        'api': 'https://www.89ip.cn/tqdl.html?num=60&address=&kill_address=&port=&kill_port=&isp=',
        # num = 60 获取60个代理ip
        'saveas': Config.FILE_DIR + '\\proxy\\pip.txt',
    }
    XL_FREE_PROXY = {
        'api': 'http://www.xiladaili.com/',
        'saveas': Config.FILE_DIR + '\\proxy\\pip2.txt'
    }


class PC:
    tasksaveas = Config.FILE_DIR + '\\task\\status'
    uid = '9421'
    host = '49.235.49.118'
    # host = "127.0.0.1"
    port = 9999
    # _PC_ = {
    #     'tasksaveas': Config.FILE_DIR + '\\task\\status.txt',
    #     'uid': '9420',
    #     'host': '127.0.0.1',
    #     'port': 9999,
    # }