'''
Created on Sep. 17, 2020

@author: shivamnautiyal
'''
import socket
import json
from json import JSONDecoder
import re
import threading
from threading import Thread
from connection_handler import clientcl

verbosity = False
header = {"Host":"a", "User-Agent":"httpc/1.0"}
thread_count = 0
in_thread_count = 0
def preprocess_command(user_input):
    split_list=user_input.split(" ")
    host=''
    param=''
    usage= False
    header=''
    if('get' in split_list):
        url=''
        filename=''
        local_param=''
        if("-o"in split_list):
            filename=split_list[len(split_list)-1]
            url=split_list[len(split_list)-3]
        else:
            url=split_list[len(split_list)-1]
        url=url.replace("'","")
        url=url.replace('"','')
        url_split=url.split("/")
        if("http:" in url_split or "https:" in url_split):
            host=url_split[2]
            for x in range(3, len(url_split)):
                param = param+"/"+url_split[x]
            if(len(url_split)==3):
                param ='/'
        else:
            host=url_split[0]
            #param = '/'
            for x in range(1, len(url_split)):
                param = param+"/"+url_split[x]
            if(len(url_split)==1):
                param ='/'
        if('-v' in split_list):
            usage = True
        else:
            usage = False
        if('-h' in split_list):
            head = user_input.replace("httpc","")
            head = head.replace("-v", "")
            head = head.replace("get", "")
            if "localhost" not in head:
                head = head.split("'http")
            else:
                head = head.split("'localhost")
            header_list=head[0].split("-h")
            del header_list[0]
            for x in header_list:
                temp_list=x.split(":")
                if(len(temp_list)<2):
                    break;
                header=header+temp_list[0].lstrip()+":"+temp_list[1]+'\r\n'
            #header_list = usage.split("-h")
            #print(header_list)
            #http.GET(host, param,usage)
            #httpc get -v -h "Accept: application/json" -h "Content-Type: application/json" 'http://httpbin.org/get?course=networking&assignment=1'
        if "localhost" in host:
            local_param = split_list[2]
        data={}
        data["method"] = 'get'
        data["host"] = host
        data["param"]= param
        data["usage"] = usage
        data["header"] = header
        data["filename"]= filename
        data["local_param"] = local_param
        return data
    elif('post' in split_list):
        url=''
        filename=''
        local_param=''
        overwrite = False
        if("-o"in split_list):
            filename=split_list[len(split_list)-1]
            url=split_list[len(split_list)-3]
        else:
            url=split_list[len(split_list)-1]
        url=url.replace("'","")
        url=url.replace('"','')
        url_split=url.split("/")
        if("http:" in url_split):
            host=url_split[2]
            for x in range(3, len(url_split)):
                param = param+"/"+url_split[x]
            if(len(url_split)==3):
                param ='/'
        else:
            host=url_split[0]
            #param = '/'
            for x in range(1, len(url_split)):
                param = param+"/"+url_split[x]
            if(len(url_split)==1):
                param ='/'
        if('-v' in split_list):
            usage = True
        else:
            usage = False
        if('-h' in split_list):
            head = user_input.replace("httpc","")
            head = head.replace("-v", "")
            head = head.replace("overwrite=true","")
            head = head.replace("overwrite=false","")
            head = head.replace("post", "")
            head = head.split("--d", 1)[0]
            head = head.split("--f", 1)[0]
            header_list=head.split("-h")
            del header_list[0]
            for x in header_list:
                temp_list=x.split(":")
                if(len(temp_list)<2):
                    break;
                header=header+temp_list[0].lstrip()+":"+temp_list[1]+'\r\n'
            #header_list = usage.split("-h")
            #print(header_list)
            #http.GET(host, param,usage)
            #httpc get -v -h "Accept: application/json" -h "Content-Type: application/json" 'http://httpbin.org/get?course=networking&assignment=1'
        json={}
        if('--d' in split_list and '--f' in split_list):
            print("Wrong Arguments")
            init()
        elif('--d' in split_list):
            temp_json = user_input.split("--d", 1)[1]
            if "localhost" not in temp_json:
                temp_json_list = temp_json.split("'http")
            else:
                temp_json_list = temp_json.split("'localhost")
            json = temp_json_list[0].lstrip()
        elif('--f' in split_list):
            filename_new = user_input.split("--f", 1)[1]
            filename_list = filename_new.split("'http")
            if "localhost" in filename_new:
                filename_list = filename_new.split("'localhost")
            filename_new = filename_list[0].lstrip()
            filename_new = filename_new.rstrip()
            filename_new = filename_new.replace("'","")

            file = open( filename_new, "r")
            json = file.read()

        if "localhost" in host:
            local_param = split_list[2]
        if("overwrite=true" in split_list):
            overwrite = True
        data={}
        data["method"] = 'get'
        data["host"] = host
        data["param"]= param
        data["usage"] = usage
        data["header"] = header
        data["filename"]= filename
        data["json"]= json
        data["local_param"] = local_param
        data["overwrite"] = overwrite
        return data

def thread_reduce():
    global thread_count
    thread_count = thread_count-1


def multithread():
    global thread_count
    global in_thread_count
    in_thread_count = 1
    thread_count = 0
    getthreads=2
    getthreadlist=[]
    ports =[]
    ports.clear()
    for a in range(0,getthreads):
        temp=input("Enter your commands: ")
        getthreadlist.append(temp)
        temp_port=int(input("Enter your clients port: "))
        ports.append(temp_port)
    i = 0
    for a in getthreadlist:
        split_list=a.split(" ")
        # Thread(target=run_client, args=(host, port,a)).start()
        if('get' in split_list):
            data = preprocess_command(a)
            thread_count = thread_count+1
            Thread(target=GET, args=(data["host"],data["param"],data["usage"],data["header"],data["filename"],data["local_param"],ports[i])).start()


        elif('post' in split_list):
            thread_count = thread_count+1
            data = preprocess_command(a)
            Thread(target=POST, args=(data["host"],data["param"],data["usage"],data["header"],data["filename"],data["json"],data["local_param"],data["overwrite"],ports[i])).start()
        i = i+1

    while thread_count > 0:
      lol=0
    in_thread_count = 0

def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
def extract_html_objects(a):
    match = a.find('<', 0)
    a[match:]
def GET(host,param,usage,header,filename,local_param,user_port):
    hostfinal = host
    port = 80
    global in_thread_count
    if "localhost" in host:
        url_split=host.split(":")
        hostfinal = url_split[0]
        port = int(url_split[1])
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((hostfinal,port))
        except socket.gaierror:
            print ("Address-related error connecting to server:")
            init()
        except socket.error:
            print ("Connection error:")
            init()
    #inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n\r\n" % (param,host,"Accept: application/json"+"\r\n"+ "Content-Type: application/json")
    header=header.replace('"','')
    header=header.lstrip()
    obj=clientcl()
    inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n" % (param,hostfinal,header)
    if "localhost" in host:
        header = header.replace("\r\n","-h ")
        header = header[:-4]
        inputString = "GET "+local_param+" "+hostfinal+":"+str(port)+param+" -h "+header
        #s.sendall(inputString.encode("utf-8"))
        #inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n" % (param,host,header)
        obj.bind_port(user_port)
        reply=obj.client(inputString, 'localhost', 3000, 'localhost', port)
        print(reply)
        print("")
        thread_reduce()
        del obj
        if in_thread_count == 0:
            init()
        else:
            return 0

def POST(host,param,usage,header,filename,json_data,local_param,overwrite,user_port):
    hostfinal = host
    port = 80
    global in_thread_count
    obj=clientcl()
    if "localhost" in host:
        url_split=host.split(":")
        hostfinal = url_split[0]
        port = int(url_split[1])
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((hostfinal,port))
        except socket.gaierror:
            print ("Address-related error connecting to server:")
            init()
        except socket.error:
            print ("Connection error:")
            init()
    #inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n\r\n" % (param,host,"Accept: application/json"+"\r\n"+ "Content-Type: application/json")
    header=header.replace('"','')
    header=header.lstrip()
    json_data= json_data.replace("'","")
    header = header+"Content-Length: "+str(len(json_data))+'\r\n'
    inputString="POST %s HTTP/1.0\r\nHost: %s\r\n%s\r\n%s"%(param,host,header,json_data)
    #inputString = "POST /auth HTTP/1.1\r\nHost: %s\r\n%s\r\n\r\n%s" % (param,host,header,json)

    #inputString = "GET %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n" % (param,host,header)
    if "localhost" in host:
        header = header.replace("\r\n","-h ")
        header = header[:-4]
        if overwrite == True:
            inputString = "POST "+local_param+" "+hostfinal+":"+str(port)+param+" overwrite=true -d "+json_data+" -h "+ header
        else:
            inputString = "POST "+local_param+" "+hostfinal+":"+str(port)+param+" overwrite=false -d "+json_data+" -h "+ header
        # s.sendall(inputString.encode("utf-8"))
        obj.bind_port(user_port)
        reply=obj.client(inputString, 'localhost', 3000, 'localhost', port)
        print(reply)
        print("")
        thread_reduce()
        del obj
        if in_thread_count == 0:
            init()
        else:
            return 0
    
def init():
    global thread_count
    thread_count = 0
    user_input=input()
    if(user_input == 'q'):
        exit()
    if(user_input == 'm'):
        multithread()
    split_list=user_input.split(" ")
    host=''
    param=''
    usage= False
    header=''
    #host_list=[]
    if('help' in split_list):
        if('get' in split_list):
            print("usage: httpc get [-v] [-h key:value] URL")
            print("Get executes a HTTP GET request for a given URL.")
            print("\t -v \t Prints the detail of the response such as protocol, status, and headers.")
            print("\t -h \t key:value Associates headers to HTTP Request with the format 'key:value'.\n")
            init()
        elif('post' in split_list):
            print("usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL")
            print("Post executes a HTTP POST request for a given URL with inline data or from file.")
            print("\t -v \t Prints the detail of the response such as protocol, status, and headers.")
            print("\t -h \t key:value Associates headers to HTTP Request with the format 'key:value'.")
            print("\t -d \t string Associates an inline data to the body HTTP POST request.")
            print("\t -f \t file Associates the content of a file to the body HTTP POST request.")
            print("Either [-d] or [-f] can be used but not both. \n")
            init()
        else:
            print("httpc is a curl-like application but supports HTTP protocol only.")
            print("Usage:")
            print("\t httpc command [arguments]")
            print("The commands are:")
            print("\t get \texecutes a HTTP GET request and prints the response.")
            print("\t post \texecutes a HTTP POST request and prints the response.")
            print("\t help \tprints this screen.")
            print("Use \"httpc help [command]\" for more information about a command. \n")
            init()
    elif('get' in split_list):
        print("Please Porvide Clients Port")
        user_port=int(input())
        data = preprocess_command(user_input)
        GET(data["host"],data["param"],data["usage"],data["header"],data["filename"],data["local_param"],user_port)
        init()
    elif('post' in split_list):
        print("Please Porvide Clients Port")
        user_port=int(input())
        data = preprocess_command(user_input)
        POST(data["host"],data["param"],data["usage"],data["header"],data["filename"],data["json"],data["local_param"],data["overwrite"],user_port)
        init()
init()
