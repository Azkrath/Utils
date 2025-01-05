#!/bin/python
import socket, os, sys, time, requests

def main(sone, stwo):
    num = 0
    ip = sone
    port = stwo
    while True:
        num, port = connect(ip, port, num)
        time.sleep(1)

def connect(ip, port, num):
    print(str(port) + " : " + str(num))
    if port == 9765:
        print("finished")
        sys.exit()
    try:
        response = requests.get("http://"+ip+":"+str(port))
        time.sleep(1)
        if response.status_code == 200:
            print(response.text)
            r = response.text
            op = r.split(' ')[0]
            if op == 'add':
                num += float(r.split(' ')[1])
            elif op == 'minus':
                num -= float(r.split(' ')[1])
            elif op == 'multiply':
                num *= float(r.split(' ')[1])
            elif op == 'divide':
                num /= float(r.split(' ')[1])
            elif op == 'STOP':
                print("finished")
                sys.exit()
            port = int(r.split(' ')[2])
        return num, port
    except KeyboardInterrupt:
        sys.exit()
    except:
        return num, port

# Main
if __name__ == '__main__':
    # 8743
    print(sys.argv[1])
    print(sys.argv[2])
    main(sys.argv[1], sys.argv[2])
