from customerstreamapp import createStreamingContext

if __name__ == "__main__":
    print('Welcome to customerstreamapp!\n')
    print('-----------------------------')
    customer = 'A'
    #customer = str(sys.argv[0])

    if customer == 'B':
        list_of_topics = ['0001', '0002', '0003', '0004']
        window_size = 43200000
    elif customer == 'A':
        list_of_topics = ['1084', '1085', '1086']
        window_size = 86400000

    numPartitions = 5
    stream = createStreamingContext(list_of_topics, window_size, numPartitions)
