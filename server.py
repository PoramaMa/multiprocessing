import threading
from multiprocessing import Process
from flask import Flask, request, jsonify
import queue
import time
import math
import random
app = Flask(__name__)
threads = []
process = []
tasks = {}
data_task = {}
check_open = False

def startTest():
    global threads
    for _ in range(10):  # Creating 10 threads
        t = threading.Thread(target=heavy_computation)
        threads.append(t)

    # Starting threads
    for item in threads:
        item.start()

    print("threads starting ::: " , threads)

    # Waiting for all threads to complete
    for item in threads:
        item.join()
        
    print("threads complete ::: " , threads)


# def startTest():
#     global process
#     for _ in range(10):  # Creating 10 processes
#         p = Process(target=heavy_computation)
#         process.append(p)

#     # Starting processes
#     for item in process:
#         item.start()

#     print("process starting ::: ", process)

#     # Waiting for all processes to complete
#     for item in process:
#         item.join()

#     print("process complete ::: ", process)


def heavy_computation():
    print("pass: heavy_computation")
    global check_open
    result = 0
    while True:
        result += 1
        print(f"Result: {result}")
        print(f"check_open: {check_open}")
        if result == 20:
            check_open = True
        time.sleep(1)
    # ======================================
    # while True:
    #     # for _ in range(1):
    #     for i in range(10**8):  # Performing a very large number of computations
    #         result += i
    #     print(f"Result: {result}")
    #     time.sleep(1)
    #     # if result > 5:
    #     #     break


def runTest():
    p = Process(target=heavy_computation)
    process.append(p)

    # Starting processes
    for item in process:
        item.start()

    print("process starting ::: ", process)

    # Waiting for all processes to complete
    # for item in process:
    #     item.join()
    
    # print("process complete ::: ", process)

    # เปลี่ยนลิสต์คำศัพท์ตามที่คุณต้องการ
    word_list = ["แมว", "หมา", "นก", "ช้าง", "ลิง"]
    random_word = random.choice(word_list)

    tasks[random_word] = {'process': p, 'queue': queue.Queue()}
    

@app.route('/getThreads')
def getThreads():
    resp = {'threads': threads}
    return resp


@app.route('/getProcess')
def getProcess():
    resp = {'process': process}
    return resp


@app.route('/test')
def test():
    return jsonify("pass")


@app.route('/runtest')
def runtest():
    runTest()
    return jsonify("pass")


@app.route('/getTaskById/<taskname>')
def taskById(taskname):
    global tasks
    resp = {'status': 'task not found'}
    data = 'no data'
    for task_name in tasks:
        if task_name.lower() == taskname.lower():
            if tasks[task_name]['process'].is_alive():
                # data = data_task[task_name]
                resp = {'task': task_name,
                        'status runn': 'running', 'data': data}
            else:
                resp = {'task': task_name,
                        'status': 'finished', 'data': data}
    return jsonify(resp)


@app.route('/getTaskAll')
def get_tasks():
    global tasks
    task_list = []
    for task_name in tasks:
        task = tasks[task_name]["process"]
        if task.is_alive():
            status = "running"
        else:
            status = "finished"
        task_list.append(
            {'task_id': task.ident, 'task': task_name, 'status': status})
    return jsonify(task_list)


@app.route('/deleteTaskById/<taskname>', methods=["DELETE"])
def delete_task_by_id(taskname):
    global tasks
    for task_name in tasks:
        if task_name.lower() == taskname.lower():
            if tasks[task_name]['process'].is_alive():
                tasks[task_name]['queue'].put({'data': 'stop'})
                del tasks[task_name]
                del data_task[task_name]
                return jsonify({'status': 'stopped'})
            else:
                del tasks[task_name]
                del data_task[task_name]
                return jsonify({'status': 'deleted'})
    app.logger.info('start delete_task_by_id')
    return jsonify({'status': 'not found'})


if __name__ == '__main__':

    # t = threading.Thread(target=startTest)
    # t.start()

    # p = Process(target=startTest)
    # p.start()

    app.run(host='0.0.0.0', port=2222)
    app.run(debug=False)
