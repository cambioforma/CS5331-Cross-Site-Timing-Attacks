# Introduction 

## Background 

Timing attack has existed for a long time. However, web developers tend to overlook the issue during the design phase as such attacks are largely dependent on implementation and compiler optimization. While timing attack often target server’s information assets, it may also be launched against the clients. When browsers accessed web resources, some may be cached in the system to increase performance in fetching information. Using the timing attack, server may probabilistically determine the clients’ recent browsing activities and potentially infringe on their privacy. 

## Objectives 
To develop a Client-side JavaScript Plugin that performs the timing attack to probabilistically determine whether the user has recently visited certain websites by measuring the required access time.  

## Scope 
In "Timing Attacks on Web Privacy", it is noted that JavaScript provide the most accurate means of measuring access time. Thus, the scope will be limited to JavaScript for this project. 

Implementation of server-side timing attacks as described in the research papers referenced below: 

1. Creation of Client-Side JavaScript Plugin 
2. Creation of simple Web Application as proof-of-concept (POC) 
3. Testing of attacks on simple Web Application 
4. Measurements on Client and Server Side 

## System Setup 

### Server side 
1. NodeJS or Python Web Server
2. Database (For logging) - MySQL or PostgreSQL 

### Client Side 
Web browsers i.e. Google Chrome, Mozilla Firefox, Microsoft Edge, Safari 

## References 
Timing Attacks on Web Privacy - https://dl.acm.org/citation.cfm?id=352606

Exposing Private Information by Timing Web Applications - https://dl.acm.org/citation.cfm?id=1242656 
