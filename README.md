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


# Key Flags

