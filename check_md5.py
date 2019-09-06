import subprocess
import re
err_num = 0
for i in range(1, 973):
    print('当前核对MD5的是第【%d】个文件,一共【972】个文件' % i)

    md5_check = subprocess.Popen('md5sum -c  pubmed19n0%.3d.xml.gz.md5'%i, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    the_file_out = md5_check.stdout.read().decode('utf-8')
    print(the_file_out)
    print(type(the_file_out))
    res = re.search(r"(成功\n)|(ok\n)|(成功)|(ok)",the_file_out)
    if not res:
        err_num+=1
        with open(r'md5_check.log', 'a', encoding='utf-8') as f1:
            err_str = 'pubmed19n0%.3d.xml.gz.md5: check not ok\n\n'%i

            f1.write(err_str)

    print('第【%d】个md5文件核对完成\n' % i)


print('所有文件核对完成，共【%d】个文件核对出错'%err_num)
