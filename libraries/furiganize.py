import pykakasi.kakasi as kakasi
import re
import MeCab

kakasi = kakasi()
mecab = MeCab.Tagger("-Owakati")

class Token:

    def __init__(self, _kanji, _reading):
        self.kanji = _kanji
        self.reading = _reading
    
def getReading(expr, type = "hira"):
    '''Types: "orig", "kana", "hira", "hepburn", "kunrei", "passport". Default is hiragana.'''
    dict = kakasi.convert(expr)
    out = u""
    for entry in dict:
        out = out + entry[type]
    return out


def splitKanji(token, match):
    if len(token.kanji) == 1:
        return [token]
    result = []
    if len(token.kanji) == len(token.reading) or len(match) < 2:
        for i in range(len(token.kanji)):
            if token.kanji[i] == token.reading[i]:
                result.append(Token(token.kanji[i], None))
            else: result.append(Token(token.kanji[i], token.reading[i]))
        return result
    # for cases where 
    raise RuntimeError("""Error: Kanji and it's reading have several matches. Not yet implemented.\n
                       {} - {}""".format(token.kanji, token.reading))

    # readings = getReading(token.kanji[0])
    # for reading in readings:
    #     if token.reading[:len(reading)] == reading:
    #         result.append(Token(token.kanji[0], reading))
    #         token.kanji = token.kanji[1:]
    #         token.reading = token.reading[len(reading):]
    #         result = result + SplitKanji(token)
    #         return result
    # return[token]

def processLyrics(expr):
    lines = expr.split("\n")
    lines = [mecab.parse(line) for line in lines]
    out = []
    for line in lines:  
        for kanji in line.split(" "):
            reading = getReading(kanji)
            # scuff english fix
            if re.search(r"[a-zA-Z,]", kanji):
                out.append(Token(kanji + " ", None))
                continue
            # hiragana, punctuation, not japanese, lacking a reading or newline
            if kanji == reading or not reading or kanji == "\n":
                out.append(Token(kanji, None))
                continue
            # katakana
            if kanji == getReading(kanji, "kana"):
                out.append(Token(kanji, None))
                continue
            # don't add readings of numbers
            if kanji in u"一二三四五六七八九十０１２３４５６７８９":
                out.append(Token(kanji, None))
                continue
            # strip matching characters and beginning and end of reading and kanji
            # reading should always be at least as long as the kanji
            pref = u""
            post = u""
            while len(kanji) > 0 and kanji[0] == reading[0]:
                pref = pref + kanji[0]
                kanji = kanji[1:]
                reading = reading[1:]

            while len(kanji) > 0 and kanji[-1] == reading[-1]:
                post = post + kanji[-1]
                kanji = kanji[:-1]
                reading = reading[:-1]

            out.append(Token(pref, None))

            # check for kana inside words
            match = ''.join(set(kanji).intersection(reading))
            if match != "":
                print(kanji, reading)
                for token in splitKanji(Token(kanji, reading), match):
                    out.append(token)
            else: out.append(Token(kanji, reading))

            out.append(Token(post[::-1], None))
    return out
    
def getFurigana(text):
    tokens = processLyrics(text)
    out = u""
    for token in tokens:
        if token.reading is not None:
            out = out + "<ruby>{}<rt>{}</rt></ruby>".format(token.kanji, token.reading)
            # out = out + token.kanji + "[" + token.reading + "]"
        else: out = out + token.kanji
    # scuff fix removes spaces between words and - , . ] ) : ;
    out = re.sub(r"([A-Za-z]) ([-,.\]):;])", r"\1\2", out)
    # out = out.replace("\n", "<br>")    # already in lyric-spot
    return out

# Tests
if __name__ == "__main__":
    # expr = u"カリン、 千葉 千葉 千 彼二千三百六十円も使った。回転寿司."
    # expr = u"私は日本人です"
    expr = u"水田をみる.水をのむ."
    # expr = u"今書いています"
    # expr = u"また追い込んじゃったんだ?"

    print(getFurigana(expr))