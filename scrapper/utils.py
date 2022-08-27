import genanki
import random
from datetime import datetime
from django.conf import settings
import tempfile
import cloudinary.uploader
import cloudinary
from django.core.files import File
from django.core.files.storage import default_storage


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
        
        f = tempfile.NamedTemporaryFile()
        f.name = _deck_name
        package.write_to_file(f)
        f.seek(0)

        file = cloudinary.uploader.upload(f,resource_type="raw")

        return file


    def create_deck_name(self):
        _deck_name = "new_vocabulary"

        date_time_object = datetime.now()

        date_time_string = date_time_object.strftime("%d-%m-%Y_%H-%M-%S")

        _deck_name += "_" + date_time_string

        self.deck_name = _deck_name

        return 0

        


