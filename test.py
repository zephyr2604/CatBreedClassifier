import requests

resp = requests.post("http://localhost:5000/predict",files={'file':open('siamese.jpg','rb')})

print(resp.text)