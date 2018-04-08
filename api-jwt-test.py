import os, jwt, sys, base64

# Note:  the JWT public key needs to be put in an environment variable called JWT_PUBLIC_KEY
#        the contents of this will be a PEM formatted file containing only the public key
#        you can recognise these because they start with a line saying "-----BEGIN PUBLIC KEY----"
#
#        command to extract from a PEM-formatted certificate:
#
#            openssl x509 -pubkey -noout -in cert.pem
#
#        to get a PEM-formatted certificate file from Auth0
#
#            https://[yourdomain].eu.auth0.com/.well-known/jwks.json

public_key = os.environ["JWT_PUBLIC_KEY"]
jwt.decode(sys.argv[1], public_key, algorithms=['RS256'])
