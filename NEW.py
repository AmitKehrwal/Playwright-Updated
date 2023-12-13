import subprocess

# Clone the repository
subprocess.run(["git", "clone", "https://github.com/AmitKehrwal/Playwright-Updated.git"])

# Change to the repository directory
os.chdir("Playwright-Updated")


# Give execution permission to install_brave.sh
subprocess.run(["chmod", "+x", "install_brave.sh"])

# Run install_brave.sh
subprocess.run(["./install_brave.sh"])
