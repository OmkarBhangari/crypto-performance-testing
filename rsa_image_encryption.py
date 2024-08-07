# -*- coding: utf-8 -*-
"""rsa_image_encryption.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f6reR8Kjfql7mn1tZ-zoGISu-UqcV5tG
"""

import hashlib
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
import os

def generate_random_data(size):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=size))

def test_asymmetric_algorithm(data, key_size=512):
    max_data_size = key_size // 8 - 2 * hashes.SHA256().digest_size - 2
    chunks = [data[i:i + max_data_size] for i in range(0, len(data), max_data_size)]
    encrypted_chunks = []
    decrypted_chunks = []

    try:
        start_time = time.time()
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        end_keygen_time = time.time()

        public_key = private_key.public_key()

        for chunk in chunks:
            ciphertext = public_key.encrypt(
                chunk.encode(),
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            encrypted_chunks.append(ciphertext)
        end_encryption_time = time.time()

        for encrypted_chunk in encrypted_chunks:
            decrypted_text = private_key.decrypt(
                encrypted_chunk,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            decrypted_chunks.append(decrypted_text)
        end_decryption_time = time.time()

        return {
            "input_text": data,
            "private_key": private_key,
            "public_key": public_key,
            "ciphertext": b''.join(encrypted_chunks),
            "decrypted_text": b''.join(decrypted_chunks).decode(),
            "keygen_time": end_keygen_time - start_time,
            "encryption_time": end_encryption_time - end_keygen_time,
            "decryption_time": end_decryption_time - end_encryption_time
        }
    except Exception as e:
        print(f"An error occurred in asymmetric algorithm testing: {e}")
        return None

def test_ecdsa_algorithm(data):
    try:
        start_time = time.time()
        private_key = ec.generate_private_key(ec.SECP256R1())
        end_keygen_time = time.time()

        public_key = private_key.public_key()
        signature = private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
        end_signing_time = time.time()

        verification_result = public_key.verify(signature, data.encode(), ec.ECDSA(hashes.SHA256()))
        end_verification_time = time.time()

        return {
            "input_text": data,
            "private_key": private_key,
            "public_key": public_key,
            "signature": signature,
            "verification_result": verification_result,
            "keygen_time": end_keygen_time - start_time,
            "signing_time": end_signing_time - end_keygen_time,
            "verification_time": end_verification_time - end_signing_time
        }
    except Exception as e:
        print(f"An error occurred in ECDSA algorithm testing: {e}")
        return None

from PIL import Image
import numpy as np

def aes_encrypt_image(image, key):
    try:
        # Convert image to RGB if not already
        image = image.convert('RGB')
        image_bytes = np.array(image).tobytes()

        # Create AES cipher
        iv = bytes([random.randint(0, 255) for _ in range(16)])
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        encryptor = cipher.encryptor()

        # Encrypt the image bytes
        encrypted_image = encryptor.update(image_bytes) + encryptor.finalize()

        return encrypted_image, iv
    except Exception as e:
        print(f"An error occurred in AES encryption: {e}")
        return None, None

def aes_decrypt_image(encrypted_image, key, iv, image_size):
    try:
        # Create AES cipher
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        decryptor = cipher.decryptor()

        # Decrypt the image bytes
        decrypted_image_bytes = decryptor.update(encrypted_image) + decryptor.finalize()

        # Convert bytes back to image
        image_array = np.frombuffer(decrypted_image_bytes, dtype=np.uint8).reshape(image_size[1], image_size[0], 3)
        decrypted_image = Image.fromarray(image_array, 'RGB')

        return decrypted_image
    except Exception as e:
        print(f"An error occurred in AES decryption: {e}")
        return None


def plot_and_save_asymmetric_results(results, filename):
    try:
        input_sizes = list(results.keys())
        keygen_times = [results[size]['keygen_time'] for size in input_sizes]
        encryption_times = [results[size]['encryption_time'] for size in input_sizes]
        decryption_times = [results[size]['decryption_time'] for size in input_sizes]

        plt.plot(input_sizes, keygen_times, label='Key Generation Time', marker='o')
        plt.plot(input_sizes, encryption_times, label='Encryption Time', marker='o')
        plt.plot(input_sizes, decryption_times, label='Decryption Time', marker='o')
        plt.xlabel('Input Size (bytes)')
        plt.ylabel('Time (s)')
        plt.title('Asymmetric Algorithm Performance')
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting asymmetric results: {e}")

def plot_and_save_ecdsa_results(results, filename):
    try:
        input_sizes = list(results.keys())
        keygen_times = [results[size]['keygen_time'] for size in input_sizes]
        signing_times = [results[size]['signing_time'] for size in input_sizes]
        verification_times = [results[size]['verification_time'] for size in input_sizes]

        plt.plot(input_sizes, keygen_times, label='Key Generation Time', marker='o')
        plt.plot(input_sizes, signing_times, label='Signing Time', marker='o')
        plt.plot(input_sizes, verification_times, label='Verification Time', marker='o')
        plt.xlabel('Input Size (bytes)')
        plt.ylabel('Time (s)')
        plt.title('ECDSA Algorithm Performance')
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting ECDSA results: {e}")

def save_to_csv(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

# Testing
input_sizes = [256, 512, 1024, 2048, 4096]
data_samples = [generate_random_data(size) for size in input_sizes]

# Collect results
asymmetric_results = {}
ecdsa_results = {}

for data in data_samples:
    data_size = len(data)

    # Asymmetric encryption/decryption
    asym_result = test_asymmetric_algorithm(data)
    if asym_result:
        asymmetric_results[data_size] = {
            "input_text": asym_result["input_text"],
            "private_key": asym_result["private_key"],
            "public_key": asym_result["public_key"],
            "ciphertext": asym_result["ciphertext"],
            "decrypted_text": asym_result["decrypted_text"],
            "keygen_time": asym_result["keygen_time"],
            "encryption_time": asym_result["encryption_time"],
            "decryption_time": asym_result["decryption_time"]
        }

    # ECDSA signing/verification
    ecdsa_result = test_ecdsa_algorithm(data)
    if ecdsa_result:
        ecdsa_results[data_size] = {
            "input_text": ecdsa_result["input_text"],
            "private_key": ecdsa_result["private_key"],
            "public_key": ecdsa_result["public_key"],
            "signature": ecdsa_result["signature"],
            "verification_result": ecdsa_result["verification_result"],
            "keygen_time": ecdsa_result["keygen_time"],
            "signing_time": ecdsa_result["signing_time"],
            "verification_time": ecdsa_result["verification_time"]
        }

# Plot and save results for asymmetric algorithm
plot_and_save_asymmetric_results(asymmetric_results, "asymmetric_performance.png")

# Plot and save results for ECDSA algorithm
plot_and_save_ecdsa_results(ecdsa_results, "ecdsa_performance.png")

# Save asymmetric algorithm results to CSV
asymmetric_results_csv = []
for size, result in asymmetric_results.items():
    asymmetric_results_csv.append({
        "Input Size (bytes)": size,
        "Input Text": result["input_text"],
        "Private Key": result["private_key"].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode(),
        "Public Key": result["public_key"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode(),
        "Ciphertext": result["ciphertext"].hex(),
        "Decrypted Text": result["decrypted_text"],
        "Key Generation Time (s)": result["keygen_time"],
        "Encryption Time (s)": result["encryption_time"],
        "Decryption Time (s)": result["decryption_time"]
    })
save_to_csv(asymmetric_results_csv, "asymmetric_algorithm_results.csv")

# Save ECDSA algorithm results to CSV
ecdsa_results_csv = []
for size, result in ecdsa_results.items():
    ecdsa_results_csv.append({
        "Input Size (bytes)": size,
        "Input Text": result["input_text"],
        "Private Key": result["private_key"].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode(),
        "Public Key": result["public_key"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode(),
        "Signature": result["signature"].hex(),
        "Verification Result": result["verification_result"],
        "Key Generation Time (s)": result["keygen_time"],
        "Signing Time (s)": result["signing_time"],
        "Verification Time (s)": result["verification_time"]
    })
save_to_csv(ecdsa_results_csv, "ecdsa_algorithm_results.csv")

# Image encryption and decryption testing
image_path = '/content/Fina_output.jpg'
if os.path.exists(image_path):
    image = Image.open(image_path)
    image_size = image.size
    key = bytes([random.randint(0, 255) for _ in range(32)])

    # Encrypt the image
    encrypted_image, iv = aes_encrypt_image(image, key)
    if encrypted_image:
        # Decrypt the image
        decrypted_image = aes_decrypt_image(encrypted_image, key, iv, image_size)
        if decrypted_image:
            # Save the encrypted and decrypted images
            encrypted_image_path = 'encrypted_image.png'
            decrypted_image_path = 'decrypted_image.png'
            Image.frombytes('RGB', image_size, encrypted_image).save(encrypted_image_path)
            decrypted_image.save(decrypted_image_path)

            # Print paths for verification
            print(f"Encrypted image saved at: {encrypted_image_path}")
            print(f"Decrypted image saved at: {decrypted_image_path}")
        else:
            print("Decryption failed.")
    else:
        print("Encryption failed.")
else:
    print(f"Image file not found: {image_path}")

from google.colab import drive
drive.mount('/content/drive')