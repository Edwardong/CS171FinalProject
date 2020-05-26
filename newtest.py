def chunkstring(string, length):
    return [string[0+i:length+i] for i in range(0, len(string), length)]

if __name__ == '__main__':
    a_str = '11cc8b78282538c927185f662af278f0c37e29cc61118a920a92d87c7ae761bd'
    new_list = chunkstring(a_str, int(64/5) + 1)
    print(len(new_list))