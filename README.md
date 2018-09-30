# tenda-n301-api
Unofficial Tenda Model N301 API

Install it using:
```
pip install tenda-n301-python-api
```

These are the function currently available.

```
import tendan301api

manager = tendan301api.TendaManager('<ip_address>', '<your_password>')

# Get QOS
online_devices = manager.get_online_devices()
blocked_devices = manager.get_black_list()

# Set QOS
manager.block_device('<some_mac_address>')
```
