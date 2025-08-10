import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def hash_passwords():
    """Utility script to hash passwords in the config file"""
    # Load config file
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    # Hash all passwords
    config['credentials'] = stauth.Hasher.hash_passwords(config['credentials'])
    
    # Save updated config
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
    
    print("Passwords have been hashed and config updated!")

if __name__ == "__main__":
    hash_passwords()