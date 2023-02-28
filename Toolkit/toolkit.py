import PySimpleGUI as sg
import requests
import webbrowser
import subprocess
import platform
from faker import Faker

fake = Faker()


sg.theme('DarkBlue17')

# Creates the main window layout with some basic device info
mainWindowlayout = [[sg.Text('Device Name: ' + platform.node())],
                    [sg.Text('Operating System: ' + platform.system() + ' ' + platform.release())],
                    [sg.Text('Version: ' + platform.version())],
                    [sg.Text('Python Version: ' + platform.python_version())],
                    [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('System Info')],
                    [sg.Button('Fake Info Generator'), sg.Button('Placeholder2'), sg.Button('Placeholder3')],
                    [sg.Exit()]]

MainWindow = sg.Window('My toolkit', icon=r'icon.ico', grab_anywhere=True).Layout(mainWindowlayout)


# Function that creates the main window layout
def main_window():
    layout = [[sg.Text('Device Name: ' + platform.node())],
                    [sg.Text('Operating System: ' + platform.system() + ' ' + platform.release())],
                    [sg.Text('Version: ' + platform.version())],
                    [sg.Text('Python Version: ' + platform.python_version())],
                    [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('System Info')],
                    [sg.Button('Fake Info Generator'), sg.Button('Placeholder2'), sg.Button('Placeholder3')],
                    [sg.Exit()]]
    return sg.Window('My Toolkit', layout, icon=r'icon.ico', grab_anywhere=True)


while True:

    event, values = MainWindow.Read()

    if event in (None, 'Exit'):
        MainWindow.close()
        break

    elif event == 'IP Scanner':
        MainWindow.close()

        ipscannerLayout = [[sg.Text('Enter the ip address you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')],
                   [sg.Exit()]]

        IPscannerwindow = sg.Window('IP Scanner', ipscannerLayout, icon=r'icon.ico', grab_anywhere=True)
        event, values2 = IPscannerwindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                IPscannerwindow.close()
                MainWindow = main_window()
                break

            if event == "Submit":

                text_input = values2[0]
                results = requests.get("https://internetdb.shodan.io/" + str(text_input)).json()

                # Sorts the vulnerabilities by year from oldest to newest
                results["vulns"].sort()

                # If statement checks to see if the amount of vulns detected is greater than 0
                # If it is, a listbox listing the results is created, otherwise no listbox is created and the user is notified
                if len(results["vulns"]) > 0:

                    layoutIPscanresults = [[sg.Text("IP Scanned: ")], [sg.Text(text_input)], [sg.Text("Open ports:")],
                                           [sg.Text(results['ports'])],
                                           [sg.Text("Vulnerabilities:")],
                                           [sg.Listbox(results["vulns"], size=(50, len(results["vulns"])), key='-VULN-',
                                                       enable_events=True, text_color='blue')],
                                           [sg.Button('Exit', key='Exit', size=(10, 1))]]
                else:
                    layoutIPscanresults = [[sg.Text("IP Scanned: ")], [sg.Text(text_input)], [sg.Text("Open ports:")],
                                           [sg.Text(results['ports'])],
                                           [sg.Text("No vulnerabilities detected.")],
                                           [sg.Button('Exit', key='Exit', size=(10, 1))]]

                IPresultswindow = sg.Window("IP Results", layoutIPscanresults, icon=r'icon.ico', grab_anywhere=True)

                url_opened = None

                while True:
                    event, IPvalues = IPresultswindow.Read()
                    if event == sg.WIN_CLOSED or event == "Exit":
                        IPresultswindow.Close()
                        break
                    if event == "-VULN-":
                        selected_url = IPvalues["-VULN-"][0]
                        selected_index = results["vulns"].index(selected_url)
                        if selected_url != url_opened:
                            url_opened = selected_url
                            webbrowser.open("https://nvd.nist.gov/vuln/detail/" + selected_url)

                IPscannerwindow.Close()
                MainWindow = main_window()
                keepRunning = False



    elif event == 'Email Checker':

        MainWindow.close()

        emailcheckerLayout = [[sg.Text('Enter the email you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')],
                   [sg.Exit()]]

        EmailCheckerWindow = sg.Window('Email Checker', emailcheckerLayout, icon=r'icon.ico', grab_anywhere=True)

        event, values3 = EmailCheckerWindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                EmailCheckerWindow.close()
                MainWindow = main_window()
                break

            if event == "Submit":
                text_input = values3[0]
                url = "https://breachdirectory.p.rapidapi.com/"
                querystring = {"func": "auto", "term": "{}".format(text_input)}
                headers = {

                    "X-RapidAPI-Key": "YOUR-BREACH-DIRECTORY-API-HERE",  # <==================CHANGE TO YOUR OWN API

                    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"

                }

                response = requests.request("GET", url, headers=headers, params=querystring).text

                sg.popup_scrolled('Results', response, icon=r'icon.ico', grab_anywhere=True)

                EmailCheckerWindow.close()
                MainWindow = main_window()

                keepRunning = False



    elif event == 'System Info':

        MainWindow.close()

        sysinfoLayout = [[sg.Text('Use this tool to gather system information')],
                   [sg.Text('Click below to gather OS, Architecture, IP addressing, Hotfixes, etc..')],
                   [sg.Button('Gather!')], [sg.Exit()]]

        systeminfowindow = sg.Window('System Info', sysinfoLayout, icon=r'icon.ico', grab_anywhere=True)
        event, values4 = systeminfowindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                systeminfowindow.close()
                MainWindow = main_window()
                break

            if event in (None, 'Gather!'):

                Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
                new = []

                # arrange the string into clear info
                for item in Id:
                    new.append(str(item.split("\r")[:-1]))


                layout = [[sg.Text(i[2:-2])] for i in new]
                window = sg.Window('test', layout, grab_anywhere=True, icon=r'icon.ico')
                button, values = window.read()

                systeminfowindow.Close()
                MainWindow = main_window()

            keepRunning = False



    elif event == 'Fake Info Generator':
        MainWindow.close()

        fakeinfoLayout = [
            [sg.Text('Select the information you want to generate:')],
            [sg.Checkbox('Name', default=False, key='name'), sg.Checkbox('License Plate', default=False, key='license_plate'), sg.Checkbox('Email', default=False, key='email')],
            [sg.Checkbox('Address', default=False, key='address'), sg.Checkbox('Credit Card', default=False, key='credit_card'), sg.Checkbox('Job title', default=False, key='job_title')],
            [sg.Checkbox('Phone Number', default=False, key='phone'), sg.Checkbox('Ipv4 addr.', default=False, key='ipv4_addr'), sg.Checkbox('Ipv6 addr.', default=False, key='ipv6_addr')],
            [sg.Checkbox('Social Security Number', default=False, key='ssn'), sg.Checkbox('Mac Addr.', default=False, key='mac_addr'), sg.Checkbox('Coordinates', default=False, key='latlng')],
            [sg.Button('Generate'), sg.Button('Exit'), sg.Button('Select/Deselect ALL')],
            [sg.Output(size=(65, 20), font=('Helvetica', 18), key='generatedinfo')]
        ]


        fakeinfoWindow = sg.Window('Fake Information Generator', fakeinfoLayout, grab_anywhere=False, icon=r'icon.ico')

        keepRunning = True

        checkbox_states = {key: True if key == 'test' else False for key in ['name', 'address', 'phone', 'ssn', 'job_title', 'email', 'license_plate', 'credit_card', 'ipv4_addr', 'ipv6_addr', 'mac_addr', 'latlng']}
        check_all_state = False

        while keepRunning is True:
            event, values = fakeinfoWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

            if event == 'Generate':

                # User selects the info they want generated
                generated_info = ''
                if values['name']:
                    generated_info += "Name: " + fake.name() + '\n'
                if values['address']:
                    generated_info += "Address: " + fake.address() + '\n'
                if values['phone']:
                    generated_info += "Phone Number: " + fake.phone_number() + '\n'
                if values['job_title']:
                    generated_info += "Job Title: " + fake.job() + '\n'
                if values['ssn']:
                    generated_info += "SSN: " + fake.ssn() + '\n'
                if values['email']:
                    generated_info += "Email: " + fake.ascii_email() + '\n' + '\n'
                if values['license_plate']:
                    generated_info += "License Plate: " + fake.license_plate() + '\n'
                if values['credit_card']:
                    generated_info += "Credit Card: " + fake.credit_card_full() + '\n'
                if values['ipv4_addr']:
                    generated_info += "Ipv4 Address: " + fake.ipv4() + '\n'
                if values['ipv6_addr']:
                    generated_info += "Ipv6 Address: " + fake.ipv6() + '\n'
                if values['mac_addr']:
                    generated_info += "Mac Address: " + fake.mac_address() + '\n'
                if values['latlng']:
                    lat, lng = fake.latlng()
                    generated_info += "Coordinates: ({}, {})\n".format(lat,lng)


                # outputs generated info to the window
                fakeinfoWindow['generatedinfo'].update(generated_info)

            if event == 'Select/Deselect ALL':
                # Set the value of all checkboxes to True
                check_all_state = not check_all_state
                for key in checkbox_states.keys():
                    checkbox_states[key] = check_all_state
                    fakeinfoWindow[key].update(checkbox_states[key])




        # Closes the fake info generator and re-opens main window
        fakeinfoWindow.close()
        MainWindow = main_window()



