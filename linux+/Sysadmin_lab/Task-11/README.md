## Task 11 – Final Topology and Private Network Diagram

This task wraps up the core lab setup by visualizing the simplified private network we've built using **Packet Tracer**.

The updated topology consists of three machines:

- **Server1** – Ubuntu Server (Main controller node)
- **Mint** – Desktop client
- **Lubuntu** – Lightweight desktop client

---

### 🧠 Network Design Summary

- All three machines are connected using **Fast Ethernet** cables
- Each device is assigned a **static IP** within the `10.99.99.0/24` subnet
- The network is completely **isolated** using VMware's `vmnet99` (host-only adapter)
- All devices can communicate with each other — verified via ping tests

---

### 🖼️ Diagram

The complete topology is documented in the following files:

- `basicprivate.png` – Static image of the network layout  


---

> ⚠️ This network is intentionally simple for learning purposes. A more advanced, multi-segmented network will be created in a future project.

