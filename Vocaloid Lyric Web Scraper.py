# Project Idea:
# Go to a random song page on the Miku wiki (https://www5.atwiki.jp/hmiku/tag/曲)
# Or go to a page on the Vocaloid Lyrics Wiki
# Get the song name, lyrics, producer, singer, and page link
# Display the data in a window
# Have the ability to repeat as much as you want

'''Miku wiki'''
# Song lyrics start at .find("h3", text = "歌詞")
# and end right before .find("h3", text = コメント")
# Song pages will be like: https://www5.atwiki.jp/hmiku/pages/NUMBER.html
# The NUMBER doesn't start at 1, need to find min/max values

'''Vocaloid Lyrics wiki'''
# Song lyrics stored in a <table>
# Can get all lyrics with .find("table", style = "width:100%")
# Random song page: "https://vocaloidlyrics.fandom.com/wiki/Special:Random"

'''
    Use beautifulsoup for scraping,
    requests for getting website data,
    and lxml for parsing the HTML
'''
from bs4 import BeautifulSoup
import requests, codecs
# Test with AstroPage
'''
web_data = requests.get("https://astropage.neocities.org").text
web_soup = BeautifulSoup(web_data, "lxml")

print(web_soup.prettify())
'''

def vlw_song_get():
    ### vlw_ will be for "Vocaloid Lyrics Wiki" ###
    '''Song with Japanese, Romaji, and English'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/ゴキブリの味_(Gokiburi_no_Aji)").text
    '''Song with Japanese and Romaji only'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/闇屋の娘は眼で殺す_(Yamiya_no_Musume_wa_Me_de_Korosu)").text
    '''Song with only one language'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/I%27m_Breathless").text
    '''Random song, will be the final choice used when finished'''
    vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/Special:Random").text
    
    vlw_soup = BeautifulSoup(vlw_song, "lxml")
    # First handle if an individual song's page isn't selected
    if ("(disambiguation)" in vlw_soup.title.text):
        print("Disambiguation page found")
        print(vlw_soup.title.text)
        print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
    else:
        try:
            title_format = vlw_soup.title.text.find("|")
 
            print("Title:", vlw_soup.title.text[:title_format].strip())
            
            print(vlw_soup.find("b", text = "Producer(s)").text + ":")
            print(vlw_soup.find("b", text = "Producer(s)")
                  .next_element.next_element.next_element.next_element.text.strip())

            print(vlw_soup.find("b", text = "Singer").text + "(s):")
            print(vlw_soup.find("b", text = "Singer")
                  .next_element.next_element.next_element.next_element.text.strip())

            print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
            print()
            try:
                #print(vlw_soup.find("table", style = "width:100%").text)
                skip_line = ["Japanese", "Romaji", "English"]
                for lyric in vlw_soup.find("table", style = "width:100%").stripped_strings:
                    if (lyric in skip_line):
                        pass
                    else:
                        print(lyric)
            except AttributeError:
                '''For when there is only one language. No further formatting needed.'''
                print(vlw_soup.find("div", class_ = "poem").text)
        except Exception as e:
            print(e)

    '''Save lyrics to file for testing, may leave the option in the finished program.'''
    ##with codecs.open("Lyrics_Test_File_Stripped.txt","w", encoding = "utf-8") as f:
    ##    for lyric in vlw_soup.find("table", style = "width:100%").stripped_strings:
    ##        f.write(lyric)

vlw_song_get()
