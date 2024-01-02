# tenda
Unofficial Tenda Model N301 API

Install it using:
```s
$ pip install tenda
```

These are the function currently available.

```python
import tenda

manager = tenda.TendaManager('<ip_address>', '<your_password>')

# Get QOS
online_devices = manager.get_online_devices_with_stats()
blocked_devices = manager.get_black_list()

# Set QOS
manager.block_device('<some_mac_address>')

# Reboot 
manager.reboot()
```
