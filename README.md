# Stark Bank Challenge Project with Flask

This is the thecnical challenge for join Stark Bank company as Dev.

## Language/tools Requirements

**Python 3.8.x**
**Flask newest version**
**pip newest version**
**ngrok newest version**


**NOTE 1:** some print in some methods are just to see the execution flow because of we are in homolog environment. In the production, they should be removed.


**NOTE 2:** For testing this app, make some changes.
Go to file 'utils/config_constants_paths.py' and make your changes to:

     TOTAL_ROUNDS = X
     SLEEP_MINUTES = Y

## STEPS TO RUN THIS APP ON YOUR MACHINE

### 1 | Clone the remote repository to start testing

     git clone https://github.com/idelfrides/StarkBankChallengeFlask.git

### 2 | You gonna need an external lib to make this project works. Accees the link bellow and follow steps defined at that repository.

[ACCESS LINK HERE --> ](https://github.com/idelfrides/IJGeneralUsagePackage)

### 3 | Create a sandbox account and  then make login to that environment. project in stark bank sandbox environment or use mine (alredy created)

     create an account and then make login .

### 4 | Create your virtualenv like

     virtualenv [your_venv_name]

### 5 | Virtualenv activation

     source [your_venv_name]/bin/activate

If you are using fish, write

     source [your_venv_name]/bin/activate.fish

### 6 | Install requirements

     pip install -r requirements.txt


### 7 | To Set up all project, first you gonna need to run flask server, like this

     python flask_stark_bank_app.py


**[WARNING]: Now you goint to need to create a project in stark bank sandbox environment or use mine (alredy created)**

### 8 | if you want to use your own project informations, run this curl, otherwise do nothing

     curl "http://localhost:7007/gen_project_keys"


**[WARNING]: Now, go to stark bank sandbox environment and  create your project. Keep PROJECT_ID and PROJECT_NAME, you gonna need them.**


**NOTE 3: [RECOMENDATION] if you want to use my project informations, do nothing.**

     My project informations will be used


### 9 | INSTALL, CONFIGUE AND RUN NGROK


1 - INSTALL NGROK

**snap install ngrok**

2 - ADD AUTHTOKEN

**ngrok config add-authtoken <API_KEY>**

3 - ADD API-KEY

**ngrok config add-api_key <NGROK_API_KEY_ID>**

4 - START NGROK

**ngrok http <MY_FLASK_PORT>**


### 10 | MAKE A CHANGE TO MAKE NGROK API WORKS
In file 'config_contants_paths.py' replace the folling line with the real value present in the file you received.


**NGROK_API_KEY = <NGROK_API_KEY>**

### 11 | Now, the Setup will: Create public and private keys, create stark bank project user, create diretories, file RANDOM_PERSON.text, get public url from NGROK API, remove all previous webhook and finaly, create a new webhook . run the folling command just one time.

**RUN SETUP WITH YOUR PROJECT_ID and PROJECT_NAME**

     curl "http://localhost:7007/setup_starkbankapp/<PROJECT_ID>/<PROJECT_NAME>"


**RUN SETUP WITH MY PROJECT_ID and PROJECT_NAME**

     curl "http://localhost:7007/setup_starkbankapp"


### 12 | Now you can run the application using curl. in your

     curl "http://localhost:7007/starkbank_runapp"

### 13 | [OPTIONAL]  You may run test to see results

     python tests/test_keys.py


**[RESULT]: the result of these tests must be FAILED because there is no repetition of key generation. The keys will certainly be different.**
