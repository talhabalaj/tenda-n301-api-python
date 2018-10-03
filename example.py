import tendan301api

manager = tendan301api.TendaManager("192.168.0.1", "")
print(manager.get_online_devices())
