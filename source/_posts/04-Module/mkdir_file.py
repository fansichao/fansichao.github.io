import os
def create_file(file_name):
    "创建文件"
    if not os.path.exists(file_name):
        file = open(file_name, 'w')
        file.close
def generate_muti_file(start_name):
    " 生成多个文件名称 "
    ll = ['00技术文档', '01部署文档','02使用文档','03模块功能','04配置详解','05命令详解','06其他资源']
    for l in ll:
        file_name = ''.join(['Module-',start_name,'-',l, '.md'])
        print(file_name)
        create_file(file_name)

if __name__ == '__main__':
    start_name = input('输入名称：')
    generate_muti_file(start_name)