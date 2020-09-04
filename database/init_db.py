import os
import configparser

config = configparser.ConfigParser()
config.read('../credentials.txt')

cmd = ''.join(['psql -h ',config['remote']['server'],' -d ',config['remote']['database'],' -U ',config['remote']['user'],' -a -q -f ../sql/create_tables.sql'])
os.system(cmd)