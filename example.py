from tendan301api import TendaManager


manager = TendaManager('<ip_address>', '<your_password>')

# Get QOS
online_devices = manager.get_online_devices_with_stats()
blocked_devices = manager.get_black_list()

# Set QOS
manager.block_device('<some_mac_address>')
manager.limit_device('<some_mac_address>', '<download_speed>', '<upload_speed>')

# Get current wifi_settings
manager.get_wifi_settings()

# Reboot 
manager.reboot()