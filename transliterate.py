#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mapper;

mapper.loadFile('data/gu_mappings')

_results = []

def _isTypeAllowd(prevType, thisType):
    if thisType == 'matra':
        if prevType == 'consonant':
            return True
        else:
            return False

    if thisType == 'matra_standalone' and \
        (prevType == 'matra_standalone' or prevType == ''):
        return False

    return True

def _getGlue(prevType, thisType):
    if thisType == 'consonant' and prevType == 'consonant':
        return ['', mapper.getSpecial('virama')]

    return ['']

def _processTransliterate(seqLeft, previous = u'', lastMapType = u'', score = []):
    if not len(seqLeft):
        _results.append([previous, score])
        return

    i = 1
    chunk = ''

    while i <= len(seqLeft) and mapper.shouldContinue(chunk):
        chunk = seqLeft[:i]
        chunkLeft = seqLeft[i:]

        maps = mapper.getMaps(chunk)

        for mapping in maps:
            if not _isTypeAllowd(lastMapType, mapping[1]):
                continue
            glues = _getGlue(lastMapType, mapping[1])

            for glue in glues:
                _processTransliterate(
                    chunkLeft,
                    previous + glue + mapping[0],
                    mapping[1],
                    score + [mapping[2]]
                )

        i += 1

def transliterate(word):
    """Returns list of possible transliterations for given word"""
    global _results
    _results = []
    _processTransliterate(word)
    result = map(lambda x: (x[0], sum(x[1]) / float(len(x[1]))), _results)
    result.sort(key=lambda x: x[1], reverse = True)
    return result

if __name__ == '__main__':
    result = transliterate('nisarg')
    for i in result:
        print i[0].encode('utf-8'), i[1]
