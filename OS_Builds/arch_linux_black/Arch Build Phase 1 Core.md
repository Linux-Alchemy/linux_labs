### Phase 1: Base Install
**If you haven't yet, download the ISO here:**

[arch_linux](https://archlinux.org/download/)

**Be sure to run the checksum to ensure the file integrity**

#### Create the new VM
*Note: I am using VMware Workstation Pro 17.x. Your actual setup may differ depending on what hypervisor you're using.*

In Vmware:
- Type: **Linux**
- Version: **Other Linux 6.x kernel 64-bit**
- Memory: ~12GB RAM 
- Disk: 50GB (SCSI or SATA)
- Network: NAT (vmnet66)
- Mount the ISO as the boot device
- **Don't power on the VM right away. First be sure to set it to boot up in UEFI**

---

#### Boot into the VM

- On boot menu select: `Arch Linux install medium (x86_64, UEFI)`

---

### Testing Network Connection
*Note: I'm using a wired connection*
- **DHCP** should auto-connect
- Confirm with:
```bash
ping -c 3 archlinux.org
```

##### Keyboard layout
```bash
loadkeys us
# change `us` for whatever layout you use
```

##### Optimize Mirrorlist
```bash
pacman -Sy reflector
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak # making a back up
reflector -c [country(s)] --age 24 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
```
- `-c` -> indicate specific country
- `--age 24` -> only use mirrors updated in the last 24 hours (adjust as you want or skip)
- `--protocol https` -> ensures secure connection
- `-- sort rate` -> ranks by speed
- `--save` -> saves to the specified file

---

##### Partition the Disk 
Confirm the disk label
In Vmware it should look something like `sda` 
```bash
lsblk
```
Then run:
```bash
cfdisk /dev/sda
```
##### To create partitions (EFI + Root):

1. **Select `Free Space`** using the arrow keys.
2. Hit **Enter** on `[ New ]`.
3. You will then be prompted to **enter the partition size manually**.
     - For EFI: type `512M` → press Enter.
     - After that, select `[ Type ]` and choose **EFI System** (usually option #1).
        
4. Now repeat for the **remaining space**:
     - Arrow down to the new free space.
     - `[ New ]` → press Enter.
     - Accept the default size (it will fill the rest of the disk).
     - Leave the type as default (Linux filesystem).
5. When done, go to `[ Write ]`, type `yes` to confirm writing the partition table.
6. Then `[ Quit ]` to exit `cfdisk`.
7. Run `lsblk` again to confirm partitions

---

##### Format and Mount Partitions
```bash
# Format partitions 
mkfs.fat -F32 /dev/sda1 # EFI 
mkfs.btrfs /dev/sda2 # Root

# Create Btrfs subvolumes (no .snapshots) 
mount /dev/sda2 /mnt 
btrfs subvolume create /mnt/@ # Root subvolume 
btrfs subvolume create /mnt/@home # Home subvolume 
umount /mnt

# Mount with compression for space efficiency 
mount -o compress=zstd,subvol=@ /dev/sda2 /mnt 
mkdir -p /mnt/{home,efi} 
mount -o compress=zstd,subvol=@home /dev/sda2 /mnt/home 
mount /dev/sda1 /mnt/efi

```
*Note: The use of the btrfs format is for snapshots on the system before/after updates for easier roll backs when something breaks -- using ext4 is perfectly fine too.*

---

##### Install the Base System and Essential Tools
```bash
pacstrap /mnt base linux-lts linux-lts-headers linux-firmware base-devel nano git btrfs-progs grub efibootmgr grub-btrfs snap-pac amd-ucode networkmanager pipewire pipewire-alsa pipewire-pulse pipewire-jack wireplumber zsh zsh-autosuggestions zsh-syntax-highlighting openssh man-db man-pages flatpak 
```
This is installing the LTS (Long term support) version of the Arch kernel that's more stable along with a bunch of essential tools.

---

##### Generate fstab
```bash
# check for /mnt/etc/
ls /mnt/etc
# if missing -> re-run `pacstrap`

genfstab -U /mnt >> /mnt/etc/fstab

# Confirm Btrfs subvolumes are correctly listed | ensure `compress=zstd`
cat /mnt/etc/fstab
```
- `fstab` -> tells Linux what drives to mount where and with what options when the system boots up
- `-U` ->  use the `UUID` to identify each partition instead of the device name like `/dev/sda1` which can change

---

##### Chroot into the new system
```bash
arch-chroot /mnt
```
- moving into the newly installed file system

---

##### Time Zone
```bash
# to find your region/city
ls /usr/share/zoneinfo
ls /usr/share/zoneinfo/[country]
ln -sf /usr/share/zoneinfo/[country]/[region] /etc/localtime
hwclock --systohc # syncs hardware clock to system time
```

---

#####  Localization (language settings)
```bash
nano /etc/locale.gen
# Uncomment: en_US.UTF-8 UTF-8

locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```
- Use whichever setting is best for your set up; I'm just using US English on UTF-8

---

##### Hostname and Hosts File
```bash
echo "hostname here" > /etc/hostname # assign name for the host

# set up host file to resolve local names
cat >> /etc/hosts <<EOF 
127.0.0.1   localhost
::1         localhost
127.0.1.1   [hostname-you-picked].localdomain [hostname-you-picked]
EOF
```

---

##### Set Root Password
```bash
passwd
```

---

##### Create a User + Sudo Access
It's always a good idea to create a non-root user
```bash
useradd -m -G wheel -s /bin/bash [newuser]
passwd [newuser]
EDITOR=nano visudo
# Uncomment: %wheel ALL=(ALL:ALL) ALL
```
- `-m` -> Creates a home directory at /home/newuser
- `G wheel` -> Adds the user to the **wheel group** which can be granted sudo rights
- `-s /bin/bash` -> Sets the login shell

---

##### Enable Networking
```bash
systemctl enable NetworkManager.service
```

---

##### Install GRUB (UEFI)
```bash
grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# confirm correct loading of GRUB
ls /efi/EFI/GRUB
# should see something like:
grubx64.efi
```

---

##### Install Git
```bash
pacman -S git
pacman -S git git-lfs # easier to handle larger files in git
git lfs install
```

---

##### Install VMware Tools
```bash
sudo pacman -S open-vm-tools gtkmm3
sudo systemctl enable vmtoolsd.service
sudo systemctl start vmtoolsd.service
# note that is also including what's needed for use with the GUI later
```

---

##### Exit and Reboot
```bash
exit
umount -R /mnt
reboot
```

---

##### Install and Configure Snapper for Snapshot Management
```bash
pacman -S snapper
snapper -c root create-config /
snapper -c home create-config /home
# Edit retention policies (e.g., keep 10 snapshots, delete after 5 days)
nano /etc/snapper/configs/root
# Example settings:
# NUMBER_LIMIT="10"
# TIMELINE_LIMIT_DAILY="5"
# TIMELINE_LIMIT_HOURLY="0"
# TIMELINE_LIMIT_WEEKLY="0"
# TIMELINE_LIMIT_MONTHLY="0"
# TIMELINE_LIMIT_YEARLY="0"
systemctl enable snapper-timeline.timer
systemctl enable snapper-cleanup.timer
```

---

##### Install AUR (Arch User Repo)
*Boot back in and log in as the new user*
```bash
sudo pacman -S base-devel git
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

---

### Validation
Confirm **LTS** kernel
```bash
uname -r
```

Verify Network
```bash
ping -c 3 archlinux.org
```

Check **Btrfs** subvolumes
```bash
btrfs subvolume list /
```

Verify **GRUB** install
```bash
ls /boot/grub
```

Snapshots
```bash
snapper list
```

---

### Notes

- Btrfs with subvolumes enables timeshift snapshots for rollbacks.
- LTS kernel ensures better stability.
- btrfs-progs must be installed before subvolume commands.
- Ensure 50GB disk has sufficient free space (~10GB recommended post-install).