# pybuster
# A dir buster clone that doesn't derp out when a connection fails.
# 
# Laurance Yeomans 2018
#
# Why:
# dirb has a sad when it fails and stops.
# This adds a 5 sec time out before trying again.
#
# No license. Do whatever with it.

import requests
import sys
import time
import signal

# Using dirb's default wordlist. Change to preferred default list.
# Also presuming this is being used within a default Kali environment
default_wordlist = '/usr/share/dirb/wordlists/common.txt'

def sigint_handler(signal,frame):
    print("\n\nCtrl + C caught. Terminating.")
    sys.exit(1)

def show_usage():
    print("Usage: pybuster -u target_url [-w wordlist] [-o outfile]")

def process_args():
    ret_args = dict()
    ret_args['url'] = ''
    ret_args['wordlist'] = default_wordlist
    ret_args['outfile'] = ''
    if len(sys.argv) < 1:
        ret_args['show_usage'] = True
    else:
        ret_args['show_usage'] = False
        for i in range(0,len(sys.argv)):
            if sys.argv[i] == '-o':
                ret_args['outfile'] = sys.argv[i+1]
            elif sys.argv[i] == '-w':
                ret_args['wordlist'] = sys.argv[i+1]
            elif sys.argv[i] == '-u':
                url_test = sys.argv[i+1]
                if url_test[len(url_test)-1] != '/':
                    ret_args['url'] = url_test + '/'
                else:
                    ret_args['url'] = url_test
    return ret_args
    
def main():
    signal.signal(signal.SIGINT,sigint_handler) # Catch Ctrl + C
    args = process_args()
    if args['show_usage']:
        show_usage()
        sys.exit(0)
    if args['url'] == '':
        print("No target URL specified. Please specify with -u parameter.\n")
        show_usage() 
        sys.exit(0)
    try:
        with open(args['wordlist'],'r') as f_wordlist:
            # pylint: disable=unused-argument
            for i,l in enumerate(f_wordlist):
                pass
            word_count = i + 1
    except IOError:
        print("Error: Unable to open {0}.".format(args['wordlist']))
        sys.exit(1)
    print("  |------------|")
    print("  |  pybuster  |")
    print("  |------------|\n")
    print("Starting tests with the following:")
    print("  URL: {0}\n  Wordlist: {1}\n  Word count: {2}\n".format(args['url'],args['wordlist'],word_count))
    with open(args['wordlist'],'r') as f_wordlist:
        # hack job to clear buffer text ...
        hack_job_string = ' ' * 25

        # lines = [line.rstrip('\n') for line in f_wordlist]
        if args['outfile'] != '':
            f_outfile = open(args['outfile'],'w')
            f_outfile_opened = True
        else:
            f_outfile_opened = False
        for raw_line in f_wordlist:
            line = raw_line.rstrip('\n')
            done = False
            retry_count = 1
            while not done:
                try:
                    sys.stdout.write("\r--> Testing: {0}{1}".format(line,hack_job_string))
                    sys.stdout.flush()
                    r = requests.get(args['url'] + line)
                    if r.status_code == 404:
                        done = True
                        break
                    else:
                        print("\n  * [Found: {0}] [CODE: {1}]".format(args['url']+line,r.status_code))
                        if f_outfile_opened:
                            f_outfile.write("[Found: {0}] [CODE: {1}]\n".format(args['url']+line,r.status_code))
                        done = True
                except:
                    if retry_count == 1:
                        print("\n")
                    err_msg = "\r  ! ConnectionError testing {0}: Trying again in 5 sec. (Retry count: {1})".format(line,retry_count)
                    sys.stdout.write(err_msg)
                    sys.stdout.flush()
                    time.sleep(5)
                    sys.stdout.write('\b' * (len(err_msg)-1)) # Clear the err msg before testing again.
                    retry_count += 1
        print("\n\nDone!")
        if f_outfile_opened:
            f_outfile.close()
            
if __name__ == "__main__":
    main()