## Arch Linux Black

**Arch Linux Black** is a proof-of-concept build created as a lightweight, heavily customized Arch-based system. The goal was to replicate the overall usability and visual styling of my daily driver — but built entirely from scratch on Arch, for full control and performance.

This project was part of a broader exploration of Arch as a potential long-term OS base for future workflows and custom Linux distros.

---

### 🧱 What This Is

- Clean Arch install with a full Phase 1–3 build process
- GNOME desktop environment, themed black and red (Material Black Cherry + Flat Remix)
- Daily apps, core utilities, privacy tools, and system hardening included
- System managed with Btrfs subvolumes, Snapper snapshots, and minimal startup overhead
- Targeted app sandboxing using Firejail + Flatpak
- AppArmor enabled and protecting core services (after some manual setup)

All build phases are fully documented in this repo.

---

### 🧪 What Broke / What Bit Back

- **VMware Tools** were a royal pain in the ass. DKMS module builds kept failing due to upstream issues and kernel changes. After multiple retries and patches, I shelved it — not worth the headache right now.
- **Btrfs** has some quirks — especially around mounting, subvolumes, and snapshot behavior. Works great once it’s set up right, but it doesn’t hold your hand.
- **AppArmor** isn't native to Arch like it is on Ubuntu. Needed to manually mount `securityfs`, load profiles, and tune it to avoid false negatives. That said, it’s working clean now and running system-level protections.

---

### 🔐 Security Highlights

- **AppArmor** active for core system services
- **Firejail** manually applied to high-risk apps (Firefox, VLC, Tor Browser, etc.)
- **Flatpak** used where Firejail was overkill or too restrictive
- **Snapper** configured for root and home snapshots, with retention policies in place
- **UFW** active with sane default rules

---

### 🧠 Final Thoughts

Honestly? Arch surprised me. The install process was smoother than expected, and once the core config was locked in, it ran like a damn dream. Light, fast, and incredibly customizable.

I wouldn't move to it full-time **yet** — mostly because of the VMware kernel module nonsense. But once that’s sorted (or I switch to a hypervisor that plays nice), this setup could absolutely replace my current daily OS.

Highly recommend building it yourself if you're even a little curious. There’s no substitute for bleeding a bit on the Arch altar.

---

### 📁 Repo Structure

- `Phase 1`: Base system install + filesystem + essential packages
- `Phase 2`: Daily apps, DE, theming, tools
- `Phase 3`: Hardening + security layers

Each phase is its own Markdown doc — clean, annotated, and meant to be cloned, modified, or built on.

---

#### 🛠️ Status

Project is complete and frozen for now. A new Arch-based ISO build (leaner, tighter, ISO-convertible) is in planning.

