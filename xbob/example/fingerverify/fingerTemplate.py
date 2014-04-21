def savetoDic(name, row_value, col_value, value, orient, dict_type, galDic, probeDic):
	# a dict_type of 1 represents a gallery image
	if dict_type == 1:
		galDic[name].append(value)
		galDic[name].append(row_value)
		galDic[name].append(col_value)
		galDic[name].append(orient)
	elif dict_type == 2:
		probeDic[name].append(value)
		probeDic[name].append(row_value)
		probeDic[name].append(col_value)
		probeDic[name].append(orient)
	else:
		print('Incorrect Value for dict_type, needs to be set to 1 for gallery or 2 for probe')
	return galDic,probeDic
#creates the dictionaries for the program based on the gallery and probe images
def createDic(galnames, probenames):
	galDic = {}
	probeDic = {}
	for x in range(len(galnames)):
		galn = galnames[x]
		print(galn)
		galDic[galn] = []
	for x in range(len(probenames)):
		proben = probenames[x]
		probeDic[proben] = []
	return galDic,probeDic


