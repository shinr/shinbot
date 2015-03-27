# sample plugin
# methods:
# init() - ran at load
# run(message) - when a privmsg is received

# input = message
# return = tuple(target, message) which is sent via privmsg
# 			or None for nullop
# target can be a channel or a user
# quite basic atm
# just loops back to the sender what was said
def run(message):
	return (message[0].split('!')[0], ' '.join(message[3:]))