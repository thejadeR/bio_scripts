# -*- coding: UTF-8 -*-
import glob
import subprocess

gz_file_list = glob.glob('*.gz')
# print(gz_file_list)
# 'pubmed19n0964.xml.gz', 'pubmed19n0865.xml.gz', 'pubmed19n0041.xml.gz']

gz_num = len(gz_file_list)
num = 1
for i in gz_file_list:
    print('all【%d】files，pre is【%d】\n'%(gz_num,num))
    xml_name = i[:i.rfind('.')]
    # subprocess.Popen('gunzip -c %s > ./xml_data/%s' % (i, xml_name), shell=True)
    subprocess.Popen('gzip -d %s'%(i), shell=True)

    num+=1