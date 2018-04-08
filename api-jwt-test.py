import os, jwt, sys

# Note:  the JWT public key needs to be put in an environment variable called JWT_PUBLIC_KEY
#        this is the string value extracted from a JWKS, for example one found from auth0
#        see https://auth0.com/docs/api-auth/tutorials/verify-access-token#how-can-i-verify-the-signature-

public_key = os.environ["JWT_PUBLIC_KEY"]
jwt.decode(sys.argv[1], public_key, algorithms=['RS256'])
