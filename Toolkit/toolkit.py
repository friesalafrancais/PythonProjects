import PySimpleGUI as sg
import requests
import copy
import webbrowser
import json

sg.theme('DarkBlue17')



mainWindowlayout = [[sg.Text('Select your tool!')],
            [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('Placeholder')],
            [sg.Exit()]]

MainWindow = sg.Window('My toolkit', icon=r'icon.ico', grab_anywhere=True).Layout(mainWindowlayout)



def main_window():
    layout = [[sg.Text('Select your tool!')],
              [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('Placeholder')],
              [sg.Exit()]]
    return sg.Window('My Toolkit', layout, icon=r'icon.ico', grab_anywhere=True)



while True:

    event, values = MainWindow.Read()

    if event in (None, 'Exit'):
        MainWindow.close()
        break

    elif event == 'IP Scanner':
        MainWindow.close()

        layout2 = [[sg.Text('Enter the ip address you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')],
                   [sg.Exit()]]

        IPscannerwindow = sg.Window('IP Scanner', icon=r'icon.ico', grab_anywhere=True).Layout(copy.deepcopy(layout2))
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
                            [sg.Listbox(results["vulns"], size=(50, len(results["vulns"])), key='-VULN-', enable_events=True, text_color='blue')],
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

        layout3 = [[sg.Text('Enter the email you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')],
                   [sg.Exit()]]

        EmailCheckerWindow = sg.Window('Email Checker', icon=r'icon.ico', grab_anywhere=True).Layout(
            copy.deepcopy(layout3))

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

                    "X-RapidAPI-Key": "YOUR-BREACH-DIRECTORY-API-HERE",                                #<==================CHANGE TO YOUR OWN API

                    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"

                }


                response = requests.request("GET", url, headers=headers, params=querystring).text


                sg.popup_scrolled('Results', response, icon=r'icon.ico', grab_anywhere=True)

                EmailCheckerWindow.close()
                MainWindow = main_window()

                keepRunning = False

            
            
    elif event == 'Placeholder':

        MainWindow.close()

        layout4 = [[sg.Text('Placeholder, no function! ')], [sg.InputText()], [sg.Button('Submit')], [sg.Exit()]]

        placeholderwindow = sg.Window('Placeholder', icon=r'icon.ico', grab_anywhere=True).Layout(
            copy.deepcopy(layout4))
        event, values4 = placeholderwindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):

                placeholderwindow.close()
                MainWindow = main_window()
                break

            if event in (None, 'Submit'):

            # Do stuff

                placeholderwindow.Close()
                MainWindow = main_window()

            keepRunning = False
