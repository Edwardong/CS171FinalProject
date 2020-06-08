import prettytable
import hashlib, pickle
def chunkstring(string, length):
    return [string[0+i:length+i] for i in range(0, len(string), length)]

if __name__ == '__main__':
    # a_str = '11cc8b78282538c927185f662af278f0c37e29cc61118a920a92d87c7ae761bd'
    # new_list = chunkstring(a_str, int(64/5) + 1)
    # print(len(new_list))
    #print(prettytable.__version__)
    transactions = [1, 2, 5]
    nonce = "0"
    payload = {"T": transactions,
               "N": nonce}
    attempt = hashlib.sha256(pickle.dumps(payload)).hexdigest()
    print("first attempt: {}".format(attempt))
    while int(attempt[-1], 16) > 4:
        payload["N"] = hex(int(payload["N"] , 16) + 1)
        attempt = hashlib.sha256(pickle.dumps(payload)).hexdigest()
        print("New attempt: {}".format(attempt))

    print("finished. Nonce is: {}, \n hash value is: {}".format(payload["N"],attempt))
