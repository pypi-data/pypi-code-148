from cakework import Client
import time 

client = Client("hello-world", "916208fb4657fd7f1be7e88a4ddfce99e0a9e97c6864daefbe77f5e3fdfb1b0e", local=True)

run_id = client.run(project="hello-world", task="say-hello",params={"name": "jessie"}, compute={"cpu":1, "memory": 256})
print(run_id)
status = client.get_run_status(run_id)
while status == 'PENDING' or status == 'IN_PROGRESS':
    time.sleep(1)
    print("got a status")
    print(status)

    status = client.get_run_status(run_id)
if status == 'SUCCEEDED':
    result = client.get_run_result(run_id)
    print(result)
else:
    print("Failed")
