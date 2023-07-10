from dashboard import get_prediction


def test_get_prediction_accord():
    '''Test la fonction get_prediction() du dashboard pour un client dont le prêt est considéré 'accordé'.'''
    assert get_prediction(192535) == (0.481, 'Accordé')


def test_get_prediction_refus():
    '''Test la fonction get_prediction() du dashboard pour un client dont le prêt est considéré 'refusé'.'''
    assert get_prediction(420554) == (0.678, 'Refusé')

