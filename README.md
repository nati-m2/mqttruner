# MQTT Runner

## Overview
MQTT Runner is a tool designed to receive messages via MQTT and execute commands on a computer based on the received messages. It supports various actions such as executing shell commands, opening URLs, simulating keyboard presses, and mouse clicks.

## Features
- Execute shell commands received as MQTT messages.
- Open URLs in the default browser.
- Simulate keyboard key presses and mouse clicks.
- Filter ignored messages based on configuration.
- Error logging for debugging purposes.

## Requirements
- Python 3.x
- Required Python libraries:
  - `paho-mqtt`
  - `pyautogui`
  - `multiprocessing`
  - `subprocess`
  - `json`
- Supported operating systems:
  - Windows
  - macOS
  - Linux

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nati-m2/mqttruner.git
   cd mqttruner
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the configuration files (`mqttrunerConfig.json` and `mapKeys.json`) are properly set up.

## Configuration
### `mqttrunerConfig.json`
The configuration file should include:
- `addr`: MQTT broker address.
- `port`: MQTT broker port.
- `username`: MQTT username.
- `password`: MQTT password.
- `keepalive`: MQTT keepalive interval.
- `topics`: A list of topics to subscribe to.
- `rTopic`: The main topic index.
- `debug`: Enable or disable error logging.
- `ignoreMsg`: A list of messages to ignore.
- `loopPressDelay`: Delay for repeated key presses (in milliseconds).

### `mapKeys.json`
A mapping of keys for specific actions, used to translate payloads to keyboard keys.

## Usage
1. Start the MQTT Runner script:
   ```bash
   python mqttruner.py
   ```
2. Publish MQTT messages to the subscribed topics to trigger actions.

### Supported Actions
- **Execute a shell command:**
  ```json
  {
    "type": "exec",
    "cmd": "<command>"
  }
  ```
- **Open a URL:**
  ```json
  {
    "type": "url",
    "cmd": "<url>"
  }
  ```
- **Simulate a key press:**
  ```json
  {
    "type": "press",
    "cmd": "<key>"
  }
  ```
- **Simulate a mouse click:**
  ```json
  {
    "type": "click",
    "cmd": [<x>, <y>]
  }
  ```
- **Disconnect from MQTT broker:**
  ```json
  {
    "type": "disconnect"
  }
  ```

## Logging
Error logs are written to `log.txt` if debugging is enabled in the configuration file.

## Contributing
Feel free to fork the repository and submit pull requests. Issues and feature requests are welcome.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
Use this tool responsibly. Ensure that the MQTT broker is secure and properly configured to prevent unauthorized access.

---

For more information, visit the [GitHub repository](https://github.com/nati-m2/mqttruner).

