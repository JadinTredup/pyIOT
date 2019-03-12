import serial
import time
import thingspeak
import PySimpleGUI as sg

##################################################################
##                                                              ##
##             IOT/Arduino Communication Class                  ##
##                                                              ##
##################################################################

class ThingSpeaker():

    def __init__(self, channel_no, api_key):
        self.ch = thingspeak.Channel(channel_no, api_key)


    def connect_serial_device(self, port_name, baud_rate = 9600):
        self.ser = serial.Serial(port_name, baud_rate)


    def get_value(self):
        value = self.ser.readline()
        return value


    def update_cloud(self):
        self.ch.update(self.get_value())


##################################################################
##                                                              ##
##                      GUI CLASS                               ##
##                                                              ##
##################################################################

class ThingSpeakBroadcastGUI():
    """
    Class for creating GUI interfaces for broadcasting data from an Arduino, read via serial connection,
    to a Thingspeak IOT server.
    """

    def __init__(self):
        self.font = 'helvetica'
        self.RUNNING = False


    def run(self):
        layout = self.create_window(win_type='info')
        window = sg.Window('EGG101 Thingspeak Application - Startup', font=(self.font, 12)).Layout(layout)
        self.RUNNING = True

        # window loop
        while self.RUNNING:
            event, values = window.Read()
            if event == 'Submit':
                channel_no, api_key = values
                self.RUNNING = False
            elif event is None or event == 'Exit':
                self.RUNNING = False
                break

        window.Close()
        ts = ThingSpeaker(channel_no, api_key)
        layout = self.create_window(win_type='main')
        self.main_loop(layout, ts)


    def main_loop(self, layout, ts):
        window = sg.Window('EGG101 Thingspeak Application - Running', font=(self.font, 12)).Layout(layout)
        self.RUNNING = True

        # Broadcasting loop
        while self.RUNNING:
            event, values = window.Read()
            if event is None or event == 'Exit':




    def create_window(self, win_type='info'):
        """
        Create the GUI window layouts for the application.

        :param win_type: Type of GUI window to create. Others are "main"
        :return: Returns the layout object for a pysimplegui window
        """
        if win_type is 'info':
            layout = [[sg.Text('EGG101 - Data Broadcaster', font=(self.font, 16), justification='center')],
                      [sg.Text('Enter Desired Channel to Connect to:', font=(self.font, 10)),
                           sg.Input(do_not_clear=True)],
                      [sg.Text('Enter API Key:', font=(self.font, 10)), sg.Input(do_not_clear=True)],
                      [sg.Submit(), sg.Cancel()]]
        elif win_type is 'main':
            layout = [[sg.Text('EGG101 - Data Broadcaster', font=(self.font, 16), justification='center')],]

        return layout


if __name__=="__main__":
    app = ThingSpeakBroadcastGUI()
    app.run()