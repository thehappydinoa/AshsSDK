from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import logging
import time
import datetime
import json

host = "xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "RPi.cert.pem"
privateKeyPath = "RPi.private.key"
clientId = "client"
topic = "things/lambda/V3"
responseTopic = topic + "/response"
logTopic = "log"

class color:
	HEADER = '\033[95m'
	IMPORTANT = '\33[35m'
	NOTICE =  '\033[33m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	UNDERLINE = '\033[4m'
	LOGGING = '\33[34m'

def callbackHandler(client, userdata, message):
		try:
			request = message.payload
			logging.info(request)
			if message.topic == 'log':
				printLog(request)
				return True
			request = json.loads(request)
			endpointId = request['directive']['endpoint']['endpointId']

			if endpointId == "VirtualDevice_Device1":
				printRequest("Received request for " + endpointId)
				return handleDevice1(request)
			else:
				return responseBuilder("NO_SUCH_ENDPOINT", request)
		except Exception as e:
			printError(str(e))

def clearScreen():
	os.system("clear")
	return True

def getTimeStamp():
	return datetime.datetime.now().ctime() + " "

def printError(error):
	print(color.OKGREEN)
	print("/" + "=" * 18 + " ERROR " + "=" * 18 + "/")
	print("| Time: " + getTimeStamp())
	print("| Error" + error)
	print("/" + "=" * 44 + "/\n")
	print(color.ENDC)

def printAction(device,action):
	print(color.OKGREEN)
	print("/" + "=" * 18 + " ACTION " + "=" * 18 + "/")
	print("| Time: " + getTimeStamp())
	print("| Device: " + device)
	print("| Action: " + action)
	print("/" + "=" * 44 + "/\n")
	print(color.ENDC)

def printRequest(request):
	print(color.IMPORTANT)
	print("/" + "=" * 18 + " REQUEST " + "=" * 17 + "/")
	print("| Time: " + getTimeStamp())
	print("| " + request)
	print("/" + "=" * 44 + "/\n")
	print(color.ENDC)

def printLog(mesage):
	print(color.OKGREEN)
	print("/" + "=" * 20 + " LOG " + "=" * 19 + "/")
	print("| " + mesage)
	print("/" + "=" * 44 + "/\n")
	print(color.ENDC)

def clientInfo():
	print(color.HEADER)
	print("/" + "=" * 18 + " VERSION " + "=" * 17 + "/")
	print("| mqtt-client.py Alexa Smart Home Payload V3 |")
	print("|            Updated on 8/26/2017            |")
	print("/" + "=" * 44 + "/\n")
	print("/" + "=" * 19 + " INFO " + "=" * 19 + "/")
	print("|* Start Time: " + getTimeStamp())
	print("|* Connected to: " + host + " as " + clientId)
	print("|* Logging to Topic: " + logTopic)
	print("|* Responsing to Topic: " + responseTopic)
	print("|* Subscribed to Topic: " + topic)
	print("/" + "=" * 44 + "/")
	print(color.ENDC)

def publishResponse(response):
	print(color.OKBLUE)
	print("/" + "=" * 17 + " RESPONSE " + "=" * 17 + "/")
	print("| Time: " + getTimeStamp())
	print("| Sending..."),
	try:
		client.publish(responseTopic,json.dumps(response),1)
		print("Sent!")
		print("| " + json.dumps(response))
	except Exception:
		print(color.FAIL + "| Error Publishing" + color.ENDC + color.OKBLUE)
	print("/" + "=" * 44 + "/\n")
	print(color.ENDC)
	return response

def responseBuilder(RESPONSE_TYPE, request):
	RESPONSE_TYPE = RESPONSE_TYPE.upper()
	GENERIC_ERRORS = ["ENDPOINT_UNREACHABLE", "NO_SUCH_ENDPOINT", "INVALID_VALUE", "INVALID_DIRECTIVE", "INVALID_AUTHORIZATION_CREDENTIAL", "EXPIRED_AUTHORIZATION_CREDENTIAL", "INTERNAL_ERROR"]
	messageId = getMessageId(request)
	name = getName(request)
	payload = getPayload(request)

	if RESPONSE_TYPE == "SUCCESS":
		return {
			"context": {
				"properties": []
			},
			"event": {
				"header": {
			  "namespace": "Alexa",
			  "name": "Response",
			  "messageId": messageId,
			  "payloadVersion": "3"
			},
				"payload": {}
			}
		}

	elif RESPONSE_TYPE == "INPUT_SUCCESS":
		return {
			"context": {
				"properties": [{
				"namespace": "Alexa.InputController",
				"name": "input",
				"value": payload['input'].upper(),
				"timeOfSample": "2017-02-03T16:20:50.52Z",
				"uncertaintyInMilliseconds": 0
				}]
			},
			"event": {
				"header": {
			  "namespace": "Alexa",
			  "name": "Response",
			  "messageId": messageId,
			  "payloadVersion": "3"
			},
				"payload": {}
			}
		}

	elif RESPONSE_TYPE == "POWER_SUCCESS":
		name = name[4:].upper()
		return	{
			"context": {
					"properties": [ {
						"namespace": "Alexa.PowerController",
						"name": "powerState",
						"value": name,
						"timeOfSample": "2017-02-03T16:20:50.52Z",
						"uncertaintyInMilliseconds": 500
					} ]
				},
				"event": {
					"header": {
					"namespace": "Alexa",
					"name": "Response",
					"messageId": messageId,
					"payloadVersion": "3"
					},
					"payload": {}
				}
			}

	elif RESPONSE_TYPE == "SPEAKER_SUCCESS":
		volume = 50
		if name == "AdjustVolume" or name == "SetVolume":
			volume = payload['volume']
		return {
		  "context": {
				"properties": [
					{
						"namespace": "Alexa.Speaker",
						"name": "volume",
						"value": 50,
						"timeOfSample": "2017-02-03T16:20:50.52Z",
						"uncertaintyInMilliseconds": 0
					},
					{
					"namespace": "Alexa.Speaker",
					"name": "muted",
					"value": (name == "SetMute"),
					"timeOfSample": "2017-02-03T16:20:50.52Z",
					"uncertaintyInMilliseconds": 0
					}
				]
			},
			"event": {
				"header": {
					"namespace": "Alexa",
					"name": "Response",
					"messageId": messageId,
					"payloadVersion": "3"
				},
				"payload": {}
			}
		}
	elif RESPONSE_TYPE == "STEP_SPEAKER_SUCCESS":
		volume = 50
		if name == "AdjustVolume" or name == "SetVolume":
			volume = payload['volumeSteps']
		return {
		  "context": {
				"properties": [
					{
						"namespace": "Alexa.StepSpeaker",
						"name": "volume",
						"value": 50,
						"timeOfSample": "2017-02-03T16:20:50.52Z",
						"uncertaintyInMilliseconds": 0
					},
					{
					"namespace": "Alexa.Speaker",
					"name": "muted",
					"value": (name == "SetMute"),
					"timeOfSample": "2017-02-03T16:20:50.52Z",
					"uncertaintyInMilliseconds": 0
					}
				]
			},
			"event": {
				"header": {
					"namespace": "Alexa",
					"name": "Response",
					"messageId": messageId,
					"payloadVersion": "3"
				},
				"payload": {}
			}
		}

	elif RESPONSE_TYPE == "CHANNEL_SUCCESS":
		return {
		  "context": {
			"properties": [
			  {
				"namespace": "Alexa.ChannelController",
				"name": "channel",
				"value": {
				  "callSign": "LMAO DOES THIS EVEN MATTER??",
				  "affiliateCallSign": "callsign2"
				},
				"timeOfSample": "2017-02-03T16:20:50.52Z",
				"uncertaintyInMilliseconds": 0
			  }
			]
		  },
		  "event": {
			"header": {
			  "messageId": messageId,
			  "namespace": "Alexa",
			  "name": "Response",
			  "payloadVersion": "3"
			},
			"payload": {}
		  }
		}

	elif RESPONSE_TYPE == "VALUE_OUT_OF_RANGE":
		return {
			"event": {
				"header": {
					"namespace": "Alexa",
					"name": "ErrorResponse",
					"messageId": messageId,
					"payloadVersion": "3"
				},
				"payload": {
					"type": RESPONSE_TYPE,
					"message": "The specified value is out of range for this setting.",
					"validRange": {
						"minimumValue": 0,
						"maximumValue": 100
					}
				}
			}
		}

	elif RESPONSE_TYPE in GENERIC_ERRORS:
		return {
			"event": {
				"header": {
					"namespace": "Alexa",
					"name": "ErrorResponse",
					"messageId": messageId,
					"payloadVersion": "3"
				},
				"payload": {
					"type": RESPONSE_TYPE,
					"message": RESPONSE_TYPE.lower().replace("_", " ")
				}
			}
		}

def getNamespace(request):
	return request['directive']['header']['namespace']

def getName(request):
	return request['directive']['header']['name']

def getPayload(request):
	return request['directive']['payload']

def getMessageId(request):
	return request['directive']['header']['messageId']

powerController = "Alexa.PowerController"
speaker = "Alexa.Speaker"
speakerStep = "Alexa.StepSpeaker"
playbackController = "Alexa.PlaybackController"
inputController = "Alexa.InputController"
channelController = "Alexa.ChannelController"

def handleDevice1(request):
	response = responseBuilder("INVALID_DIRECTIVE",request)
	namespace = getNamespace(request)
	name = getName(request)
	payload = getPayload(request)
	device = "Device1"

	# Alexa.PowerController Handler
	if  namespace == powerController:
		powerState = name[4:].upper()
		if powerState == 'OFF':
			printAction(device, "Turning OFF...")
			response = responseBuilder("POWER_SUCCESS",request)
			return publishResponse(response)
		elif powerState == 'ON':
			printAction("TV", "Turning ON...")
			response = responseBuilder("POWER_SUCCESS",request)
			return publishResponse(response)

	# Alexa.Speaker/StepSpeaker Handler
	elif namespace == speaker or namespace == speakerStep:
		if name == "SetVolume":
			setVolume = payload['volume']
			printAction(device, name + ": " + str(setVolume))
			response = responseBuilder("SPEAKER_SUCCESS", request)
			return publishResponse(response)
		elif name == "AdjustVolume":
			volumeSteps = payload['volume']
			if payload['volumeDefault'] == False:
				printAction(device, name + ": "+ str(volumeSteps))
				response = responseBuilder("SPEAKER_SUCCESS", request)
				return publishResponse(response)
			else:
				sign = 1
				if volumeSteps < 0:
					sign = -1
				volumeSteps = 5 * sign
				printAction(device, name + ": "+ str(volumeSteps))
				response = responseBuilder("SPEAKER_SUCCESS", request)
				return publishResponse(response)
		elif name == "SetMute":
			if payload['mute'] == True:
				printAction(device, "MUTE: ON")
			else:
				printAction(device, "MUTE: OFF")
			response = responseBuilder("SPEAKER_SUCCESS", request)
			return publishResponse(response)

	# Alexa.PlaybackController Handler
	elif namespace == playbackController:
		if name == "FastForward":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)
		elif name == "Next":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)

		elif name == "Pause":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)

		elif name == "Play":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)

		elif name == "Previous":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)

		elif name == "Rewind":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)

		elif name == "Stop":
			printAction(device, name)
			response = responseBuilder("SUCCESS", request)
			return publishResponse(response)


	# Alexa.InputController Handler
	elif namespace == inputController:
		INPUT1 = ["INPUT1","HDMI1", "INPUT 1"]
		INPUT2 = ["INPUT2","HDMI2", "INPUT 2"]
		INPUT3 = ["INPUT3","HDMI3", "INPUT 3"]
		INPUT4 = ["INPUT4","HDMI4", "INPUT 4"]

		if payload['input'].upper() in INPUT1:
			printAction(device, name + ": " + payload['input'])
			response = responseBuilder("INPUT_SUCCESS", request)
			return publishResponse(response)

		elif payload['input'].upper() in INPUT2:
			printAction(device, name + ": " + payload['input'])
			response = responseBuilder("INPUT_SUCCESS", request)
			return publishResponse(response)

		elif payload['input'].upper() in INPUT3:
			printAction(device, name + ": " + payload['input'])
			response = responseBuilder("INPUT_SUCCESS", request)
			return publishResponse(response)

		elif payload['input'].upper() in INPUT4:
			printAction(device, name + ": " + payload['input'])
			response = responseBuilder("INPUT_SUCCESS", request)
			return publishResponse(response)

	print color.HEADER + json.dumps(response) + color.ENDC
	return publishResponse(response)

if __name__ == "__main__":
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logging.basicConfig(filename=logTopic, filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
	logger.setLevel(logging.INFO)

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
	client.subscribe(topic, 1, callbackHandler)
	client.subscribe(logTopic,1,callbackHandler)
	clearScreen()
	clientInfo()
	time.sleep(2)

	while True:
		time.sleep(0.5)
