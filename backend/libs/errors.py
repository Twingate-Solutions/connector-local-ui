import logging

def success():
    return {"status":"OK","errors":[]}

def rconnector_install_error(rcode):
    return {"errors":[{"message":"Error installing Connector.","return_code":str(rcode)}]};