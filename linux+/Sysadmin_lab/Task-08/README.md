## Task 8 - Assigning a Static IP Address to a Linux Server

In this task, I moved away from DHCP and gave `server1` a **static IP** address to prepare it for a private network configuration. This ensures consistent connectivity in my lab environment, especially once I start adding more machines and simulate networking scenarios.

### 💡 Note on Network Setup

I'm no longer using a live internet connection (NAT or Bridged). Instead, this lab is now configured on an **isolated private network** using VMware's **Host-only adapter (vmnet99)**. This prevents any real-world interference or risk. You’ll need to manually create a custom network adapter in your hypervisor of choice (VMware, VirtualBox, etc).  

🧠 *This setup makes the lab safer and allows us to assign our own IP ranges without worrying about IP conflicts with the host system or real routers.*

---

### Static IP Addressing

I gave `server1` the IP address `10.99.99.10` and used a `/24` subnet for easy readability.

**Planned Subnet for Lab Network:** `10.99.99.0/24`  
**Gateway IP (placeholder):** `10.99.99.1`

This subnet will be used across all machines in the lab. Here’s the full plan:

| Machine      | Role       | Static IP       |
|--------------|------------|-----------------|
| Server1      | Main Server| `10.99.99.10`   |
| Server2      | Secondary  | `10.99.99.11`   |
| Lubuntu VM   | Client 1   | `10.99.99.20`   |
| Mint VM      | Client 2   | `10.99.99.21`   |

---

### Key Commands & Actions

- `ip a` → Shows interface names (e.g., `ens33`) and IPs  
- `ip r` → Displays current routing table  
- `/etc/netplan/*.yaml` → Where static IP config is stored  
- `sudo nano /etc/netplan/50-cloud-init.yaml` → Open the YAML config  
- `sudo netplan apply` → Apply the config

---

### YAML Configuration Overview

This is what I placed in `/etc/netplan/50-cloud-init.yaml`:

```yaml
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: no
      addresses:
        - 10.99.99.10/24
      routes:
        - to: default
          via: 10.99.99.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]

