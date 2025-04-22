'''
 TEST - Login
 Test per verificare il corretto funzionamento del servizio di login
'''
import requests

ABU_API_BASE_URL = 'http://127.0.0.1:8001/'

def test_login_Campi1():
    '''
    login test - Campo email mancante
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': '', 
        'password': 'passwordSicura' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']['field']
    assert response.status_code == 400
    assert "email" in responseErrMsg
def test_login_Campi2():
    '''
    login test - Campo password mancante
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser12', 
        'password': '' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']['field']
    assert response.status_code == 400
    assert "password" in responseErrMsg

def test_login_NonRegistrato():
    '''
    login test - Utente non registrato
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'utenteNonEsistente', 
        'password': 'passwordSicura' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']
    assert response.status_code == 400
    assert "non registrata" in responseErrMsg
# test sull'utente con username: testUser1
def test_login_PwdSbagliata():
    '''
    login test - Utente registrato ma credenziali errate
    Consiglio - per testare bene questo caso di test, rimuovere il record dalla 
    tabella dei tentativi di accesso e riattivare l'utenza di test
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser1', 
        'password': 'passwordSicura' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']
    assert response.status_code == 400
    assert "sono errate" in responseErrMsg or "numerosi tentativi" in responseErrMsg
def test_login_TroppiAccessi():
    '''
    login test 3 - L'utente ha effettuato troppi accessi
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser1', 
        'password': 'passwordSicura' 
    }
    requests.post(url, json=data) #secondo tentativo
    requests.post(url, json=data) #terzo tentativo
    requests.post(url, json=data) #quarto tentativo
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']
    assert response.status_code == 400
    assert "numerosi tentativi" in responseErrMsg
def test_login_UtenteDisabilitatoPwd():
    '''
    login test - Login corretto, ma l'utenza risulta disabilitata
    a causa di un numero eccessivo di accessi con pwd sbagliate
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser1', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']
    assert response.status_code == 401
# test sull'utente con username: testUser2
def test_login_UtenteDisabilitato():
    '''
    login test - Login corretto, ma l'utenza risulta disabilitata da 
    un utente con privilegi alti
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser2', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    responseErrMsg = response.json()['detail']
    assert response.status_code == 401
# test sull'utente con username: testUser3 (userType: 2-partner)
def test_login_PwdScadutaBool():
    '''
    login test - Login corretto, ma l'utenza ha la pwd scaduta
    e quindi riceverà status 403, e nelle azioni obbligatorie avrà come azione quella di effettuare il cambio pwd
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser3', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 403
    assert response_json['detail'] is not None
    assert response_json['detail']['requiredAction'] is not None
    assert 'CHGPWD' in response_json['detail']['requiredAction']
# test sull'utente con username: testUser4 (userType: 3-admin collaboratore)
def test_login_PwdScadutaDT():
    '''
    login test - Login corretto, ma l'utenza ha la pwd scaduta
    perchè la data di ultima modifica della password supera il
    limite entro cui bisogna cambiarla
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser4', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 403
    assert response_json['detail'] is not None
    assert response_json['detail']['requiredAction'] is not None
    assert 'CHGPWD' in response_json['detail']['requiredAction']
# test sull'utente con username: harsh (userType: 1-admin)
def test_login_OK_admin():
    '''
    login test - Login corretto
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'harsh', 
        'password': 'funziona123!' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['userData'] != None
    assert len(response_json['token']) > 10

# test sugli orari di accesso per utenti con userType: 0-utente normale (testUser5,6,7,8,9,10)
'''
Prima di eseguire i test seguenti, sistemare gli orari degli utenti coinvolti sul db in base alla data e ora attuale
per avere dei risultati corretti
'''
def test_login_OrarioMancante():
    '''
    login test - Orario mancante
    utente utilizzato: testUser5
    Errore: campo orario non valorizzato
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser5', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 403
def test_login_Ok_OrariLiberi():
    '''
    login test - login corretto
    utente utilizzato: testUser6
    Descrizione: l'utente fa l'accesso nell'orario autorizzato
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser6', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['userData'] != None
    assert len(response_json['token']) > 10
def test_login_GiornoNonAutorizzato():
    '''
    login test
    utente utilizzato: testUser7
    Errore: giorno in cui si sta cercando di accedere non autorizzato
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser7', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 403
def test_login_OrarioNonAutorizzato():
    '''
    login test
    utente utilizzato: testUser8
    Errore: orario di accesso non autorizzato
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser8', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 403
def test_login_Ok_fasciaOraria1():
    '''
    login test - login corretto
    utente utilizzato: testUser9
    Descrizione: orario di accesso = fascia oraria 1
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser9', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['userData'] != None
    assert len(response_json['token']) > 10
def test_login_Ok_fasciaOraria2():
    '''
    login test - login corretto
    utente utilizzato: testUser10
    Descrizione: orario di accesso = fascia oraria 2
    '''
    url = ABU_API_BASE_URL + 'login'
    data = {
        'email': 'testUser10', 
        'password': 'funziona123' 
    }
    response = requests.post(url, json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['userData'] != None
    assert len(response_json['token']) > 10


# Controllati a mano e con test automatici fino a qui