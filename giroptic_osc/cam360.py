"""
For use with Giroptic 360cam. Other 360° cams may work also, but are not tested.
This implementation is not feature complete and is not fully tested. More features are added in future releases.

Currently supported are:
- set capture mode
- take picture
- transfer last took picture to PC

Usage:
import: from giroptic_osc.cam360 import Giroptic360cam

get connection to camera: cam = Giroptic360cam()

take picture: cam.take_image()

save image: cam.save_last_file('C:/temp', 'tester')
"""

import requests


class Giroptic360cam:

    def __init__(self, address='192.168.1.168', port=80, use_https=False):
        self.address = address
        self.port = port
        self.use_https = use_https

        self.session_id = self.start_session()

        self.last_took_image = ''

    def start_session(self):
        """
        Starts session and returns sessionId
        :return: sessionId as string
        """
        try:
            cam_session = requests.post(self.exec_address(), '{"name": "camera.startSession"}')
        except ConnectionError as con_err:
            print('Error while connecting to camera')

        if cam_session.status_code == 200:
            return cam_session.json()['results']['sessionId']
        else:
            self.osc_failure(cam_session)

    def set_capture_mode(self, mode):
        """
        Setting capture mode
        :param mode: chose between: image, _video, _burst, _timelapse or _live
        :return: True if successful
        """
        if self.set_option('captureMode', mode.lower()):
            return True
        else:
            raise ValueError('{s} is not a supported mode. Try image, _video, _burst, _timelapse or _live'
                             .format(s=mode))

    def get_capture_mode(self):
        mode = self.get_option('captureMode')
        try:
            return mode['results']['options']['captureMode']
        except KeyError:
            print(mode)

    def take_image(self):
        """
        Takes an image if camera is in image mode.
        :return: True if successful, False if not successful
        """
        try:
            img = requests.post(self.exec_address(),
                                '{"name": "camera.takePicture", "parameters": {"sessionId": "' + self.session_id + '"}}')
        except ConnectionError:
            print('Network error occurred while taking image')

        if img.status_code == 200:
            self.last_took_image = img.json()['results']['fileUri']
            return True
        else:
            self.osc_failure(img)
            return False

    def save_last_file(self, saving_location, file_name, delete=True):
        """
        Transfers the last captured file to the PC.
        :param saving_location: Location where to save the file
        :param file_name: file name without file format
        :param delete: True if file should be deleted on camere, False if not
        :return: True if successful, False if not
        """
        try:
            img = requests.post(self.exec_address(),
                                '{"name": "camera.getImage", "parameters": {"fileUri": "' + self.last_took_image + '"}}',
                                stream=True)
        except ConnectionError:
            print('Network error occurred while saving file')

        if img.status_code == 200:
            with open('{l}/{i}.JPG'.format(l=saving_location, i=file_name), 'wb') as fil:
                for block in img.iter_content(1024):
                    fil.write(block)
            if delete:
                self.delete_file(self.last_took_image)
            return True
        else:
            self.osc_failure(img)
            return False

    def delete_file(self, uri):
        try:
            del_fil = requests.post(self.exec_address(),
                                    '{"name": "camera.delete",'
                                    ' "parameters": {"fileUri": "' + uri + '", "recursive": "True" }}')
        except ConnectionError:
            print('Network error occurred while deleting file')

    def set_option(self, option, value):
        try:
            opt = requests.post(self.exec_address(),
                                    '{"name": "camera.setOptions", "parameters": {"sessionId": "' +
                                self.session_id + '", "options": {"' + option + '": "' + value + '"}}}')
            if opt.status_code == 200:
                return True
            else:
                return False
        except ConnectionError:
            print('Network error occurred while setting option')

    def get_option(self, option):
        try:
            opt = requests.post(self.exec_address(),
                                    '{"name": "camera.getOptions", "parameters": {"sessionId": "' +
                                self.session_id + '", "optionNames": ["' + option + '"]}}')
            if opt.status_code == 200:
                return opt.json()
            else:
                self.osc_failure(opt)
                return opt.json()
        except ConnectionError:
            print('Network error occurred while setting option')

    def close_connection(self):
        """
        Closes connection to camera.
        :return: True if successful, False if not
        """
        try:
            close = requests.post(self.exec_address(),
                                  '{"name": "camera.closeSession",'
                                  ' "parameters": {"sessionId": "' + self.session_id + '"}}')
        except ConnectionError:
            print('Network error occurred while closing connection')

        if close.status_code == 200:
            return True
        else:
            return False

    def exec_address(self):
        """
        Returns the base url for execution commands
        :return: Base url
        """
        protocol = 'https' if self.use_https else 'http'
        return '{p}://{a}/osc/commands/execute'.format(p=protocol, a=self.address)

    @staticmethod
    def osc_failure(err_req):
        print('Error occurred - Status Code {s}'.format(s=err_req.status_codes))
