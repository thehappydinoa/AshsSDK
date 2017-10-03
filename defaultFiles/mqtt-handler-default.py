from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import urllib

host = "xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "lambda.cert.pem"
privateKeyPath = "lambda.private.key"
clientId = "lambda"

endpoints = {
	"endpoints":[
		{
			"endpointId": "VirtualDevice_Device1",
			"manufacturerName": "thehappydinoa",
			"friendlyName": "Device 1",
			"description": "70in AQUOS Smart TV",
			"displayCategories": [  ],
			"cookie": {},
			"capabilities":
			[

				{
					"interface": "Alexa.PowerController",
					"version": "1.0",
					"type": "AlexaInterface"
				},
				{
					"interface": "Alexa.Speaker",
					"type": "AlexaInterface",
					"version": "1.0"
				},
				{
					"interface": "Alexa.PlaybackController",
					"type": "AlexaInterface",
					"version": "1.0"
				},
				{
					"interface": "Alexa.InputController",
					"type": "AlexaInterface",
					"version": "1.0"
				}
			]
		}
	]
}

ENDPOINT_UNREACHABLE = {
	"event": {
		"header": {
		  "namespace": "Alexa",
		  "name": "ErrorResponse",
		  "messageId": "",
		  "payloadVersion": "3"
		},
		"payload": {
		  "type": "ENDPOINT_UNREACHABLE",
		  "message": "Endpoint Unreachable"
		  }
		}
	}

def lambda_handler(request, context):
	namespace = request['directive']['header']['namespace']
	if namespace == 'Alexa.Discovery':
		return handleDiscovery(request)
	else:
		return publishAndWaitForResponse(request)

def responseCallback(client, userdata, message):
	global tempData
	tempData = json.loads(message.payload)

def publish(topic,messageDict):
	client = None
	client = AWSIoTMQTTClient(clientId)
	client.configureEndpoint(host, 8883)
	client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	client.configureAutoReconnectBackoffTime(1, 32, 20)
	client.configureOfflinePublishQueueing(-1)
	client.configureDrainingFrequency(2)
	client.configureConnectDisconnectTimeout(10)
	client.configureMQTTOperationTimeout(5)

	client.connect()
	client.publish(topic, json.dumps(messageDict), 0) #Replace test text with request
	client.disconnect()


def publishAndWaitForResponse(request):
	global tempData
	tempData = json.dumps(ENDPOINT_UNREACHABLE)

	logger = logging.getLogger("AWSIoTPythonSDK.core")
	#logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

	client = None
	client = AWSIoTMQTTClient(clientId)
	client.configureEndpoint(host, 8883)
	client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	client.configureAutoReconnectBackoffTime(1, 32, 20)
	client.configureOfflinePublishQueueing(-1)
	client.configureDrainingFrequency(2)
	client.configureConnectDisconnectTimeout(10)
	client.configureMQTTOperationTimeout(5)

	client.connect()
	client.subscribe("things/" + clientId + "/response", 1, responseCallback)
	client.publish("things/" + clientId, json.dumps(request), 0) #Replace test text with request
	time.sleep(0.75)
	client.disconnect()
	return tempData

def handleDiscovery(request):
	payload = ''
	if request['directive']['header']['name'] == 'Discover':
		publish('log',{"discovery":"Responding to Discovery Request"})
		payload = endpoints
	header = request['directive']['header']
	header['name'] = "Discover.Response"
	return { "event": {"header": header, "payload": payload }}
