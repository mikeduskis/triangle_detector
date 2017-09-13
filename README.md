# What is this?
It may not be the world's most trivial web service but it's close.
Given three lines, a, b, and c with lengths x, y, and z,
it returns true if the lines can form a triangle.

## What is it good for?
Who knows?  Maybe it will lead to a cure for cancer, or at least acne.  Butterfly wings and all that.

Its actual purpose is to support software testing exercises.  The main branch was intended to lack defects but how much stock should we place in good intentions?  The with_bugs branch was attacked by a drunk monkey one dark and stormy night.


# Installation
python setup.py install

# Starting the server
python -m triangle_detector 8042

Where 8042 is the TCP port on which the service will listen

# Contacting the service
requests.post('http://localhost:8042/', headers={'Content-type':'application-json', data=json.dumps({'a':1, 'b':1, 'c':1}))
