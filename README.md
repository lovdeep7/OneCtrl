### Inspiration
We always keep on losing remotes and cannot find the right one at the right time. We thought to eliminate this problem completely by creating a universal smart remote that can control all devices

### What it does
It identifies the device it is being pointed at changes the controls on the display accordingly. It adapts to user's preferences and style.

### How we built it
We scraped the internet for thousands of images of devices and annotated these devices. Then we trained the neural net on an AWS server to get our weight files. Created a flask server that handles the requests and processing. A raspberry pi (client) is our remote with the camera module that communicates with the flask server.

### Challenges we ran into
Emitting IR signals using a raspberry pi. It was very difficult to emit the IR rays at the desired frequency and time duration to control a device.

### Accomplishments that we're proud of
We scraped the web, annotated the images and trained a neural net in a short span of time.

### What we learned
We learned a lot about YOLO (You Only Look Once) and Darkflow. Additionally, we spent a lot of time working on the hardware that gave us a good insight into how a remote is supposed to be designed.

### What's next for OneCtrl
We plan to train it more on a wider range of devices with a larger set of images to make our net robust and accurate.