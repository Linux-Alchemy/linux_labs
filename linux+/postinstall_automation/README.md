# Quest 03: Post-Install Automation (OpenPortal Script)

## Goal
Use 'openportal.sh' to automate common post-install tasks in a dual-boot setup. This is a nifty little idea I had to save some time booting into my other OS on another drive to pull files over. With this script, just run it, and then you can port into the other side and grab what you need. Linux magic...

## How to use
- Step 1: Download the script
- Step 2: Make it executable
- ```bash
  chmod +x openportal.sh
  ```
- Step 3: Run it
- Step 4: You're a wizard

## Notes
- Make sure to replace the UUID # before you run it
- It might be neat to make this automatic on boot up so you don't have to run the script at all. But: DO NOT add this to your /fstab --> chaos will ensue...trust me
- What I'd do differently next time
    - Well not add it to the /fstab obviously
