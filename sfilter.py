#!/usr/bin/python
# coding: utf-8

import re


def filtering(s):
    """

    >>> db = ['악질경찰.The.Bad.Lieutenant.Port.of.Call.New.Orleans.2009.LiMiTED.DVDRip.XviD.AC3-ViSiON.SnP', '명탐정 코난 15기 극장판 - 침묵의 15분 -릴불명', '행오버2 The Hangover 2 DVDRip XviD-MAXSPEED', '아이 윌 팔로우 (I Will Follow) 2011.DVDRip.XviD-IGUANA', '겟 스마트 Get.Smart[2008]DvDrip-aXXo']
    >>> for a in db:
    ...  print filtering(a)
    ...
    악질경찰 The Bad Lieutenant Port of Call New Orleans 2009 LiMiTED DVDRip XviD AC3 ViSiON SnP
    명탐정 코난 15기 극장판   침묵의 15분  릴불명
    행오버2 The Hangover 2 DVDRip XviD MAXSPEED
    아이 윌 팔로우  I Will Follow  2011 DVDRip XviD IGUANA
    겟 스마트 Get Smart 2008 DvDrip aXXo
    """
    s_compiler = re.compile('[\[\].,()-]')
    s = s_compiler.sub(" ", s)

    return s

def separate(s):
    """
    >>> aa = '악질경찰.The.Bad.Lieutenant.Port.of.Call.New.Orleans.2009.LiMiTED.DVDRip.XviD.AC3-ViSiON.SnP'
    >>> separate(filtering(aa).decode('utf-8'))
    [u'The Bad Lieutenant Port of Call New Orleans 2009 LiMiTED DVDRip XviD AC3 ViSiON SnP', u'\uc545\uc9c8\uacbd\ucc30 ']
    """
    ascii_chrs = ''
    non_ascii_chrs = ''

    ascii_space = False

    for a in range(len(s)):
        char = s[a]
        char_num = ord(char)

        if char_num == 0x0020:
            if ascii_space:
                ascii_chrs += char
                continue
            else:
                non_ascii_chrs += char
                continue
            
        if char_num > 0x007b:          # non-ascii
            non_ascii_chrs += char
            ascii_space = False
        else:
            ascii_chrs += char
            ascii_space = True

    return [ascii_chrs, non_ascii_chrs]


def englishTitle(s):
    """

    >>> db = ['악질경찰.The.Bad.Lieutenant.Port.of.Call.New.Orleans.2009.LiMiTED.DVDRip.XviD.AC3-ViSiON.SnP', '명탐정 코난 15기 극장판 - 침묵의 15분 -릴불명', '행오버2 The Hangover 2 DVDRip XviD-MAXSPEED', '아이 윌 팔로우 (I Will Follow) 2011.DVDRip.XviD-IGUANA', '겟 스마트 Get.Smart[2008]DvDrip-aXXo']
    
    >>> for a in db:
    ...  sep = separate(filtering(a).decode('utf-8'))
    ...  print englishTitle(sep[0])
    ...
    The Bad Lieutenant Port of Call New Orleans 
    <BLANKLINE>
    2 The Hangover 2 
    I Will Follow  
    Get Smart 

    >>> englishTitle(None)
    """
    result = ''
    try:
        s_lower = s.lower()
    except:
        return ''
    sc = re.compile('[0-9]{4}|dvdrip|brrip|dbrip|hdrip|dvdscr')
    mc = sc.search(s_lower)

    try:
        start = mc.start()
    except:
        return result

    return s[:start]
    

def getTitle(s):
    s = filtering(s)
    s = separate(s)          
    return [englishTitle(s[0]), s[0]]   # ascii part


