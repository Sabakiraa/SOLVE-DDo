import os
from colorama import init, Fore, Style


init()

def print_colored_text(text, color):
    
    colored_text = f'{color}{text}{Style.RESET_ALL}'

   
    print(colored_text)


print_colored_text("╦╔╗╔╔═╗╔╦╗╔═╗╦  ╦  ╦╔╗╔╔═╗  ╦═╗╔═╗╔═╗ ╦ ╦╦╦═╗╔═╗╔╦╗╔═╗╔╗╔╔╦╗╔═╗", Fore.GREEN)
print_colored_text("║║║║╚═╗ ║ ╠═╣║  ║  ║║║║║ ╦  ╠╦╝║╣ ║═╬╗║ ║║╠╦╝║╣ ║║║║╣ ║║║ ║ ╚═╗", Fore.GREEN)
print_colored_text("╩╝╚╝╚═╝ ╩ ╩ ╩╩═╝╩═╝╩╝╚╝╚═╝  ╩╚═╚═╝╚═╝╚╚═╝╩╩╚═╚═╝╩ ╩╚═╝╝╚╝ ╩ ╚═╝", Fore.GREEN)
                                                                                                                                                                                   

# Requirements
os.system("pip install cloudscraper")
os.system("pip install socks")
os.system("pip install pysocks")
os.system("pip install colorama")
os.system("pip install undetected_chromedriver")
os.system("pip install httpx")
# pip3
os.system("pip3 install cloudscraper")
os.system("pip3 install socks")
os.system("pip3 install pysocks")
os.system("pip3 install colorama")
os.system("pip3 install undetected_chromedriver")
os.system("pip3 install httpx")
