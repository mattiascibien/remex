import os,sys

class Interacter:
    """Handles the interaction with the user in the console."""
    def __init__(self, defaultPauseMessage=""):
        self._defaultPauseMessage = defaultPauseMessage

    def pause(self, message=""):
        """Rewriting of raw_input which does not print the input afterwards."""
        if message == "":
            message = self._defaultPauseMessage
        print(message)
        try:
            uselessVariable = input()
        except:
            raise SystemExit
    
    def askUserChoice(self, possibleAnswers, menuMessage):
        """Asks the user to choose an item in a list. Each item must be represented by a possible answer. Returns the answer (just find out which item it stands for afterwards).
        <possibleAnswers> is the list of possible answers, not the list of items themselves. For instance, use an integer per item. 
        <menuMessage> is the message prompted to the user. Just describe the items with the answers corresponding to each one."""
        choiceWellDone = False
        while choiceWellDone is not True:
            print(menuMessage)
            try:
                choice = input()
            except KeyboardInterrupt:
                raise SystemExit
            else:
                if choice in possibleAnswers:
                    print("Very well.")
                    choiceWellDone = True
                else:
                    print("Your choice does not match any item. Please try again")
                    self.pause()
        return choice

    def askInteger(self, message):
        """Asks the user to enter an integer with <message> and returns it."""
        done = False
        while done is not True:
            print(message)
            try:
                integer = input()
            except KeyboardInterrupt:
                raise SystemExit
            else:
                try:
                    integer = int(integer)
                except ValueError: 
                    print("Please enter an integer.")
                    self.pause()
                else:
                    done = True
        return integer

    def askString(self, message):
        """Asks the user to enter a string with <message> and returns it."""
        done = False
        while done is not True:
            print(message)
            try:
                string = input()
            except KeyboardInterrupt:
                raise SystemExit
            else:
                done = True
        return string
