# Braille dictionary
braille_dict = {
    # Letters
    'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..', 'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..',
    'i': '.OO...', 'j': '.OOO..', 'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.', 'p': 'OOO.O.',
    'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.', 'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO',
    'y': 'OO.OOO', 'z': 'O..OOO',

    # Numbers
    '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..', '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..',
    '9': '.OO...', '0': '.OOO..',

    # Symbols
    ' ': '......',
    ',': '..O...',
    '.': '..OO.O',
    '!': '..OOO.',
    '?': '..O.O.',
    ';': '..O.O.',
    ':': '..OO..',
    '-': '......O',
    "'": '....O.',
    '"': '....OO',
    '(': '..OOO.',
    ')': '..OOO.',
    '#': '.O.OOO',
    'capital': '.....O',
    'number': '.O.OOO'
}

class Translator:
    def __init__(self):
        self.braille_dict = braille_dict
        self.inverse_braille_dict = {v: k for k, v in self.braille_dict.items()}
        self.number_mode = False
        self.capital_mode = False

    def is_braille(self, text):
        """
        Check if the input is in Braille or English.
        Braille will have dots (.) and Os (representing raised dots).
        """
        return all(char in "O." for char in text)

    def translate_char_to_braille(self, char, capitalize=False):
        """
        Translate a single character to Braille using the dictionary.
        If capitalize is True, add a capital symbol.
        """
        char = char.lower()
        braille_char = self.braille_dict.get(char, '......')
        if capitalize:
            braille_char = self.braille_dict['capital'] + braille_char
        return braille_char

    def translate_word_to_braille(self, word):
        """
        Translate a word to Braille, handling numbers and capitalization.
        """
        braille_word = []
        number_mode = False

        for char in word:

            if char.isdigit():
                if not number_mode:
                    braille_word.append(self.braille_dict['number'])
                    number_mode = True
                braille_word.append(self.braille_dict[char])

            elif char.isalpha():
                if number_mode:
                    braille_word.append(self.braille_dict[' '])
                    number_mode = False
                if char.isupper():
                    braille_word.append(self.braille_dict['capital'])
                braille_word.append(self.translate_char_to_braille(char))

            elif char == ' ':
                if number_mode:
                    number_mode = False
                braille_word.append(self.braille_dict[' '])

        return ''.join(braille_word)

    def translate_text_to_braille(self, text):
        """
        Translate the entire input text to Braille.
        """
        braille_output = []
        words = text.split(' ')
        for i, word in enumerate(words):
            braille_output.append(self.translate_word_to_braille(word))
            if i < len(words) - 1:
                braille_output.append(self.braille_dict[' '])
        return ''.join(braille_output)

    def translate_braille_to_english(self, braille_text):
        """
        Translate Braille to English by first handling number sequences and then translating the rest.
        """
        output = []
        i = 0
        while i < len(braille_text):
            symbol = braille_text[i:i + 6]
            i += 6


            if symbol == self.braille_dict['number']:
                self.number_mode = True
                continue  # Skip to the next symbol


            elif symbol == self.braille_dict['capital']:
                self.capital_mode = True
                continue


            elif symbol == self.braille_dict[' ']:
                output.append(' ')
                self.number_mode = False
                continue


            if self.number_mode:
                for number, braille_code in self.braille_dict.items():
                    if braille_code == symbol and number.isdigit():
                        output.append(number)
                        break
                continue


            for key, value in self.braille_dict.items():
                if value == symbol:
                    if self.capital_mode:
                        output.append(key.upper())
                        self.capital_mode = False
                    else:
                        output.append(key)
                    break

        return ''.join(output)

    def translate(self, text):
        """
        The main function to check if the text is English or Braille,
        and call the appropriate translation method.
        """
        if self.is_braille(text):
            return self.translate_braille_to_english(text)
        else:
            return self.translate_text_to_braille(text)



def main():

    translator = Translator()


    input_text = input("Enter text to translate: ")


    translated_text = translator.translate(input_text)
    print(f"{translated_text}")

if __name__ == "__main__":
    main()
