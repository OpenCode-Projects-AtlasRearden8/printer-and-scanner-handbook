# Chapter 3: Wi-Fi printing setup

Goal: print from any device in your house to the one printer in your house, without a cable in sight. Budget about 20 minutes, mostly waiting.

## How Wi-Fi printing actually works (90 seconds)

Your printer joins your Wi-Fi network exactly like a phone does: it needs the network name (SSID) and password. Once it's on the network, every computer and phone that is *also* on that network can find it by name. That's the whole trick.

Two failure modes explain nearly all Wi-Fi printing misery:

1. **The printer isn't actually on your network** (it's on a guest network, or it fell off after a router change).
2. **Devices look on the wrong network** (your laptop is on Wi-Fi, but a different band or SSID than the printer).

Everything below untangles those two.

## Step 0: Gather your tools

- Your Wi-Fi password. (If you don't know it, it's often on the router's label.)
- A USB cable, ideally. Yes, really—see the sidebar in step 1.
- The printer's own manual or the maker's setup app for your phone.

## Step 1: Put the printer on the network

You have three routes; use the first one that works.

**Route A — The printer's touchscreen menu.** Choose *Settings → Network → Wi-Fi Setup Wizard* (wording varies), pick your network, type the password with the tiny arrows, and wait for a checkmark or "Connected" message. Print the *Network Configuration* page—its IP address is useful later.

**Route B — The maker's phone app.** Manufacturers ship apps (names vary by brand) whose entire job is orchestrating this connection. The app usually asks for temporary Bluetooth or location permission to find the printer—that's normal. Follow the prompts; the app is often better at Wi-Fi passwords than the printer's buttons are.

**Route C — WPS button pairing.** Press *WPS* on the printer's menu, press the *WPS* button on your router within two minutes. No password needed.

**Route D (fallback) — The USB cable.** If Wi-Fi refuses to cooperate, connect USB, let the computer set the printer up, and enable *Wi-Fi setup via USB* in the utility app. Once the printer knows the password, unplug the cable.

> **Sidebar: why the USB cable?** A cable takes your "which link is broken?" puzzle and turns it into "it's definitely the Wi-Fi step." Serial debugging beats parallel debugging. A nurse paging a doctor knows the value of knowing *which* thing to check first.

## Step 2: Put your devices on the same network

- **Windows:** Settings → Bluetooth & devices → Printers & scanners → Add device. Your printer will appear by name in under a minute.
- **Mac:** System Settings → Printers & Scanners → the `+` button, pick your printer from the list.
- **iPhone/iPad:** use Print from the share sheet; AirPrint usually finds network printers automatically.
- **Android:** Add print service in Settings → Printing, or use the maker's app.

Check that phones, laptops, and the printer are all on the **same SSID**. Guest networks and "IoT Isolation" settings (sometimes called *Client Isolation* or *AP Isolation*) will invisibly block discovery—disable them for the printer, or move everything to the main network.

## Step 3: The test

1. From a laptop, print a one-page test document.
2. From your phone, print a photo or PDF.
3. Walk away. Print from the other room tomorrow to confirm.

If both work, you're done. If a device doesn't find the printer:

- Restart the printer (30 seconds unplugged—count them, it matters for network stacks).
- Then restart the router. Then the device. In that order.

## When Wi-Fi printing breaks months later

This is almost always one of three events:

| Trigger | Symptom | Fix |
| --- | --- | --- |
| New router or changed password | Printer went "offline" at once | Chapter 3 Step 1 again—forget the old network, rejoin |
| Printer got a new IP address | Mac or Windows "printer not responding" | In the device settings, delete and re-add the printer, or set a DHCP reservation for the printer in your router |
| ISP/router swap to 2.4 GHz and 5 GHz split bands | Phone prints, laptop doesn't (or vice versa) | Connect both to the same band or enable band steering |

**The DHCP reservation trick** is worth doing once: in your router's admin page, find the printer's MAC address and assign it a fixed IP (like `192.168.1.50`). After that, network hiccups stop re-shuffling your printer's address, and long-standing setups keep working for years.

## A word about "offline"

The word "Offline" in a print dialog usually *doesn't* mean the printer is off. It means your computer couldn't shake hands with the printer at the moment it tried. The queue is a great debug view here: if the job says "Sending…" forever, the network path is broken (chapter 7 covers queue surgery).

## Chapter 3 in one sentence

*Put the printer and your devices on the same network, fix the printer's address so it stops wandering, and keep the printer's own password page filed with the Wi-Fi password you keep forgetting.*
