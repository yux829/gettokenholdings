import PySimpleGUI as sg
import os

#sg.ChangeLookAndFeel('GreenTan')
form = sg.FlexForm('', default_element_size=(30, 1))
layout = [ [sg.Text('  Python File Create EXE(.py)  ',size=(25,1),font=("Helvetica", 20))],
           [sg.Text('Input the Python File Name')],
           [sg.Input('',key='py_file',size=(50,1)),
            sg.FileBrowse('Browse',target='py_file',initial_folder=os.getcwd(),file_types=(("Python File","*.py"),))],
          [sg.RButton('Create',size=(20,3))]
          ]
window = sg.Window('Pyinstall Py_To_EXE').Layout(layout)
while True:
    button, value = window.read()

    if button == None  :
        break

    elif button=='Create':
        command='pyinstaller -F -w '+value['py_file']
        print(command)
        f = os.popen(command, "r")
        d = f.read()  # 读文件
        print(d)
        f.close()
        print('ok.....')

    else:
        pass

window.close()