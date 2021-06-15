# Subnetting WOW app
import PySimpleGUI as sg

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
        [sg.Text('Enter your CIDR IP!', size=(30, 1), font=("Helvetica", 25))],
        # [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('255.255.255.255', key='in1'),
        sg.Combo(('/16', '/17'), key='netBits', size=(20, 1))],
        [sg.Button('Submit')],
        [sg.Button('Exit')],
    ]

    window = sg.Window('Subnet Tool for Class 21015', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read()

        if event == "Submit":
            calculateSubnet(values['in1'], values['netBits'])
        elif event in ('Exit', None):
            break

    window.close()


def calculateSubnet(ip_address, network_bits):
    """
    Function that will intake user IP address and calculate network ID and subnet ID
    """
    print(ip_address)
    print(network_bits)


if __name__ == '__main__':
    main()