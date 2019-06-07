# -*- coding: utf-8 -*-
"""
Created on Mon November 2 2018

@author: mtroyer

"""


import os
import datetime
import logging
import shutil
import traceback

ROOT = r'S:\Archaeology\Database'
TODAY = datetime.date.today()
SOURCE  = os.path.join(ROOT, 'RGFO_CULTURAL_RESOURCES_PROJECT_LOG.xlsx')
BACKUP  = os.path.join(ROOT, 'Backup', 'RGFO_CULTURAL_RESOURCES_PROJECT_LOG_{}.xlsx'.format(TODAY))
LOGFILE = os.path.join(ROOT, 'Logs', 'Backup_Project_Log.log')

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, filename=LOGFILE)


def main():
    try:
        shutil.copy(SOURCE, BACKUP)
        success = "[+] Success: Copied RGFO_CULTURAL_RESOURCES_PROJECT_LOG"
        print success
        logging.info(success)

    except:
        err = "[-] Failure:\n{}".format(traceback.format_exc())
        print err
        logging.error(err)


if __name__ == '__main__':
    main()
