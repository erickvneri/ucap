# uCap Simple Use Example

### Prerequisites

1. Micropython firmware from https://micropython.org/download/esp32/
1. [Esptool](https://github.com/espressif/esptool)
1. [ampy](https://github.com/scientifichackers/ampy) utility
1. Linux `screen` utility _(can be replaced by `picocom` or `minicom`)_

### Setup _(linux-based commands)_

1. _(optional)_ If your linux user is not part of the `dialout` group, you may
   need to execute the following line:

```
sudo chmod -R 777 /dev/ttyUSB0
```

2. Flash Micropython firmware:

```sh
> esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
...
> esptool.py \
> --chip esp32 \
> --port /dev/ttyUSB0 \
> --baud 460800 \
> write_flash -z 0x1000 esp32-*.bin
```

3. Copy the `uCap` source code into this project:

```
cp -r ../src/ucap .
```

4. Upload the app into the device:

```
> ampy --port /dev/ttyUSB0 put main.py
> ampy --port /dev/ttyUSB0 put app.py
> ampy --port /dev/ttyUSB0 put ucap
```

5. Open serial communication with the device

```
sudo screen /dev/ttyUSB0 115200
```

_(**Note**: You may need to tap `Ctrl-D` once the `screen` session has began)_

### Interact with the app
