import os
import time

print('Task starting..')

lambda_name = os.environ['LAMBDA_NAME']
request_id = os.environ['REQUEST_ID']
print(f"This task received a call from {lambda_name} with request ID {request_id}.")

time.sleep(5)
print('Task ended, took 5 seconds')