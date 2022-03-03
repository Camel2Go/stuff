#!/bin/bash
echo "User is $USER"
echo -n "Running Startup..."
cd ~/
echo "Creating files under Home-Dir -> Modem"
mkdir Modem
cd Modem
touch log.txt
cat > ~/Modem/parse.py << ENDOFFILE
file=open("Docsis_signal.asp.html","r")
html=file.read()
file.close()
out=open("output.txt","w")


def parse(i,Ident):
	x=html[i:i+7]
	while x!="nowrap>":
		i=i+1
		x=html[i:i+7]
	j=i+7
	while html[j]!="<":
		j=j+1
	if i==j-7:
		out.write(Ident+"down"+"\n")
	else:
		while html[i+7]==" ":
			i=i+1
		out.write(Ident+html[i+7:j]+"\n")
		
				


for i in range(len(html)):
	x=html[i:i+11]
	if x=='id="channel' and html[i+12]!="i":
		out.write("Channel "+html[i+12]+"\n")
	elif x=='ers="channe' or x=='ers="vch_id':
		parse(i,"    Channel ID ")
	elif x=='ers="vdsch_' and html[i+11]=="f":
		parse(i,"    Down_Freq  ")
	elif x=='ers="vch_mo':
		parse(i,"    Modulation ")
	elif x=='ers="vch_pw':
		parse(i,"    PowerLevel ")
	elif x=='ers="vdsch_' and html[i+11]=="s":
		parse(i,"    NoiseRatio ")
		out.write("\n")
	elif x=='id="up_chan':
		out.write("UpChannel "+html[i+15]+"\n")
	elif x=='s="up_vch_i':
		parse(i,"    Channel ID ")
	elif x=='s="up_vusch' and html[i+12]=="f":
		parse(i,"    Up_Freq    ")
	elif x=='s="up_vch_m':
		parse(i,"    Modulation ")
	elif x=='s="up_vusch' and html[i+12]=="b":
		parse(i,"    Bitrate    ")
	elif x=='s="up_vch_p':
		parse(i,"    PowerLevel ")
		out.write("\n")

out.close()
ENDOFFILE

echo -n "Minutes to Monitor?: "
read min
echo -n "Interval in Minutes?: "
read interval
for ((i=0;i<=$min;i=i+$interval))
do
	echo -n "fetching..."
	wget -E -q http://192.168.100.1/Docsis_signal.asp
	echo -n "parsing..."
	touch output.txt
	python3 parse.py
	echo -n "cleaning..."
	rm Docsis_signal.asp.html
	time=`date +"%H_%M_%S"`
	mv output.txt `date +"%H_%M_%S"`.txt
	echo "done! (`date +"%H:%M:%S"`)"
	echo `date +"%H:%M:%S"`" Success">>log.txt
	sleep $(($interval*60))
done
direct=`date +"%d.%m"`
mkdir $direct
rm parse.py
echo "shutting down">>log.txt
echo "shutting down..."
mv *.txt $direct
shutdown
