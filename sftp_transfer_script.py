import os
import pysftp

# Local directories
local_dir = "\directory\"
local_sent_dir = "\directory\"
local_log_file = "\directory\"

# SFTP server details
myHostname = 'hostname'
myUsername = 'username'
myPassword = 'password'
remote_dir = "/"

# Initialize SFTP connection
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
    sftp.cwd(remote_dir)  # Set the remote directory
    local_files = os.listdir(local_dir)

    for file in local_files:
        if file.endswith(".xml"):
            try:
                # Upload the file from local folder to SFTP
                sftp.put(local_dir + file, file)
                print(f"Moved {file} to SFTP server")

                # Move the file to the "sent" folder locally
                os.rename(local_dir + file, local_sent_dir + file)
                print(f"Moved {file} to {local_sent_dir}")

                # Append to the log file
                with open(local_log_file, "a") as log_file:
                    log_file.write(f"Transferred {file} successfully.\n")
            except Exception as e:
                print(f"Error transferring {file}: {e}")

print("Transfer and backup completed. Log saved in transfer_log.txt")
