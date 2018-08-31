# RSA-Cipher

This is Software was developed by i Ahmad M Ameen, which is for RSA encryption/decryption.
Please note that the software can only decrypt a text that was encrypted using the same private key(using this software),
so the software is not for hacking cipher but for encryption/decryption of your private(secret) texts.
In this project there is an additional RSA public/private key generator that a user should run first before encrypting,
or decrypting any text.

HOW TO USE

As earlier stated, a user should firstly run the makeRsaKeys.py file. You will be prompt to enter the path of the files directory,
defending on the directory you clone the project in.
After running the majeRsaKeys.py file, two new files will created by the program their and will be saved in the files directory,
those two files are your puclic and private keys which the rsafullcrypto will make use of to encrypt/decrypt your given text.

After that, you then run the rsafullcrypto.py and give the required info to the program, and all your encrypted/decrypted files
will be saved in the files directory.

NOTE

Make sure that you have python3 installed in your machine.
