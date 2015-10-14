# CS 330 
# HW 05 : Jungwoon Shin
# U22266066

#!/usr/bin/env python3

# Utilities

import configparser, sys
from pprint import pprint


def file2string(file):
    "Makes a string consisting of the conntent of the file."
    
    try: 
        fh = open(file)
    except IOError as detail:
        raise Exception("Could not open "+file, detail)
    out = fh.read()
    fh.close()
    return out

# Classes

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
    
    def __repr__(self):
        return repr(self.val)
        
# Functions

def actions2file(actions,file):
    try:
        fh = open(file, "w")
    except IOError as detail:
        raise Exception("Could not open "+file, detail)
    for action in actions:
        fh.write (str(action))
    fh.close()

# Write your functons here

def computeAofIJ(s1,s2,A,i,j):
    if i is 0 and j is 0:
        A[i][j] = 0
    if i is 0:
        A[i][j] = j
    if j is 0:
        A[i][j] = i
    if s1[i] is s2[j]:
        A[i][j] = min(A[i-1][j-1],1+A[i-1][j], 1+A[i][j-1])
    elif s1[i] is not s2[j]:
        A[i][j] = min(1+A[i-1][j], 1+A[i][j-1])

def computeA(A,i,j):
    loc = (i,j)
    if i is 0 and j is 0:
        return [loc]
    elif i is 0:
        return computeA(A,i,j-1)+[loc]
    elif j is 0:
        return computeA(A,i-1,j)+[loc]
    elif A[i-1][j-1] is not A[i][j]:
        candidates= [A[i-1][j],float("inf"),A[i][j-1]]
    elif A[i-1][j-1] is A[i][j]:
        candidates= [A[i-1][j],A[i-1][j-1],A[i][j-1]]

    minimum = candidates.index(min(candidates))
    if minimum is 0:
        return computeA(A,i-1,j) +[loc]
    elif minimum is 1:
        return computeA(A,i-1,j-1)+[loc]
    elif minimum is 2:
        return computeA(A,i,j-1)+[loc]

def computeActionsWithA(s1,s2,A):
    s1Length = len(s1)
    s2Length = len(s2)
    actions = []
    actionTupleList = computeA(A,s1Length-1,s2Length-1)
    actionTupleListLength = len(actionTupleList)
    tmp0 = 0
    tmp1 = 0

    for i in range(0,actionTupleListLength-1):

        (x1,y1) = actionTupleList[i]
        (x2,y2) = actionTupleList[i+1]

        if x2-x1 is 1 and y2-y1 is 1:
            tmp0 = 0
            tmp1 = 0
            pass

        elif x2-x1 is 1 and y2-y1 is 0:
            tmp1 = 0
            if tmp0 is 0:
                actions.append(Action('DEL',x2,1,content=''))
                tmp0 = tmp0 +1
            else:
                actions[-1].size = actions[-1].size+1
                tmp0 = tmp0 +1

        elif x2-x1 is 0 and y2-y1 is 1:
            tmp0 = 0
            if tmp1 is 0:
                actions.append(Action('ADD',x1+1,1,s2[y2]))
                tmp1 = (tmp1+ 1)
            else:
                actions[-1].size = actions[-1].size + 1
                actions[-1].content = actions[-1].content + s2[y2]
                tmp1 = (tmp1+ 1)
    return actions


def main():
    # Read the configuration    
    config = configparser.ConfigParser()
    config.read("config.ini")
    cfg = config["DEFAULT"]

    sandboxDir = cfg["sandbox folder"]
    inFile1 = sandboxDir+"/"+cfg["input file 1"]
    inFile2 = sandboxDir+"/"+cfg["input file 2"]
    actionFile = sandboxDir+"/"+cfg["action file"]

    # Read the input
    s1 = file2string(inFile1)
    s2 = file2string(inFile2)
    # sys.stderr.write("Files read\n")

    # Write here the part that computes a list of actions called
    s1Length = len(s1)
    s2Length = len(s2)

    A = [[0 for x in range(s2Length) ] for x in range(s1Length)]
    for i in range(0,s2Length):
        A[0][i] = i
    for i in range(0,s1Length):
        A[i][0] = i
    for i in range(1,s1Length):
        for j in range(1,s2Length):
            computeAofIJ(s1,s2,A,i,j)

    actions = computeActionsWithA(s1,s2,A)

    # Output the result
    actions2file(actions, actionFile)

# The executed part
if __name__ == "__main__":
    main()

