# Alexa Smart Home Skill using Smart Home Payload V3
An Alexa skill made for controlling any network controlled devices using payload V3 (Entertainment Devices)

## Requirements 
* A [AWS account](https://aws.amazon.com/)
* A [Amazon Developer account](https://developer.amazon.com)
* An Alexa-enabled device such as [Amazon Echo](https://www.amazon.com/dp/B00X4WHP5E/) or [Amazon Echo Dot](https://www.amazon.com/dp/B01DFKC2SO/)
* A Bridge (I used a [Raspberry Pi](https://www.raspberrypi.org/products/), but another computer running linux will work too)

## How to
 1. Create an AWS Role in IAM with access to Lambda, CloudWatch Logs and DynamoDB.
        ![create_role_1](https://cloud.githubusercontent.com/assets/7671574/17451098/09f64f40-5b19-11e6-82ee-b82c98387052.png "AWS Create Role Screenshot 1")
        ![create_role_2](https://cloud.githubusercontent.com/assets/7671574/17451100/0c3ef928-5b19-11e6-9aca-8cd353106396.png "AWS Create Role Screenshot 2")
     
2. IOT Device Setup
	   ![AWS Create IOT Device]( "AWS Create IOT Device")
	   
3. Bridge Set Up	   

	   ```bash
	   git clone https://github.com/thehappydinoa/alexa-smart-home-skill
	   cd alexa-smart-home-skill
	   ```
	   Copy in the .cert.pem and .private.key files made in the last step
	   ```bash
	   nano mqtt-handler.py
	   ```
	   
	   Edit the following variables `host certificatePath privateKeyPath`

4. Create an AWS Lambda function named mqtt-handler being sure to select the role created above, configuring "Alexa Skills Kit" as the "Trigger" and use the zip file created above as the source.
        ![alt text](https://s3.amazonaws.com/lantern-public-assets/audio-player-assets/aws-lambda-role.PNG "AWS Lambda Role")
        ![alt text](https://s3.amazonaws.com/lantern-public-assets/audio-player-assets/aws-lambda-ask-trigger.PNG "AWS Lambda Trigger")

## Resources
* [aws-iot-device-sdk-python](https://github.com/aws/aws-iot-device-sdk-python)
* [AQUOS-Remote-Python](https://github.com/thehappydinoa/AQUOS-Remote-Python)
* [Alexa Smart Home Skill Kit](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/overviews/understanding-the-smart-home-skill-api)
* [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
