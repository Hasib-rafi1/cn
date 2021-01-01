# COMP6461 LA1



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

#   Router
*   ./router.exe --port=3000 --drop-rate=0.2 --seed 2387230234324
*   ./router.exe --port=3000 --max-delay=100ms --seed 2387230234324
*   ./router.exe --port=3000 --drop-rate=0.2 --max-delay=100ms --seed 2387230234324

#   Server
*   python https.py
*   httpfs -p 8080 -d C:\rafi\cn


# Reference
* HTTP 1.0 Protocol
[HTTP 1.0](https://www.w3.org/Protocols/HTTP/1.0/spec.html)


# Requirements
* Python 3.5.1
