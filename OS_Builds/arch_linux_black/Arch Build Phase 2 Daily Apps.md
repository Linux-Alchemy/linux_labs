## Phase 2: Daily Apps

### Installation of the DE (GNOME)
Essentially attempting to clone a visual setup that I have on my host. On another build i will likely use a different DE

Install GNOME (base DE)
```bash
sudo pacman -S gnome gnome-tweaks gdm
```
This installs the base GNOME shell, GNOME tweaks, and the GDM display manager


Install the Extension Manager
```bash
yay -S extension-manager
```
Provides a GUI to manage extensions like Dash to Dock

Installing Dash to Dock
```bash
yay -S gnome-shell-extension-dash-to-dock
```

Installing a Theme
```bash
yay -S yaru-theme-gtk yaru-icon-theme yaru-theme-gnome-shell
```
*Note: there's loads of themes available, just doing the one now for simplicity*

Installing the GDM-settings menu (controls the login screen settings)
```bash
yay -S gdm-settings
```

Enable GDM to launch on boot up
```bash
sudo systemctl enable gdm
```

Reboot the system
```bash
sudo reboot
```

---

### Upgrade the Terminal
The stock terminal is a travesty. Time for an upgrade. This build will use zsh and Tilix as the default.
First install Z Shell:
```bash
sudo pacman -S zsh

# Make Zsh the default shell
chsh -s /bin/zsh
```

Install Tilix:
```bash
yay -S tilix
```

Tilix Integration Issue (fix)
To prevent Tilix from throwing config issues when it opens edit the `.zshrc` file:
```bash
if [[ -n "$TILIX_ID" && -f /etc/profile.d/vte.sh ]]; then
    source /etc/profile.d/vte.sh
fi
```
*add this line towards the bottom of the file*

**Potential Issue**
Sometimes GNOME will complain about Tilix integration. The fix:
```bash
sudo ln -s /etc/profile.d/vte-2.91.sh /etc/profile.d/vte.sh
```


---

### Theme Install (Material Black - Dark Cherry)
The stock GNOME dark mode is functional, but somewhat uninspired. So instead of lameness, we'll go something with a little flair and use the Material Black Dark Cherry theme for both GTK and GNOME.

Install Dependencies:
Ensure you have the Murrine Engine. If not install it now:
```bash
sudo pacman -S gtk-engine-murrine
```

Download and extract the theme pack. Use the version from [Gnome Look](https://www.gnome-look.org/p/1316887/), as it includes both GTK and Shell styling. Use the Material-Black-Cherry-BE version:
- Unzip the folder and move it to:
```bash
~/.themes/  # for single-user only
# OR
/usr/share/themes/  # for system-wide access
```

Set the Theme with GNOME Tweaks
Open GNOME Tweaks and apply:
- **Applications:** `Material-Black-Cherry-BE`
- **Shell:** `Material-Black-Cherry-BE`

*Note: If shell theming isn't showing you'll need to install `gnome-shell-extensions`*

---

### Flat-Remix-Icon
While there is matching Material Black Cherry icon pack, I prefer the Flat-Remix-Icons. You can find the downloads here: [flat remix](https://www.gnome-look.org/p/1012430) or from the GitHub repo: [flat remix gitgub](https://github.com/daniruiz/flat-remix)
Download and extract the icon pack just as above:
```bash
~/.icons/           # single-user only
# OR
/usr/share/icons/   # system-wide
```

---

### Installing Nemo (file manager)
Nothing personal to Nautilus it's just that Nemo is better. 
```bash
sudo pacman -S nemo
```

Once installed, you'll want to replace Nautilus as the default file handler for directories. Without this step Nautilus may still launch when opening folders via apps or shortcuts.
```bash
xdg-mime default nemo.desktop inode/directory
```

**Optional for GNOME only:** Unset Nautilus Autospawn. This stops GNOME from auto-lauching Nautilus to manage the desktop background. 
```bash
gsettings set org.gnome.desktop.background show-desktop-icons false
```
You can set show-desktop-icons true if you want. I don't like anything on my desktop personally. You do you.

**Optional:** Set HotKey to launch Nemo. Most DEs handle this more or less the same in the settings.
1. Open `Settings` → `Keyboard` → `Keyboard Shortcuts`
2. Scroll to bottom → `+` → Name: _Nemo_, Command: `nemo`, Shortcut: `Super + F`

---

### Productivity Apps

##### FireFox
```bash
sudo pacman -S firefox
```

##### LibreOffice Suite
```bash
flatpak install flathub org.libreoffice.LibreOffice
```

##### GIMP (Image Editor)
```bash
flatpak install flathub org.gimp.GIMP
```

##### VSCodium (Code Editor)
```bash
yay -S vscodium-bin
```
*Super important to use `-bin` otherwise you end up with a **huge** dev install -- don't do this*

##### Obsidian
```bash
sudo pacman -S obsidian
```

##### Thunderbird (Email Client)
```bash
sudo pacman -S thunderbird
```

##### Zathura (PDF Viewer)
```bash
sudo pacman -S zathura
```

##### VLC: Media Player
```bash
sudo pacman -S vlc
```

##### Timeshift: System Restore Tool
```bash
yay -S timeshift           
```

##### DKMS Install
```bash
sudo pacman -S dkms

# verify the install
dkms --version

# note it is a good idea to confirm the installation of the Linux headers
# as the DKMS requires them - for this build it is the Linux-lts-headers
# which were installed in phase 1
uname -r                      # check the kernel version 
pacman -Q linux-lts-headers   # confirm the headers are installed
# the version number of the outputs should be the same
```
DKMS (Dynamic Kernel Module Support) automatically rebuilds kernel modules when you update your kernel. That means no more redoing driver installs manually every time your system upgrades. It's one of the few things that keeps Arch from kicking your teeth in during system updates.

---

### Privacy Tools

##### Tor: Anonymous Browsing
```bash
sudo pacman -S tor             # this just downloads the daemon
yay -S tor-browser-bin         # download the browser
                               # choose `tor-browser-bin`
```

##### Onion Share: Secure File Sharing
```bash
sudo pacman -S onionshare
```

##### GnuPG: Encryption
```bash
sudo pacman -S gnupg
```
GnuPG is for digital signatures, file encryption etc

##### Veracrypt
```bash 
sudo pacman -S veracrypt
```
Veracrypt for disk encryption.

---


