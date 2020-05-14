from TEST_failure_IoT_sensor_1 import testSensor_1, testSensor_2

if __name__ == '__main__':
    '''
    Test streaming platform with wrong data
    '''
    ERROR_RATES = [0.01, 1, 10, 100, 1000] # different error rates
    MAX_ITER = 100 # number of messages will be sent
    for ERROR_RATE in ERROR_RATES:
        testSensor_1(ERROR_RATE, MAX_ITER)
        testSensor_2(ERROR_RATE, MAX_ITER)
