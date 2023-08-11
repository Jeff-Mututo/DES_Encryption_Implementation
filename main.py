from des import DesKey
from twilio.rest import Client
import secrets, string, os, keys

cipher_dict = {}

# Authenticate/Login with Twilio
client = Client(keys.account_sid, keys.auth_token)

############################
# Generate Key
############################
def random_string(size):
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(secrets.choice(letters) for i in range(size))

############################
# Display All
############################
def displayAll():
    os.system('cls')
    print('Cipher Texts:')
    for i in range(len(cipher_dict)):
        print(f'ID: {i} | Cipher: {cipher_dict[i]}')

############################
# Encryption
############################
def encrypt():
    key = random_string(8)
    #print(f'Key: {key}')
    encoded_key = bytes(key, 'ascii')
    key0 = DesKey(encoded_key)

    msg = input('Enter Msg: ')
    encoded_msg = bytes(msg, 'ascii')

    ciphertext = key0.encrypt(encoded_msg, padding=True)
    cipher_dict_len = len(cipher_dict)
    cipher_dict[cipher_dict_len] = ciphertext

    input('Press Enter To Continue...')

    twilio_msg = client.messages.create(
        body=f'DES Algorithm\nCipher ID: {cipher_dict_len}\nKey: {key}',
        from_=keys.twilio_number,
        to=keys.target_number
    )

###########################
# Decryption
###########################
def decrypt():
    cipher_id = input('Enter Cipher ID: ')
    cipher_id = int(cipher_id)
    ciphertext = cipher_dict[cipher_id]

    encoded_key = bytes(input('Enter Key: '), 'ascii')
    key0 = DesKey(encoded_key)

    try:
        plaintext = key0.decrypt(ciphertext, padding=True)
        plaintext = str(plaintext, 'ascii')
        print(f'\nPLAINTEXT: {plaintext}\n')
    except:
        print('Invalid Key!')
    
    input('Press Enter To Continue...')

############################
# Working
############################
while True:
    displayAll()

    print('\nPress 1 to encrypt a new message')
    print('Press 2 to decrypt a cipher text')
    choice = input('>: ')
    if choice == '1':
        encrypt()
    elif choice == '2':
        decrypt()
    elif choice == 'q':
        break
    else:
        print('Invalid Choice!')

# Clear Screen and Exit
os.system('cls')
exit()