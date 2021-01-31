import praw
import math as m
import csv

reddit = praw.Reddit(
	client_id="tpp4an78GZRSYw",
	client_secret="_n1hYNswBLlshDw6N5_KDo54pZpqIA",
	user_agent="stonks"
)

print("Is started: " + str(reddit.read_only))  # Output: True
numBuckets = 120
bucketInterval = 300

with open("cryptos.txt","r") as inputFile:
	readCSV = csv.reader(inputFile, delimiter = ',')
	tickerArray = []
	for i in readCSV:
		tickerArray.append(i)

print(tickerArray)
tickerCount = len(tickerArray)

counts = []
for i in range(tickerCount):
	counts.append([0]*numBuckets)

checked_inBuck = [0]*numBuckets

iterative = 0;


def checkString(inString, bucket):
	if bucket < 0 or bucket >= numBuckets:
		return(0)
	checked_inBuck[bucket] += 1
	for i in range(tickerCount):
		for checkString in tickerArray[i]:
			if checkString in inString:
				# print(checkString)
				# print(bucket)
				# print(str(i) + ' ' + str(bucket))
				counts[i][bucket] += 1
				break

def saveState():
	print("SAVING-------")
	# Print Titles
	out = open("output.csv","w")
	out.write("Time,TotalChecked")
	for j in range(tickerCount):
		out.write(',' + str(tickerArray[j][0]))

	for i in range(tickerCount):
		maxVal = 0
		for j in range(numBuckets):
			if counts[i][j] > maxVal:
				maxVal = counts[i][j]

		if maxVal < 1:
			continue
	out.write("\n")

	for i in range(numBuckets):
		out.write(str(i) + ',' + str(checked_inBuck[i]))
		for j in range(tickerCount):
			out.write(',' + str(counts[j][i]))
		out.write("\n")

def checkMentions(subredditName, iterative):
	# submissions = 0
	maxTime = 0
	timeSet = 0
	for submission in reddit.subreddit(subredditName).new(limit = None):
		iterative += 1
		if iterative > 50:
			saveState()
			iterative = 0
		# submissions += 1
		# print(submission.title)

		#Check title
		time = m.floor(submission.created_utc/bucketInterval)
		if timeSet == 0:
				timeSet = 1
				maxTime = time
				print(str(maxTime) + "----------------------------------------------------------------------------------------------------------------------------------------")

		bucket = numBuckets - 1 + time - maxTime
		print(bucket)
		if bucket < 0:
			# print("SSB:" + str(bucket))
			continue
		checkString(submission.title.lower(),bucket)

		submission.comments.replace_more(limit=2)
		for comment in submission.comments:
			iterative += 1
			if iterative > 50:
				saveState()
				iterative = 0
			#Check comments
			time = m.floor(comment.created_utc/bucketInterval)


			bucket = numBuckets - 1 + time - maxTime
			if bucket < 0:
				continue
			checkString(comment.body.lower(),bucket)
			# commentCount += 1


# submissions = 0
checkMentions("satoshistreetbets", iterative)
print("WSB TIME BABEY __________________________________________________________________________________")
checkMentions("wallstreetbets", iterative)

saveState()