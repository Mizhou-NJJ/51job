import xlwt
import xlrd
from pathlib import Path
import os
from config import Config
from tool.tool import OocFile
from xlutils.copy import copy
from entity.entity import Job


class XLS:
    def __init__(self):
        pass
    def open_book(self,filename):
        return xlrd.open_workbook(filename)

    def set_style(self,name = 'Times New Roman', height = 220, bold=True):
        style = xlwt.XFStyle()

        font = xlwt.Font()

        font.name = name

        font.bold = bold

        font.color_index = 4

        font.height = height

        style.font = font

        return style

    def new_workbook(self):
        return xlwt.Workbook()
    def write_keys(self, data = None, path=Config.FILE_DIR_KEYWORD,sheetName = Config.SHEET_NAME_51JOB):
        '''
        写入爬到的关键字
        :param path: 文件路径
         sheetName : 写入那个sheet
        :return:
        '''
        oocf = OocFile()
        if not data:
            return None
        fpath= oocf.judge_and_create(path,cfile=False)
        fullpath = fpath+Config.FILE_NAMES['keyword']+".xls"
        # 先读入
        if os.path.exists(fullpath):
            workbook = xlrd.open_workbook(fullpath)
            sheets = workbook.sheets()
            sheet=sheets[0]
            # 读取单元格中的数据
            keys = set()
            row = sheet.nrows
            for i in range(0,row):
                keys.add(sheet.cell_value(i,0))
            # 求差集
            ddate= data.union(keys)
            wWorkbook = xlwt.Workbook()
            wsheet=wWorkbook.add_sheet("职位关键字", cell_overwrite_ok=False)
            for i in range(0,len(ddate)):
                wsheet.write(i,0,ddate.pop())
            wWorkbook.save(fullpath)
            #添加
        else:
            print("文件不存在")
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("职位关键字", cell_overwrite_ok=False)  # cell_over.. 是否覆盖已经操作的单元格
            for i in range(0,len(data)):
                sheet.write(i,0,data.pop())
            workbook.save(fullpath)



        # print(fpath)
        # workbook = xlwt.Workbook()
        # sheet1 = workbook.add_sheet("51job职位关键字", cell_overwrite_ok=False)  # cell_over.. 是否覆盖已经操作的单元格
        # sheet1.write(0, 2, 'Firstw')
        # sheet1.write(0, 3, "Secondw")
        # workbook.save(fullpath)
    def write_job(self,jobmap ,filename,modelkey,cityname):
        if jobmap is None:
            return
        else:
            path = path = Config.FILE_DATE_DIR + '\\' + modelkey + '\\' + filename
            oocf = OocFile()
            oocf.judge_and_create(path)  #  先检测或创建文件夹
            wWorkbook = xlwt.Workbook()
            wsheet = wWorkbook.add_sheet(modelkey+cityname, cell_overwrite_ok=False)
            row_title = ['jobid','jobname','coid','coname','jobnum','workyear','degree',
                         'cityname','welfare','jobtag','salary','cotype','jobinfo']
            style = self.set_style()
            # 表头 --------------------------
            for col in range(0, len(row_title)):
                wsheet.write(0,col,row_title[col],style)
                # ---------------------------------------
            row = 1
            for key in jobmap.keys():
                job = jobmap.get(key)
                if job is not None:
                    wsheet.write(row, 0, job.jobid)
                    wsheet.write(row, 1, job.jobname)
                    wsheet.write(row, 2, job.coid)
                    wsheet.write(row, 3, job.coname)
                    wsheet.write(row, 4, job.jobnum)
                    wsheet.write(row, 5, job.workyear)
                    wsheet.write(row, 6, job.degree)
                    wsheet.write(row, 7, job.cityname)
                    wsheet.write(row, 8, job.welfare)
                    wsheet.write(row, 9, job.jobtag)
                    wsheet.write(row, 10, job.salary)
                    wsheet.write(row, 11, job.cotype)
                    wsheet.write(row, 12, job.jobinfo)
                    row = row + 1
            wWorkbook.save(path)


    def read_job(self,filename,modelkey):
        path = Config.FILE_DATE_DIR + '\\' + modelkey + '\\' + filename
        if os.path.exists(path):  # 存在则读取
            workbook = xlrd.open_workbook(path)
            sheets = workbook.sheets()
            sheet = sheets[0]
            jobmaps = {}
            rows = sheet.nrows  # 总行数
            # print(rows)
            # cols = sheet.ncols  # 总列数
            for row in (range(1,rows)):
                job = Job()
                job.jobid = sheet.cell_value(row, 0)
                job.jobname = sheet.cell_value(row, 1)
                job.coid = sheet.cell_value(row, 2)
                job.coname = sheet.cell_value(row, 3)
                job.jobnum = sheet.cell_value(row, 4)
                job.workyear = sheet.cell_value(row, 5)
                job.degree = sheet.cell_value(row, 6)
                job.cityname = sheet.cell_value(row,7)
                job.welfare = sheet.cell_value(row, 8)
                job.jobtag = sheet.cell_value(row, 9)
                job.salary = sheet.cell_value(row, 10)
                job.cotype = sheet.cell_value(row, 11)
                job.jobinfo = sheet.cell_value(row, 12)
                # print(job.jobid)
                jobmaps[job.jobid] = job
            return jobmaps
        else:
            return None


