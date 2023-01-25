from gravity_auto_exit.main import AutoExit

# left, upper, right, lower
# 2592*1944

if __name__ == '__main__':
    def engine_callback(*args, **kwargs):
        print('MAIN')

    def take_shot(inst):
        photo = inst.cam.take_shot()

    inst = AutoExit(  #
       #'http://172.16.6.173',
        'http://127.0.0.1',
        'admin',
        'Assa+123',
        debug=True,
        # 2592*1944
        #resize_photo=(800, 400, 1700, 1300),
        cam_port=83,
        neurocore_login="admin",
        neurocore_password="admin",
        engine_callback=engine_callback,
    )
    # inst.set_post_request_url('http://127.0.0.1:8080/start_auto_exit')
    result = inst.try_recognise_plate()
    if not 'error' in result:
        print(result['number'])
    else:
        print(result['error'])
    #print(result['result'])
    inst.start()
