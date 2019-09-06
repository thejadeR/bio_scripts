import subprocess

for i in range(1, 973):
    print('当前下载的是第【%d】个文件,一共【972】个文件' % i)

    file_url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0%.3d.xml.gz' % i
    file_res = subprocess.Popen('wget %s' % file_url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # the_file_out = file_res.stdout.read().decode('utf-8')
    the_file_err = file_res.stderr.read().decode('utf-8')

    # print('out:',the_out)
    # print('err:', the_err)

    # If there is an error in the execution of the Enal Linux Command，
    # then Log the error message in the log file
    if the_file_err:
        with open(r'file_download.log', 'a', encoding='utf-8') as f1:
            err_str = 'pubmed19n0%.3d.xml.gz:\n%s\n' % (i,the_file_err)

            f1.write(err_str)

    print('第【%d】个文件下载完成\n' % i)