# import psutil
#
# print(psutil.cpu_percent(interval=1, percpu=True))
# print(psutil.cpu_stats())
# print(psutil.virtual_memory().percent)
# print(psutil.swap_memory().percent)
# print(psutil.disk_io_counters())

import psutil
import logging
import time

logging.basicConfig(filename='system_monitor.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

start_time = time.time()
end_time = start_time + 120  # 120 seconds = 2 minutes

while time.time() < end_time:
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent

    load_avg = psutil.getloadavg()

    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv
    time.sleep(1)
    net_io_counters = psutil.net_io_counters()
    new_bytes_sent = net_io_counters.bytes_sent
    new_bytes_recv = net_io_counters.bytes_recv
    bytes_sent_rate = (new_bytes_sent - bytes_sent) / 1000000
    bytes_recv_rate = (new_bytes_recv - bytes_recv) / 1000000

    logging.info(f'CPU utilization: {cpu_percent}%')
    logging.info(f'System load average - 1 minute: {load_avg[0]}, 5 minutes: {load_avg[1]}, 15 minutes: {load_avg[2]}')
    logging.info(f'Memory utilization: {mem_percent}%')
    logging.info(f'Network bandwidth utilization rate - Sent: {bytes_sent_rate} Mbps, Received: {bytes_recv_rate} Mbps')


logging.info('Program finished.')