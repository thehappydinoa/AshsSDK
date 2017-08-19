# Alexa Smart Home Skill using Smart Home Payload V3
An Alexa skill made for controlling any network controlled devices using payload V3 (Entertainment Devices)

## Requirements 
* A [AWS account](https://aws.amazon.com/)
* A [Amazon Developer account](https://developer.amazon.com)
* An Alexa-enabled device such as [Amazon Echo](https://www.amazon.com/dp/B00X4WHP5E/) or [Amazon Echo Dot](https://www.amazon.com/dp/B01DFKC2SO/)
* A Bridge (I used a [Raspberry Pi](https://www.raspberrypi.org/products/), but another computer running linux will work too)

## How to
 1. AWS IAM Setup
 	
 	Create an [AWS Role in IAM](https://console.aws.amazon.com/iam/homet) called mqtt_handler with access to Lambda.
        ![Create Role](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Create+new+Role+Edit.png "AWS Create Role")
        ![Select Role Type](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Select+Role+Type+Edit.png "AWS Select Role Type")
	![Attach Policy](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Attach+Policy.png "AWS Attach Policy")
	![Set Role NAme](https://s3.amazonaws.com/alexa-smart-home-skill/IAM+Management+Console+Set+role+name.png "AWS Set Role Name")
     
2. AWS IOT Device Setup

	1. Lambda Virtual `device` 
	
	
	2. Client Device
	
	Make sure to download your public and private keys to some place secure. You will not be able to re-download these.
	
3. Bridge Set Up

	Clone this repo and install dependencies
	```bash
	git clone https://github.com/thehappydinoa/alexa-smart-home-skill
	cd alexa-smart-home-skill/bridge
	pip install -r requirements.txt
	```

	Copy in the .cert.pem and .private.key files made in step 2

	Edit `host` in `lambda-client.py` to match your IOT MQTT Server made in step 2
	```bash
	nano lambda-handler.py
	```

	Zip Folder and upload to AWS
	```bash
	zip -r ../lambda-handler.zip *
	```

4. Create Alexa Skill
	Create or login to an [Amazon Developer account](https://developer.amazon.com).  In the Developer Console:

	[Create an Smart Home Payload V3 Alexa Skill](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function) named AQUOS.
      ![alt text](https://s3.amazonaws.com/lantern-public-assets/audio-player-assets/prod-skill-info.png "Developer Portal Skill Information")
	Copy the Lambda ARN from above.
      ![alt text](https://s3.amazonaws.com/lantern-public-assets/audio-player-assets/prod-configuration.png "Developer Portal Configuration")

5. Configuring "Alexa Smart Home" as the "Trigger"
	Go to https://console.aws.amazon.com/lambda/home
	Select mqtt-handler function
	Add Trigger "Alexa Smart Home with your Alexa Application Id
        ![alt text](https://s3.amazonaws.com/lantern-public-assets/audio-player-assets/aws-lambda-ask-trigger.PNG "AWS Lambda Trigger")

## Resources
* [aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python)
* [AQUOS-Remote-Python](https://github.com/thehappydinoa/AQUOS-Remote-Python)
* [Alexa Smart Home Skill Kit](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/overviews/understanding-the-smart-home-skill-api)
* [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
