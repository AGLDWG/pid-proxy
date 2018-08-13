# pid-proxy
This is the documentation of server configuration and data back-up for the Australian Government Linked Data Working Group (AGLDWG)'s Persistent ID (PID) proxy service that manages URI for Linked Data resources.

The PID proxy manages persistent URIs within the following domains:

* `linked.data.gov.au` - the main, operational, domain
* `environment.data.gov.au`, `reference.data.gov.au` - legacy domains for which existing URIs will be supported but none new added

Also managed are a number of non-persistent domains:

* `test.linked.data.gov.au` - for testing candidate PID URIs
* `www.linked.data.gov.au` - the main AGLDWG website
* `catalogue.linked.data.gov.au` - the catalogue tracking PID URI allocations


## Server configuration
This repository documents the setup of the PID proxy.

### In outline
The server is a small Virtual Machine (VM) that running Linux within which is installed the Apache 2 web server program which is configured to make URI redirects and proxying. The only other program of significance (i.e. not 'out-of-the-box' Linux programs) installed on the VM is Git which is used to pull updated Apache server config files from this repository to the server.

### In detail
* The server is a Virtual Machine established on the [NeCTAR](nectar.org.au) cloud
  * The specific VM and the Floating IP address allocated to it is provided within the NeCTAR project 'AGLDWG' allocation by [QRISCloud](https://www.qriscloud.org.au/) which is a NeCTAR provider institution
* The Floating IP of the PID Proxy is [203.100.30.55](http://203.100.30.55)
* The Virtual Machine image of the current VM acting as PID Proxy is name: pid-prod8, ID: b8567a35-adaf-41cc-8228-b3e7f70d74e7
  * The installation log of the server is in this repository as [install.sh](install.sh)


## Backup
Redirection and proxying configuration implemented in the PID Proxy is slaved to this repository. This means that the configuration you see here (the files ending in .conf) is the master copy of Apache config which is then pulled to the server for deployment. So far, the three PID domains managed by the PID Proxy use configuration from the files:

* [linked.data.gov.au.conf](conf/linked.data.gov.au.conf)
* [environment.data.gov.au.conf](conf/environment.data.gov.au.conf)
* [reference.data.gov.au.conf](conf/reference.data.gov.au.conf)

The non-persistent domains are managed using .conf files with their names.

All .conf files loaded onto the server are contained within the [conf/](conf/] folder.


## PID Governance
In order to create new URI PIDs within `linked.data.gov.au.conf` (the other two managed domains being in maintenance-only mode with no new URI patterns to be added), a governed process must be followed. That process is detailed on the AGLDWG's website:

* [linked.data.gov.au/governance](http://linked.data.gov.au/governance)


## PID Testing
The `test.linked.data.gov.au` domain is available for testing proposed PIDs. Contact the WG to implement URIs using this domain but know that they will be purged semi regularly (quarterly or as needed).

All PIDs accepted for allocation within `linked.data.gov.au` will be added to the PID Proxy conf file for that domain and then have the test suite run against the updated result. All tests must pass before the new PID becomes fully implemented and thus [stable](http://linked.data.gov.au/def/reg-status/stable). This ensure that it doesn't interfere with existing PIDs.

The test suite for `linked.data.gov.au` is a `Python pytests` script in this repository at [tests/linked.data.gov.au.py](tests/linked.data.gov.au.py).

The workflow governing this testing is contained within the current AGLDWG's [URI Guidelines](https://github.com/AGLDWG/guidelines).

## License
This repository is licensed under Creative Commons 4.0 International. See the [LICENSE deed](LICENSE) in this repository for details.


## Contacts
System Owner:  [Australian Government Linked Data Working Group](http://linked.data.gov.au)

System Owner contact:  
**Nicholas Car**  
*Senior Experimental Scientist*  
*Co-chair, AGLDWG*  
CSIRO Land & Water  
<nicholas.car@csiro.au>  

Technical Contact:  
**Edmond Chuc**  
*Research Projects Officer*  
CSIRO Land & Water  
<edmond.chuc@csiro.au>  
