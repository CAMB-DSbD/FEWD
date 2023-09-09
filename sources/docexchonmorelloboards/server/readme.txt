

4 Jun 2023, carlos.molina@cl.cam.ac.uk

https://stackoverflow.com/questions/16056135/how-to-use-openssl-to-encrypt-decrypt-files



1) I'm encrypting the file simon.txt which is located in my 
   current folder. Mac Book air, macOS Catalina Version 10.15.7


2) bash-3.2$ openssl version
OpenSSL 3.1.1 30 May 2023 (Library: OpenSSL 3.1.1 30 May 2023)



bash-3.2$ openssl aes-256-cbc -e -salt -pbkdf2 -iter 10000 -in cat.jpg -out cat_encrypted.dat
enter AES-256-CBC encryption password:
Verifying - enter AES-256-CBC encryption password: /* XXXXX */
bash-3.2$ 

bash-3.2$ openssl aes-256-cbc -d -salt -pbkdf2 -iter 10000 -in cat_encrypted.dat -out cat_decrypted.jpg
enter AES-256-CBC decryption password: /* XXXXXX */


/*
 * cat_decrypted.jpg  is correct
 */



