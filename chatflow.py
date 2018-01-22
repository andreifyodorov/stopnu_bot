#!/usr/bin/env python

class ChatContext(object):
    def __init__(self):
        self.state = None
        self.topics = set()
        self.stat = dict()


class Chatflow(object):
    def __init__(self, context, reply_callback):
        self.context = context
        self.reply = reply_callback


    def process_message(self, text):
        tokens = text.lower().split(" ");  # tokenize

        if len(tokens) == 0:
            return

        if self.context.state == 'add_what':
            tokens.insert(0, 'add')
            self.context.state = None

        if self.context.state == 'add_confirm':
            command = tokens.pop(0)
            if command == "yes":
                self.context.state = None
                self.context.topics.add(self.context.new_topic)
                self.reply("Added new topic %s" % self.context.new_topic)
                return
            elif command == "no":
                self.context.state = None
                self.reply("Ok, what else can I do for you?")
                return
            else:
                self.reply("Yes or no?")

        if self.context.state is None:
            command = tokens.pop(0)

            if command == 'help':
                self.reply('I understand commands "help", "stat" and "add [topic]" to add topics')
                if self.context.topics:
                    self.reply('Known topics are: %s' % ', '.join(self.context.topics))

            elif command == 'stat':
                self.reply('Here are your stats')
                for k, v in self.context.stat.iteritems():
                    self.reply('%s - %d' % (k, v))

            elif command == 'add':
                if len(tokens) == 0:
                    self.context.state = 'add_what'
                    self.reply('Add what topic?')
                else:
                    self.context.state = 'add_confirm'
                    self.context.new_topic = tokens.pop(0)
                    self.reply('Add new topic "%s"?' % self.context.new_topic)

            elif command in self.context.topics:
                count = self.context.stat.get(command, 0) + 1
                self.context.stat[command] = count
                self.reply('Now it\'s %d %ss' % (count, command))

            else:
                self.reply('I don\'t understand "%s"' % command)





if __name__ == '__main__':
    def output(msg):
        print msg

    chatflow = Chatflow(ChatContext(), output)

    while True:
        try:
            s = raw_input('> ')
        except (EOFError, KeyboardInterrupt):
            break
        chatflow.process_message(s)

