# Subnetting WOW app
import PySimpleGUI as sg
import ipaddress

'''
    Simple GUI to help our class subnet
'''

def main():
    # sg.theme('TanBlue')

    column1 = [
        [sg.Text('Column 1', background_color=sg.DEFAULT_BACKGROUND_COLOR,
              justification='center', size=(10, 1))],
        [sg.Spin(values=('Spin Box 1', '2', '3'),
                 initial_value='Spin Box 1', key='spin1')],
        [sg.Spin(values=('Spin Box 1', '2', '3'),
                 initial_value='Spin Box 2', key='spin2')],
        [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3', key='spin3')]]

    layout = [
        [sg.Text('Enter your !', size=(30, 1), font=("Helvetica", 25))],
        # [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('192.0.2.1', key='ipAddress')],
        # sg.InputText('255.255.255.255', key='subnetMask')],
        [sg.Combo(('/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', '/10', '/11', '/12', '/13', '/14', '/15', '/16', '/17', '/18', '/19', '/20', '/21', '/22', '/23', '/24', '/25', '/26', '/27', '/28', '/29', '/30', '/31', '/32'), key='netBits', size=(20, 1))],
        [sg.Button('Submit')],
        [sg.Button('Exit')],
    ]

    window = sg.Window('Subnet Tool for Class 21015', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read()

        if event == "Submit":
            calculateSubnet(values['ipAddress'], values['netBits'])
        elif event in ('Exit', None):
            break

    window.close()


def calculateSubnet(ip_address, netBits):
    """
    Function that will intake user IP address and calculate network ID and subnet ID
    """
    host1 = ipaddress.ip_interface(ip_address + netBits)
    print('IP:', host1)
    print('Network:', host1.network)


if __name__ == '__main__':
    main()