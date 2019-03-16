HTTPdiscover_multithread-Python

USAGE:

$ python multiGET.py [ip dictionary file]

    It should work on the brand new BASH for Windows. It works fine on any linux.

    This script is very useful if you want to discover http servers on the web.

    You must create an ip dictionary and feed the script with it in the commandline. Here's an easy way to create an ip dictionary for a given mask:

    $ for i in $(seq 0 255);do echo 192.168.0.$i;done > ip_dictionary

    Before sending the HTTP request, the script checks if the host is alive with one ICMP request. (ping) It opens 10 threads and it starts sending HTTP-GET requests to the specified port. (80) It then writes the server response, if found, to an html file with the ip by name.

    The program only saves the html response of the server. It doesn't download any css,js or img tagged in the html code.

    The user must then examine each created html file for further information.

I hope you find this script useful.

JGilHutton