# Subnetting WOW app
import PySimpleGUI as sg
import ipaddress

'''
    Simple GUI to help our class subnet
'''

def main():
    # sg.theme('TanBlue')

    input_column = [
        [sg.Text('Enter your CIDR IP!', size=(30, 1), font=("Helvetica", 25))],
        # [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('192.0.2.1', key='ipAddress')],
        # sg.InputText('255.255.255.255', key='subnetMask')],
        [sg.Combo(('/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', '/10', '/11', '/12', '/13', '/14', '/15', '/16', '/17', '/18', '/19', '/20', '/21', '/22', '/23', '/24', '/25', '/26', '/27', '/28', '/29', '/30', '/31', '/32'), key='netBits', size=(20, 1))],
        [sg.Button('Submit')],
        [sg.Button('Exit')],
    ]
    ouput_data_column = [
        [sg.Text("IP Address"),
        sg.Text(size=(40, 1), key="ipOut")],
        [sg.Text("Subnet ID"),
        sg.Text(size=(40, 1), key="subnetOut")],
        [sg.Text("Number of hosts"),
        sg.Text(size=(40, 1), key="numHostsOut")],
    ]

    layout = [
        [
            sg.Column(input_column),
            sg.VSeparator(),
            sg.Column(ouput_data_column),
        ]
    ]

    window = sg.Window('Subnet Tool for Class 21015', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read()

        if event == "Submit":
            ipOut, subnetOut, numHostsOut = calculateSubnet(values['ipAddress'], values['netBits'])
            window['ipOut'].update(ipOut)
            window['subnetOut'].update(subnetOut)
            window['numHostsOut'].update(numHostsOut)

        elif event in ('Exit', None):
            break

    window.close()


def calculateSubnet(ip_address, netBits):
    """
    Function that will intake user IP address and calculate network ID and subnet ID
    """
    host1 = ipaddress.ip_interface(ip_address + netBits)
    subnet1 = ipaddress.ip_network(host1.network)
    print('IP:', host1)
    print('Subnet ID:', subnet1)
    print('Number of possible hosts:', subnet1.num_addresses)
    return host1, subnet1, subnet1.num_addresses


if __name__ == '__main__':
    main()