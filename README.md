# lightbulb-lan-esp32
WS2812 / LAN / ESP-WROOM-32 / Micropython


Thread Flow pseudo-diagram:

:: Boot thread
  1. `machine.Timer.init` for 300s (5mins)
  2. `AP.active(True)`
  - If `ap.isconnected`:
      + Run server
      + `machine.Timer.deinit`
  - If no STA
      + Timer triggers
      + AP and server disabled

:: App thread
  1. Check if parent node exists
  - If `node_parent`:
    + Send state notification
  - else:
    + Don't send notification
  2. `machine.lightsleep([3000ms])`
