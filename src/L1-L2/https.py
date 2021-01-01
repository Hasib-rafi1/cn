import os
import socket
import glob
from threading import Lock
import shutil
inputt=''
while True:
    inputt=input()
    if("httpfs" not in inputt):
        print("Invalid command to run server\nEnter proper command to run the server")
        continue
    else:
        break;
inp=inputt.replace("[","")
inp1=inp.replace("]","")
port=8080
dirr=os.getcwd()
input_list=inp1.split(" ")
if '[-v]' in input_list:
    print("Debugging Messages: " +"\n \n"
        "200 OK: Successful GET Request."+"\n"
        "201 OK: Successful POST Request."+"\n"
        "400 Bad Request: A malformed request."+"\n"
        "403 Forbidden: Server has denied access to the resource."+"\n"
        "404 Not Found: Server cannot retrieve the page that was requested."+"\n"
        )
if '-p' in input_list:
    port=int(input_list[input_list.index('-p')+1])
if '-d' in input_list:
    dirr=input_list[input_list.index('-d')+1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',port)
print ('Starting up on %s port %s' % server_address)
print("Directory= ",dirr)
s.bind(server_address)
s.listen(1)
while True:
    print ('Waiting for a connection\n')
    con, c_add = s.accept()
    file_name=''
    headerr=''
    list_file=[]
    headers= ''
    with os.scandir(dirr) as listOfEntries:
        for entry in listOfEntries:
            # print all entries that are files
            if entry.is_file():
                file_name=file_name+str(entry.name) +"\n"
                list_file.append(entry.name)
    data=(con.recv(10000)).decode('UTF-8')
    #print(data)
    lock = Lock()
    lock.acquire()
    data_list=data.split(" ")
    print(data_list)
    filename=''
    if(data_list[1].count("/")==1 and len(data_list[1])!=1):
        filename=data_list[1].replace("/","")

    if(data_list[1]!=dirr)and(data_list[1]!='/'and (filename=='')):
        path_list=data_list[1].split("/")
        filename=path_list.pop(len(path_list)-1)
        path='/'.join(path_list)
        if(path!=dirr):
            con.sendall(bytes("403 Forbidden: Server has denied access to the resource.", 'UTF-8'))
            #print("403 Forbidden: Server has denied access to the resource."+"\n"")
            continue
    if filename=='':
        data_list[1]='/'
    else:
        data_list[1]="/"+filename
    header = data.split("-h")
    header = header[1:]
    header = [x.strip(' ') for x in header]
    print(header)
    for i in header:
        headers=headers+"\r\n"+i
    #print(list_file)
    if 'GET' in data:
        if "Content-Type:application/plain" in header or "Accept:txt" in header:
            headerr = "plain"
        elif "Content-Type:application/html" in header or "Accept:html" in header:
            headerr = "HTML"
        elif "Content-Type:application/json" in header or "Accept:json" in header:
            headerr = "JSON"
        elif "Content-Type:application/xml" in header or "Accept:xml" in header:
            headerr = "XML"
        else:
            for i in header:
                if 'Content-Type:application/' in i or 'Accept:' in i:
                    headerr = "Invalid"

        if data_list[1]=='/':
            if headerr == '':
                print ('sending data back to the client')

                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(file_name))+headers+"\r\n"+file_name
                con.sendall(bytes(content, 'UTF-8'))
            elif headerr=='HTML':
                html_file=''
                for file_nam in glob.glob(os.path.join(dirr, '*.html')):
                    file_nam=file_nam.replace(dirr+'/','')
                    file_nam=file_nam.replace(dirr+'\\','')
                    html_file=html_file+file_nam
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(html_file))+headers+"\r\n"+html_file
                con.sendall(bytes(content, 'UTF-8'))
            elif headerr=='JSON':
                html_file=''
                for file_nam in glob.glob(os.path.join(dirr, '*.json')):
                    file_nam=file_nam.replace(dirr+'/','')
                    file_nam=file_nam.replace(dirr+'\\','')
                    html_file=html_file+file_nam
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(html_file))+headers+"\r\n"+html_file
                con.sendall(bytes(content, 'UTF-8'))
            elif headerr=='XML':
                html_file=''
                for file_nam in glob.glob(os.path.join(dirr, '*.xml')):
                    file_nam=file_nam.replace(dirr+'/','')
                    file_nam=file_nam.replace(dirr+'\\','')
                    html_file=html_file+file_nam
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(html_file))+headers+"\r\n"+html_file
                con.sendall(bytes(content, 'UTF-8'))
            elif headerr=='plain':
                html_file=''
                for file_nam in glob.glob(os.path.join(dirr, '*.txt')):
                    file_nam=file_nam.replace(dirr+'/','')
                    file_nam=file_nam.replace(dirr+'\\','')
                    html_file=html_file+file_nam
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(html_file))+headers+"\r\n"+html_file
                con.sendall(bytes(content, 'UTF-8'))
            else:
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len("Invalid File Format"))+headers+"\r\n"+"Invalid File Format"
                con.sendall(bytes(content, 'UTF-8'))
        else:
            f_name=data_list[1].replace('/','')
            f_name_1 = f_name
            if os.name == 'nt':
                f_name = dirr+"\\"+f_name
            else:
                f_name = dirr+"/"+f_name
            if headerr=='':
                f_name = f_name
            elif headerr=='HTML':
                if '.html' not in f_name:
                    f_name = f_name+'.html'
                    f_name_1 = f_name_1+'.html'
            elif headerr=='JSON':
                if '.json' not in f_name:
                    f_name = f_name+'.json'
                    f_name_1 = f_name_1+'.json'
            elif headerr=='XML':
                if '.xml' not in f_name:
                    f_name = f_name+'.xml'
                    f_name_1 = f_name_1+'.xml'
            elif headerr=='plain':
                if '.txt' not in f_name:
                    f_name = dirr+"\\"+f_name+'.txt'
                    f_name_1 = f_name_1+'.txt'
            else:
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len("Invalid File Format"))+headers+"\r\n"+"Invalid File Format"
                con.sendall(bytes(content, 'UTF-8'))
            if f_name_1 in list_file:
                f = open(f_name, "r")
                c = f.read()
                if("Content-Disposition" in header[len(header)-1]):
                    if('filename' in header[len(header)-1]):
                        head_val=header[len(header)-1].split(";")
                        file_split=head_val[1].split("=")
                        file_name=file_split[1].replace("'","")
                        extention=file_name.split(".")
                        m_fname_extention = f_name_1.split(".")[1]
                        print("Extention="+extention[1])
                        print("headerr="+headerr)
                        if(m_fname_extention!=extention[1].lower()):
                            content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len("Invalid File Format"))+headers+"\r\n"+"Invalid File Format for Content Disposition"
                            con.sendall(bytes(content, 'UTF-8'))
                        else:
                            if os.name == 'nt':
                                shutil.copy(f_name,"C:\\rafi\\download\\"+file_name)
                            else:
                                shutil.copy(f_name,"/Users/shivamnautiyal/Downloads/"+file_name)
                            content= "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(f.read()))+headers+"\r\n"+ c + "\r\nFile Downloaded Successfully with name "+ file_name
                            con.sendall(bytes(content, 'UTF-8'))
                    elif("attachment" in header[len(header)-1] and ";" not in header[len(header)-1]):
                        print("5")
                        if os.name == 'nt':
                            shutil.copy(f_name,"C:\\rafi\\download\\")
                        else:
                            shutil.copy(f_name,"/Users/shivamnautiyal/Downloads/")
                        content= "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(f.read()))+headers+"\r\n"+ c + "\r\nFile Downloaded Successfully with name "
                        con.sendall(bytes(content, 'UTF-8'))
                    else:
                        content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(f.read()))+headers+"\r\n"+ c
                        con.sendall(bytes(content, 'UTF-8'))
                else:
                    content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(f.read()))+headers+"\r\n"+ c
                    con.sendall(bytes(content, 'UTF-8'))
            else:
                print ('sending data back to the client')
                con.sendall(bytes("HTTP/1.0 404 Not Found\r\n No files are found in the directory.",'UTF-8'))
    elif "POST" in data:
        file_content = data.split("-d")[1]
        file_content = file_content.split("-h")[0]
        if "Content-Type:application/plain" in header or "Accept:txt" in header:
            headerr = "plain"
        elif "Content-Type:application/html" in header or "Accept:html" in header:
            headerr = "HTML"
        elif "Content-Type:application/json" in header or "Accept:json" in header:
            headerr = "JSON"
        elif "Content-Type:application/xml" in header or "Accept:xml" in header:
            headerr = "XML"
        else:
            for i in header:
                if 'Content-Type:application/' in i or 'Accept:' in i:
                    headerr = "Invalid"

        if data_list[1]=='/':
            print ('sending data back to the client')
            content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len("Invalid File Format"))+headers+"\r\n"+"Invalid File Format"
            con.sendall(bytes(content, 'UTF-8'))
        else:
            f_name=data_list[1].replace('/','')
            f_name_1 = f_name
            if os.name == 'nt':
                f_name = dirr+"\\"+f_name
            else:
                f_name = dirr+"/"+f_name
            if headerr=='':
                f_name = f_name
            elif headerr=='HTML':
                if '.html' not in f_name:
                    f_name = f_name+'.html'
                    f_name_1 = f_name_1+'.html'
            elif headerr=='JSON':
                if '.json' not in f_name:
                    f_name = f_name+'.json'
                    f_name_1 = f_name_1+'.json'
            elif headerr=='XML':
                if '.xml' not in f_name:
                    f_name = f_name+'.xml'
                    f_name_1 = f_name_1+'.xml'
            elif headerr=='plain':
                if '.txt' not in f_name:
                    f_name = dirr+"\\"+f_name+'.txt'
                    f_name_1 = f_name_1+'.txt'
            else:
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len("Invalid File Format"))+headers+"\r\n"+"Invalid File Format"
                con.sendall(bytes(content, 'UTF-8'))

            if f_name_1 in list_file and 'overwrite=true' in data:
                f = open(f_name, "w+")
                f.write(file_content)
                f.close()
                #print ('sending data back to the client')
                content = "HTTP/1.0 201 OK \r\n Content-Length: " +str(len(file_content))+headers+"\r\n"+"File created.File name: "+f_name
                con.sendall(bytes(content, 'UTF-8'))
            elif f_name_1 in list_file and 'overwrite=false' in data:
                content = "HTTP/1.0 200 OK \r\n Content-Length: " +str(len(file_content))+headers+"\r\n"+"File already exists and You chose not to Overwrite."
                con.sendall(bytes(content, 'UTF-8'))
            else:
                f=open(f_name, "w+")
                f.write(file_content)
                f.close()
                content = "HTTP/1.0 201 OK \r\n Content-Length: " +str(len(file_content))+headers+"\r\n"+"File updated.File name: "+f_name
                con.sendall(bytes(content, 'UTF-8'))
    lock.release()
