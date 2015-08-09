#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

_mappings = {}
_mapMappings = {}
_specialMaps = {}

def loadFile(fileName):

    mapFile = codecs.open(fileName, 'r', 'utf-8')

    mapType = ''

    for line in mapFile:
        line = line.strip();

        if not len(line) or line[0] == u'#':
            continue

        elif line[0] == u'-':
            mapType = line[2:-2].strip()

        elif len(line) and u'-' in line:
            mapping = map(lambda x: x.strip(), line.split('-'))

            if mapType == 'special':
                _specialMaps[mapping[0]] = mapping[1]

            if len(mapping) <= 2:
                mapping.append(1)  # Set default weight

            if mapping[0] not in _mappings:
                _mappings[mapping[0]] = []

            _mappings[mapping[0]].append([mapping[1], mapType, float(mapping[2])])

            if mapping[0].lower() not in _mapMappings:
                _mapMappings[mapping[0].lower()] = []

            if mapping[0] not in _mapMappings[mapping[0].lower()]:
                _mapMappings[mapping[0].lower()].append(mapping[0])

    mapFile.close()

def getMaps(chunk):
    if chunk.lower() in _mapMappings:
        allMapChunks = _mapMappings[chunk.lower()]
    else:
        return []

    returnMappings = []
    if chunk in _mappings:
        returnMappings.extend(_mappings[chunk])

    for aChunk in allMapChunks:
        if aChunk == chunk:
            continue;
        returnMappings.extend(_mappings[aChunk])
        # May want to lower the weight

    return returnMappings

def shouldContinue(chunk):
    """Should check if longer chunks starting from `chunk` exists or not"""
    for key in _mapMappings.keys():
        if key.find(chunk.lower()) == 0 and len(key) > len(chunk):
            return True

    return False

def getSpecial(what):
    return _specialMaps[what]

if __name__ == '__main__':
    print "This file is not supposed to be called directly."
