import subprocess

# Install Playwright and dependencies
subprocess.run(['pip', 'install', 'playwright'])
subprocess.run(['playwright', 'install'])
subprocess.run(['pip', 'install', 'faker'])
subprocess.run(['playwright', 'install-deps'])

# Install additional system dependencies
subprocess.run(['sudo', 'apt-get', 'install', '-y',
                'libnss3', 'libnspr4', 'libatk-bridge2.0-0',
                'libdrm2', 'libxkbcommon0', 'libatspi2.0-0',
                'libgbm1', 'libasound2'])
