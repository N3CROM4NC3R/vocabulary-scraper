# Vocabulary Scraper
Vocabulary Scraper will allow you to create decks of vocabulary to learn languages faster, by using online dictionaries.

It creates decks for an app named Anki, which is a flashcard program that uses Spaced Repetition as a principal studying method.

It also uses wordreference.com as the online dictionary to get words.

## Set it up for development
1. Clone the repo

        git clone https://github.com/N3CROM4NC3R/vocabulary-scraper

2. Create a conda environment with the python version of the file runtime.txt and activate it.

        conda create -n vocabulary-scraper python=3.8.10
        conda activate vocabulary-scraper

3. Install the dependencies in the requeriments.txt file
        
        pip install -r requirements.txt

4. Copy and paste .env-example, and rename it to .env.

5. Configurate the .env file with database credentials

6. Create an account in cloudinary, get the cloud name, API key, and API secret, then, put them in .env,

4. Make migrations and migrate them.
        
        python manage.py makemigrations
        python manage.py migrate

5. Run the development server.

        python manage.py runserver