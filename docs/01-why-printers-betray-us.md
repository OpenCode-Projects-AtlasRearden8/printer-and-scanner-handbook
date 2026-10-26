# Chapter 1: Why printers betray us

Let's start by clearing something up: your printer is not broken, cursed, or holding a grudge. It is doing exactly what it was designed to do, which is to be a $49 machine pretending to be a $400 machine.

## The economics of the "cheap" printer

Printer manufacturing runs on a strange bargain:

- **The box is nearly given away.** The manufacturer may barely profit—or lose money—on the printer itself.
- **The supplies are where the money lives.** Ink is one of the most expensive liquids on Earth by volume, and cartridges carry fat margins.
- **You are the subscription.** Every time you buy ink, yesterday's "great deal" finishes paying for itself.

This explains a lot of behavior that looks like betrayal:

1. **"Genuine ink" warnings** that appear before the ink is actually gone. Caution is legal cover, not measurement.
2. **Cartridges that "dry out"** between rare printings. Inside many inkjets, a printhead sits exposed to air; neglect it and it clogs.
3. **Ink subscriptions with page limits and region locks.** Subscription pricing wants loyal customers, and loyalty is hard to engineer if ink works flawlessly forever.

## Why printers are *harder* than they sound

People who design software for a living are often humbled by printer firmware. Printers are hard because they combine four disciplines at once:

- **Physics:** squirting picoliter-sized ink droplets accurately onto moving paper, or fusing dry powder with a heated roller.
- **Mechanics:** rollers, gears, sensors, trays, and paper that's slightly damp, slightly curved, or slightly static-charged.
- **Networking:** a low-memory device that must speak Wi-Fi to laptops, phones, and tablets made by companies who don't coordinate with each other.
- **Firmware updates:** the equivalent of open-heart surgery performed while the patient is in use.

Most "the printer is possessed" moments are actually one of these four systems having a small, ordinary failure. That's good news. Ordinary failures have ordinary fixes.

## The behavior that isn't a bug

A few "features" feel adversarial but have boring explanations:

| What it does | Why | What to do |
| --- | --- | --- |
| Says "paper jam" with no paper visible | A tiny sensor flag is stuck | Chapter 7's sensor sweep, 5 minutes |
| Refuses black-and-white when one color is empty | Nozzles mix ink; one dry channel can clog others | Keep all cartridges above empty, or buy a laser |
| Wi-Fi vanishes after the router updated the network | Printer remembered the old settings | Chapter 3: forget and rejoin the network, 10 minutes |
| Jobs sit as "Sending" forever | The spooler is holding a stuck job | Chapter 7: clear the queue |

## The maintenance ritual that prevents almost everything

Printers thrive on routine the way plants do. Once a month, about five minutes:

1. **Print a test page or a colorful something** so nozzles stay clear.
2. **Wipe the scanner glass** with a damp microfiber cloth (inkjet-safe glass cleaner sparingly).
3. **Vacuum or blow out the paper tray** area; dust is a jam in training.
4. **Leave the printer powered on or use its own sleep mode.** Turning inkjets fully off and on aggressively trips automatic cleaning cycles that waste ink.

That's it. The monthly ritual is deliberately dull. Dull means the emergencies never happen.

> **Calm humor corner:** A printer is like a cat. It doesn't need much, it needs it predictably, and it has no concept of your deadline. Respect the schedule and you'll get along fine.

## What this means for chapter 2

Now that you know the rules of the game, you can choose machines that either play it well (reliable workhorses with cheap supplies) or sidestep it (laser printers that shrug at neglect). That's exactly what the next chapter is for.
