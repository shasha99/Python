 The script can be used for configuring the network for a linux box.
 The intension behing writing this script was to solve the problem of configuring a raw virtual machine which is accessible by logging into the server (vCenter for example).


 Requirements:
 Python 2.7

 How to USE ?
 The script takes the following parameters from command line. Note that the sequence must be same:
   1. network type - s/d  (static/dynamic)
   2. hostname
   3. domain
   4. primary_dns
   5. ip
   6. netmask
   7. gateway
   8. secondry_dns

 Note that in case of DHCP, values of IP, Netmask, gateway will be ignored.

