#-*- coding:utf-8 -*-
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import InputText
import gettokenholdings
sg.theme('lightgrey2')


def main():
    name = 'ParaFi'
    data=[]
    header_list = ['序号', '币种', '数量', '单价($)', '持有价值($)','占比']
    layout = [[sg.T('*查询地址:',size=(10,1)),sg.Multiline(key='key_address',size=(70,2),default_text="0x5028d77b91a3754fb38b2fbb726af02d1fe44db6;0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363;0xd9b012a168fb6c1b71c24db8cee1a256b3caa2a2"),sg.Button('查询')],[sg.T('cookie:',size=(10,1)),sg.Multiline(key='key_cookie',size=(70,3),default_text='')],[sg.T('代理服务器:',size=(10,1)),sg.InputText(key='key_proxy',size=(70,2),default_text='')],[sg.InputText(default_text='备注：多个地址以分号分割,从https://cn.etherscan.com/tokenholdings?a=0x5028d77b91a3754fb38b2fbb726af02d1fe44db6 获取cookie',font=("微软雅黑", 10),justification='left',readonly = True,size=(120,1))],[sg.Table(key='key_results',values=data,
                        headings=header_list,
                        auto_size_columns=False,
                        col_widths=[5,10, 10, 20, 30],
                        justification='center',
                        row_height=30,
                        pad=2,
                        num_rows=max(len(data), 20))]]

    window = sg.Window('查询机构持仓', layout, font=("微软雅黑", 12),default_element_size=(100,10) )

    while True:
        event, values = window.read()
        if event in (None, '关闭'):   
            break
        if event == '查询':
            address = values['key_address']
            proxyvalue=values['key_proxy']
            proxy ={}
            if proxyvalue:
                proxy ={"http":proxyvalue,"https":proxyvalue}

            cookies=values['key_cookie']
            if cookies :
                cookies=' '

            if address :
                print(address)
                print(proxy)
                print(cookies)
                data = gettokenholdings.queryAsset(address,proxy,cookies)
                if data:
                    window['key_results'].update(data)
                else :
                    sg.popup('没有查询到结果,可能是地址输入错误,或cookie时效过期,需要重新获取! ')    
            else:
               sg.popup('请输入查询地址   ',font=("微软雅黑", 10),line_width=40,title='')
  
    window.close()


if __name__ == '__main__':
    main()
