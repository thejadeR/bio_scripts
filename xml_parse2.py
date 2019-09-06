import gevent
from gevent import monkey
monkey.patch_all()

import subprocess
import glob
import traceback
import os
import time
import re

#create log dir if not exists,if there is any log files in log dir ,then remove all log files
if not os.path.exists('./errors_log/'):
    os.makedirs('errors_log')
else:
    cre_cmd = subprocess.Popen('touch ./errors_log/sample.log', shell=True)
    cre_cmd.wait()

    del_cmd = subprocess.Popen('rm ./errors_log/*.log', shell=True)
    del_cmd.wait()

if not os.path.exists('./xml_txt/'):
    os.makedirs('./xml_txt/')



def sigle_parse(j):
    filename = j[:j.rfind('.')]
    try:
        if not os.path.exists('./%s'%filename):
            unzip_cmd = subprocess.Popen('gzip -d %s' %(j), shell=True)
            unzip_cmd.wait()  # !!!

        print('pre is [%s]'%filename)

        with open(filename, 'r') as f1:
            # res = f1.read(300000)
            xml_content = f1.read()
            # res2 = re.findall(r'<AbstractText.*</AbstractText>', res, re.M)
            AbstractText_list = re.findall(r'<AbstractText[^>]*>(.*)</AbstractText>', xml_content, re.M)

            AbstractText = '\n\n'.join(AbstractText_list)
            AbstractText_correct = re.sub(pattern=r'<[^>]*>', repl='', string=AbstractText, count=0, flags=re.M)

            print('[%s]get AbstractText finish,write to txt...'%filename)
            with open('./xml_txt/%s.txt' % filename, 'w', encoding='utf-8') as f1:
                f1.write(AbstractText_correct)

        print('write over')

    except Exception:
        print('[%s] is faild,err info write in [%s.log]' % (filename,filename))

        if not os.path.exists('./errors_log/%s.log'):
            os.system('touch ./errors_log/%s.log' % filename)

        with open('./errors_log/%s.log'%filename,'w',encoding='utf-8') as f3:
            info = traceback.format_exc()
            f3.write(info)
    else:
        print('[%s] is finish\n'%filename)
        # subprocess.Popen('rm ./%s' % filename, shell=True)

gz_file_list = glob.glob('*.gz')
# print(gz_file_list)
# 'pubmed19n0964.xml.gz', 'pubmed19n0865.xml.gz', 'pubmed19n0041.xml.gz']
gz_num = len(gz_file_list)
num = 1


g_list = []
s = time.time()
for j in gz_file_list:
    print('all【%d】files，pre is【%d】\n'%(gz_num,num))

    # xml_name = i[:i.rfind('.')]
    # subprocess.Popen('gunzip -c %s > ./xml_data/%s' % (i, xml_name), shell=True)
    # sigle_parse(j)

    g = gevent.spawn(sigle_parse, j)
    g_list.append(g)

    # subprocess.Popen('rm ./%s' % file_name, shell=True)
    num+=1

gevent.joinall(g_list)
e = time.time()

timecost = 'all xml is finish!,花费时间:%s\n' % (str(e - s))
print(timecost)






