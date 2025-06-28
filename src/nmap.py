import subprocess
import sys

# Function to run Nmap with version detection and XML output
def run_nmap(ip_address, output_file="nmap_output.xml"):
    try:
        command = ["nmap", "-sV", "-oX", output_file, ip_address]
        print(f"Running Nmap command: {' '.join(command)}")

        # Run the Nmap command
        subprocess.run(command, check=True)
        print(f"Nmap scan completed. Output saved to: {output_file}")

    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)

# Main execution block to get IP from command-line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nmap.py <target_ip>")
    else:
        ip = sys.argv[1]
        run_nmap(ip)
