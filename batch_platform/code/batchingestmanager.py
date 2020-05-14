from mysimbdp import fetchdata
import clientbatchingestapp_1
import clientbatchingestapp_2

def batchingestmanager(folder_dir=None,customer_ID=None):
    '''
    This method implements the mysimbdp-batchingestmanager
    '''
    #customer files to be ingested into the final sink
    print("MYSIMBDP BATCHINGESTMANAGER v0.1\n")
    if folder_dir == None and customer_ID == None:
        folder_dir = input('Give data directory: ')
        customer_ID = input('Give your customer ID (type A or B):')

    files = fetchdata(folder_dir)

    if customer_ID == 'A':
        clientbatchingestapp_1.ingest(files)
    elif customer_ID == 'B':
        clientbatchingestapp_2.ingest(files)
    else:
        print("No customer found with this ID")

if __name__ == '__main__':
    batchingestmanager()
