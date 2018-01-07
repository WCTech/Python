def base10ToBase26Letter(num):
        ''' Converts any positive integer to Base26(letters only) with no 0th case.
        Useful for applications such as spreadsheet columns to determine which
        Letterset goes with a positive integer.
        '''
        if num <= 0:
            return ''
        elif num <= 26:
            return chr(96 + num)
        else:
            return self.base10ToBase26Letter(
                int((num - 1) / 26)) + chr(97 + (num - 1) % 26)

    def base26LetterToBase10(string):
        ''' Converts a string from Base26(letters only) with no 0th case to a
        positive integer. Useful for figuring out column numbers from letters so
        that they can be called from a list.
        '''
        string = string.lower()
        if string == ' ' or len(string) == 0:
            return 0
        if len(string) == 1:
            return ord(string) - 96
        else:
            return self.base26LetterToBase10(string[1:]) \
                + (26**(len(string) - 1)) \
                * (ord(string[0]) - 96)