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

<img width="545" height="89" alt="изображение" src="https://github.com/user-attachments/assets/4db8f645-6b64-4885-95a2-acb13216f0d6" />

You can also use a SOCKS5 proxy. This is done using the --socks5-address,--socks5-port,--socks5-username and --socks5-password flags. You can launch the Tor service and carry out the attack through it by simply specifying the address and port. If you wish to use a private proxy, you can also provide a username and password.

To reduce your chances of getting banned by IDS, I recommend using the --random-timeout, --host-timeout, --delay-between, and --max-time flags. Using the first flag, you can specify a range of values ​​to use as the timeout. --host-timeout controls the timeout when testing multiple hosts. You can also specify multiple hosts for testing using the --hosts-list flag. --delay-between will add delays before testing, and the --max-time flag allows you to specify a specific runtime for the program. Here's an example command with all these flags:

```
python3 voltforce.py --hosts-list "hosts.txt" -P "passwords.txt" -U "users.txt" --random-timeout "1-30" --host-timeout 300 --delay-between 4 --max-time 300
```


You can specify only one username or one password when testing using the --single-username and --single-password flags, respectively. You can also specify the --stop-on-success flag to terminate the test after the credentials are found.

I'd like to mention a few more important flags. I think the most interesting are the --reverse-usernames and --reverse-passwords flags. They allow you to reverse wordlists for usernames and passwords, respectively. This flag is very useful when you've already checked part of a wordlist and need to check the last passwords in the list.
The --no-duplicates flag is equally useful. It removes duplicates from both wordlists. This is a very useful flag; it allows you to bypass checking wordlists for duplicates.
The --general-wordlist flag is also very useful. Instead of two wordlists, you can specify a single wordlist where usernames and passwords should be written in a columnar format, "username:password." This way, you don't have to waste time specifying two wordlists.
Another cool and useful flag is --ignore-errors. It will ignore all program errors and continue working.
As for the last useful flags, I can't help but mention the --min-length-username, --max-length-username, --min-length-password, and --max-length-password flags. These can filter your wordlist by the minimum and maximum lengths of usernames and passwords, respectively. Sorting can take time, O(n) to be exact, but it's worth it. This flag is incredibly useful.

# Brute-Forcing with SSH Keys

VoltForce supports brute-force mode with SSH keys. To do this, you'll need to specify the --ssh-key flag. It's essentially the same as the --single-password flag. You only need to specify the path to the key file. Paramiko will detect the key type automatically. After specifying the wordlist with usernames and the target key, the brute-force process will begin. You can also specify the --keys-list flag. This is the same as --passwords-list. You should specify the paths to the target keys in the column. I decided to break this mode into a separate paragraph because it's essentially a hack. In the main code, it's actually substituted into the password field. It can confuse the user when analyzing the code, so I decided to write about it. You can easily use --passwords-list instead of --keys-list , and nothing will change, but I don't see the point unless you're really lazy.

# Connections and Arbitrary Code Execution

Yes, VoltForce can do that too. This mode is currently in testing, but you can already execute arbitrary code for SSH, Telnet, Redis, MySQL, and PostgreSQL after receiving login credentials. VoltForce activates interactive mode, and it will print the command output. This flag is super useful, but still rather crude. This is where the --keep-open flag comes in. It allows you to keep the connection open after receiving the data. This flag is useful when you need to immediately begin executing commands.

# Parameters that can be used

Here I'll mention some flags. Similar ones include: --banner, --no-banner, --delay, --quiet, --timer, and --shuffle-seed.
--banner only displays the logo and exits. Honestly, I don't even know where such a flag would be useful.
--no-banner, on the other hand, will simply not display the banner.
--delay will delay before running the specified number of seconds.
--quiet will not output anything at all. You might think the program is working incorrectly, but that's a lie. Logs will be written, and all attempts will be saved to the log file. If logging isn't enabled, this flag will enable it automatically.
--timer will start a timer for the entire run and display the total run time at the end of the program. This flag is simply useful.
--shuffle-seed allows you to specify a custom seed for shuffling the wordlist. You need to specify any positive integer. The seed allows you to specify a custom sort order. Use this flag with caution, as a poor seed will make the shuffling non-random.

# About logging, threads, and the progress bar

Let's start with logging. You can specify it using the -o parameter. If you don't specify a logging filename, VoltForce will create one named after the current date. The logging will record everything in detail. The time in the logging will be the most accurate date possible, including five decimal places for seconds. The message type will also be displayed. For example, if a parameter is being tested, the word "TESTING" will be displayed. Next, the service being tested and the logging message itself will be listed. This approach will ensure the most accurate logging for future security audits. You can disable logging using the --no-log flag.
Now about threads. You can specify them using the -thr flag. By default, VoltForce uses 10 threads. Threads increase the speed by a factor of N, meaning that opening two threads will cut the search time in half. The more threads you have, the more connections you'll have, which means a higher chance of being blocked by IDS. Therefore, avoid using too many threads, especially if you have a slower PC.
You can also specify the --progress-bar flag, which will display a progress bar showing your progress.Since the tqdm library is not thread-friendly, VoltForce will automatically disable it if the number of threads exceeds 15. Disabling this feature will cause tqdm to become extremely slow. You can also forcefully disable the progress bar using the --no-progress-bar flag. Therefore, if you want to perform an effective scan with a large number of threads and don't want to be banned by the IDS, use flags that reduce the chance of being banned. I've already listed them.

# Disclaimer

The author assumes no liability for the unauthorized use of this tool to obtain credentials. This tool is intended and used exclusively for legitimate security testing and testing of services on servers. Do not use it for malicious purposes!

# License

This tool is distributed under the MIT license. So to prevent you from opening the LICENSE file, I will write its contents here:

```

MIT License

Copyright (c) 2026 Vesel4ak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,
OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

# About tool improvements

This tool is truly a great thing. I plan to introduce many new flags and make it on par with giants like Hydra. At a minimum, we plan to add the --mutate flag to specify a target file containing multiple different strings for mutating logins and passwords. I think it will be a very useful flag. I'd also like to add the --resume flag so that, like in Hydra, you could pause and resume from a specific point after stopping. Another useful feature, I think, would be the introduction of brute-force mode for S3 buckets. I think this feature is really cool, and I only noticed it in the GObuster tool. I think it's truly a cool feature. Accordingly, since we're talking about web testing, it would be worth adding brute-force authentication for web pages like login.php. This would take the tool to the next level and allow it to be turned into something like WFUZZ or something similar. I'm also considering adding the --proxy-list flag, where you can specify a column of proxies for testing. Therefore, brute-forcing web forms will allow you to add HTTP proxies. Honestly, a tool like this could be developed almost endlessly. You could add 200 new flags, but then the usefulness of those flags becomes questionable. I think my latest addition suggestions are truly necessary and useful. I hope at least one person will be able to use this tool. It does, however, brute-force passwords and usernames quite quickly thanks to its multithreading. That's what saves it. You can run a tool like this on powerful computers and open multiple threads for maximum performance. Please, if you're a casual GitHub user, give this tool a try. I assure you, you won't regret it. I know the code is still pretty raw as of 2026. There are a lot of bugs, but I'm trying to fix them. Right now, you can safely use most of the parameters; they all work, though some are still buggy. And please, find me a single brute-forcer online that can provide such a flexible set of parameters for security testing.
