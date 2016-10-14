#!/bin/bash

for i in {000..999}
do
    echo $i\8
    echo -e david\\n$i\8 | ./access | grep Success && break
done
