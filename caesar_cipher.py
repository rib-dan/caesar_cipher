
import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text=text
        self.valid_words=load_words("words.txt")

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        #Creates auxiliary variables
        lower_letters = string.ascii_lowercase
        upper_letters = string.ascii_uppercase
        shift_map={}
        aux_upper = {}
        
        #Assert that shift's value is valid
        assert shift < 26 and shift >=0, "shift's value should be between 0 and 26"
        
        #Iterate through the alfabet and apply the shift
        for i in range(0,26):
            if i+shift>=26:
                rounding_aux = i+shift-26
            else:
                rounding_aux = i+shift
            shift_map[lower_letters[i]] = lower_letters[rounding_aux]
            aux_upper[upper_letters[i]] = upper_letters[rounding_aux] 
            
        shift_map.update(aux_upper)
        
        #return the dictionary mapping the original characters to the new ones
        return shift_map
    
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        
        #List of punctuation to ignore on the original message
        punctuation = " .,:;!?-"
        #Auxiliary variable to store the shifted message
        shifted_message = ''
        #Get the shift map for encription
        shift_map = self.build_shift_dict(shift)
        
        #Iterates through message to apply the shift
        for letter in self.message_text:
            if letter not in punctuation:
                shifted_message = shifted_message+shift_map[letter]
            else:
                shifted_message = shifted_message+letter
        #Return the shifted message
        return shifted_message
        
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        #Inherits the initialization from Message class
        Message.__init__(self, text)
        
        #Initializes the other attributes
        self.shift=shift
        self.encryption_dict=Message.build_shift_dict(self, shift)
        self.message_text_encrypted=Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        shift_return = self.shift
        return(shift_return)

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.shift=shift
        self.encryption_dict=Message.build_shift_dict(self, shift)
        self.message_text_encrypted=Message.apply_shift(self, shift)



class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        #Inherits Message's class initialization
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        #Create auxiliary variables
        aux_message = ''
        valid_max=-10000
        valid_counter = 0
        max_valid_shift = 0
        
        #Iterates through the alphabet
        for shift in range(1,26):
            #Apply reverse shift
            aux_message = self.apply_shift(26-shift)
            
            #Iterates through the result of the reverse shift to count the number of valid words
            for word in aux_message.split():
                if is_word(self.valid_words, word) == True:
                    valid_counter = valid_counter+1
                    
            #Updates variables if number of valid words is higher than the previous max
            if valid_counter>valid_max:
                valid_max = valid_counter
                max_valid_shift=shift
            valid_counter = 0
            
        #Return best shift and decoded message
        return [max_valid_shift, self.apply_shift(26-max_valid_shift)]

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    msg = PlaintextMessage("Hello Sire!",5)
    print("Original message: ", msg.get_message_text())
    print("Encrypted message: ", msg.get_message_text_encrypted())
    decode_msg = CiphertextMessage(msg.message_text_encrypted)
    print("Decoded message: ", decode_msg.decrypt_message()[1])
