# Subnetting WOW app
from sys import prefix
import PySimpleGUI as sg
import ipaddress

'''
    Simple GUI to help our class subnet
'''

def main(subnetNumber = 2):
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
    data = make_table(subnetNumber + 1, num_cols=6)
    headings = ['Network Name', 'Hosts', 'Host Bits', 'Subnet Mask', 'Subnet ID', 'Broadcast Address']
    
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
                    display_row_numbers=False,
                    justification='center',
                    num_rows=subnetNumber,
                    # alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=35,
                    tooltip='This is a table')],
    ]
    
    # Dynamic Inputs and Outputs
    for x in range(1, int(subnetNumber) + 1):
        input_column.append(
            [sg.InputText('Subnet' + str(x), key='subnet' + str(x)),
            sg.InputText('250', key='numHostsSubnet' + str(x))
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
            main(int(values['numSubnets']))
        
        elif event == "Submit":
            ipOut, subnetOut, numHostsOut = calculateSubnet(values['ipAddress'], values['netBits'])
            vlsmList = calcualteVSLM(subnetOut, values)
            newData = fill_table(vlsmList, subnetNumber)
            window['-TABLE-'].update(values=newData)
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

def calcualteVSLM(startingSubnet, valuesDict):
    """"
    Caclulate variable length subnet masks for each desired subnet
    Return as a sorted list of tuples
    """
    numSubNets = int(valuesDict['numSubnets'])
    subnetList = []
    for x in range(1, numSubNets + 1):
        subnetX = [valuesDict['subnet' + str(x)], int(valuesDict['numHostsSubnet' + str(x)])]
        subnetList.append(subnetX)
    # Sort by number of hosts descending
    subnetList.sort(key = lambda x: x[1], reverse=True)

    # VSLM for each desired subnet
    for subnetXList in subnetList:
        # Find host bits required.  Add 2 for the network and broadcast address
        hostBits = (subnetXList[1] + 2).bit_length()
        subnetXList.append(hostBits)
        
        netmask = '{:032b}'.format(8589934591)
        hostBitsBinary = '{:032b}'.format(subnetXList[1])
        print(8589934591 & hostBits)
    
    hostBits = (subnetList[0][1] + 2).bit_length()
    subnetCIDR = 32 - hostBits
    # print(subnetCIDR)
    # print(list(startingSubnet.subnets(new_prefix=subnetCIDR)))

    return subnetList

# ------ Some functions to help generate data for the table ------
def make_table(num_rows, num_cols, data = []):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    return data

def fill_table(subnetList, num_rows, num_cols=6):
    # Init 2d data matrix
    outData = [[j for j in range(num_cols)] for i in range(num_rows)]
    # Assign subnet name and number of hosts
    for i in range(num_rows):
        for j in range(len(subnetList[0])):
            outData[i][j] = subnetList[i][j]
    return subnetList


if __name__ == '__main__':
    main()