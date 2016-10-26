import subprocess
import sys
import shutil
import os

class NetworkConfiguration:
        def __init__(self):
                self.ntype=""
                self.hostname=""
                self.domain=""
                self.pdns=""
                self.sdns=""
                self.ip=""
                self.netmask=""
                self.gway=""
                self.files=["/etc/sysconfig/network/ifcfg-eth0",
                                "/etc/sysconfig/network/routes",
                                "/etc/resolv.conf",
                                "/etc/HOSTNAME"
                                ]

        def writeIntoFile(self,filename,s,mode):
                f=open(filename,mode)
                f.write(s)
                f.close()

        def buildString(self,filename):
                ret_str=""
                if filename == self.files[0] :
                        ret_str="DEVICE=eth0"
                        ret_str+="\n"+"STARTMODE=auto"
                        ret_str+="\n"+"BOOTPROTO="
                        if self.ntype=="s":
                                ret_str+="static"
                        else:
                                ret_str+="dhcp"
                        ret_str+="\n"+"USERCONTROL=no"
                        ret_str+="\n"+"ONBOOT=yes"
                        if self.ntype=="s":
                                ret_str+="\n"+"IPADDR="+self.ip
                                ret_str+="\n"+"NETMASK="+self.netmask
                elif filename==self.files[1]:
                        if self.ntype=="s":
                                ret_str="defualt "+self.gway+" - -"
                elif filename==self.files[2]:
                        ret_str="search "+self.domain
                        ret_str+="\n"+"nameserver "+self.pdns
                        if self.sdns!="":
                                ret_str+="\n"+"nameserver "+self.sdns
                elif filename==self.files[3]:
                        ret_str=self.hostname+"."+self.domain

                return ret_str


        def runProcess(self,args):
                p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                return p.communicate()
#------------------------Class Ends Here---------------------------------------

if __name__ == "__main__" :
        nCog=NetworkConfiguration()

        # Recieving arguments from commmand line.
        #sequence is: network_type,hostname,domain,primary_dns,ip,netmask,gateway,secondry_dns
        # note : IP, Netmask, gateway are not required in case of DHCP.
        try:
                nCog.ntype=sys.argv[1]
                if nCog.ntype=="s" and  len(sys.argv)<8:
                        raise Exception("Too few arguments passed for static configuration!!!")
                elif nCog.ntype=="d" and len(sys.argv)<5:
                        raise Exception("Too few arguments passed for DHCP configuration!!!")
                elif nCog.ntype!="s" and nCog.ntype!="d":
                        raise Exception("Not a valid network type!!!")

                nCog.hostname=sys.argv[2]
                nCog.domain=sys.argv[3]
                nCog.pdns=sys.argv[4]

                if nCog.ntype=="s":
                        nCog.ip=sys.argv[5]
                        nCog.netmask=sys.argv[6]
                        nCog.gway=sys.argv[7]
                        if len(sys.argv)==9:
                                nCog.sdns=sys.argv[8]
                elif len(sys.argv)==6:
                        nCog.sdns=sys.argv[5]

        except Exception, e:
                print(e)

        # Writing network configurations into the appropriate files.
        for f in nCog.files:
                ret_str=nCog.buildString(f)
                nCog.writeIntoFile(f,ret_str,"w")

        # Setting the hostname
        o, e=nCog.runProcess(['hostname',nCog.hostname])

        # restart the network
        o, e=nCog.runProcess(['service','network restart'])
        print("restarting the network:\n------------------------------------")
        print("output: "+o+"\n error: "+e)

        # Adding gateway ip to the routing table in case static ip is assigned.
        print os.system("sudo ip route add default via %s" % (nCog.gway))
