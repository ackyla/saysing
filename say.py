#!/usr/bin/python
# -*- coding: utf-8 -*-

import sing
import sys

if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 2:
        print "Usage: python %s filename" % argvs[0]
        quit()

    lines = open(argvs[1]).read().split('\n')[:-1]
    if len(lines) < 1 or len(lines) > 4:
        print "FileFormat:\n  notes\n  lyric\n  bpm\n  voice"
        quit()

    SaySing = sing.Sing(lines[0].split(','), unicode(lines[1], "utf-8"))
    SaySing.synth(argvs[1][:-4], int(lines[2]), lines[3])
