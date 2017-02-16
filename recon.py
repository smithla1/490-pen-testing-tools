#!/usr/bin/python

"""
NAME
    recon.py - Reconnaissance tool for Penetration Testing

SYNOPSIS
    recon [-dei] [url]

DESCRIPTION
    This is a script which streamlines a number of steps in
    the reconnaissance phase of a penetration test. It allows
    for the input of a flag and an URL which will be used to
    gather information about a website, where the flag determines
    what information is gathered.

REQUIREMENTS
    This script is intended to be run with Python 2.7. It is not compatible
    with Python 3 and above. It is preferable to run the script on a Linux
    operating system such as Kali Linux.   

OPTIONS
    If only a URL is entered, the command will return an aggregated list
    of all available information concerning that URL.

    If no operands are given, a help message will be displayed and the
    command will do nothing else.

        -d          Return information about DNS servers associated with
                    the given URL.

        -e          Return information about email addresses associated with
                    the given URL.

        -i          Return information about IP addresses associated with
                    the given URL.

        -n          Return information about names associated with the given
                    URL.

EXAMPLES
    recon.py -i google.com
    recon.py -d apple.com
    recon.py -n amazon.com

AUTHORS
    Patrick Knight
    Logan Smith
"""

import string
import subprocess
import sys


"""
    This method will gather and store in a local file information about the
    Domain Name Servers associated with a given URL.
"""
def get_DNS_servers(website):
    subprocess.call("whois %s > temp.txt" % website, shell=True)

    with open("temp.txt", 'r') as f:	
        content = f.readlines()

    dns_servers = []
    for line in content:
        if "Name Server" in line:
            line = line.strip()
            dns_servers.append(line)

    # remove duplicates from dns_servers
    dns_servers = list(set(dns_servers))
    
    
    i = 0
    for dns_server in dns_servers:
        if i == 0:
            subprocess.call("echo DNS recon info on %s > dns_servers.txt" % website, shell=True);
            subprocess.call("echo %s >> dns_servers.txt" % dns_server, shell=True)
        else:
            subprocess.call("echo %s >> dns_servers.txt" % dns_server, shell=True)
        i = i + 1

    # remove temp.txt file
    subprocess.Popen("rm temp.txt", shell=True)


"""
    This method will gather and store in a local file information about the
    IP addresses associated with a given URL.
"""
def get_IP_addresses(website):

    # get the IP address for the website	
    subprocess.call("host %s > temp.txt" % website, shell=True)
    with open("temp.txt", 'r') as f:       
        first_line  = f.readline().strip()

    subprocess.call("echo %s IP address: > IPs.txt" % website, shell=True)
    subprocess.call("echo %s >> IPs.txt" % first_line, shell=True)


    # get the IP addresses for the websites DNS servers
    subprocess.call("whois %s > dns_temp.txt" % website, shell=True)
    with open("dns_temp.txt", 'r') as f:	
        content = f.readlines()

    dns_servers = []
    for line in content:
        if "Name Server" in line:
            line = line.strip()
            dns_servers.append(line)

    # remove duplicates from dns_servers
    dns_servers = list(set(dns_servers))
    
    subprocess.call("echo %s DNS server IP addresses: >> IPs.txt" % website, shell=True)
    for dns_server in dns_servers:
	dns_server_name = string.replace(dns_server, "Name Server: ", "")
        subprocess.call("host %s >> IPs.txt" % dns_server_name, shell=True) 
    
    subprocess.call("rm temp.txt dns_temp.txt", shell=True)


"""
    This method will gather and store in a local file information about the
    email addresses associated with a given URL.
"""
def get_email_addresses(website):
    subprocess.call("whois %s > email_temp.txt" % website, shell=True)
    with open("email_temp.txt", 'r') as f:
        content = f.readlines()
    
    emails=[]
    for line in content:
        if "Email" in line:
            line = line.strip()
            emails.append(line)

    subprocess.call("echo %s Email Addresses: > emails.txt" % website, shell=True)
    for email in emails:
        subprocess.call("echo %s >> emails.txt" % email, shell=True)

    subprocess.call("rm email_temp.txt", shell=True)


"""
    This method will gather and store in a local file information about the
    names associated with a given URL.
"""
def get_Names(website):
    subprocess.call("whois %s > name_temp.txt" % website, shell=True)
    with open("name_temp.txt", 'r') as f:
        content = f.readlines()

    names = []
    for line in content:
        if "Name" in line:
            line = line.strip()
            names.append(line)

    subprocess.call("echo %s Names: > names.txt" % website, shell=True)
    for name in names:
        subprocess.call("echo %s >> names.txt" % name, shell=True)

    subprocess.call("rm email_temp.txt", shell=True)


"""
    This method will drive the operation of the reconnaissance tool.
"""
def main():

    helpMessage = ("To use this command, call in the following format:\n\n"+
                   "\trecon.py -e google.com\n\n"+
                   "The following options are available:\n\n"+
                   "\t-d\tgather DNS information\n"+
                   "\t-e\tgather email addresses\n"+
                   "\t-i\tgather IP addresses\n"+
                   "\t-i\tgather names\n\n"+
                   "This information is gathered on the second provided\n"+
                   "argument, which is a website address. If no options\n"+
                   "and only a URL is provided, then all options will be\n"+
                   "used. If no arguments are provided, then the script\n"+
                   "will not run.")
    usageMessage = ("Invalid usage!\n"+
                    "Usage: recon.py -[dein] [url]\n"+
                    "Example: recon.py -d amazon.com\n"+
                    "Type 'recon.py help' for more information.")

    if len(sys.argv) < 2 or len(sys.argv) > 3: #not enough or too many args
        print(usageMessage)
        return
    else:
        if len(sys.argv) == 2: # Only one arg was provided
            if sys.argv[1].lower() == "help": # User wants usage information
                print(helpMessage)
                return
            else:  # only URL was provided, gather all potential information
                get_IP_addresses(sys.argv[-1])
                get_DNS_servers(sys.argv[-1])
                get_email_addresses(sys.argv[-1])
                print("IP reconnaissance successful!\n\"IPs.txt\" created")
                print("DNS reconnaissance successful!\n\"dns_servers.txt\" created")
                print("email reconnaissance successful!\n\"emails.txt\" created")

        elif sys.argv[1].lower() == "-i":
            get_IP_addresses(sys.argv[-1])
            print("IP reconnaissance successful!\n\"IPs.txt\" created")
        elif sys.argv[1].lower() == "-d":
            get_DNS_servers(sys.argv[-1])
            print("DNS reconnaissance successful!\n\"dns_servers.txt\" created")
        elif sys.argv[1].lower() == "-e":
            get_email_addresses(sys.argv[-1])
            print("email reconnaissance successful!\n\"emails.txt\" created")
        elif sys.argv[1].lower() == "-n":
            get_Names(sys.argv[-1])
            print("Name reconnaissance successful!\n\"names.txt\" created")
        else: # User input unknown flag
            print(usageMessage)
            return
    

if __name__ == "__main__":
    main()
