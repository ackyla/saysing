#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import wave
import struct
import commands

class Sing:
    def __init__(self, vector, lyric):
        self.notes = self.vector_to_notes(vector)
        self.lyric = self.Kana_to_Moji(lyric)
        
    def vector_to_notes(self, vector):
        duration = 1
        notes = []
        vector.reverse()

        for num in vector:
            if num != '1000':
                notes.append([num, duration])
                duration = 1
            else:
                duration += 1

        notes.reverse()

        return notes

    def Kana_to_Moji (self, sentence_uni):
        words_uni = []
    
        for i in sentence_uni:
            # 拗音は一つ前の文字にくっつける
            if i == u'ャ' or i == u'ュ' or i == u'ョ' or i == u'ァ' or i == u'ィ' or i == u'ゥ' or i == u'ェ' or i == u'ォ':
                try:
                    words_uni[len(words_uni)-1] += i
                # 先頭に拗音が来てしまった場合は例外処理（大文字をアペンド）
                except IndexError:
                    dict = {u'ャ': u'ヤ', u'ュ': u'ユ', u'ョ': u'ヨ', u'ァ': u'ア', u'ィ': u'イ', u'ゥ': u'ウ', u'ェ': u'エ', u'ォ': u'オ'}
                    words_uni.append(dict[i])
            # 撥音は前の文字の母音に変換する
            elif i == u'ッ' or i == u'ー':
                try:
                    temp = commands.getoutput('echo ' + words_uni[len(words_uni)-1].encode('utf-8') + ' | kakasi -Ka -i utf8')
                    temp = temp[len(temp)-1]
                    if temp == 'a':
                        words_uni.append(u'ア')
                    elif temp == 'i':
                        words_uni.append(u'イ')
                    elif temp == 'u':
                        words_uni.append(u'ウ')
                    elif temp == 'e':
                        words_uni.append(u'エ')
                    elif temp == 'o':
                        words_uni.append(u'オ')
                # 先頭に撥音などがきてしまったらとりあえずアをアペンド
                except IndexError:
                    words_uni.append(u'ア')
            # それ以外の文字はアペンドする
            else:
                words_uni.append(i)

        return words_uni
    
    def h2p (self, word_uni):
        dict = {u"ア": "AA",  u"イ": "IY",  u"ウ": "UW",  u"エ": "EH",  u"オ": "AO",
                u"カ": "kAA", u"キ": "kIY", u"ク": "kUW", u"ケ": "kEH", u"コ": "kAO",
                u"ガ": "gAA", u"ギ": "gIY", u"グ": "gUW", u"ゲ": "gEH", u"ゴ": "gAO",
                u"サ": "sAA", u"シ": "sIY", u"ス": "sUW", u"セ": "sEH", u"ソ": "sAO",
                u"ザ": "zAA", u"ジ": "zIY", u"ズ": "zUW", u"ゼ": "zEH", u"ゾ": "zAO",
                u"タ": "tAA", u"チ": "CIY", u"ツ": "CUW", u"テ": "tEH", u"ト": "tAO",
                u"ダ": "dAA", u"ヂ": "zIY", u"ヅ": "zUW", u"デ": "dEH", u"ド": "dAO",
                u"ナ": "nAA", u"ニ": "nIY", u"ヌ": "nUW", u"ネ": "nEH", u"ノ": "nAO",
                u"ハ": "hAA", u"ヒ": "hIY", u"フ": "hUW", u"ヘ": "hEH", u"ホ": "hAO",
                u"バ": "bAA", u"ビ": "bIY", u"ブ": "bUW", u"ベ": "bEH", u"ボ": "bAO",
                u"パ": "pAA", u"ピ": "pIY", u"プ": "pUW", u"ペ": "pEH", u"ポ": "pAO",
                u"マ": "mAA", u"ミ": "mIY", u"ム": "mUW", u"メ": "mEH", u"モ": "mAO",
                u"ヤ": "yAA", u"ユ": "yUW", u"ヨ": "yAO",
                u"ラ": "lAA", u"リ": "lIY", u"ル": "lUW", u"レ": "lEH", u"ロ": "lAO",
                u"ワ": "wAA", u"ヲ": "wAO",
                u"ン": "nUW", # ン は音程がないので ヌ で代用
                u"キャ": "kyAE", u"キュ": "kyUH", u"キェ": "kyEH", u"キョ": "kyAO",
                u"ギャ": "gyAE", u"ギュ": "gyUH", u"ギェ": "gyEH", u"ギョ": "gyAO",
                u"シャ": "SAE",  u"シュ": "SUH",  u"シェ": "SEH",  u"ショ": "SAO",
                u"ジャ": "JAE",  u"ジュ": "JUH",  u"ジェ": "JEH",  u"ジョ": "JAO",
                u"デャ": "dyAE", u"デュ": "dyUH", u"デェ": "dyEH", u"デョ": "dyAO",
                u"チャ": "CAE",  u"チュ": "CUH",  u"チェ": "CEH",  u"チョ": "CAO",
                u"ヂャ": "JAE",  u"ヂュ": "JUH",  u"ヂェ": "JEH",  u"ヂョ": "JAO",            
                u"ニャ": "nyAE", u"ニュ": "nyUH", u"ニェ": "nyEH", u"ニョ": "nyAO",
                u"ヒャ": "hyAE", u"ヒュ": "hyUH", u"ヒェ": "hyEH", u"ヒョ": "hyAO",
                u"ビャ": "byAE", u"ビュ": "byUH", u"ビェ": "byEH", u"ビョ": "byAO",
                u"ピャ": "pyAE", u"ピュ": "pyUH", u"ピェ": "pyEH", u"ピョ": "pyAO",
                u"ミャ": "myAE", u"ミュ": "myUH", u"ミェ": "myEH", u"ミョ": "myAO",
                u"リャ": "lyAE", u"リュ": "lyUH", u"リェ": "lyEH", u"リョ": "lyAO",
                u"ファ": "fAA", u"フィ": "fIY", u"フゥ": "fUW", u"フェ": "fEH", u"フォ": "fAO",
                u"アァ": "AA", u"イィ": "yIY", u"イェ": "yEH", u"ウィ": "wIY", u"ウェ": "wEH"}

        try:
            return dict[word_uni]
        except KeyError:
            return "AA"
 
    def synth(self, name, bpm, voice):
        notes = self.notes
        lyric = [self.lyric]
        resolution = 30 # 解像度：16分音符を使う場合は15
        bar = 0
        word = 0

        fpw = wave.open(name + '_out.wav', 'w')
        # パラメータを決定するためのダミーファイルを作成
        os.system('say -o ' + name + '.aiff "a"')
        os.system('sox ' + name + '.aiff ' + name + '.wav')
        fpr = wave.open(name + '.wav', 'r')
        frate = fpr.getframerate()
        fpw.setparams(fpr.getparams())
        fpr.close()

        for note in notes:
            # 書き込むフレーム数は フレームレート÷BPM×解像度×デュレーション
            nframes = frate / bpm * resolution * note[1]

            if note[0] == '1001':
                wframes = ''
                for i in range(nframes):
                    wframes += '\x00\x00'

            else:
                # 1音のファイルを生成し読み込む
                os.system('say -o ' + name + '.aiff -v ' + voice + ' "[[pmod 0; rate 10; pbas ' + note[0] + '; inpt PHON]]~' + self.h2p (lyric[bar][word]) + ',"')
                os.system('sox ' + name + '.aiff ' + name + '.wav')    
                fpr = wave.open(name + '.wav', 'r')

                # 音声ファイルの加工
                rframes = fpr.readframes(fpr.getnframes()) # 書き込むフレーム数分読み込む
                wframes = ''
                for i in range(fpr.getnframes()):
                    # 無音区間以外を書き込む
                    if struct.unpack('!h', rframes[i*2:i*2+2])[0] != 0:
                        wframes += rframes[i*2:i*2+2]
                # 音声ファイルが書き込むフレーム数より短い場合は無音を書き込む
                if fpr.getnframes() < nframes:
                    for i in range(nframes-fpr.getnframes()):
                        wframes += '\x00\x00'                    

                if word < len(lyric[bar])-1:
                    word += 1
                else:
                    bar += 1
                    word = 0

                if bar == 4:
                    bar = 0
                    word = 0

            # 音声の書き込み
            fpw.writeframes(wframes[:nframes*2])

        fpr.close()
        fpw.close()
        os.system('rm -rf ' + name + '.wav ' + name + '.aiff')
