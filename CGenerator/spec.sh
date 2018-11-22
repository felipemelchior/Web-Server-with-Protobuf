#!/bin/bash
echo "------CPU:------" >> specs.txt
sudo lscpu >> specs.txt
echo "">> specs.txt

echo "------MEMORIA:------" >> specs.txt
sudo free >> specs.txt
echo "">> specs.txt

echo "------DISCO:------" >> specs.txt
sudo hdparm -i /dev/sda >> specs.txt
echo "">> specs.txt
