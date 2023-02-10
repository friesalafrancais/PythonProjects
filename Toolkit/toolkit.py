import PySimpleGUI as sg
import requests
import copy
import json



layout = [[sg.Text('Select your tool!')],
            [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('Placeholder')],
            [sg.Exit()]]

layout2 = [[sg.Text('Enter the ip address you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')], [sg.Exit()]]

layout3 = [[sg.Text('Enter the email you would like to scan: ')], [sg.InputText()], [sg.Button('Submit')], [sg.Exit()]]

layout4 = [[sg.Text('Placeholder, no function! ')], [sg.InputText()], [sg.Button('Submit')], [sg.Exit()]]

window = sg.Window('My toolkit', icon=r'icon.ico').Layout(layout)

keepRunning = True


def main_window():
    layout = [[sg.Text('Select your tool!')],
              [sg.Button('IP Scanner'), sg.Button('Email Checker'), sg.Button('Placeholder')],
              [sg.Exit()]]
    return sg.Window('My Toolkit', layout, icon=r'icon.ico')



while True:

    event, values = window.Read()

    if event in (None, 'Exit'):
        window.close()
        break

    elif event == 'IP Scanner':
        window.close()
        window2 = sg.Window('IP Scanner', icon=r'icon.ico').Layout(copy.deepcopy(layout2))
        event, values2 = window2.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                window2.close()
                window = main_window()
                break

            if event == "Submit":

                text_input = values2[0]
                results = requests.get("https://internetdb.shodan.io/" + str(text_input)).json()
                sg.popup_scrolled('IP Scanned:', text_input, 'Open Ports:', results['ports'], 'Tags:',
                                  results['tags'], 'Vulnerabilities:', results['vulns'], 
                                  icon=r'C:\Users\AM\PycharmProjects\MyToolkit\icon.ico')


                window2.Close()
                window = main_window()
                keepRunning = False

    elif event == 'Email Checker':

        window.close()
        window3 = sg.Window('Email Checker', icon=r'icon.ico').Layout(
            copy.deepcopy(layout3))
        event, values3 = window3.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                window3.close()
                window = main_window()
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


                sg.popup_scrolled('Results', response, icon=r'icon.ico')

                window3.close()
                window = main_window()

                keepRunning = False

    elif event == 'Placeholder':

        window.close()
        window4 = sg.Window('Placeholder', icon=r'icon.ico').Layout(
            copy.deepcopy(layout4))
        event, values4 = window4.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):

                window4.close()
                window = main_window()
                break

            if event in (None, 'Submit'):

            # Do stuff

                window4.Close()
                window = main_window()

            keepRunning = False
