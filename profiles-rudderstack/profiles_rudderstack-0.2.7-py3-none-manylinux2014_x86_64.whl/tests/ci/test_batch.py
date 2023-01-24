import argparse
import subprocess
import sys

def get_tests(path):
    cmd = ['go', 'test', path, '-list=.']
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_tests = [x for x in result.stdout.decode('utf-8').split('\n') if x.startswith('Test')]
    return all_tests
    
def get_batch(tests, index, total):
    tests.sort()
    return [x for i, x in enumerate(tests) if i % total == index]

def run_batch(batch, path, siteconfig_path, timeout):
    run_arg = '|'.join(batch)
    cmd = ['go', 'test', path, '-v', '-run', run_arg, '-timeout', timeout]
    if siteconfig_path:
        cmd += ['--siteconfig_path', siteconfig_path]
    print(' '.join(cmd))
    return subprocess.run(cmd, check=True)

def run_tests(args):
    all_tests = get_tests(args.test_dir_path)
    batch = get_batch(all_tests, args.batch_index, args.batch_total)
    run_batch(batch, args.test_dir_path, args.siteconfig_path, args.timeout)
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run test batch')
    parser.add_argument('batch_index', type=int)
    parser.add_argument('batch_total', type=int)
    parser.add_argument('--test_dir_path', type=str, default='./..')
    parser.add_argument('--siteconfig_path', type=str, default='')
    parser.add_argument('--timeout', type=str, default='15m')
    args = parser.parse_args()
    run_tests(args)
      
