#! /usr/local/bin/python3
#Please supply the path to a python3 installation with access to NumPy.
#If you do not have NumPy, try running "pip3 install numpy".


import sys
from numpy import array, dot
from itertools import combinations
from copy import deepcopy

def help():
    print('''
Usage: To process structure.hkl, run "2twin structure" and follow the
prompts. Manually duplicate structure.ins to structure-2twin.ins and ensure it
has HKLF 5 and the correct number of BASF parameters.


Description: 2twin takes an input hkl file (HKLF 4 or 5 format), applies one or
more (pseudo-)merohedral twin laws, and outputs an HKLF 5 file containing one
batch for every twin-related domain. 

For example, you might have a three-component HKLF 5 file and wish to apply 
2[110] as an additional merohedral twin law. In ShelXL, TWIN and HKLF 5 are not 
mutually compatible, so both forms of twinning cannot be refined together. 
Instead, we transform every reflection in the HKLF 5 file by the merohedral
twin law, generating a new file with twice the number of entries.

The input HKLF 5 file might contain the following group of three overlapping
reflections, where "m should be positive for the last contributing component
and negative for the remaining ones".

   2   2   1 89993.4 1839.96  -3
   3  -1   0 89993.4 1839.96  -2
  -1   1   2 89993.4 1839.96   1

After processing with 2twin, each reflection in the group has been copied and
transformed by the merohedral twin law 010/100/00-1. The hkl file contains
all merohedrally and non-merohedrally related twin components, and the 
refinement proceeds with 6 - 1 = 5 BASF parameters.

   2   2  -1 89993.4 1839.96  -6
   2   2   1 89993.4 1839.96  -3
  -1   3   0 89993.4 1839.96  -5
   3  -1   0 89993.4 1839.96  -2
   1  -1  -2 89993.4 1839.96  -4
  -1   1   2 89993.4 1839.96   1


The following combinations of twin laws are currently supported. Other
combinations may be added; contact the author or try editing compDict.
     1 merohedral TL, order 2
     1 merohedral TL, order 3
     2 merohedral TLs, orders 2 and 2
     2 merohedral TLs, orders 3 and 2
     3 merohedral TLs, all order 2
     1 non-merohedral and 1 merohedral, each order 2
     1 non-merohedral and 1 merohedral, orders 3 and 2
     1 non-merohedral and 1 merohedral, orders 2 and 3
     1 non-merohedral and 2 merohedral, all order 2
     1 non-merohedral and 2 merohedral; orders 3, 2, 2
     1 non-merohedral and 3 merohedral; orders 3, 2, 2, 2


Note that your agreement factors may be artifically increased if you have
switched from TWIN/HKLF 4 refinement to HKLF 5 refinement. This is because
merging is disabled for HKLF 5 data. For a fair comparison, run your TWIN/HKLF 4
refinement with MERG 0.
    ''')

def makeCompDict():

    compDict = {
        #This dictionary is only for hklf entries that we generate using 
        #transform, so output component #s are generally negative. Components
        #that would never be generated by transform are written with positive 
        #comp #s and only included for completeness.'''
        
        # 1 merohedral TL, order 2
        ('1',''): 1,
        ('1','1'): -2,
        # 1 merohedral TL, order 3
        ('11',''): 1,
        ('11','1'): -2,
        ('11','11'): -3,
        # 2 merohedral TLs, orders 2 and 2
        ('12',''): 1,
        ('12','1'): -2,
        ('12','2'): -3,
        ('12','12'): -4,
        # 2 merohedral TLs, orders 3 and 2
        ('112',''): 1,
        ('112','1'): -2,
        ('112','11'): -3,
        ('112','2'): -4,
        ('112','12'): -5,
        ('112','112'): -6,
        # 3 merohedral TLs, all order 2
        ('123',''): 1,
        ('123','1'): -2,
        ('123','2'): -3,
        ('123','3'): -4,
        ('123','12'): -5,
        ('123','13'): -6,
        ('123','23'): -7,
        ('123','123'): -8,
        # 1 non-merohedral and 1 merohedral, each order 2:
        ('01',''): 1,
        ('01','0'): 2,
        ('01','1'): -3,
        ('01','01'): -4,
        # 1 non-merohedral and 1 merohedral, orders 3 and 2:
        ('001',''): 1,
        ('001','0'): 2,
        ('001','00'): 3,
        ('001','1'): -4,
        ('001','01'): -5,
        ('001','001'): -6,
        # 1 non-merohedral and 1 merohedral, orders 2 and 3:
        ('011',''): 1,
        ('011','0'): 2,
        ('011','1'): -3,
        ('011','01'): -4,
        ('011','11'): -5,
        ('011','011'): -6,
        # 1 non-merohedral and 2 merohedral, all order 2:
        ('012',''): 1,
        ('012','0'): 2,
        ('012','1'): -3,
        ('012','2'): -4,
        ('012','01'): -5,
        ('012','02'): -6,
        ('012','12'): -7,
        ('012','012'): -8,
        #1 non-merohedral and 2 merohedral; orders 3, 2, 2
        ('0012', ''): 1,
        ('0012', '0'): 2,
        ('0012', '00'): 3,
        ('0012', '1'): -4,
        ('0012', '01'): -5,
        ('0012', '001'): -6,
        ('0012', '2'): -7,
        ('0012', '02'): -8,
        ('0012', '002'): -9,
        ('0012', '12'): -10,
        ('0012', '012'): -11,
        ('0012', '0012'): -12,
        # 1 non-merohedral and 3 merohedral; orders 3, 2, 2, 2
        ('00123', ''): 1,
        ('00123', '0'): 2,
        ('00123', '00'): 3,
        ('00123', '1'): -4,
        ('00123', '01'): -5,
        ('00123', '001'): -6,
        ('00123', '2'): -7,
        ('00123', '02'): -8,
        ('00123', '002'): -9,
        ('00123', '3'): -10,
        ('00123', '03'): -11,
        ('00123', '003'): -12,
        ('00123', '12'): -13,
        ('00123', '012'): -14,
        ('00123', '0012'): -15,
        ('00123', '13'): -16,
        ('00123', '013'): -17,
        ('00123', '0013'): -18,
        ('00123', '23'): -19,
        ('00123', '023'): -20,
        ('00123', '0023'): -21,
        ('00123', '123'): -22,
        ('00123', '0123'): -23,
        ('00123', '00123'): -24
        }
    return compDict


class Hklf(object):

    def __init__(self, hklfString, fileInfo):
        self.h = int(hklfString[0:4])
        self.k = int(hklfString[4:8])
        self.l = int(hklfString[8:12])
        self.f2 = hklfString[12:20]
        self.sig = hklfString[20:28]
        self.hkl = array([[self.h], [self.k], [self.l]])

        if fileInfo['hklType'] == '5': 
            self.comp = int(hklfString[28:32])
        else: 
            self.comp = 1

        self.tlFlags = '0' * (-1 + abs(self.comp))

    def transform(self, twinLaw, compDict, tlAll):
        self.hkl = dot(twinLaw.tlArray, self.hkl)
        self.h, self.k, self.l = self.hkl[:,0]
        self.tlFlags += twinLaw.tlNumber
        self.comp = compDict[ (tlAll, self.tlFlags) ]

    def nTransform(self, transString, compDict, fileInfo):
        hklfTemp = deepcopy(self)
        for trans in transString:
            tlNumber = int(trans)
            twinLaw = fileInfo['tlList'][tlNumber-1]
            hklfTemp.transform(twinLaw, compDict, fileInfo['tlAll'])
        return hklfTemp


    def output(self):
        if self.h % 1 + self.k % 1 + self.l % 1 > 0.1:
            return ''
        else:
            return '{: 4}{: 4}{: 4}{}{}{: 4}\n'.format(
                int(round(self.h)), int(round(self.k)), int(round(self.l)), 
                self.f2, self.sig, self.comp 
                )
                

class TwinLaw(object):
    def __init__(self, tlString, tlNumber):
        tlList = [float(n) for n in tlString.split()]
        self.tlArray = array(
            [tlList[0:3], tlList[3:6], tlList[6:9]]
            )
        self.tlMult = int(tlList[9])
        self.tlNumber = tlNumber


def makeFamily(hklfIn, fileInfo, compDict):
    '''Takes an input hklf object. Transforms it the appropriate number of 
    times to generate additional hklf objects with new indices and comp #s. 
    Returns them all, formatted, in the correct order.
    '''
    familyList = [hklfIn.output()]
    for trans in fileInfo['transList']:
        familyList.insert(
            0,hklfIn.nTransform(trans, compDict, fileInfo).output())
    return ''.join(familyList)







def getInfo():
    '''This makes a dictionary of some information about the run. 
    hklType: 4 or 5.
    hklf5TwinMult: The number of twin components in the input hkl file.
    tlCount: Number of independent twin laws to be supplied by user.
    tlList: A list of TwinLaw objects. 
    tlAll: A string encoding all the twin operators that may be applied, with
        their multiplicity. Non-merohedral twin laws are encoded as 0's. User-
        supplied merohedral twin laws are numbered 1, 2, ...
        If the input file is hklf4 and the user supplies a 3fold and a 2fold
        twin law, tlAll is '112'. If the input file is hklf5 with 3 components
        and the user supplies two 2fold twin laws, tlAll is '0012'.
    transList: a list of substrings of tlAll encoding the transformations that
        actually must be applied to each reflection. If tlAll is '0112', then 
        transList is ['1', '2', '11', '12', '112']. The 0's are omitted from 
        transList because non-merohedrally twin-related reflections have
        already been sorted out in data reduction.  
    nComp: total number of twin-related orientations.''' 

    #define prompts:
    hklTypePrompt = '\nWhat is the format of the input hkl file? Enter 4 or 5: '
    hklf5TwinMultPrompt = '\nHow many twin components are in the input file? '
    tlCountPrompt = '\nHow many independent (pseudo-)merohedral twin laws will\
 be applied? \nInversion twinning should be included if necessary. '
    tlPrompt = '\nEnter twin law #{} in ShelXL format. Do not use a negative\
 value of N.\n'


    #collect information:
    hklType = input(hklTypePrompt)
    if hklType == '5':
        hklf5TwinMult = int(input(hklf5TwinMultPrompt))
    else:
        hklf5TwinMult = 1
    nComp = hklf5TwinMult

    tlCount = int(input(tlCountPrompt))

    tlList = []
    for i in range(tlCount):
        tlNumber = i+1
        tlStringTemp = input(tlPrompt.format(tlNumber))
        tlList.append(TwinLaw(tlStringTemp, str(tlNumber)))
        nComp *= tlList[-1].tlMult

    #make the transformation list for family generation
    tlAll = ''
    tlAll += (-1 + hklf5TwinMult) * '0'
    for tl in tlList:
        tlAll += (-1 + tl.tlMult) * tl.tlNumber

    tlAllMero = tlAll.lstrip('0')
    transList = []
    for i in range(len(tlAllMero)):
        transSubListTemp = list(combinations(tlAllMero, i+1))
        for trans in transSubListTemp:
            if trans not in transList:
                transList.append(trans)


    #make a dictionary:
    fileInfo = {}
    for i in ['hklType', 'hklf5TwinMult', 'tlCount', 'tlList', 'tlAll',
        'transList', 'nComp']:
        fileInfo[i] = locals()[i]
    return fileInfo


def main(hklName):

    fileInfo = getInfo()
    compDict = makeCompDict()
    print('\nProcessing...') 
    inFile = open((hklName + '.hkl'), 'r')
    outFile = open((hklName  + '-2twin.hkl'), 'w') 

    while True:
        entry = inFile.readline()
        if not entry.split() or entry.split()[0:3] == ['0','0','0']: break
        hklf = Hklf(entry, fileInfo)
        outFile.write(makeFamily(hklf, fileInfo, compDict))

    inFile.close()
    outFile.close()
    
    print(
        '''\nOutput written to {}. 
Continue refinement with HKLF 5 and {} BASF parameters.'''
        .format((hklName + '-2twin.hkl'), fileInfo['nComp']-1)
        )
    



print('''
################################################################################
                2twin: Multiple independent twinning in ShelXL. 
                             Daniel W. Paley, 2017.
                         Contact: dwp2111@columbia.edu
################################################################################
''')

if len(sys.argv) == 1 or sys.argv[1] == '--help':
    help()
else:
    main(sys.argv[1])









