import win32com.client as win32
import os


def xlsToXlsx(sourceFilePath):
    files = os.listdir(sourceFilePath)
    for filename in files:
        if filename.find('.xls')>0:
            fname = sourceFilePath + filename
            XlsFileChange(fname)






def XlsFileChange(fname):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(fname + "x", FileFormat=51)  # FileFormat = 51 is for .xlsx extension
    wb.Close()  # FileFormat = 56 is for .xls extension
    excel.Application.Quit()