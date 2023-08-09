import json
import sys
from os import uname

import boto3
from botocore.config import Config
import requests

ec2_metadata_url = 'http://169.254.169.254/latest/'

def get_instance_key_pair(url):
  resp = requests.get(url + '/meta-data/public-keys')
  if resp.status_code != 200:
    raise TypeError("Failed to fetch data: ", resp.status_code)
  return resp.text.split('=')[1]

def get_region(url):
  resp = requests.get(url + "/dynamic/instance-identity/document")
  if resp.status_code != 200:
    raise TypeError("Failed to fetch data: ", resp.status_code)
  data = resp.json()
  return data['region']

def get_pub_key(client, key_pair_name):
  resp = client.describe_key_pairs(
    KeyNames=[
      key_pair_name
    ],
    IncludePublicKey=True
  )
  return resp['KeyPairs'][0]['PublicKey']

def update_pub_key(auth_key_path, pub_key):
  with open(auth_key_path, 'w') as auth_key:
    auth_key.write(pub_key)

def main(version):
  hostname = uname()[1]
  auth_key_path = '/home/ubuntu/.ssh/authorized_keys'
  instance_key_pair_name = get_instance_key_pair(ec2_metadata_url) + "-" + version
  region = get_region(ec2_metadata_url)

  client = boto3.client('ec2', config=Config(region_name=region))
  pub_key = get_pub_key(client, instance_key_pair_name)
  update_pub_key(auth_key_path, pub_key)
  print(f"{hostname} - {region},{instance_key_pair_name},{pub_key}")

def usage():
  print(f"Usage: {sys.argv[0]} <version>")

if __name__ == "__main__":
  try:
    if sys.argv[1] == "":
      usage()
      sys.exit(1)
  except IndexError:
    usage()
    sys.exit(0)

  main(sys.argv[1])
