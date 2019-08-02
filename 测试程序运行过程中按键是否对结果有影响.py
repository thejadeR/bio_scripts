

'''
此脚本用来测试程序运行过程中按回车键是否会对结果有影响
测试结果为并没有影响
'''

def getDepth(fileN):
    print('当前执行的文件是：【%s】'%fileN)

    with open('11.txt','a') as f1:
        for i in range(1,11):
            f1.write(str(i))
        f1.write('\n')

    print('【%s】......执行完毕'%fileN)

if __name__ == '__main__':
    the_num = 10
    for fileN in range(1,11):
        getDepth(fileN)

        the_num = the_num - 1
        print('当前还剩【%d】个未处理' % the_num)
        print("")

    print('文件全部处理完成，程序结束')



