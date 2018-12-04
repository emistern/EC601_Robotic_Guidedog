## Monitor modules for robotic guide dog

* the image_server module is used by wrapper to publish image to the internet
* the image_client module is a simple receiver you can run to receive and display images published by the image_server

* dependency: a python library to send and receive data through mqtt protocol over internet

    pip install paho-mqtt
