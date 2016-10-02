echo 0008
echo -e david\\n0008 | access | grep Success && break

for ((i=1; i<=9; ++i))
do 
    echo 00$(($i*10+8)) 
    echo -e david\\n00$(($i*10+8)) | access | grep Success && break
done

for ((i=10; i<=99; ++i))
do 
    echo 0$(($i*10+8)) 
    echo -e david\\n0$(($i*10+8)) | access | grep Success && break
done

for ((i=100; i<=999; ++i))
do 
    echo $(($i*10+8)) 
    echo -e david\\n$(($i*10+8)) | access | grep Success && break
done

