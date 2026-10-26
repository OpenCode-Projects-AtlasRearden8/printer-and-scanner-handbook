# Chapter 7: Driver and spooler fixes

This is the repair manual for the 90% of "my printer doesn't work" cases. Do the steps in order; stop as soon as printing works. Total time: usually 10 minutes. No tears, no calls.

## The 60-second triage (do this first, every time)

1. **Is the printer on?** Lights on, no error icon on the screen.
2. **Is there paper, loaded correctly?** Square in the tray, not over the fill line.
3. **Any error on the printer's own screen?** It will often tell you exactly what's wrong; the computer's dialog may not.
4. **Is the printer paused or offline in the queue?** See below.
5. **Does a test/copy work from the printer's own panel?** If the printer can copy but the computer can't print, it's a computer-side issue (spooler/driver). If it can't even copy, it's a printer-side issue (supplies, jam, sensor).

## First stop: the print queue (spooler surgery)

The spooler is the assembly line between your "Print" click and the printer. A single stuck old job can stop the whole line.

**Windows:**

1. Open the queue: Settings → Bluetooth & devices → Printers & scanners → your printer → **Open print queue**.
2. Right-click every job → **Cancel**. Or click the queue's menu → *Cancel all*.
3. If a job won't cancel: restart the **Print Spooler** service. Press `Win+R`, type `services.msc`, find *Print Spooler*, right-click → Restart. Then open `C:\Windows\System32\spool\PRINTERS` and delete files there (only with the spooler stopped) if it's still frozen.

**Mac:** Open Printer settings (System Settings → Printers & Scanners → your printer) and click completed/stuck jobs to cancel. If the queue is cursed, delete the printer and re-add it (it takes 30 seconds; your settings don't matter much).

> Confirming the classic: roughly half of all "the printer does nothing" moments end at this exact step. Cancel all, resend.

## Second stop: the driver (when jobs do nothing or print garbage)

**Symptoms that mean "driver":** pages of gibberish symbols, jobs vanish without printing, printer ignores dialogs entirely.

- **Restart-then-repair:** Windows Settings → your printer → "Remove", then Add device again. The modern stack matches most printers automatically with a good generic driver.
- **The maker's driver:** if the generic route misbehaves, download the *full feature* driver from the manufacturer's support page (not the model number you remember—the number on the sticker). Install after uninstalling the old one.
- **Mac:** delete the printer in Printers & Scanners, re-add it; macOS fetches its own driver set. For stubborn cases, the maker's utility "removes and reinstalls" in one click.
- **USB escape hatch:** if Wi-Fi printing is cursed but the machine and cable are available, USB sidesteps the entire network dimension. It's not permanent—it's diagnostic. (Chapter 3 uses the same trick in reverse.)

## Third stop: the jam (the careful version)

1. **Turn the printer off** before hunting jammed paper—moving rollers find fingers.
2. **Open all the doors** (front tray, rear duplex door, ADF lid) and *look along the paper path*. Use a phone flashlight; a torn corner hiding in a roller is the classic repeat jammer.
3. **Pull paper in its direction of travel**, both hands, slowly. Yanking sideways tears corners or worse.
4. **Clear the ADF separately.** ADF jams hide under the small lid next to the scanner—lift it, look for the rolled page edge.
5. **Check for obstructions** (paperclips like to live in the tray's paper guide), and confirm all doors click fully shut; an unlatched sensor stops printing as surely as a jam does.

## Fourth stop: "Paper jam" with no paper anywhere

A tiny plastic flag sensor is stuck. With the printer **off**:

- Gently wave a firm sheet of cardstock or stiff paper through every paper path door, in and out, both directions, to flip the sensor back.
- Blow out (or vacuum) the path. Dust + humidity makes sensor flags stick.

That's the whole ritual. Five minutes, and it fixes the ghost-jam that isn't there.

## Fifth stop: supplies and quality

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Faded, streaky, or striped pages | Low/empty tank, or a clogged nozzle (inkjet only) | Run the printer's own **head cleaning** utility, then a nozzle check; two cycles max, then wait an hour—over-cleaning wastes ink and heats the head |
| Ghost images or grey smears (laser) | Drum/fuser near end of life or dirty | Replace the drum unit per the printer's guide, or run its cleaning page |
| Vertical white lines only in color photos | One empty color channel | Replace that cartridge; mixed-channel printing mixes ink |
| Wrinkled/creased paper | Damp paper, wrong tray setting, bad roller | Fresh ream, fanned, correct tray size setting in the dialog |
| Everything skewed at an angle | Paper guide too wide in the tray | Slide the guide snug against the stack |

## Fifth-and-half stop: the networks again

If the printer "shows offline" only sometimes: chapter 3's DHCP-reservation trick ends the endless offline flicker. If it shows offline *always* after a router change: forget the printer's saved Wi-Fi, rejoin the network, then re-add the printer on each computer once.

## The escalation ladder (when 90% fails)

1. **Restart everything in order:** printer unplugged 30 seconds → router → computer.
2. **Print from a different device.** If phone prints and laptop doesn't, it's laptopy. If nothing anywhere prints, it's printerly.
3. **Print a self-test from the printer's own panel.** This tells you the machine's hardware opinion independent of every computer.
4. **Update firmware** from the maker's app (a 5–15 minute non-negotiable wait; don't power off mid-update).
5. **Search the model number + your exact error text.** Somebody has had this in 2019; their thread is your shortcut.

> **Calm humor corner:** You now know the sequence: queue → driver → jam → supplies → network → firmware. You will almost never reach step six. Print this chapter once, put it in the drawer under the printer, and let the drawer do the remembering.
