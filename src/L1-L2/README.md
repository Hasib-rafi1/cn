# COMP6461 LA1

#   Demo
*   python httpc.py
*   httpc help
*   httpc help get
*   httpc help post
*   httpc get 'http://httpbin.org/get?course=networking&assignment=1'
*   httpc get -v 'http://httpbin.org/get?course=networking&assignment=1'
*   httpc get -h Content-Type:application/json 'http://httpbin.org/get?course=networking&assignment=1'
*   httpc get -v -h Content-Type:application/json 'http://httpbin.org/get?course=networking&assignment=1'
*   httpc get -v -h Content-Type:application/json 'http://httpbin.org/get?course=networking&assignment=1' -o hello.txt
*   httpc post -h Content-Type:application/json --d '{"Assignment": 1}' 'http://httpbin.org/post'
*   httpc post -v -h Content-Type:application/json --d '{"Assignment": 1}' 'http://httpbin.org/post'
*   httpc post -v -h Content-Type:application/json --f 'file.json' 'http://httpbin.org/post'
*   httpc post -v -h Content-Type:application/json --f 'file.json' 'http://httpbin.org/post' -o hello.txt
*   httpc post -v -h Content-Type:application/json --d'{"Ass":1}' --f 'file.json' 'http://httpbin.org/post'
*   httpc get -v 'http://google.com'

#   Run Localserver to execute this commands
*   httpc get / 'localhost:8080'
*   httpc get /log 'localhost:8080'
*   httpc get /file -h Content-Type:application/json 'localhost:8080'
*   httpc get /file -v -h Content-Type:application/json 'localhost:8080'
*   httpc get /hello/bob -h Content-Type:application/json 'localhost:8080'
*   httpc get /file.json -h Content-Type:application/json -h Content-Disposition:attachment;filename="abc.json" 'localhost:8080'
*   httpc post /bob -h Content-Type:application/json --d '{"Ass":1}' 'localhost:8080'
*   httpc post /bob -h Content-Type:application/json --f 'file.json' 'localhost:8080'
*   httpc post /bob overwrite=false -h Content-Type:application/json --d '{"Assignment":10}' 'localhost:8080'
*   httpc post /bob overwrite=true -h Content-Type:application/json --d '{"Assignment":10}' 'localhost:8080'
#   Multi thread
*   to start theread - press m and enter
##  get Same file
*   httpc get /file -h Content-Type:application/json 'localhost:8080'
*   httpc get /file -h Content-Type:application/json 'localhost:8080'
##  same file read and write
*   httpc get /bob -h Content-Type:application/json 'localhost:8080'
*   httpc post /bob overwrite=true -h Content-Type:application/json --d '{"Assignment":9}' 'localhost:8080'
##  Same file write 
*   httpc post /bob overwrite=true -h Content-Type:application/json --d '{"Assignment":10}' 'localhost:8080'
*   httpc post /bob overwrite=true -h Content-Type:application/json --d '{"Assignment":12}' 'localhost:8080'
##  To Quit
*   to quit  - press q and enter.

#   Server
*   python https.py
*   httpfs -p 8080 -d C:\\rafi\\cn

# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)


# Requirements
* Python 3.5.1
