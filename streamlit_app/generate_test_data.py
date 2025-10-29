"""
Generate 20 test CSV files with varied network connection data
Each file contains 10-15 samples with different characteristics
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Feature names (41 features)
FEATURE_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

# Categorical values
PROTOCOLS = ['tcp', 'udp', 'icmp']
SERVICES = ['http', 'ftp', 'smtp', 'telnet', 'ssh', 'pop3', 'domain', 'finger', 'private', 'eco_i']
FLAGS = ['SF', 'S0', 'REJ', 'RSTR', 'RSTO', 'SH', 'S1', 'S2', 'RSTOS0', 'S3', 'OTH']

def generate_normal_traffic(n_samples):
    """Generate normal network traffic patterns"""
    data = []
    for _ in range(n_samples):
        row = {
            'duration': np.random.randint(0, 100),
            'protocol_type': np.random.choice(['tcp', 'udp'], p=[0.8, 0.2]),
            'service': np.random.choice(['http', 'ftp', 'smtp', 'telnet', 'ssh'], p=[0.4, 0.2, 0.15, 0.15, 0.1]),
            'flag': np.random.choice(['SF', 'S0', 'REJ'], p=[0.7, 0.2, 0.1]),
            'src_bytes': np.random.randint(100, 10000),
            'dst_bytes': np.random.randint(100, 10000),
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 1,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': np.random.randint(0, 3),
            'num_shells': 0,
            'num_access_files': 0,
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': 0,
            'count': np.random.randint(1, 50),
            'srv_count': np.random.randint(1, 50),
            'serror_rate': np.random.uniform(0, 0.1),
            'srv_serror_rate': np.random.uniform(0, 0.1),
            'rerror_rate': np.random.uniform(0, 0.1),
            'srv_rerror_rate': np.random.uniform(0, 0.1),
            'same_srv_rate': np.random.uniform(0.7, 1.0),
            'diff_srv_rate': np.random.uniform(0, 0.3),
            'srv_diff_host_rate': np.random.uniform(0, 0.2),
            'dst_host_count': np.random.randint(1, 255),
            'dst_host_srv_count': np.random.randint(1, 255),
            'dst_host_same_srv_rate': np.random.uniform(0.7, 1.0),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.3),
            'dst_host_same_src_port_rate': np.random.uniform(0, 0.5),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.2),
            'dst_host_serror_rate': np.random.uniform(0, 0.1),
            'dst_host_srv_serror_rate': np.random.uniform(0, 0.1),
            'dst_host_rerror_rate': np.random.uniform(0, 0.1),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.1),
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_dos_attack(n_samples):
    """Generate DoS attack patterns (Denial of Service)"""
    data = []
    for _ in range(n_samples):
        row = {
            'duration': 0,
            'protocol_type': np.random.choice(['tcp', 'icmp'], p=[0.6, 0.4]),
            'service': np.random.choice(['http', 'eco_i', 'private']),
            'flag': np.random.choice(['S0', 'REJ', 'RSTO'], p=[0.5, 0.3, 0.2]),
            'src_bytes': 0,
            'dst_bytes': 0,
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': 0,
            'count': np.random.randint(50, 500),
            'srv_count': np.random.randint(50, 500),
            'serror_rate': np.random.uniform(0.8, 1.0),
            'srv_serror_rate': np.random.uniform(0.8, 1.0),
            'rerror_rate': np.random.uniform(0, 0.2),
            'srv_rerror_rate': np.random.uniform(0, 0.2),
            'same_srv_rate': np.random.uniform(0.8, 1.0),
            'diff_srv_rate': np.random.uniform(0, 0.1),
            'srv_diff_host_rate': np.random.uniform(0, 0.1),
            'dst_host_count': 255,
            'dst_host_srv_count': 255,
            'dst_host_same_srv_rate': np.random.uniform(0, 0.2),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.1),
            'dst_host_same_src_port_rate': np.random.uniform(0.8, 1.0),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.1),
            'dst_host_serror_rate': np.random.uniform(0.8, 1.0),
            'dst_host_srv_serror_rate': np.random.uniform(0.8, 1.0),
            'dst_host_rerror_rate': np.random.uniform(0, 0.2),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.2),
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_probe_attack(n_samples):
    """Generate Probe/Scan attack patterns"""
    data = []
    for _ in range(n_samples):
        row = {
            'duration': 0,
            'protocol_type': np.random.choice(['tcp', 'icmp', 'udp']),
            'service': np.random.choice(['private', 'eco_i', 'http']),
            'flag': np.random.choice(['S0', 'REJ', 'RSTR']),
            'src_bytes': 0,
            'dst_bytes': 0,
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': 0,
            'num_failed_logins': 0,
            'logged_in': 0,
            'num_compromised': 0,
            'root_shell': 0,
            'su_attempted': 0,
            'num_root': 0,
            'num_file_creations': 0,
            'num_shells': 0,
            'num_access_files': 0,
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': 0,
            'count': np.random.randint(10, 100),
            'srv_count': np.random.randint(1, 10),
            'serror_rate': np.random.uniform(0.5, 1.0),
            'srv_serror_rate': np.random.uniform(0.5, 1.0),
            'rerror_rate': np.random.uniform(0, 0.3),
            'srv_rerror_rate': np.random.uniform(0, 0.3),
            'same_srv_rate': np.random.uniform(0, 0.3),
            'diff_srv_rate': np.random.uniform(0.7, 1.0),
            'srv_diff_host_rate': np.random.uniform(0, 0.5),
            'dst_host_count': 255,
            'dst_host_srv_count': np.random.randint(1, 50),
            'dst_host_same_srv_rate': np.random.uniform(0, 0.3),
            'dst_host_diff_srv_rate': np.random.uniform(0.7, 1.0),
            'dst_host_same_src_port_rate': np.random.uniform(0, 0.2),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.5),
            'dst_host_serror_rate': np.random.uniform(0.5, 1.0),
            'dst_host_srv_serror_rate': np.random.uniform(0.5, 1.0),
            'dst_host_rerror_rate': np.random.uniform(0, 0.3),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.3),
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_r2l_attack(n_samples):
    """Generate R2L (Remote to Local) attack patterns"""
    data = []
    for _ in range(n_samples):
        row = {
            'duration': np.random.randint(0, 200),
            'protocol_type': 'tcp',
            'service': np.random.choice(['ftp', 'telnet', 'ssh', 'http']),
            'flag': np.random.choice(['SF', 'S0', 'REJ']),
            'src_bytes': np.random.randint(0, 5000),
            'dst_bytes': np.random.randint(0, 5000),
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': np.random.randint(0, 5),
            'num_failed_logins': np.random.randint(1, 10),
            'logged_in': np.random.choice([0, 1], p=[0.7, 0.3]),
            'num_compromised': np.random.randint(0, 5),
            'root_shell': np.random.choice([0, 1], p=[0.8, 0.2]),
            'su_attempted': np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1]),
            'num_root': np.random.randint(0, 3),
            'num_file_creations': np.random.randint(0, 5),
            'num_shells': np.random.randint(0, 2),
            'num_access_files': np.random.randint(0, 5),
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': np.random.choice([0, 1], p=[0.7, 0.3]),
            'count': np.random.randint(1, 20),
            'srv_count': np.random.randint(1, 20),
            'serror_rate': np.random.uniform(0, 0.3),
            'srv_serror_rate': np.random.uniform(0, 0.3),
            'rerror_rate': np.random.uniform(0, 0.5),
            'srv_rerror_rate': np.random.uniform(0, 0.5),
            'same_srv_rate': np.random.uniform(0.3, 0.8),
            'diff_srv_rate': np.random.uniform(0.2, 0.7),
            'srv_diff_host_rate': np.random.uniform(0, 0.5),
            'dst_host_count': np.random.randint(1, 100),
            'dst_host_srv_count': np.random.randint(1, 100),
            'dst_host_same_srv_rate': np.random.uniform(0.3, 0.8),
            'dst_host_diff_srv_rate': np.random.uniform(0.2, 0.7),
            'dst_host_same_src_port_rate': np.random.uniform(0, 0.5),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.5),
            'dst_host_serror_rate': np.random.uniform(0, 0.3),
            'dst_host_srv_serror_rate': np.random.uniform(0, 0.3),
            'dst_host_rerror_rate': np.random.uniform(0, 0.5),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.5),
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_u2r_attack(n_samples):
    """Generate U2R (User to Root) attack patterns"""
    data = []
    for _ in range(n_samples):
        row = {
            'duration': np.random.randint(0, 300),
            'protocol_type': 'tcp',
            'service': np.random.choice(['telnet', 'ftp', 'ssh', 'login']),
            'flag': 'SF',
            'src_bytes': np.random.randint(50, 2000),
            'dst_bytes': np.random.randint(50, 2000),
            'land': 0,
            'wrong_fragment': 0,
            'urgent': 0,
            'hot': np.random.randint(1, 10),
            'num_failed_logins': np.random.randint(0, 5),
            'logged_in': 1,
            'num_compromised': np.random.randint(1, 20),
            'root_shell': 1,
            'su_attempted': np.random.randint(1, 5),
            'num_root': np.random.randint(1, 50),
            'num_file_creations': np.random.randint(0, 10),
            'num_shells': np.random.randint(0, 5),
            'num_access_files': np.random.randint(0, 10),
            'num_outbound_cmds': 0,
            'is_host_login': 0,
            'is_guest_login': 0,
            'count': np.random.randint(1, 10),
            'srv_count': np.random.randint(1, 10),
            'serror_rate': np.random.uniform(0, 0.2),
            'srv_serror_rate': np.random.uniform(0, 0.2),
            'rerror_rate': np.random.uniform(0, 0.3),
            'srv_rerror_rate': np.random.uniform(0, 0.3),
            'same_srv_rate': np.random.uniform(0.5, 1.0),
            'diff_srv_rate': np.random.uniform(0, 0.5),
            'srv_diff_host_rate': np.random.uniform(0, 0.3),
            'dst_host_count': np.random.randint(1, 50),
            'dst_host_srv_count': np.random.randint(1, 50),
            'dst_host_same_srv_rate': np.random.uniform(0.5, 1.0),
            'dst_host_diff_srv_rate': np.random.uniform(0, 0.5),
            'dst_host_same_src_port_rate': np.random.uniform(0, 0.5),
            'dst_host_srv_diff_host_rate': np.random.uniform(0, 0.3),
            'dst_host_serror_rate': np.random.uniform(0, 0.2),
            'dst_host_srv_serror_rate': np.random.uniform(0, 0.2),
            'dst_host_rerror_rate': np.random.uniform(0, 0.3),
            'dst_host_srv_rerror_rate': np.random.uniform(0, 0.3),
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_mixed_traffic(n_samples, normal_ratio=0.6):
    """Generate mixed normal and attack traffic"""
    n_normal = int(n_samples * normal_ratio)
    n_attack = n_samples - n_normal
    
    # Generate normal traffic
    df_normal = generate_normal_traffic(n_normal)
    
    # Generate attacks (split among different types)
    attack_types = [generate_dos_attack, generate_probe_attack, generate_r2l_attack, generate_u2r_attack]
    dfs_attack = []
    
    for _ in range(n_attack):
        attack_func = np.random.choice(attack_types)
        dfs_attack.append(attack_func(1))
    
    if dfs_attack:
        df_attack = pd.concat(dfs_attack, ignore_index=True)
        df = pd.concat([df_normal, df_attack], ignore_index=True)
    else:
        df = df_normal
    
    # Shuffle
    return df.sample(frac=1).reset_index(drop=True)

# Generate 20 test files
print("=" * 60)
print("Generating 20 Test CSV Files")
print("=" * 60)

output_dir = 'test'
os.makedirs(output_dir, exist_ok=True)

test_configs = [
    # Files 1-5: Mostly normal traffic with varying sizes
    {'name': 'test1.csv', 'generator': generate_normal_traffic, 'n': 10, 'desc': 'Pure normal traffic (10 samples)'},
    {'name': 'test2.csv', 'generator': generate_normal_traffic, 'n': 15, 'desc': 'Pure normal traffic (15 samples)'},
    {'name': 'test3.csv', 'generator': generate_normal_traffic, 'n': 12, 'desc': 'Pure normal traffic (12 samples)'},
    {'name': 'test4.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.9), 'n': 13, 'desc': 'Mostly normal (90% normal, 10% attacks)'},
    {'name': 'test5.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.8), 'n': 14, 'desc': 'Mostly normal (80% normal, 20% attacks)'},
    
    # Files 6-10: DoS attacks with varying proportions
    {'name': 'test6.csv', 'generator': generate_dos_attack, 'n': 10, 'desc': 'Pure DoS attacks'},
    {'name': 'test7.csv', 'generator': generate_dos_attack, 'n': 15, 'desc': 'Pure DoS attacks (larger set)'},
    {'name': 'test8.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.5), 'n': 12, 'desc': 'Balanced (50% normal, 50% attacks)'},
    {'name': 'test9.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.3), 'n': 11, 'desc': 'Attack-heavy (30% normal, 70% attacks)'},
    {'name': 'test10.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.1), 'n': 13, 'desc': 'Mostly attacks (10% normal, 90% attacks)'},
    
    # Files 11-15: Specific attack types
    {'name': 'test11.csv', 'generator': generate_probe_attack, 'n': 10, 'desc': 'Pure Probe/Scan attacks'},
    {'name': 'test12.csv', 'generator': generate_probe_attack, 'n': 14, 'desc': 'Pure Probe/Scan attacks (larger)'},
    {'name': 'test13.csv', 'generator': generate_r2l_attack, 'n': 12, 'desc': 'Pure R2L (Remote to Local) attacks'},
    {'name': 'test14.csv', 'generator': generate_r2l_attack, 'n': 15, 'desc': 'Pure R2L attacks (larger)'},
    {'name': 'test15.csv', 'generator': generate_u2r_attack, 'n': 11, 'desc': 'Pure U2R (User to Root) attacks'},
    
    # Files 16-20: Mixed scenarios with varied distributions
    {'name': 'test16.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.7), 'n': 13, 'desc': 'Mixed (70% normal, 30% attacks)'},
    {'name': 'test17.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.4), 'n': 14, 'desc': 'Mixed (40% normal, 60% attacks)'},
    {'name': 'test18.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.6), 'n': 10, 'desc': 'Mixed (60% normal, 40% attacks)'},
    {'name': 'test19.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.85), 'n': 15, 'desc': 'Mostly normal (85% normal, 15% attacks)'},
    {'name': 'test20.csv', 'generator': lambda n: generate_mixed_traffic(n, 0.2), 'n': 12, 'desc': 'Attack-dominant (20% normal, 80% attacks)'},
]

for i, config in enumerate(test_configs, 1):
    filename = config['name']
    generator = config['generator']
    n_samples = config['n']
    description = config['desc']
    
    # Generate data
    df = generator(n_samples)
    
    # Save to CSV
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    
    print(f"{i:2d}. ✓ {filename:<15} - {n_samples:2d} samples - {description}")

print("\n" + "=" * 60)
print(f"✅ Successfully generated 20 test CSV files in '{output_dir}/' folder")
print("=" * 60)
print("\nTest file characteristics:")
print("• Files 1-5:   Normal traffic with varying attack ratios")
print("• Files 6-10:  DoS attacks and mixed scenarios")
print("• Files 11-15: Specific attack types (Probe, R2L, U2R)")
print("• Files 16-20: Varied mixed traffic distributions")
print("\nAll files ready for testing in Streamlit app!")
