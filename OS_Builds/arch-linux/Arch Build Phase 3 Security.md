## Hardening and Security
---

##### Firewall (ufw)
```bash
sudo pacman -S ufw
```

##### AppArmor
```bash
sudo pacman -S apparmor

# In order to use AppArmor (AA), the file system must be mounted. AA uses the `securityfs` virtual filesystem to store and manage profile states.

sudo mount -t securityfs securityfs /sys/kernel/security

sudo systemctl enable apparmor
sudo systemctl start apparmor
sudo apparmor_status
```
*Note: In this case, AppArmor is being used to harden just the core system services.*


##### Install Flatseal (Flatpak app security management)
```bash
flatpak install flathub flatseal
```
*Note: Flatpak acts as a sandbox around apps. This is being used on apps where FireJail either doesn't apply or is too restrictive on app function*

##### Lynis: Vulnerability Scanning Tool
```bash
sudo pacman -S lynis
```

##### Firejail: Sandboxing for apps
```bash
sudo pacman -S firejail
firejail --version             # verify the install
```

---

##### Implementing Firejail
To reduce the attack surface of internet-facing and file-handling applications, **Firejail** was implemented as the primary sandboxing tool in this build. Rather than relying on full system-wide enforcement, a **manual and targeted approach** was taken — applying Firejail only to **high-risk applications** that interact with the web, open files from untrusted sources, or connect to external services. 
Each relevant `.desktop` file (used to generate app launchers in the GUI) was edited to prepend `firejail` to the `Exec=` line. This ensures the app is sandboxed whether launched via terminal, menu, or desktop shortcut.
**Example:**
```bash

# Path: /usr/share/applications/firefox.desktop

[Desktop Entry]
Name=Firefox

# before
Exec=/usr/lib/firefox/firefox %u  
# after
Exec=firejail /usr/lib/firefox/firefox %u
Icon=firefox
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;
```
This pattern was repeated for each selected application, including Thunderbird, OnionShare, VLC, Zathura, and Tor Browser. 

---

##### Enable and Start SSH
```bash
sudo systemctl enable sshd
sudo systemctl start sshd
sudo systemctl status sshd
```

##### Implementing Firewall Rules (Basic)
```bash
sudo ufw status verbose
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

---