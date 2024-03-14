#!/bin/bash

i=0
while [[ $i -lt 5000 ]]; do
	echo $i >> reverieInput
	i=$((i+1))
done
