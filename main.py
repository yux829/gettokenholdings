import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import InputText
import gettokenholdings
sg.theme('lightgrey2')


def main():
    name = 'ParaFi'
    data=[]
    header_list = ['序号', '币种', '数量', '单价($)', '持有价值($)','占比']
    layout = [[sg.T('代理服务器:',size=(10,1)),sg.InputText(key='key_proxy',size=(70,2),default_text='')],[sg.T('cookie:',size=(10,1)),sg.Multiline(key='key_cookie',size=(70,3),default_text='_ga=GA1.2.429915406.1624182334; _pk_id.10.1f5c=dd00b85d5da40747.1632440771.; CultureInfo=zh-CN; etherscan_userid=yux829; etherscan_pwd=4792:Qdxb:fcJNWoIaUOFfR/oK2gudIw==; etherscan_autologin=True; cf_clearance=WCqYNihBTPi4ZiUtRMJDQ_LbXWXME3XDQpiOCY20Aoo-1634041148-0-250; __cf_bm=.cNgNxkQTXgfzTzdKtr9YI9_Un93wmJRhG6rKVQkEG0-1634213487-0-Ae3IHM/Wd7J3P+EM+OSuDOBwqDdY0yrWLqQsSK8Ecf1ycMf1Pn/sI2XkJxS0RCSdkWvG9Ptbn9m9AYnWyCQuTC9AjF+IIOzUIwdpnvAAkCth8XnBORQqAPf+Nn2asUmdCA==; ASP.NET_SessionId=r4gidhhgloju0fnqy15jatop; _pk_ref.10.1f5c=%5B%22%22%2C%22%22%2C1634213729%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3De1XtrHzVUdhPIs3zYjv7LWp2IJ2Gp40L-nX4zCn-a1yRTKAUrZ06e5nmTG3BM0Ux%26wd%3D%26eqid%3D8a6075ad000384d60000000661657b30%22%5D; _pk_ses.10.1f5c=1')],[sg.T('查询地址:',size=(10,1),),sg.Multiline(key='key_address',size=(70,2),default_text='0x5028d77b91a3754fb38b2fbb726af02d1fe44db6;0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363;0xd9b012a168fb6c1b71c24db8cee1a256b3caa2a2'),sg.Button('查询')],[sg.InputText(default_text='备注：多个地址以分号分割,从https://cn.etherscan.com/tokenholdings?a=0x5028d77b91a3754fb38b2fbb726af02d1fe44db6 获取cookie',font=("微软雅黑", 10),justification='left',readonly = True,size=(120,1))],[sg.Table(key='key_results',values=data,
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

            if address and cookies:
                print(address)
                print(proxy)
                print(cookies)
                data = gettokenholdings.queryAsset(address,proxy,cookies)
                if data:
                    window['key_results'].update(data)
                else :
                    sg.popup('没有查询到结果,可能是地址输入错误,或cookie时效过期,需要重新获取! ')    
            else:
               sg.popup('请输入cookie和查询地址   ',font=("微软雅黑", 10),line_width=40,title='')
  
    window.close()


if __name__ == '__main__':
    main()
