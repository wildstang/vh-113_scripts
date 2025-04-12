from time import sleep

from vh113.status import get_status
from vh113.config import send_config, DEFAULT_CONFIG


while True:
    res = send_config(DEFAULT_CONFIG, '192.168.69.1')
    print(res)
    sleep(5)

    if res['success']:
        print('SUCCESS')
        break
