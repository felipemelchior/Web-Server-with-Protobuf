import sys, random, string

letters = string.ascii_lowercase
commands = ["GET", "POST", "DELETE"]
files = []

try:
	numa = int(sys.argv[1])
	numc = int(sys.argv[2])
	cmds = open("cmds", "w")
	for i in range(numa):
		ofile = open("{}.t".format(i), "w")
		files.append("{}.t".format(i))
		ofile.write(''.join(random.choice(letters) for i in range((i+1)*50)))
		ofile.close()
	for i in range(numc):
		cmds.write("{}\n{}\n".format(
			random.choice(commands),
			random.choice(files)
		))
	cmds.write("SAIR")
except:
	print("tente {} <numeroDeArquivos> <numeroDeComandos>".format(sys.argv[0]))
