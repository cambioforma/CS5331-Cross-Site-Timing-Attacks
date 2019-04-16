# CS5331 Cross Site Timing Attack [Preydator]

## Background 

Timing attack has existed for a long time. However, web developers tend to overlook the issue during the design phase as such attacks are largely dependent on implementation and compiler optimization. While timing attack often target server’s information assets, it may also be launched against the clients. When browsers accessed web resources, some may be cached in the system to increase performance in fetching information. Using the timing attack, server may probabilistically determine the clients’ recent browsing activities and potentially infringe on their privacy. 

## Objectives 
To develop a tool (Preydator) that satisfies both attack and defence scenario in the Cross-site timing attack. It performs the timing attack and collects the required accessed time of web resources automatically. 
Preydator includes the following components:
1.	Client-side JavaScript Plugin
2.	Sample Malicious Web application
3.	Administrator Dashboard (Configuration & Analysis of Results)
4.	Other Server-side Hosting, Logging and Storage


## Scope 
In "Timing Attacks on Web Privacy", it is noted that JavaScript provide the most accurate means of measuring access time. Thus, the scope of this project will be set to JavaScript. While there are many resources a webpage may require, Preydator will focus on image. The process is similar for other resources such as JavaScript and CSS and may be considered as a possible future enhancement. 

Implementation of Cross-site timing attacks as described in "Timing Attacks on Web Privacy":
1.	Creation of Client-Side JavaScript Plugin
2.	Creation of simple server-side application as proof-of-concept (POC)
3.	Testing attacks on sample websites
4.	Measurements of timing for cached and un-cached resources
5.	Analyse collected data
Preydator focuses on the implementation of the technique mentioned in the research papers as well as a new feature to test for vulnerability against cross-site attacks, and experimentation with them through several test cases.


## System Setup 

### Server side 
1. Python Web Server
2. Database (For logging) - MySQL

### Client Side 
Web browsers i.e. Google Chrome, Mozilla Firefox, Microsoft Edge, Safari 

## References 
Timing Attacks on Web Privacy - https://dl.acm.org/citation.cfm?id=352606

Exposing Private Information by Timing Web Applications - https://dl.acm.org/citation.cfm?id=1242656 
