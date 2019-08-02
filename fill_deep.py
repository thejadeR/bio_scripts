# -*- coding: UTF-8 -*-
import glob
import os
import sys
import traceback
import time

import numpy as np
import pandas as pd
from pandas import Series,DataFrame

def getDepth(fileN,res_dir):
    # fileN：/mnt/hgfs/PGD18/20180607-2/IonXpress_096_rawlib.bam
    # res_dir:/mnt/hgfs/vmshare

    print('当前执行的文件是：【%s】'%fileN)
    fileN1 = fileN.split('/')[-1]
    # fileN1:IonXpress_096_rawlib.bam

    # 结果目录
    res_dir1 = '%s/%s'%(res_dir,fileN.split('/')[-2])
    # res_dir1:/mnt/hgfs/vmshare/20180607-2

    if not os.path.exists(res_dir1):
        print('')
        print('【%s】文件夹不存在！'%res_dir1)
        os.makedirs(res_dir1)
        print('【%s】文件夹已自动创建成功！'%res_dir1)


    the_out = '%s/%s_CHR16_20w.txt'%(res_dir1, fileN1)
    # the_out:/mnt/hgfs/vmshare/20180607-2/IonXpress_096_rawlib.bam_CHR16_20w.txt  //这个结果是提取的16号染色体，然后提取的71277-336701位点的信息

    os.system("/usr/bin/samtools depth %s | grep 'chr16' | awk '{if($2>=71277 && $2<=336701) print $1,$2,$3}' > %s" %(fileN,the_out))



    # 创建深度模板区间，之所以是336702而不是336701是因为右边取不到
    print('创建深度模板区间为：【71277 - 336701】')
    temp_Position_range = np.arange(71277, 336702)
    # temp_Position_range

    temp_deep_range = np.arange(0, 265425)
    # temp_deep_range

    template_df = DataFrame(index=temp_Position_range)
    template_df['Deep0'] = temp_deep_range
    # template_df

    sample = pd.read_csv(the_out, sep=' ', header=None, names=['Chromosome', 'Position', 'Deep'])
    sample1 = sample.sort_values('Position').copy()
    # sample1

    new_sample_df = DataFrame(index=sample1['Position'].values)
    new_sample_df['Chromosome'] = sample1['Chromosome'].values
    new_sample_df['Position'] = sample1['Position'].values
    new_sample_df['Deep'] = sample1['Deep'].values
    # new_sample_df

    merge_res = pd.concat([template_df, new_sample_df], join='outer', axis=1)
    # merge_res

    finally_res = merge_res.fillna(value=0).copy()
    # finally_res

    res = res = finally_res[['Deep']]

    # 创建补全位点后的结果路径out_dir：/mnt/hgfs/vmshare/results/20180607-2
    out_dir = '%s/results/%s'%(res_dir,fileN.split('/')[-2])
    if not os.path.exists(out_dir):
        print('')
        print('【%s】补零位点后的最终结果文件夹不存在！'%out_dir)
        os.makedirs(out_dir)
        print('【%s】补零位点后的最终结果文件夹已自动创建成功！'%out_dir)

    # 最终结果文件名字
    out_filename =  '%s/result-%s.txt'%(out_dir,fileN1)
    # out_filename:/mnt/hgfs/vmshare/results/20180607-2/result-IonXpress_096_rawlib.bam.txt

    res.to_csv(out_filename, sep='\t',index=True,header=False)

    print('【%s】......执行完毕' %fileN)
    print('输出文件存于:【%s】' %out_filename)


usage = '''
使用方法：python 脚本名 待处理的文件路径 输出的结果路径

例子：
python3 /home/mylinux/Desktop/biosoft/fill_deep.py /mnt/hgfs/PGD18/20180607-2 /mnt/hgfs/vmshare
'''


usage2 = '''
bam:         /mnt/hgfs/PGD18/20180607-2
res_txt:    /mnt/hgfs/vmshare
soft:      /home/mylinux/Desktop/biosoft/fill_deep.py
cmd:       python3 /home/mylinux/Desktop/biosoft/fill_deep.py /mnt/hgfs/PGD18/20180607-2 /mnt/hgfs/vmshare
'''

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print(usage)
        print()
        print(usage2)

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

            try:
                getDepth(fileN,res_dir)

            except:
                print('')
                error = traceback.format_exc()

                with open(r'~/Desktop/log.txt','a') as f1:

                    f1.write(fileN)
                    f1.write(error)
                    f1.write("\n")

            the_num = the_num - 1
            print('当前还剩【%d】个未处理' %the_num)
            print("")


        print('文件全部处理完成，程序结束')



