import re
import os

host = ""
lambdaCertificatePath = ""
lambdaPrivateKeyPath = ""
clientCertificatePath = ""
clientPrivateKeyPath = ""


class color:
    HEADER = '\033[95m'
    IMPORTANT = '\33[35m'
    NOTICE = '\033[33m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    LOGGING = '\33[34m'


def OKGREEN(text):
    return color.OKGREEN + text + color.ENDC


def log(text):
    print color.HEADER + text + color.ENDC
    return text


def user_input():
    global host, lambdaCertificatePath, lambdaPrivateKeyPath, clientCertificatePath, clientPrivateKeyPath
    while True:
        h = raw_input(OKGREEN(
            "Endpoint (Looks like: xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com)\n> "))
        if h:
            if ".iot." in h and ".amazonaws.com" in h:
                host = h
                break
            else:
                print color.FAIL + "Invalid URL" + color.ENDC

    default = "lambda.cert.pem"
    lcp = raw_input(OKGREEN(
        "lambda Certificate Path Default:[%s] Click enter to use defualt\n> " % default))
    if not lcp:
        lambdaCertificatePath = default
    else:
        lambdaCertificatePath = lcp
    default = "lambda.private.key"
    lpkp = raw_input(OKGREEN(
        "lambda Private Key Path Default:[%s] Click enter to use defualt\n> " % default))
    if not lpkp:
        lambdaPrivateKeyPath = default
    else:
        lambdaPrivateKeyPath = lpkp
    default = "client.cert.pem"
    clientCertificatePath = raw_input(OKGREEN(
        "client Certificate Path Default:[%s] Click enter to use defualt\n> " % default))
    if not clientCertificatePath:
        clientCertificatePath = default
    default = "lambda.private.key"
    clientPrivateKeyPath = raw_input(OKGREEN(
        "client Private Key Path Default:[%s] Click enter to use defualt\n> " % default))
    if not clientPrivateKeyPath:
        clientPrivateKeyPath = default


def makeFiles():
    log("Host: [%s]\nlambdaCertificatePath: [%s]\nlambdaPrivateKeyPath:[%s]\nclientCertificatePath: [%s]\nclientPrivateKeyPath: [%s]\n" % (
        host, lambdaCertificatePath, lambdaPrivateKeyPath, clientCertificatePath, clientPrivateKeyPath))

    clientFile = open("defaultFiles/mqtt-client-default.py", "r")
    clientLines = clientFile.readlines()
    clientFile.close()

    clientLines = "".join(clientLines)
    clientLines = re.sub(
        "xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com", host, clientLines)
    clientLines = re.sub("client.cert.pem", lambdaCertificatePath, clientLines)
    clientLines = re.sub("client.private.key",
                         lambdaPrivateKeyPath, clientLines)

    clientFile = open("client/mqtt-client.py", "w")
    clientFile.write(clientLines)
    clientFile.close()

    log("Client File Successfully Created")

    lambdaFile = open("defaultFiles/mqtt-handler-default.py", "r")
    lambdaLines = lambdaFile.readlines()
    lambdaFile.close()

    lambdaLines = "".join(lambdaLines)
    lambdaLines = re.sub(
        "xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com", host, lambdaLines)
    lambdaLines = re.sub("lambda.cert.pem", lambdaCertificatePath, lambdaLines)
    lambdaLines = re.sub("lambda.private.key",
                         lambdaPrivateKeyPath, lambdaLines)

    lambdaFile = open("lambda/mqtt-handler.py", "w")
    lambdaFile.write(lambdaLines)
    lambdaFile.close()

    log("Lambda File Successfully Created")


def zipFiles():
    while True:
        r = raw_input(
            OKGREEN("Would you like me to make your zip file for you? (Y/n)\n> "))
        if r.lower() == 'y':
            OKGREEN("Zipping Lambda Folder. Could take a minute")
            print color.OKBLUE
            os.system("zip -r mqtt-handler.zip lambda/*")
            print color.ENDC
            log("Lambda Zip Created")
            break
        elif r.lower() == 'n':
            break
        else:
            print color.FAIL + "Invalid Response" + color.ENDC


if __name__ == "__main__":
    user_input()
    makeFiles()
    zipFiles()
