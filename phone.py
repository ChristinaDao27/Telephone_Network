"""
File:    phone.py
Author:  Christina Dao
Date:    11/27/2020
Section: 41
E-mail:  cdao1@umbc.edu
Description:
  This Program holds the phone class for the telephone network project(3).
"""


class Phone:
    phone_list = []
    def __init__(self, number, switchboard):
        """
        Constructor function that creates the phone objects.
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        :return: None
        """
        self.number = number
        self.switchboard = switchboard
        self.connected_to = []  # Will only be able to connect to one other phone!
        # Keep a list of all of the phones.
        Phone.phone_list.append(self)

        
    def connect(self, area_code, other_phone_number):
        """
        This function connects the phone to the other phone on the call.
        :param area_code: the area code of the other phone number
        :param other_phone_number: the other phone number without the area code
        :return: None
        """
        # Append the area code and the number of the phone on the other end of the call.
        self.connected_to.append(area_code)
        self.connected_to.append(other_phone_number)

        
    def disconnect(self):
        """
        Terminates a call by disconnecting the phone. My code in if __name__ == "__main__"
        will call this function for both phones on each end.
        :return: None
        """
        # There are two elements in a connected phone's connected_to list, so remove both of them.
        self.connected_to.remove(self.connected_to[0])
        self.connected_to.remove(self.connected_to[0])

