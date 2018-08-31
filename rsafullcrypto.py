# RSA Cipher 

__author__ = 'Ahmad M Ameen <ahmadmameen7@gmail.com>'
__copyright__ = 'Copyright (c) 2018, algebra'
__version__ = "1.1"

import sys, os

print()
print('-'*80)
info = input('\t\tThis is RSA encrypting/decrypting software, \n\t\tdeveloped by Ahmad M Ameen (Algebra). \n\t\tPress enter to proceed.')
print('-'*80)
print()
os.getcwd()
my_dir = input('Enter your path to the files folder: ')
os.chdir(my_dir)

DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.


def main():
    filename = 'encrypted.txt'
    print()
    mode = input('Enter mode: ')
    name = ('%sed.txt' %(mode))
    print()
            
    if mode == 'encrypt':
        print()
        typ = input('Enter "file" if your message is inside a file or enter "self" if you want to write the message direct\n     : ')
        
        if typ == "file":
            txt_file = input('Enter name of the file: ')
            text = open(txt_file)
            content = text.read()
            message = content
        else:
            print()
            message = input('Enter text\n     :')
    
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print()
        print('Encrypting and writing to %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)
        
        print()
        print('Encrypted text:')
        print('=' * 80)
        print(encryptedText)
        print('='* 80)
        print('Full %sed text is saved to files directory.' %(mode))
        
        with open(name, 'w') as file:
            file.write(encryptedText)

    elif mode == 'decrypt':
        print()
        typ = input('Enter "file" if your message is inside a file or enter "self" if you want to write the message direct\n     : ')
        
        if typ == "file":
            text = open('encrypted.txt')
            content = text.read()
            message = content
        else:
            print()
            message = input('Enter text\n     :')

        privKeyFilename = 'al_sweigart_privkey.txt'
        print()
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)
        
        print()
        print('Decrypted text:')
        print('=' * 80)
        print(decryptedText)
        print('='* 80)
        print('Full %sed text is saved to files directory.' %(mode))
        
        with open(name, 'w') as file:
            file.write(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    
    messageBytes = message.encode('ascii') 
    
    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    keySize, n, e = readKeyFile(keyFilename)

    if keySize < blockSize * 8: 
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Either increase the block size or use different keys.' % (blockSize * 8, keySize))

    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)
    
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # Write out the encrypted string to the output file.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    # Also return the encrypted string.
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)

    # Read in the message length and the encrypted message from the file.
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    
    if keySize < blockSize * 8: 
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the keysize. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    # Convert the encrypted message into large int values.
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)

if __name__ == '__main__':
    main()
