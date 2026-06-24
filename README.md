# VoltForce
VoltForce (Versatile Offensive Login Tool) is an open-source Python tool for wordlist-based brute-force attacks. It is actively maintained by the developer and currently supports brute-forcing across nine different protocols. For more detailed information, please refer to the README.md file.

<img width="1169" height="132" alt="изображение" src="https://github.com/user-attachments/assets/40a97f4f-1ac8-4713-89b5-332b22dee81e" />

About the Tool

VoltForce is a tool designed for brute-force attacks. Currently, it can test the security of services such as SSH, FTP, SMB, Telnet, MySQL, PostgreSQL, Redis, MongoDB, and POP3, as well as perform SSH testing via key brute-forcing.

# Installation

```
git clone https://github.com/vesel4akProjects/VoltForce.git
cd VoltForce
pip install -r requirements.txt --break-system-packages
```

# Important note: The tool includes the `impacket` Python library. Windows Defender typically blocks its installation, as it flags it as malicious software. Be sure to disable your antivirus when installing on Windows.

To view all 51 of the tool's parameters, run:

```
python3 voltforce.py -h
```


# Description of all parameters


| Parameter name | What does the parameter do | Usage example |
|----------------|----------------------------|----------------|
| --host | A mandatory flag used to specify the target host for testing. | python3 voltforce.py --host "127.0.0.1" |
| -P/--passwords-list | A list of passwords to be tried. The list should contain passwords in a column. If you only need to specify one password, create a list with only one password or use --single-password flag | python3 voltforce.py --host "127.0.0.1" -P "passwords.txt" |
| -U/--usernames-list | List of usernames to check. The list must contain usernames in the column. If you only need to specify one username, create a list with only one username or use --single-username flag | python3 voltforce.py --host "127.0.0.1" -U "users.txt" |
| -t/--timeout | Timeout between connection attempts in seconds. For real attacks, it's best to set it to at least 60 seconds. The initial value is 0.1 seconds | python3 voltforce.py --host "127.0.0.1" -t 0.5 |
| -siu/--single-username | This flag is used to specify the username for brute-force attacks. Knowing the username will speed up the brute-force attack. | python3 voltforce.py --host "127.0.0.1" -siu "admin" |
| -sip/--single-password | This flag is used to specify the password. If you know the password but not the username, you can speed up the brute-force attack. Can be combined with the --single-username flag. | python3 voltforce.py --host "127.0.0.1" -sip "password123" |
| -G/--general-wordlist | This flag is used to specify wordlists that store values line by line in the 'username:password' format. After specifying this flag, you don't need to specify the -P or -U flags. | python3 voltforce.py --host "127.0.0.1" -G "creds.txt" |
| -sr/--save-results | This flag is used to save successful connection attempts to a target file. | python3 voltforce.py --host "127.0.0.1" -sr "results.txt" |
| -d/--delay | Delay before starting work in seconds | python3 voltforce.py --host "127.0.0.1" -d 5 |
| -shu/--shuffle | Shuffle wordlists before starting | python3 voltforce.py --host "127.0.0.1" -shu |
| -shuc/--shuffle-count | This flag controls how many times to mix the password. By default, VoltForce mixes passwords 10 times. | python3 voltforce.py --host "127.0.0.1" -shu -shuc 5 |
| --seed/--shuffle-seed | A flag is used to specify a custom seed for shuffling. Specify an integer, and shuffling will work the same way. | python3 voltforce.py --host "127.0.0.1" -shu --seed 42 |
| -q/--quiet | Disables all console output. VoltForce won't notify you of any messages, but this mode enables logging, and all data will be written there. | python3 voltforce.py --host "127.0.0.1" -q |
| -b/--banner | Show banner and exit | python3 voltforce.py -b |
| -thr/--threads | The number of threads to be checked. The higher the number of threads, the more noise and activity will be in the logs. The initial value is 5 threads. | python3 voltforce.py --host "127.0.0.1" -thr 10 |
| -pb/--progress-bar | Progress bar to show the process of searching and counting the number of combinations. | python3 voltforce.py --host "127.0.0.1" -pb |
| -npb/--no-progress-bar | Forces the progress bar to be disabled if someone changes the tool's values or decides not to include it. | python3 voltforce.py --host "127.0.0.1" -npb |
| -p/--port | Specifies the port for further connections. Brute-force functions use default ports for connections; for example, SSH uses port 22. | python3 voltforce.py --host "127.0.0.1" -p 2222 |
| -mr/--max-retries | This setting controls the maximum number of connection attempts to the host. Once the maximum number of connection attempts is reached, VoltForce will shut down. | python3 voltforce.py --host "127.0.0.1" -mr 100 |
| -o/--output-file | This parameter is responsible for logging all program actions. | python3 voltforce.py --host "127.0.0.1" -o "log.txt" |
| -nl/--no-log | Forces logging to be disabled if someone changes the tool's values or decides not to enable logging. | python3 voltforce.py --host "127.0.0.1" -nl |
| -ko/--keep-open | This flag ensures that we don't close the connection after the first login credentials are detected. Specifying this flag will save you connection time. | python3 voltforce.py --host "127.0.0.1" -ko |
| -e/--exec/--execute | This flag is used to execute arbitrary commands after gaining privileges. Specify a command that VoltForce will execute immediately after receiving the required data. | python3 voltforce.py --host "127.0.0.1" -e "whoami" |
| -rt/--random-timeout | This flag is used to specify a range of values that will be selected using cryptographically strong randomness based on the entropy of your OS and used as a random timeout. | python3 voltforce.py --host "127.0.0.1" -rt 0.5-2.0 |
| -ht/--host-timeout | This flag controls the timeout between host tests. If you're testing more than one host, after testing one host, there will be a delay of the specified number of seconds before testing the next host. | python3 voltforce.py --host "127.0.0.1" -ht 10 |
| -ie/--ignore-errors | This flag is used to ignore errors. If this flag is enabled, VoltForce will stop displaying any error or warning messages and continue running. | python3 voltforce.py --host "127.0.0.1" -ie |
| -so/--success-only | This flag is used to output only successful data search attempts to the console. If you specify this flag, the program may appear to hang. However, the brute-force process will still continue. | python3 voltforce.py --host "127.0.0.1" -so |
| -mt/--max-time | Maximum operating time | python3 voltforce.py --host "127.0.0.1" -mt 300 |
| -nc/--no-color | Color output will be disabled | python3 voltforce.py --host "127.0.0.1" -nc |
| -m/--mode | The tool's operating mode. By default, the search mode is SSH. Available modes: ssh, ftp, smb, telnet, mysql, postgres, redis, mongodb, pop3, ssh-key | python3 voltforce.py --host "127.0.0.1" -m ftp |
| --log-mode | Log mode: w = overwrite, a = append (default: a) | python3 voltforce.py --host "127.0.0.1" --log-mode w |
| -H/--hosts-list | List of hosts in the file. To specify targets. Hosts should be specified in a column. | python3 voltforce.py -H "hosts.txt" |
| -sk/--ssh-key | This flag is used to specify the SSH authorization key. You only need to specify the path to the key file. You must also select the ssh-key mode using the --mode flag. | python3 voltforce.py --host "127.0.0.1" -m ssh-key -sk "id_rsa" |
| -kl/--keys-list | This flag is used to specify a file containing a list of paths to keys for SSH authentication. The flag should contain a wordlist containing file paths in a column. | python3 voltforce.py --host "127.0.0.1" -m ssh-key -kl "keys.txt" |
| -nb/--no-banner | Don't show the banner | python3 voltforce.py --host "127.0.0.1" -nb |
| -sa/--socks5-address | A flag for specifying a SOCKS5 proxy address that hides the real IP address. If you want to use the TOR network as a SOCKS5 proxy, first start the TOR service itself and then specify the address 127.0.0.1. | python3 voltforce.py --host "127.0.0.1" -sa "127.0.0.1" |
| -sp/--socks5-port | Parameter for specifying the SOCKS5 proxy port. If you want to use the Tor network as a proxy, first start the Tor service and then specify port 9050. | python3 voltforce.py --host "127.0.0.1" -sa "127.0.0.1" -sp 9050 |
| -su/--socks5-username | Flag for specifying the username for the SOCKS5 proxy. If your SOCKS5 proxy doesn't require a username, do not specify this parameter. | python3 voltforce.py --host "127.0.0.1" -sa "127.0.0.1" -su "user" |
| -spas/--socks5-password | Flag for specifying a password for the SOCKS5 proxy. If your SOCKS5 proxy does not require a password, do not specify this parameter. | python3 voltforce.py --host "127.0.0.1" -sa "127.0.0.1" -spas "pass" |
| -s/--stop-on-success | Stops the program after finding at least one login and password | python3 voltforce.py --host "127.0.0.1" -s |
| -time/--timer | Show execution time at the end | python3 voltforce.py --host "127.0.0.1" -time |
| -ru/--reverse-usernames | Reverse the usernames wordlist order | python3 voltforce.py --host "127.0.0.1" -ru |
| -rp/--reverse-passwords | Reverse the passwords wordlist order | python3 voltforce.py --host "127.0.0.1" -rp |
| --min-length-username | Minimum username length to try | python3 voltforce.py --host "127.0.0.1" --min-length-username 4 |
| --max-length-username | Maximum username length to try | python3 voltforce.py --host "127.0.0.1" --max-length-username 16 |
| --min-length-password | Minimum password length to try | python3 voltforce.py --host "127.0.0.1" --min-length-password 6 |
| --max-length-password | Maximum password length to try | python3 voltforce.py --host "127.0.0.1" --max-length-password 20 |
| -nd/--no-duplicates | Remove duplicate entries from wordlists | python3 voltforce.py --host "127.0.0.1" -nd |
| -db/--delay-between | Delay between attempts on the same host (seconds) | python3 voltforce.py --host "127.0.0.1" -db 0.5 |

<img width="1316" height="480" alt="изображение" src="https://github.com/user-attachments/assets/8d5bbb05-7569-4a78-aa40-c65d863923f9" />

# Use case

This tool can be safely used in brute-force attacks against wordlists. Below is an example of a typical usage command:

```
python3 voltforce.py --host "110.124.65.231" -P "/usr/share/dirb/wordlists/common.txt" -siu "root" --timeout 0 --mode "ftp" --port 21 -o report.txt -sr "result.txt" -d 5 -shu -thr 200 -ie --timer
```

<img width="1300" height="177" alt="изображение" src="https://github.com/user-attachments/assets/dae3c635-4ece-4279-aacb-adf78c83d649" />



This example demonstrates a typical usage scenario. All output from VoltForce is quite minimalistic. Important note: the more threads, the greater the load on your system. If you have too many threads, you will quickly be blocked by the IDS in real attacks. For seamless use, be sure to use the --random-timeout flag to specify the random timeout radius during testing, the --delay-between flag to specify delays between tests, and the very interesting --shuffle flag, which will shuffle your wordlists as many times as desired. The number of shuffles can be specified using the --shuffle-count flag.



