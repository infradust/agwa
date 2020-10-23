**AGLabler**

**System Diagram**
![diagram](aglabler.png)


**ToDo**
* add tests for detection
* verify on actual deployed system (current data structures were taken from AWS documentations)
* performance testing (actual rekognition response times)


**Links**
* [aws example system](https://aws.amazon.com/blogs/machine-learning/create-a-serverless-solution-for-video-frame-analysis-and-alerting/)
* [lambda with firehose](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesisfirehose.html)
* [boto3 - rekognition - detect labels](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client.detect_labels)