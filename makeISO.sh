#!/bin/bash
sourceDirectory=$1
name=$2

mkisofs -lJR -V "$name" -o ${name}.iso "$sourceDirectory"
