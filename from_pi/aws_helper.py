from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os

# Constants for AWS IoT configuration
BASE_PATH = '/home/nero/Desktop/object_detection/aws_files'
ROOT_CA_PATH = os.path.join(BASE_PATH,'rootCA.pem')
PRIVATE_KEY_PATH = os.path.join(BASE_PATH,'my-private.pem.key')
CERTIFICATE_PATH = os.path.join(BASE_PATH,'my-certificate.pem.crt')
ENDPOINT_FILE_PATH = os.path.join(BASE_PATH,'endpoint.txt')


def load_endpoint():
    try:
        with open(ENDPOINT_FILE_PATH, "r") as file:
            endpoint = file.read().strip()
        return endpoint
    except Exception as e:
        print(f"Error reading endpoint file: {str(e)}")
        return None


def aws_setup():
    myMQTTClient = AWSIoTMQTTClient("shonku")
    endpoint = load_endpoint()
    if not endpoint:
        return None

    myMQTTClient.configureEndpoint(endpoint, 8883)
    myMQTTClient.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

    return myMQTTClient


def aws_connect(mqttClient):
    try:
        mqttClient.connect()
        print("Connected to AWS IoT Core")
        return True
    except Exception as e:
        print(f"Unable to connect: {str(e)}")
        return False


def send_data(mqttClient, topic, message):
    if aws_connect(mqttClient):
        mqttClient.publish(topic, message, 0)
        print(f"Published: {message} to {topic}")


def custom_callback(client, userdata, message):
    print("Received a new message:")
    print(f"Topic: {message.topic}")
    print(f"Message: {message.payload}")
    print("--------")


def receive_data(mqttClient, topic):
    if aws_connect(mqttClient):
        mqttClient.subscribe(topic, 1, custom_callback)


if __name__ == "__main__":
    
    client = aws_setup()
    topic = "my-topic"
    if client:
        # Define your AWS Itopic = "my-topic"
        receive_data(client, topic)

    while True:
        user_input = input("Type 'send' to send data or 'exit' to exit: ")
        if user_input == "send":
            message = input("Enter the message to send: ")
            send_data(client, topic, message)
        elif user_input == "exit":
            break
