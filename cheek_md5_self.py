# -*- coding: UTF-8 -*-
import subprocess
import re
err_num = 0

for i in range(1, 973):
    print('pre is [%d],all 972 files' % i)

    md5_check = subprocess.Popen('md5sum pubmed19n0%.3d.xml.gz'%i, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    the_file_out = md5_check.stdout.read().decode('utf-8')
    print(the_file_out)
    print(type(the_file_out))

    a = the_file_out.split(' ')[0]

    md5_check2 = subprocess.Popen('cat pubmed19n0%.3d.xml.gz.md5' % i, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    the_file_out2 = md5_check2.stdout.read().decode('utf-8')
    print(the_file_out2)
    print(type(the_file_out2))

    b = the_file_out2.split('=')[1].strip()
    print(a)
    print(b)
    if a != b:
        err_num+=1
        with open(r'md5_check.log', 'a',encoding='utf-8') as f1:
            err_str = 'wget ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0%.3d.xml.gz\n'%i

            f1.write(err_str)

    print('[%d] file is finish\n' % i)


print('all have [%d] err files '%err_num)
