# coding=UTF-8

# pip install modbus_tk
import sys


def read_modbus(ip, address, length):
    import modbus_tk
    import modbus_tk.defines as cst
    import modbus_tk.modbus_tcp as modbus_tcp

    master = modbus_tcp.TcpMaster(host=ip, port=502, timeout_in_sec=5.0)
    try:
        print master.execute(3, cst.READ_HOLDING_REGISTERS, address, length)
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())
    finally:
        master.close()
       
read_modbus("192.168.2.93", 40043, 2)
