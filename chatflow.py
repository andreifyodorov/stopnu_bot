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


    def help(self):
        self.reply('I understand commands "help", "stat" and "add [topic]" to add topics')
        if self.context.topics:
            self.reply('Known topics are: %s' % ', '.join(self.context.topics))


    def stat(self):
        self.reply('Here are your stats')
        for k, v in self.context.stat.iteritems():
            self.reply('%s - %d' % (k, v))


    def add(self, topic=None):
        if topic is None:
            self.reply('Add what topic?')
            return 'add_what'
        else:
            self.reply('Add new topic "%s"?' % topic)
            self.context.new_topic = topic
            return 'add_confirm'


    def add_what(self, topic):
        return self.add(topic)


    def add_confirm(self, answer):
        if answer == "yes":
            self.context.topics.add(self.context.new_topic)
            self.reply("Added new topic %s" % self.context.new_topic)

        elif answer == "no":
            self.reply("Ok, what else can I do for you?")

        else:
            self.reply("Yes or no?")
            return 'add_confirm'


    def command(self, command):
        count = self.context.stat.get(command, 0) + 1
        self.context.stat[command] = count
        self.reply('Now it\'s %d %ss' % (count, command))


    def default(self, command):
        self.reply('I don\'t understand "%s"' % command)


    def process_message(self, text):
        tokens = text.lower().split(" ");  # tokenize

        if len(tokens) == 0:
            return

        self.context.state = self.dispatch(tokens)


    def dispatch(self, tokens):
        if self.context.state == 'add_what':
            return self.add_what(*tokens)

        if self.context.state == 'add_confirm':
            return self.add_confirm(*tokens)

        if self.context.state is None:
            command = tokens.pop(0)

            if command == 'help':
                return self.help()

            elif command == 'stat':
                return self.stat()

            elif command == 'add':
                return self.add(*tokens)

            elif command in self.context.topics:
                return self.command(command)

            else:
                return self.default(command)



if __name__ == '__main__':
    def output(msg):
        print msg

    context = ChatContext()
    chatflow = Chatflow(context, output)

    while True:
        try:
            s = raw_input('%s> ' % context.state)
        except (EOFError, KeyboardInterrupt):
            break
        chatflow.process_message(s)

