"""
File:    network.py
Author:  Christina Dao
Date:    11/26/2020
Section: 41
E-mail:  cdao1@umbc.edu
Description:
  The definition file for the Network class as well
  as the driver for the program.
"""

from phone import Phone
from switchboard import Switchboard


HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'
SWITCHBOARD = "switchboard "
TRUNK = "trunkline "
PHONE_NUM = "phone_num "


class Network:

    
    def __init__(self):
        """
        This function creates the Network object with
        a switchboard "container" attribute.
        :return: None
        """
        # Switchboard "container"
        self.switchboards = []
        

    def load_network(self, filename):
        """
        This functions loads a file with network info.
        :param filename: the name of the file to be loaded.
        :return: The loaded network.
        """
        
        # Read the file that is to be loaded.
        loaded_network = open(filename + ".txt", "r")

        self = Network()
        # Read the file.
        all_info = loaded_network.read()
        list_info = all_info.split("\n")
        # Removing the empty list at the end.
        listed_info = list_info[0: len(list_info) - 1]

        self.switchboards = []

        # Create switchboards FIRST.
        for lines in listed_info:
            line_info = lines.split()
            #Create the switchboards of the loaded network.
            if line_info[0] == SWITCHBOARD.strip():
                self.add_switchboard(int(line_info[1]))

        for lines in listed_info:
            line_info = lines.split()
            # Create the trunklines
            if line_info[0] == TRUNK.strip():
                for switchboard in self.switchboards:
                    # Check if they've already been connected.
                    if int(switchboard.area_code) == int(line_info[1]) and int(line_info[2]) not in switchboard.trunks:
                        self.connect_switchboards(int(line_info[1]), int(line_info[2]))

            # Create the phones, and add to the correct switchboard's phone list.
            if line_info[0] == PHONE_NUM.strip():
                for switchboard in self.switchboards:
                    if int(switchboard.area_code) == int(line_info[1]):
                        new_phone = Phone(int(line_info[2]), switchboard)
                        switchboard.add_phone(new_phone)

        loaded_network.close()
        return self

        
    def save_network(self, filename):
        """
        This function clears/creates the file that the user inputs,
        and saves the Network info into the file, by a specific format.
        I believe the way I coded, I should be able to save any network.

        :param filename: the name of your file to save the network.
        :return: None
        """
        # Create variable for file.
        # My code WILL ADD ".txt" to whatever is inputted as filename.
        saved_network = open(filename + ".txt", "w")

        # Save each switchboards' area code
        for switch in self.switchboards:
            saved_network.write(SWITCHBOARD + str(switch.area_code) + "\n")
            
            # Save the AREA CODE of the switchboards that are connected to the current.
            # each trunkline in the switchboard's trunkline list is just the other area code.
            for trunks in switch.trunks:
                # Save the area code of the current switchboard as well as the area of
                # the switchboard it is connected to.
                saved_network.write(TRUNK + str(switch.area_code) + " " + str(trunks) + "\n")
                
            # Save the phone numbers of the phones on the switchboard.
            for phones in switch.phones:
                saved_network.write(PHONE_NUM + str(switch.area_code) + " " + str(phones.number) + "\n")

        saved_network.close()

        
    def add_switchboard(self, area_code):
        """
        Creates a switchboard and adds it to the network.
        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return: None
        """

        # Check if area codes switchboard already exists or not.
        for switchboards in self.switchboards:
            if area_code == switchboards.area_code:
                print("\tA switchboard with this area code already exists")
                return

        # Create and add switchboard to network
        new_switchboard = Switchboard(area_code)
        self.switchboards.append(new_switchboard)

        
    def connect_switchboards(self, area_1, area_2):
        """
        Connects the two switchboards (creates a trunk line between them)
        so that long distance calls can be made.

        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: True if boards can connect, False if not.
        """

        # Check that the switchboards exist.
        switchboards = []
        for switchboard in self.switchboards:
            switchboards.append(switchboard.area_code)
            
        if area_1 not in switchboards:    
            print("\tThe switchboard with the area code", area_1, "does not exist.\n")
            return False

        if area_2 not in switchboards:
            print("\tThe switchboard with the area code", area_2, "does not exist.\n")
            return False

        # Connect the switchboards with a trunkline.
        # Find the right switchboards to work with.
        for board in range(len(self.switchboards)):
            if self.switchboards[board].area_code == area_1:
                # Attempting to connect boards
                # Function add_trunk_connection will check if they're already connected or not.
                if self.switchboards[board].add_trunk_connection(area_2):
                    for boards in range(len(self.switchboards)):
                        if self.switchboards[boards].area_code == area_2:
                            if self.switchboards[boards].add_trunk_connection(area_1):
                                return True
        return False     
                            
        
    def display(self):
        """
        This function outputs the status of the phone network.
        :return: None
        """
        # Display information by each switchboard.
        for switchboards in self.switchboards:
            print("Switchboard with area code:  ", switchboards.area_code, "\n\tTrunk lines are:")
            # Display Trunklines of switchboard.
            for trunk_lines in switchboards.trunks:
                print("\t\tTrunk line connection to:  ", trunk_lines)
                
            print("\tLocal phone numbers are:")
            # Display phones of the switchboard and their current call status.
            if not switchboards.phones:
                print()
            else:
                for phones in switchboards.phones:
                    if len(phones.connected_to) == 0:
                        print("\t\tPhone with number:  ", phones.number, "is not in use.")
                    
                    else:
                        print("\t\tPhone with number:  ", phones.number, "is connected to", str(phones.connected_to[0]) + "-" + str(phones.connected_to[1]))
                print()


if __name__ == '__main__':
    the_network = Network()
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            if the_network.connect_switchboards(area_1, area_2):
                print("\tThe switchboards for area numbers", area_1, "and", area_2, "have been connected with a trunkline.\n")
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            the_network.add_switchboard(int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))

            ###### MY CODE STARTS HERE ######
            
            # Check if the area code of the number exists or not.
            area_codes = []
            for switchboard in the_network.switchboards:
                area_codes.append(switchboard.area_code)
            if area_code not in area_codes:
                print("\tThe area code of this number does not exist.\n")

            # Check if the number exists already or not.
            # Find correct switchboard that number may belong to.
            for switchboard in the_network.switchboards:
                if area_code == switchboard.area_code:
                    numbers = []
                    for phones in switchboard.phones:
                        numbers.append(phones.number)

                    if phone_number in numbers:
                        print("\tThis phone number already exists.\n")
                    else:
                        # Create the phone number object.
                        new_phone = Phone(phone_number, switchboard)
                        # Add phone to correct switchboard.
                        switchboard.add_phone(new_phone)

                        
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            the_network.save_network(split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            the_network = Network()
            the_network = the_network.load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            
            ###### MY CODE STARTS HERE AGAIN ######

            # lets make a list of the area codes.
            area_codes = [] 
            for switches in the_network.switchboards:
                area_codes.append(switches.area_code)

            # Check that the area_codes of both of the numbers exist.
            if src_area_code not in area_codes or dest_area_code not in area_codes:
                print("An area code of one of the phone numbers does not exist.")
                print(split_command[1], "and", split_command[2], "were not connected.\n")
                
            else:
                # Find correlating switchboard to the numbers
                for switchboards in the_network.switchboards:
                    if switchboards.area_code == src_area_code:
                        # Check that the first phone number exists
                        phones_1 = []
                        for telephone in switchboards.phones:
                            phones_1.append(telephone.number)
                            
                        if src_number not in phones_1:
                            print("The number", split_command[1], "does not exist.")
                            print(split_command[1], "and", split_command[2], "were not connected.\n")

                        # First number exists, check second number.
                        else:
                            for switchboard in the_network.switchboards:
                                if switchboard.area_code == dest_area_code:
                                    # Check that the second phone number exists
                                    phones = []
                                    for phone in switchboard.phones:
                                        phones.append(phone.number)

                                    if dest_number not in phones:
                                        print("The number", split_command[2], "does not exist.")
                                        print(split_command[1], "and", split_command[2], "were not connected.\n")

                                    # Both numbers exist.
                                    else:
                                        # Both numbers exist - Check if they are already on a call or not
                                        for phones in Phone.phone_list:
                                            if phones.number == src_number and int(phones.switchboard.area_code) == int(src_area_code):
                                                first_phone = phones
                                            elif phones.number == dest_number and int(phones.switchboard.area_code) == int(dest_area_code):
                                                second_phone = phones

                                        if len(first_phone.connected_to) != 0 or len(second_phone.connected_to) != 0:
                                            print("One of the phones is already on a call.")
                                            print(split_command[1], "and", split_command[2], "were not connected.\n")

                                        # Both phones available, connect call.
                                        else:
                                            # Runs if they are on same switchboard.
                                            if src_area_code == dest_area_code:
                                                first_phone.connect(second_phone.switchboard.area_code, second_phone.number)
                                                second_phone.connect(first_phone.switchboard.area_code, first_phone.number)
                                                print(split_command[1], "and", split_command[2], "have been connected.\n")
                                                
                                            # Different switchboards...
                                            else:
                                                # Find the correlating switchboard to the first phone number.
                                                for switch_board in the_network.switchboards:
                                                    if switch_board.area_code == first_phone.switchboard.area_code:
                                                        prev_codes = []
                                                        area_2 = second_phone.switchboard.area_code
                                                        # Try and find the path to the other phone's switchboard.
                                                        if switch_board.connect_call(area_2, second_phone.number, prev_codes, the_network):
                                                            print(split_command[1], "and", split_command[2], "have been connected.\n")
                                                            first_phone.connect(second_phone.switchboard.area_code, second_phone.number)
                                                            second_phone.connect(first_phone.switchboard.area_code, first_phone.number)
                                                        else:
                                                            print(split_command[1], "and", split_command[2], "were not connected.\n")
                                                                
                                                    
        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))

            ###### MY CODE STARTS HERE AGAIN ######
            
            # Used to check if area code exists.
            # Find the right switchboard. 
            switch_count = 0
            for switchboards in the_network.switchboards:
                if int(switchboards.area_code) == area_code:
                    switch_count = 1
                    switch = switchboards

            # Runs if area_code/switchboard of phone number does not exists.
            if switch_count == 0:
                print("The area code of the number does not exist \nUnable to disconnect.\n")

            # Area code exists.
            elif switch_count == 1:
                # Used to check if phone exists.
                # Find the correlating phone.
                phone_count = 0
                for cell_phone in switch.phones:
                    if cell_phone.number == number:
                        phone_count = 1
                        current_cell = cell_phone
                        
                # Runs if the phone number does not exist.
                if phone_count == 0:
                    print("This phone number does not exist. \nUnable to disconnect.\n")

                # Phone exists.
                elif phone_count == 1:
                    # Check if phone is even on a call or not.
                    if len(current_cell.connected_to) == 0:
                            print("The phone is not even on a call.\nUnable to disconnect.\n")
                    else:
                        # Find other cell phone to disconnect and then disconnect both.
                        for switchbord in the_network.switchboards:
                            if int(switchbord.area_code) == int(cell_phone.connected_to[0]):
                                for cell in switchbord.phones:
                                    if int(cell.number) == int(cell_phone.connected_to[1]):
                                        other_phone = cell
                            
                        print("Hanging up...")
                        # Hang up both of the phones
                        cell_phone.disconnect()
                        other_phone.disconnect()
                        print("Connection Terminated.\n")

                        
        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            the_network.display()

        s = input('Enter command: ')
