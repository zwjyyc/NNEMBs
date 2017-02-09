import sys

goldLabels = []
modelLis = []

modelPreds = []

propModels = []

loadLabel = False
cnt0 = cnt1 = cnt2 = 0
wcnt0 = wcnt1 = wcnt2 = 0

with open(sys.argv[1], 'r') as fin:
    for line in fin.readlines():
	print line
	
	modelPred = []	
	predLabels = []
	with open(line.strip(), 'r') as fin1:
	    for line1 in fin1.readlines():
		items = line1.strip().split('\t')
		predLabels.append(int(items[0]))
		if not loadLabel:
		    goldLabels.append(int(items[1]))
		
		vals = []
		itemss = items[2].split()
		for item in itemss:
		    vals.append(float(item))
		modelPred.append(vals)
	    
	    cnt0 = cnt1 = cnt2 = 0
	    wcnt0 = wcnt1 = wcnt2 = 0
	    for pred, gold in zip(predLabels, goldLabels):
		if gold == 0:
		    cnt0 += 1
		    if gold == pred:
			wcnt0 += 1
		elif gold == 1:
		    cnt1 += 1
		    if gold == pred:
			wcnt1 += 1
		elif gold == 2:
		    cnt2 += 1
		    if gold == pred:
			wcnt2 += 1
	recall0 = 1.0 * wcnt0 / cnt0
	recall1 = 1.0 * wcnt1 / cnt1
	recall2 = 1.0 * wcnt2 / cnt2
	recallA = (recall0 + recall1 + recall2) / 3
	print "ACCURACY " + str(1.0 * (wcnt0 + wcnt1 + wcnt2) / (cnt0 + cnt1 + cnt2)) + "\tRECALL_NEG: " + str(recall0) + "\tRECALL_NEU: " + str(recall1) + "\tRECALL_POS: " + str(recall2)
	print "RECALL_AVERAGE: " + str(recallA)

	print "==================================================================="
	modelPreds.append(modelPred)

print "ENSEMBLE RESULTS"

modelNum = len(modelPreds)
instanceNum = len(modelPreds[0])
print "Model Num " + str(modelNum)
print "INSTANCE NUM " + str(instanceNum)

predLabels = []
for i in range(instanceNum):
    sums = []
    sums.append(0.0)
    sums.append(0.0)
    sums.append(0.0)
    for j in range(modelNum):
	vals = modelPreds[j][i]
	sums[0] += vals[0]
	sums[1] += vals[1]
	sums[2] += vals[2]

    pred = 0
    maxV = -1000.0
    for k in range(3):
	if sums[k] > maxV:
	    pred = k
	    maxV = sums[k]
    predLabels.append(pred)

with open("EnsembleOff.result", 'w') as fout:
    for pred, gold in zip(predLabels, goldLabels):
        fout.write(str(pred) + '\t' + str(gold) + '\n')


cnt0 = cnt1 = cnt2 = 0
wcnt0 = wcnt1 = wcnt2 = 0

for pred, gold in zip(predLabels, goldLabels):
    if gold == 0:
	cnt0 += 1
	if gold == pred:
	    wcnt0 += 1
    elif gold == 1:
	cnt1 += 1
	if gold == pred:
	    wcnt1 += 1
    elif gold == 2:
	cnt2 += 1
	if gold == pred:
	    wcnt2 += 1

recall0 = 1.0 * wcnt0 / cnt0
recall1 = 1.0 * wcnt1 / cnt1
recall2 = 1.0 * wcnt2 / cnt2
recallA = (recall0 + recall1 + recall2) / 3
print "ACCURACY " + str(1.0 * (wcnt0 + wcnt1 + wcnt2) / (cnt0 + cnt1 + cnt2)) + "\tRECALL_NEG: " + str(recall0) + "\tRECALL_NEU: " + str(recall1) + "\tRECALL_POS: " + str(recall2)
print "RECALL_AVERAGE: " + str(recallA)
print "==============================="










