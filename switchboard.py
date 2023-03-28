"""
File:    switchboard.py
Author:  Christina Dao
Date:    11/26/2020
Section: 41
E-mail:  cdao1@umbc.edu
Description:
  The definition file for the class Switchboard for project 3.
"""

from phone import Phone


class Switchboard:

    
    def __init__(self, area_code):
        """
        This function is the constructor that creates the switchboard objects
        :param area_code: the area code to which the switchboard will be associated.
        :return: None
        """
        self.area_code = area_code
        # Lists to store information.
        self.trunks = []
        self.phones = []

        
    def add_phone(self, phone_object):
        """
        This function takes in a phone object, and assigns it to
        the switchboard as a local phone.

        :param phone_object: The entire phone object which is local to this switchboard.
        :return: None
        """
        # Append to the "container"/list of phones, of the switchboard..
        self.phones.append(phone_object)

        
    def add_trunk_connection(self, switchboard):
        """
        Connects the switchboard (self) to the switchboard (switchboard)

        :param switchboard: the area code of the connecting switchboard.
        :return: True for successful connection, False for failed connection.
        """
        # Check if switchboards are already connected.
        if self.trunks:
            for connect in self.trunks:
                if switchboard == connect:
                    print("\tThese switchboards are already connected\n")
                    return False

        self.trunks.append(switchboard)
        return True

    
    def connect_call(self, area_code, number, previous_codes, network):
        """
        Recursive function that finds the path through the switchboards to connect a call.

        :param area_code: the area code to which the destination phone belongs.
        :param number: the phone number of the destination phone without area code.
        :param previous_codes: list of previously tracked area codes.
        :param network: The entire network.
        :return: True if there is a path, False if not.
        """

        # Basecase
        if self.area_code == area_code:
            return True

        else:
            # Try each connected switchboard to see if it connects with the destination area.
            for boards in self.trunks:
                # Make sure we didn't already try the path yet.
                if boards not in previous_codes:
                    previous_codes.append(boards)
                    # Do this to recursively call this function on connected switchboard.
                    for board in network.switchboards:
                        if board.area_code == boards:
                            the_current_switch = board
                    # Recursive call.
                    if the_current_switch.connect_call(area_code, number, previous_codes, network):
                        return True
                                  
        return False

    
