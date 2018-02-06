import cv2
import sys
import requests
import time
import numpy as np
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from openalpr import Alpr
from sinesp_client import SinespClient
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


alpr = Alpr("br", "openalpr.conf", "runtime_data")

if not alpr.is_loaded():
    print("Erro ao carregar o OpenALPR")
    sys.exit(1)



if len(sys.argv) > 1:
    filepath = str(sys.argv[1])
else:
    print "Erro no caminho do programa."
    sys.exit(1)

alpr.set_top_n(1)
sc = SinespClient()

old = 'ABC1234'
lista = [old]
cap = cv2.VideoCapture(filepath)
while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)

    results = alpr.recognize_ndarray(gray)
    i = 0
    for plate in results['results']:
        #print(results)
        i += 1
        x = plate['candidates'][0]['plate']

        if (old != x):
            if not (x in lista):
                lista.append(x)
                print ("Placa: %s" % x)
                resultado = sc.search(x)
                print ("Cidade: %s\nEstado: %s\nMarca: %s\nModelo: %s\nCor: %s\nAno de Fabricacao: %s\nChassi: %s\nStatus: %s\nRetorno: %s\n\n" %( resultado['city'], resultado['state'], resultado['brand'], resultado['model'], resultado['color'], resultado['model_year'], resultado['chassis'], resultado['status_message'], resultado['return_message']))




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
alpr.unload()

