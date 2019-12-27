#!/bin/bash
mkdir bak

let i=1                               # define an incremental variable
for file in *.txt                     # *.jpg means all jpg files in current directory
do
    cp ${file} bak
    mv ${file} ${i}
    echo "${file} renamed as ${i}"
    let i=i+1
done
