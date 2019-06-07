# -*- coding: utf-8 -*-


"""
Created on Tue Oct 23 09:44:50 2018

@author: mtroyer
"""


import datetime
import logging
import os
# import sys
import traceback
import pandas as pd

# sys.path.append(r'C:\Users\mtroyer\python\Other_Tools\ftps')

import pysftp

#living on the edge..
import warnings
warnings.filterwarnings('ignore')


def get_project_log(log_path, out_path, key_field, key_value, add_field=None, add_value=None):
    
    print '[+] Getting {}'.format(os.path.basename(out_path))
    
    project_df = pd.read_excel(log_path)

    if (add_field and add_value):
        posting_df = project_df[(
            project_df[key_field].str.contains(key_value, na=False)
            |
            project_df[add_field].str.contains(add_value, na=False)
            )
            ].copy()
    else:
        posting_df = project_df[project_df[key_field].str.contains(key_value)].copy()
    
    writer = pd.ExcelWriter(out_path)
    posting_df.to_excel(writer, os.path.basename(out_path), index=False)
    writer.save()
    print '[+] Done..'


def post_project_log(post_log_path, host, port, user, pswx, ftp_dir):

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    with pysftp.Connection(host=host, port=port, username=user, password=pswx, cnopts=cnopts) as sftp:
    
        print '[+] Connected to [{}] as [{}]'.format(host, user)

        with sftp.cd(ftp_dir):
            try:
                print '[+] Removing old log..'
                sftp.remove(os.path.basename(post_log_path))
            except:
                pass
            print '[+] Transferring data..'
            sftp.put(post_log_path)
            print '[+] Done..'


if __name__ =='__main__':
    
    src_path = r'S:\Archaeology\Database\RGFO_CULTURAL_RESOURCES_PROJECT_LOG.xlsx'
    tmp_path = r'S:\Archaeology\Database\Backup\BLM_RGFO_PROJECT_LOG.xlsx'
    log_file = r'S:\Archaeology\Database\Logs\Post_SHPO_Log.log'
    
    logging.basicConfig(
            level=logging.INFO,
            filename=log_file,
            format='%(asctime)s  %(levelname)-10s %(message)s'
            )
    
    host = <host>
    port = 22
    user = <user>
    pswx = <password>
    fdir = r'/OAHP/BLM-For SHPO use ONLY/RGFO'
        
    now = datetime.date.today() 
    fy  = now.year if now < datetime.date(now.year, 10, 15) else now.year + 1
    
    #Unique select mechanism
    key_field = 'BLM NUMBER'
    key_value =  'CR-RG-{}'.format(str(fy)[2:])
    add_field = 'COMMENTS'
    add_value = 'BACKLOG'
    
    try:
        get_project_log(src_path, tmp_path, key_field, key_value, add_field, add_value)
        post_project_log(tmp_path, host, port, user, pswx, fdir)
        logging.info('Successfully posted [{}]'.format(os.path.basename(tmp_path)))
        
    except Exception as e:
        err = traceback.format_exc()
        print '[-] Error: {}'.format(err)
        logging.error('Failed to post [{}]\n\t{}'.format(os.path.basename(tmp_path), err))
