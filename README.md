# bible_text_generation_web_app


## **Setup manual**
#### **Clone**
git clone https://github.com/vip30service123/bible_text_generation_web_app.git </br>
cd bible_text_generation_web_app
#### **Virtual Environment with Conda**
conda create --name {env_name} python={version} (version <= 3.11) </br>
conda activate {env_name} </br>
conda install pip </br>
pip install -r requirements.txt </br>
#### **Run App**
flask --app main.py run </br>
Open web browser, go to localhost:5000

## **Setup with Docker**
#### **Clone**
git clone https://github.com/vip30service123/bible_text_generation_web_app.git </br>
cd bible_text_generation_web_app
#### **Run Docker**
docker compose up --build </br>
Open web browser, go to localhost:5000

## **Dev**
Before commiting, reformatting the code by "black bible_app", "black tests" or "python -m black bible_app" and "python -m black tests" </br>

## **Unfinished Tasks**
CI/CD </br>
Update Model </br>
