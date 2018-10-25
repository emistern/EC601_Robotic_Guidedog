f = open("train.txt", 'w')
for i in range(2578):
	f.write("data/obj/"+str(i+1)+".jpg"+'\n')
