# Subnetting WOW app
import PySimpleGUI as sg
import ipaddress
import random
import string

from PySimpleGUI.PySimpleGUI import Text

'''
    Simple GUI to help our class subnet
'''

def main(subnetNumber = 8):
    # sg.theme('TanBlue')

    # Static inputs
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
    ]

    # ------ Make the Table Data ------
    data = make_table(num_rows=15, num_cols=6)
    headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
    
    # Static outputs
    ouput_data_column = [
        [sg.Text("IP Address"),
        sg.Text(size=(40, 1), key="ipOut")],
        [sg.Text("Subnet ID"),
        sg.Text(size=(40, 1), key="subnetOut")],
        [sg.Text("Number of hosts"),
        sg.Text(size=(40, 1), key="numHostsOut")],
        [sg.Table(values=data[1:][:], headings=headings, max_col_width=25,
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=20,
                    # alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=35,
                    tooltip='This is a table')],
    ]
    
    # Dynamic Inputs and Outputs
    for x in range(1, int(subnetNumber) + 1):
        input_column.append(
            [sg.InputText('Subnet' + str(x), key='subnet' + str(x)),
            sg.InputText('0', key='numHostsSubnet' + str(x))
            ]
        )
    input_column.append(
        [sg.Button('Submit'),
        sg.Button('Exit')]
        )


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
            vslmDict = calcualteVSLM(ipOut, values)
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

def calcualteVSLM(ipaddress, valuesDict):
    """"
    Caclulate variable length subnet masks for each desired subnet
    """
    numSubNets = int(valuesDict['numSubnets'])
    subnetDict = {}
    subnetList = []
    for x in range(1, numSubNets + 1):
        # print(valuesDict['subnet' + str(x)])
        subnetDict[valuesDict['subnet' + str(x)]] = int(valuesDict['numHostsSubnet' + str(x)])
        subnetTuple = (valuesDict['subnet' + str(x)], int(valuesDict['numHostsSubnet' + str(x)]))
        subnetList.append(subnetTuple)
    # Sort by number of hosts descending
    # subnetDict = dict(sorted(subnetDict.items(), key=lambda item: item[1]))
    subnetList.sort(key = lambda x: x[1], reverse=True)
    print(subnetList)

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for __ in range(num_cols)]
    for i in range(1, num_rows):
        data[i] = [word(), *[number() for i in range(num_cols - 1)]]
    return data

if __name__ == '__main__':
    main()