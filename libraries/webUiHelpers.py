import re

# removes artifacts from webscraping
def formatGeniusLyrics(lyrics, artist):

    # remove header
    index = lyrics.find("Lyrics")
    if index != -1:
        lyrics = lyrics[index + len("Lyrics"):]
                        
        # remove embed tag
        lyrics = lyrics[:-5]
        while (True):
            if lyrics[len(lyrics)-1].isdigit():
                lyrics = lyrics[:-1]
            else:
                break
                        
        # remove suggestions
        lyrics = lyrics.replace("You might also like", "")

        # remove ticket ad
        lyrics = re.sub(r'\$[0-9]+', '$', lyrics)
        lyrics = lyrics.replace("See " + artist + " LiveGet tickets as low as $", "")

        return lyrics
    
# edits a config value
def updateConfig(key, value):
        
    # read config data
    file = open("files/config.ini", "r")
    lines = file.readlines()
    file.close()

    # write updated value to given key
    file = open("files/config.ini", "w")
    for line in lines:
        if line.startswith(key + " = "):
            line = key + " = " + value + "\n"
        file.write(line)
    file.close()
