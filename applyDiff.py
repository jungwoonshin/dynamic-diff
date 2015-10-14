#!/usr/bin/env python3
"""
This program reads the actions from an action file (representing deletions and additions),
and applies it to an input file in order to transform it into an output file.
It defines the Action class for this purpose, as well as the format of the action file.
"""

# Utilities

import configparser, re

def file2string(file):
    "Makes a string consisting of the content of the file."
    try: 
        fh = open(file)
    except IOError as detail:
        raise Exception("Could not open "+file, detail)
    out = fh.read()
    fh.close()
    return out

def string2file(outString,file):
    try:
        fh = open(file, "w")
    except IOError as detail:
        raise Exception("Could not open "+file, detail)
    fh.write (outString)
    fh.close()

# Classes

""" An action is a deletion or an addition done to some string s1.
Its parameters are its place in s1, its size (how many to delete or add) and, in case of the addition, the content (what to add).
The string representation is for example
DEL 122 4\n
for deleting 4 characters starting at position 122, and
ADD 122 5 {bla b}\n
for inserting the string 'bla b' of length 5 at position 122 into s1.
"""
class Action:
    def __init__ (self, name, place, size, content):
        if not ("DEL" == name or "ADD" == name):
            raise Exception("Invalid action name.")
        if ("ADD" == name) and len(content) != size:            
            raise Exception("Action size "+str(size)+" does not match content {"+content+"}")
        self.name = name
        self.place = place
        self.size = size
        self.content = content
                        
    def __str__ (self):
        if "ADD" == self.name:
            contentStr = ' {'+self.content+'}'
        else:
            contentStr = self.content
        return self.name+' '+str(self.place)+' '+str(self.size)+contentStr+'\n'
    
# Functions

"""
A string representing a list of actions is a concatenation of the strings representing each action.
"""
def string2actions(s):
    actions = []
    name = ""
    i = 0
    while i < len(s):
        name = s[i:i+3]
        i += 3
        place = 0
        size = 0
        content = ""
        if "DEL" == name:
            m = re.match(r' (\d+) (\d+)\n',s[i:])
            if None == m:
                raise Exception("No match for parameters of DEL in "+s[i:])
            (place, size) = m.groups()
            (place, size) = (int(place), int(size))
            i += m.end()
            content = ""
        elif "ADD" == name:
            m = re.match(r' (\d+) (\d+) {',s[i:])
            if None == m:
                raise Exception("No match for parameters of ADD in "+s[i:])
            (place, size) = m.groups()
            (place, size) = (int(place), int(size))
            i += m.end()
            content = s[i:i+size]
            i += size + 2  # }\n
        else:
            raise Exception("Invalid action name fund: "+name)
        action = Action(name, place, size, content)
        # print(str(action))
        actions.append(Action(name, place, size, content))

    return actions
                       
            
def actions2file(actions,file):
    try:
        fh = open(file, "w")
    except IOError as detail:
        raise Exception("Could not open "+file, detail)
    for action in actions:
        fh.write (str(action))
    fh.close()

def applyActions(actions,inString):
    length = 0
    out = ""
    currentPlace=0
    for action in actions:
        if action.place < currentPlace or action.place > len(inString):
            raise Exception("Invalid place of action.")
        out += inString[currentPlace : action.place]
        currentPlace = action.place
        
        if "ADD" == action.name:
            out += action.content
        elif "DEL" == action.name:
            currentPlace += action.size
            
        if currentPlace > len(inString):
            raise Exception("The change goes beyond the end.")

    out += inString[currentPlace:]            
    return out
    
def main():
    # Read the configuration
    config = configparser.ConfigParser()
    config.read("config.ini")
    cfg = config["DEFAULT"]

    sandboxDir = cfg["sandbox folder"]
    inFile = sandboxDir+"/"+cfg["input file 1"]
    outFile = sandboxDir+"/"+cfg["output file"]
    actionFile = sandboxDir+"/"+cfg["action file"]

    # Read the input
    inString = file2string(inFile)
    actionString = file2string(actionFile)
    actions = string2actions(actionString)

    # The main work
    outString = applyActions(actions, inString)
    



    

    # print('instring:',inString)
    # print('actionString:\n',actionString)
    # for i in actions:
    #     print ('action: ', i)
    # print('outString:\n', outString)
    # Output the result
    string2file(outString, outFile)

# The executed part

if __name__ == "__main__":
    main()

