# Gamma Ray Burst for Amateur

This project is all about connecting Amateur Astronomers with the Ferm Satellite.
This platform will allow:
* Astronomers to register for event notification when the Ferm Satellite detect a GRB event
* Publish their observation
* Receive notification by email
* Receive notification directly to a client that can start an observation and recording


## RoadMap

1. Website that allow to register to notification with email.
2. Website that can download the client.
3. AlertSys that keep track of Fermi alert from Nasa GCN kafka server. 

The webserver will use FastAPI/Vue.js.
The rest will use python.

## Security of the client

I don't want to require registering with an email and a password. To avoid security issue, I will use a set of private and public key.
All client will receive encoding message with a private key. They will all be able to use a public key to decrypt the message. This will
garantee that a client won't be diverted by attackers.
