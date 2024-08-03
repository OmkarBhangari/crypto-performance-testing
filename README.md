# Crypto Performance Testing

This repository contains a comprehensive Python script designed for evaluating the performance of various cryptographic algorithms. It includes functionalities for RSA encryption/decryption, ECDSA signing/verification, and AES encryption/decryption of images. The script measures and visualizes the performance of these algorithms, providing insights into their efficiency and security.

## Features

- **RSA Encryption/Decryption**: Measures the performance of RSA encryption and decryption operations. Includes key generation, encryption, and decryption time metrics.
- **ECDSA Signing/Verification**: Evaluates the performance of ECDSA (Elliptic Curve Digital Signature Algorithm) for signing and verifying data. Provides timing metrics for key generation, signing, and verification.
- **AES Image Encryption/Decryption**: Demonstrates AES (Advanced Encryption Standard) encryption and decryption applied to image files. Shows how AES can be used to secure image data.
- **Performance Metrics Visualization**: Generates plots of performance metrics for RSA and ECDSA operations. Helps visualize the impact of data size on cryptographic performance.
- **CSV Export**: Saves detailed results of cryptographic tests, including key generation times, encryption times, and decrypted data, into CSV files for further analysis.

## Requirements

To run the script, you need Python 3.x and the following Python libraries:

- `pandas`: For data handling and CSV operations.
- `matplotlib`: For plotting performance metrics.
- `Pillow`: For image handling and manipulation.
- `numpy`: For numerical operations and handling image data.
- `cryptography`: For cryptographic operations including RSA, ECDSA, and AES.

Install the required libraries using pip:

```bash
pip install pandas matplotlib Pillow numpy cryptography
