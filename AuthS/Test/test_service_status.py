'''
 TEST - Service Status
 Test per verificare il corretto stato di attività del servizio
'''
import requests

ABU_API_BASE_URL = 'http://127.0.0.1:8001/'

def test_checkS_1():
    '''
    checkS test1 - controlla se il servizio è raggiungibile    
    '''
    url = ABU_API_BASE_URL + 'checkS'
    response = requests.get(url)
    assert response.status_code == 200
def test_checkSDB_2():
    '''
    checkSDB test2 - controlla se il db del servizio è raggiungibile
    '''
    url = ABU_API_BASE_URL + 'checkSDB'
    response = requests.get(url)
    assert response.status_code == 200

# Controllati a mano e con test automatici fino a qui