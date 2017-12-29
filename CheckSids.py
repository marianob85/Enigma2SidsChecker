#===============================================================================
# Author: Mariusz Brzeski
# Date 01.02.2012
#===============================================================================
import os
import subprocess
import shutil
import re
import sys
import fileinput
import codecs
import binascii
from optparse import OptionParser

import Bouquets
import LameDB



if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-l", "--lameDB",
                      action="store",
                      type="string",
                      dest="LameDBile",
                      help="Enigma 2 files list: path to lamedb file")
    parser.add_option("-i", "--in",
                      action="store",
                      type="string",
                      dest="InputSids",
                      help="")
    parser.add_option("-o", "--out",
                      action="store",
                      type="string",
                      dest="NotSupportedSids",
                      help="")

    (options, args) = parser.parse_args()

    cEnigma2Struct = LameDB.CEnigma2Struct( options.LameDBile )

    cBouquetPath = os.path.dirname(options.LameDBile)
    cBouquetPath = os.path.join(cBouquetPath, "bouquets.tv")

    cBouquets = Bouquets.CBouquets()
    cBouquetsList = cBouquets.Read(cBouquetPath)

    sids=set()

    with open(options.InputSids, "r") as lines:
        for line in lines:
            for sid in line.split():
                sids.add( int(sid.strip(), 16) )
    notUsedSids = sids.copy()
    outFile = open(options.NotSupportedSids, "w")

    for cBouquet in cBouquetsList:
        outFile.write(cBouquet.Name)
        outFile.write('\n')
        for cBouquetService in cBouquet.Services:
            if not cBouquetService.ServiceID in sids:
                cService = cEnigma2Struct.FindService(cBouquetService.ServiceID, cBouquetService.TransportStreamID,
                                                      cBouquetService.OriginalNetworkID, cBouquetService.DVBNameSpace)
                if cService == None:
                    print "Can't find serviceID: " + cBouquetService.ServiceID
                    exit(0)

                outFile.write('\t{:04X}:{}:\t{}'.format(cBouquetService.ServiceID,cBouquetService.ServiceID, cService.ChannelName))
                outFile.write('\n')
            else:
                notUsedSids.remove(cBouquetService.ServiceID)
    outFile.write("Sind not found in Bouquets\n")
    for sid in notUsedSids:
        service = cEnigma2Struct.FindServiceID(sid)
        if service == None:
            outFile.write('\t{:04X}:{}\n'.format(sid,sid))
        else:
            outFile.write('\t{:04X}:{}:\t{}\n'.format(sid, sid, service.ChannelName ))