import genanki
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.conf import settings


import tempfile
import cloudinary.uploader
import cloudinary
from django.core.files import File
from django.core.files.storage import default_storage

class WordreferenceScrapper ():

    wordreference_url = "https://www.wordreference.com/es/translation.asp"
    list_anki_notes = []
    conditionals = {
        "principal-translation":{"search":True,"text":"Principal Translations"},
        "additional-translation":{"search":True,"text":"Additional Translations"},
        "compound-form":{"search":True,"text":"Phrasal verbs"},
        "verbal-elocution":{"search":True,"text":"Compound Forms"},
        }

    def __init__(self, _list_words, _conditionals = [], _deck_name = ""):
        
        

        
        self.list_words = _list_words
        
        for key, value in _conditionals.items():
            self.conditionals[key]["search"] = value

        self.deck_name = _deck_name

        return 

    def start(self):
        
        _list_anki_notes = {}

        for word in self.list_words:
            html_text = self.request(word)

            soup = self.create_soup(html_text)

            anki_notes = self.scan_words(soup)
            
            _list_anki_notes.update(anki_notes)
            
    
        self.list_anki_notes = _list_anki_notes

        file = self.create_anki_deck()

        return file
        
        #file_absolute_url = self.create_anki_deck()

        
        #return file_absolute_url 

    def request(self, word):
        
        self.url = self.wordreference_url + "?tranword=" + word
        self.url = "http://api.scraperapi.com?api_key=f58a320d5f2cfdbc2e354eca449ac7eb&url=" + self.url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }


        response = requests.get(self.url,timeout=60,headers = headers)
        print(response.request.headers)

        return response.text


    def create_soup(self, html_text):
        
        soup = BeautifulSoup(html_text, 'html.parser')

        return soup

    def scan_words(self, soup_object):
        wrd_tags = soup_object.select('.WRD')
        
        html_tags = []
        i = 0
        for wrd_tag in wrd_tags:
            for key,condition_info in self.conditionals.items():

                if(condition_info["search"] == True and wrd_tag.select('.wrtopsection td')[0].attrs["title"] == condition_info["text"]):
                    
                    html_tags += wrd_tag.select('.even, .odd')
           

                    break
            i += 1

        
        data_notes = {}

        anki_note_question = ""
        anki_note_answer = ""

        completed_anki_note_questions = []
        
        for html_tag in html_tags:
            
            if anki_note_question == "":
                anki_note_question = self.fill_new_question(html_tag)

            anki_note_answer += str(html_tag)
                    
            if self.is_end_question(html_tags, html_tag):
                
                if not (anki_note_question in completed_anki_note_questions):
                    data_notes[anki_note_question] = anki_note_answer
                else:
                    data_notes[anki_note_question] += anki_note_answer
                
                completed_anki_note_questions.append(anki_note_question)
                
                anki_note_question = ""
                anki_note_answer = ""
            """ End of the code section"""
            
        return data_notes
        
    def is_end_question(self,html_tags, html_tag):
        next_index = html_tags.index(html_tag) + 1

        if next_index < len(html_tags):
            next_tag = html_tags[next_index]
            return True if "id" in next_tag.attrs else False
        else:
            return True

    def fill_new_question(self,html_tag):
        note_question = ""
        
        words_tag = html_tag.select(".FrWrd")[0]

        note_word_question_tag = words_tag.select("strong")[0]
        
        allowed_titles = ["something", "somebody","something or somebody","somebody or something"]
        
        for note_word_question in note_word_question_tag.contents:

            if isinstance(note_word_question, str) or len(note_word_question.attrs) != 0 and note_word_question.attrs["title"] in allowed_titles:
                note_question += str(note_word_question) 

        word_type_tag = words_tag.select(".POS2")[0]
        word_type_content = word_type_tag.contents

        if len(word_type_content) > 0:
            word_type_text = word_type_content[0]
            note_question += " <strong>" + str(word_type_text) + "</strong>"
        

        return note_question


    def create_anki_deck(self):

        _list_anki_notes = self.list_anki_notes
        _deck_name = self.deck_name 
        
        
        vocabulary_anki_deck_creator_object = VocabularyAnkiDeckCreator(_list_anki_notes, _deck_name)

        #file_absolute_url = vocabulary_anki_deck_creator_object.create()    


        #return file_absolute_url

        file = vocabulary_anki_deck_creator_object.create()


        return file





class VocabularyAnkiDeckCreator():

    def __init__(self, _list_anki_notes, _deck_name = ""):
        

        self.list_anki_notes = _list_anki_notes

        self.deck_name = _deck_name
        
        return 


    def create(self):

        note_css = """
            .question{
                text-align:center;
            }

            table{
                margin:0 auto;
            }
            table.WRD {
                width: 100%;
                border-collapse: collapse;
                border-top: solid 1px #dcdcdc;
                border-bottom: solid 1px #dcdcdc;
                cursor: pointer;
            }

            .even {
                background-color: #f2f2f7;
                vertical-align: top;
            }
            :not(.even)+.even, :not(.odd)+.odd {
                border-top: 1px solid #dcdce6;
            }
            .WRD tr td:nth-child(1):not(.FrEx):not(.ToEx) {
                width: 24%;
            }
            .WRD td.FrWrd {
                padding-left: 5px;
            }
            .WRD td {
                padding: 2px;
            }
            .tooltip {
                display: inline;
                position: relative;
            }
            .POS2 {
                color: #0645ad;
            }
            .tooltip span:not(.ph):not(.rh_sc):not(.ford) {
                z-index: 10;
                display: none;
                padding: 12px;
                bottom: 18px;
                margin-left: -70px;
                width: 240px;
                line-height: 16px;
                border-radius: 5px;
                opacity: .8;
                font-style: normal;
                text-decoration: none;
                cursor: default;
            }
        """

        model_id = random.randrange(1,10)

        my_model = genanki.Model(
            model_id,
            'Simple Model',
            fields=[
                {'name':'Question'},
                {'name':'Answer'}
            ],
            templates=[
                {
                    'name':'{{Question}}',
                    'qfmt':'<div class="question">{{Question}}</div>',
                    'afmt':'{{FrontSide}}<hr id="answer"><table><tbody>{{Answer}}</tbody></table>'
                }
            ],
            css=note_css
        )

        deck_id = random.randrange(1, 10)

        """ TODO: That the user can change the name of the deck via another argument than "-o" """
        my_deck = genanki.Deck(deck_id, self.deck_name)

        list_anki_notes = self.list_anki_notes

        for question, answer in list_anki_notes.items():

            my_card = genanki.Note(my_model,[question,answer])
            my_deck.add_note(my_card)


        package = genanki.Package(my_deck)
        
        if( self.deck_name == ""):
            self.create_deck_name()

        _deck_name = self.deck_name
        
        _deck_name += ".apkg" if not (".apkg" in _deck_name) else ""
        
        #f = open("%s/%scopy" %(settings.MEDIA_ROOT,_deck_name), "a+",encoding="utf8")
        f = tempfile.NamedTemporaryFile()
        f.name = _deck_name
        package.write_to_file(f)
        f.seek(0)


        
        file = cloudinary.uploader.upload(f,resource_type="raw")
        #file = default_storage.save(_deck_name,f)
    

    
        return file


    def create_deck_name(self):
        _deck_name = "new_vocabulary"

        date_time_object = datetime.now()

        date_time_string = date_time_object.strftime("%d-%m-%Y_%H-%M-%S")

        _deck_name += "_" + date_time_string

        self.deck_name = _deck_name

        return 0

        


