class Printer:
    def __init__(self):
        self.red = '\033[1;31;1m{}\033[0m'
        self.green = '\033[1;32;1m{}\033[0m'
        self.blue = '\033[1;33;1m{}\033[0m'

    def info(self, message):
        return self.blue.format('[*] ' + message)

    def error(self, message):
        return self.red.format('[-] ' + message)

    def prompt(self, message):
        return self.green.format('[+] ' + message)

    def normal(self, message):
        return message

    def hello(self,message):
        print(self.red.format(message))


printer = Printer()
