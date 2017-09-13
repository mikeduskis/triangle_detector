## Installation
python setup.py install

# Starting the server
python -m ptriangle_Detector 8042

Where 8042 is the TCP port on which the service will listen

# Contacting the service
requests.post('http://localhost:8042/', headers={'Content-type':'application-json', data=json.dumps({'a':1, 'b':1, 'c':1}))

English: Can 3 lines with length 1, 1, and 1 form a triangle?

