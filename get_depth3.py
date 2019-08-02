#!/usr/bin/python
# -*- coding: UTF-8 -*-
import glob
import os
import sys


def getDepth(fileN,res_dir):
    print('当前执行的文件是：【%s】'%fileN)
    # / home / denghonghui / research / PGD_data_072426 / 20190724 - 1 / IonXpress_048_rawlib.bam
    fileN1 = fileN.split('/')[-1]

    # 结果目录
    res_dir1 = res_dir + '/' + fileN.split('/')[-2]
    if not os.path.exists(res_dir1):
        print('')
        print('【%s】文件夹不存在！'%res_dir1)


        os.makedirs(res_dir1)
        print('【%s】文件夹已自动创建成功！'%res_dir1)
        print('')

    os.system("/usr/bin/samtools depth %s | grep 'chr16' | awk '{if($2>=71277 && $2<=336701) print $1, $2,$3}' > %s/%s_grepCHR16_20w.txt"%(fileN, res_dir1, fileN1))

    print('【%s】......执行完毕'%fileN)





usage = '''
ionadmin@BBD3322:/results/test/bamdata-20190731-depth$ python test.py /results/test/bamdata-20190731-depth
使用方法：python 脚本名 待处理的文件路径 输出的结果路径

例子：
python /results/test/bamdata-20190731-depth/get_depth.py /results/test/bamdata-20190731-depth /results/test/bamdata-20190731-depth/res
'''


usage2 = '''

bam:         /mnt/hgfs/PGD18
res_txt:    /mnt/hgfs/myVirtualENVShare/deep
soft:      /home/thelinux/Desktop/biosoft/get_depth.py
cmd:       python3 /home/thelinux/Desktop/biosoft/get_depth.py   /mnt/hgfs/PGD18/20180103   /mnt/hgfs/myVirtualENVShare/deep
'''

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print(usage)

    else:
        the_path = sys.argv[1]
        print('获取待处理文件路径为：【%s】' %the_path)

        file_list = glob.glob('%s/*.bam' %the_path)
        the_num = len(file_list)

        print("该路径下的bam文件有：【%d】" %the_num)
        print(file_list)
        print('')

        res_dir = sys.argv[2]

        for fileN in file_list:

            getDepth(fileN,res_dir)

            the_num = the_num - 1
            print('当前还剩【%d】个未处理' % the_num)
            print("")

        print('文件全部处理完成，程序结束')



