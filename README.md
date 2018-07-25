# pid-proxy
This is the documentation and back-up for the AGLDWG's Persistent ID (PID) proxy service that manages URI for Linked Data resources.

The PID proxy manages URIs within the (sub)domains:

* `linked.data.gov.au` - the main, operational, domain
* `environment.data.gov.au`, `reference.data.gov.au` - legacy domains for which existing URIs will be supported but none new added 


## Documentation
This repository documents the setup of the PID proxy.

**In outline**: the server is a small Virtual Machine (VM) that running Linux within which is installed the Apache 2 web server program which is configured to make URI redirects and proxying. The only other program of significance (i.e. not 'out-of-the-box' Linux programs) installed on the VM is Git which is used to pull updated Apache server config files from this repository to the server.

**In detail**: the installation log of the server is in this repository as [install.sh](install.sh).


## Backup
Redirection and proxying configuration implemented in the PID Proxy is slaved to this repository. This means that the configuration you see here (the files ending in .conf) is the master copy of Apache config which is then pulled to the server for deployment. So far, the three subdomains managed by the PID Proxy use configuration from the files:

* [linked.data.gov.au.conf](linked.data.gov.au.conf)
* [environment.data.gov.au.conf](environment.data.gov.au.conf) 
* [reference.data.gov.au.conf](reference.data.gov.au.conf).


## PID Governance
In order to create new URI PIDs within `linked.data.gov.au.conf` (the other two managed subdomains being in maintenance-only mode with no new URI patterns to be added), a governed process must be followed. That process is detailed on the AGLDWG's website:

* [linked.data.gov.au/governance](http://linked.data.gov.au/governance) <- *not working yet! Expected, August, 2018.*


## License
This repository is licensed under Creative Commons 4.0 International. See the [LICENSE deed](LICENSE) in this repository for details.


## Contacts
Product Owner:  
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water  
<nicholas.car@csiro.au>  

Technical Contact:  
**Edmond Chuc**  
*Research Projects Officer*  
CSIRO Land & Water  
<edmond.chuc@csiro.au>  
