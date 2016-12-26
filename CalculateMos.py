import sys
import os
import re

#Execute the batch code to get .txt file to be processed
os.system('"C:\\Program Files\\Wireshark\\tshark.exe" -r '+str(sys.argv[1])+' -q -z rtp,streams > Stats.txt')

#read file
file = open("Stats.txt","r")
lines = file.readlines()
file.close()

#Create dictionary {SSRC,Lost Percentage}
dictionary = {}
#Process the file line by line
for line in lines:
    #print the statisticas line by line
    print(line)
    #Get Lost Percentage
    list = re.findall(r'0[xX][0-9a-fA-F]+',line)
    #Get SSRC
    list1 = re.findall(r'[-+]?[0-9]*\.?[0-9]+%',line)
    #Make the dictionary
    if len(list)!=0 and len(list1)!=0:
        dictionary[list[0]]=list1[0]

#Print the SSRC of the flow with the worse Lost Percentage (the highest lost percentage)
maximum = max(dictionary, key=dictionary.get)
print("The flow with the highest lost percentage is: "+maximum+" -> "+dictionary[maximum])

print("==============================================================")
#Calculate the MOS for the SSRC with the highest Lost Percentage
print("\nCalculating MOS for "+maximum)
os.system('"C:\\Program Files\\Wireshark\\tshark.exe" -n -r '+str(sys.argv[1])+' -Y rtp -Y rtp.ssrc=='+maximum+' -T fields -e rtp.payload > SSRC_payload.txt')
os.system('Hextext2Bin.exe SSRC_payload.txt')
os.system('sox\Sox.exe SSRC_payload.ul SSRC_payload.wav')
os.system('PESQ.exe VOIPStream_server.wav SSRC_payload.wav +8000')