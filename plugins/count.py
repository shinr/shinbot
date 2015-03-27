count = 0

def run(message):
	global count
	sender = message[0].split('!')[0]
	message = message[3]
	if message == "!count":
		count += 1
		return (sender, "count is now "+ str(count))
	return None