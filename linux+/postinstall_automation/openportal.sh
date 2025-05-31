#!/bin/bash
# Define variables
MOUNT_POINT="/mnt/windows"  # <-- /mnt/<your folder>
DEVICE="UUID=XXXXXXXXXXXXXXXX"  #  <-- Replace with your actual device UUID

# Check if the mount point exists; if not, exit with an error.
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Error: Mount point $MOUNT_POINT does not exist. Please create it first."
    exit 1
fi

# Check if the device is already mounted
if mountpoint -q "$MOUNT_POINT"; then
    echo "The partition is already mounted at $MOUNT_POINT."
else
    echo "Mounting $DEVICE to $MOUNT_POINT..."
    # Mount the partition with ntfs-3g and proper permissions
    sudo mount -t ntfs-3g -o uid=$(id -u),gid=$(id -g),umask=022 "$DEVICE" "$MOUNT_POINT"
    if [ $? -eq 0 ]; then
        echo "Successfully mounted $DEVICE at $MOUNT_POINT."
    else
        echo "Failed to mount $DEVICE. Check the device path or permissions."
    fi
fi
