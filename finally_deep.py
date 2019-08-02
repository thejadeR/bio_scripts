#!/usr/bin/python
# -*- coding: UTF-8 -*-
import glob
import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame

def start_scripts(fileN,res_dir):
    # fileN:/mnt/hgfs/myVirtualENVShare/deep/res/20180103/IonXpress_008_rawlib.bam-out_result.txt_grepCHR16_20w.txt
    # res_dir:/mnt/hgfs/myVirtualENVShare/deep/results
    print('当前执行的文件是：【%s】' % fileN)

    # 创建深度模板区间
    print('创建深度模板区间为：【71277 - 336701】')
    temp_Position_range = np.arange(71277, 336702)
    # temp_Position_range

    temp_deep_range = np.arange(0, 265425)
    # temp_deep_range

    template_df = DataFrame(index=temp_Position_range)
    template_df['Deep0'] = temp_deep_range
    # template_df

    #awk输出多列的时候分隔符是空格
    sample = pd.read_csv(fileN, sep=' ', header=None, names=['Chromosome', 'Position', 'Deep'])
    sample1 = sample.sort_values('Position').copy()
    # sample1

    new_sample_df = DataFrame(index=sample1['Position'].values)
    new_sample_df['Chromosome'] = sample1['Chromosome'].values
    new_sample_df['Position'] = sample1['Position'].values
    new_sample_df['Deep'] = sample1['Deep'].values
    # new_sample_df

    merge_res = pd.concat([template_df, new_sample_df], join='outer', axis=1)
    # merge_res

    # 补零
    finally_res = merge_res.fillna(value=0).copy()
    # finally_res

    # 只要补零后的深度
    res = finally_res[['Deep']]
    fileN1 = fileN.split('/')[-1]

    res_dir1 = '%s/%s'%(res_dir,fileN.split('/')[-2])
    # res_dir1:/mnt/hgfs/myVirtualENVShare/deep/results/20180103

    out_filename = '%s/res-%s' % (res_dir1,fileN1)
    # out_filename:/mnt/hgfs/myVirtualENVShare/deep/results/20180103/IonXpress_008_rawlib.bam-out_result.txt_grepCHR16_20w.txt

    if not os.path.exists(res_dir1):
        print('')
        print('【%s】补零位点最终结果文件夹不存在！'%res_dir1)
        os.makedirs(res_dir1)
        print('【%s】补零位点最终结果文件夹已自动创建成功！'%res_dir1)
        print('')

    # 以制表符分割，保留索引，去除列名字段
    res.to_csv(out_filename, sep='\t',index=True,header=False)

    print('【%s】执行完毕'%fileN)
    print()

usage = '''
使用方法：python 脚本名 待处理的文件路径 输出的结果路径

例子：
python3 /home/thelinux/Desktop/fill_deep.py /mnt/hgfs/myVirtualENVShare/deep/res/20180103 /mnt/hgfs/myVirtualENVShare/deep/results
'''

usage2 = '''
grep_txt_dir:    /mnt/hgfs/myVirtualENVShare/deep/res/20180103
res_txt_dir:    /mnt/hgfs/myVirtualENVShare/deep/results
soft_dir:      /home/thelinux/Desktop/fill_deep.py
cmd:       python3 /home/thelinux/Desktop/fill_deep.py /mnt/hgfs/myVirtualENVShare/deep/res/20180103 /mnt/hgfs/myVirtualENVShare/deep/results
'''


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print(usage)

    else:
        the_path = sys.argv[1]
        print('获取待处理文件路径为：【%s】' %the_path)

        file_list = glob.glob('%s/*.txt' %the_path)
        the_num = len(file_list)

        print("该路径下的txt文件有：【%d】" %the_num)
        print(file_list)
        print('')

        res_dir = sys.argv[2]

        for fileN in file_list:
            the_num -=1
            start_scripts(fileN,res_dir)

        print('文件全部处理完成，程序结束')



