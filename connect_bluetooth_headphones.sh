#!/bin/sh 

BTMAC=$1

bluetoothctl << EOF
power on
agent on
default-agent
connect $BTMAC
trust $BTMAC
EOF

