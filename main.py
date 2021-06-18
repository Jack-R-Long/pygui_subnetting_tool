# Subnetting WOW app
import PySimpleGUI as sg
import ipaddress

from PySimpleGUI.PySimpleGUI import Text

'''
    Simple GUI to help our class subnet
'''

def main(subnetNumber = 4):
    # sg.theme('TanBlue')

    input_column = [
        [sg.Text('How many subnets do you need?')],
        [sg.InputText(subnetNumber, key='numSubnets'),
        sg.Button('Update')],
        [sg.Text('Enter your CIDR IP!')],
        [sg.InputText('192.0.2.1', key='ipAddress'),
        # sg.InputText('255.255.255.255', key='subnetMask')],
        sg.Combo(
            ['/' + str(x) for x in range(1, 33)],
            key='netBits', 
            size=(20, 1))
        ],
        [sg.Text('Subnet names'),
        sg.Text('Number of Hosts')],
        [sg.Button('Exit')],
    ]
    #  Add dynamically created list of subnets
    for x in range(1, int(subnetNumber) + 1):
        input_column.append(
            [sg.InputText('Subnet' + str(x), key='subnet' + str(x)),
            sg.InputText('', key='numHostsSubet' + str(x))
            ]
        )
    input_column.append([sg.Button('Submit')])

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

    window = sg.Window('VLSM Tool for Class 21015', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read()

        if event == "Update":
            main(values['numSubnets'])
        
        elif event == "Submit":
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