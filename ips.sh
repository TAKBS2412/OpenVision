#!/bin/bash
# Name
# 	ips - Sets the pi's IP Address.
# Synopsis
# 	ips [OPTIONS] [...]
# Description
# 	Sets the Pi's IP Address to a static or dynamic IP address.
#
#	The first argument should be a function letter (see below). If a static IP Address is being set, the Pi's IP Address, the router's IP Address, and the DNS IP Address should all be specified, in that order.
#	By default, ips will set a dynamic IP Address.


# Function letters:
# 	-d 
#		Enables DHCP.
#	-s
#		Enables static IP.
export MODE=$1
if [ "$MODE" = "-d" ] || [ "$MODE" = "" ]; then
	echo "DHCP"
	sed -i -e "s/interface\ eth0/#interface\ eth0/g" /etc/dhcpcd.conf
	sed -i -e "s/static\ ip_address=/#static\ ip_address=/g" /etc/dhcpcd.conf
	sed -i -e "s/static\ routers=/#static\ routers=/g" /etc/dhcpcd.conf
	sed -i -e "s/static\ domain_name_servers=/#static\ domain_name_servers=/g" /etc/dhcpcd.conf
elif [ "$MODE" = "-s" ]; then
	echo "STATIC"
	export IP_ADDRESS=$2
	export ROUTERS=$3
	export DNS=$4
	sed -i -r -e "s/#*interface\ eth0/interface\ eth0/g" /etc/dhcpcd.conf
	sed -i -r -e 's|#*static\ ip_address=.*|static\ ip_address='$IP_ADDRESS'|g' /etc/dhcpcd.conf # Use | as delimiter since $IP_ADDRESS may contain a forward slash (/).
	sed -i -r -e "s/#*static\ routers=.*/static\ routers=$ROUTERS/g" /etc/dhcpcd.conf
	sed -i -r -e "s/#*static\ domain_name_servers=.*/static\ domain_name_servers=$DNS/g" /etc/dhcpcd.conf
else
	echo "Error: $MODE is not a valid argument."
fi
