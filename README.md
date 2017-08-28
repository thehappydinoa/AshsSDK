# Alexa Smart Home Skill using Smart Home Payload V3
An Alexa skill made for controlling any network controlled devices using payload V3 (Entertainment Devices)

## Requirements 
* A [AWS account](https://aws.amazon.com/)
* A [Amazon Developer account](https://developer.amazon.com)
* An Alexa-enabled device such as [Amazon Echo](https://www.amazon.com/dp/B00X4WHP5E/) or [Amazon Echo Dot](https://www.amazon.com/dp/B01DFKC2SO/)
* A Bridge running [Python 2.7](https://www.python.org/downloads/) and [Pip](/installing-pip.md) (I used a [Raspberry Pi](https://www.raspberrypi.org/products/), but another computer running linux will work too)
* I recomend using [screen](/installing-screen.md) to run python headless

## How to
1. AWS IAM Setup

 	### Create an [AWS Role in IAM](https://console.aws.amazon.com/iam/homet) called mqtt_handler with access to Lambda.
	![Create Role](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Create+new+Role+Edit.png "AWS Create Role")
	![Select Role Type](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Select+Role+Type+Edit.png "AWS Select Role Type")
	![Attach Policy](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Attach+Policy.png "AWS Attach Policy")
	![Set Role NAme](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Set+role+name.png "AWS Set Role Name")
     
2. AWS IOT Device Setup

	1. Lambda Virtual `device` 
		### Create an [AWS IOT Thing](https://console.aws.amazon.com/iotv2/home#/thinghub)
		![Create Thing](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing.png "AWS Create IOT Thing")
		![Create Thing Lambda](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_lambda.png "Lambda")
		![Create Thing Lambda](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_lambda_pt2.png)
		![Create Certificates Lambda](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_lambda_certificates.png)
		![Certificates Created](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_lambda_certificates_created.png)
		#### Download these as `lambda.cert.pem, lambda.public.key, lambda.private.key`
	2. Client Device
		### Create an [AWS IOT Thing](https://console.aws.amazon.com/iotv2/home#/thinghub)
		![Create Thing](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_client.png "AWS Create IOT Thing")
		![Create Thing Client](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_client_pt2.png "Client")
		![Create Thing Client](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_client_pt3.png "Client")
		![Create Certificates](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_client_certificates.png)
		![Certificates Created](https://s3.amazonaws.com/alexa-smart-home-skill/AWS+IoT+Create+New+Thing_lambda_certificates_created.png "Client")
		#### Download these as `client.cert.pem, client.public.key, client.private.key`
	3. Get MQTT Server Hostname
		* Go to [Settings](https://console.aws.amazon.com/iotv2/home#/settings)
		* Note down the Endpoint
		* It should look like: xxxxxxxxxxxxxx.iot.us-east-1.amazonaws.com
	
	#### Note: Make sure to download your public and private keys to some place secure. You will not be able to re-download these.
	
3. Bridge Set Up

	### Clone this repo and install dependencies
	```bash
	git clone https://github.com/thehappydinoa/alexa-smart-home-skill
	cd alexa-smart-home-skill/
	pip install -r client/requirements.txt
	```
	
	#### Copy `lambda.cert.pem` and `lambda.private.key` in to the folder named `lambda`
	
	#### Copy `client.cert.pem` and `client.private.key` in to the folder named `client`
	
	```bash
	cd ..
	python fileGenerator.py
	```
4. Upload `mqtt-handler.zip` to lambda

	### Create function
	#### Click Create New Function
	![Create New Function](https://s3.amazonaws.com/alexa-smart-home-skill/Lambda+Management+Console+Create+Function.png "Create Function")
	#### Create from Scratch
	![Create from scratch](https://s3.amazonaws.com/alexa-smart-home-skill/Lambda+Management+Console+From+Scratch.png "Create from scratch")
	#### Skip adding a trigger until after the you create an Alexa Skill
	#### Configure Function
	* Name the function `Alexa-MQTT-Skill`
	* the runtime to `Python 2.7`
	* Set Code entry type to `Upload a .ZIP file`
	* Set Handler to `mqtt-handler.lambda_handler`
	* Set Role to Existing Role `mqtt_handler`
	
	![Function Confirguration](https://s3.amazonaws.com/alexa-smart-home-skill/Lambda+Management+Console+Function+Config.png "Function Confirguration")
	### Copy ARN
	Should look like `arn:aws:lambda:us-east-1:xxxxxxxxxxx:function:Alexa-MQTT-Skill`
	
	![Get ARN](https://s3.amazonaws.com/alexa-smart-home-skill/Lambda+Management+Console+Get+ARN.png "Get ARN")

5. Create Alexa Skill
	
	### Create or login to an [Amazon Developer account](https://developer.amazon.com/edw/home.html#/).  
	In the Alexa Developer Console Select `Alexa Skills Kit`
	
	[Create an Alexa Skill](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function) 
	* Set Skill Type to `Smart Home Skill API`
	* Set Name to `Alexa-MQTT-Skill`
	* Set Payload Version to `v3 (audio-visual devices)`
	
	![Skill Config](https://s3.amazonaws.com/alexa-smart-home-skill/Alexa+Skill+Info.png "Skill Config")
	#### Copy the `ID:` 
	Should look like `amzn1.ask.skill.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
	
	![Copy ID](https://s3.amazonaws.com/alexa-smart-home-skill/Alexa+Skill+ID.png "Copy ID")
	#### Go Back to the Lambda Dashboard
	#### Add `Alexa Smart Home` as the Lambda Function Trigger
	Paste in the ID
	![Alexa Smart Home as Lambda Trigger](https://s3.amazonaws.com/alexa-smart-home-skill/Set+Trigger+Lambda+Function.png "Alexa Smart Home as Lambda Trigger")

## You Now should be able to interact with your Skill 
Try saying `Alexa, Turn on Device1`

## Resources
* [aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python)
* [AQUOS-Remote-Python](https://github.com/thehappydinoa/AQUOS-Remote-Python)
* [Alexa Smart Home Skill Kit](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/overviews/understanding-the-smart-home-skill-api)
* [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
