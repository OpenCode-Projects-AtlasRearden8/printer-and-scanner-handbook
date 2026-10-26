# Troubleshooting flowchart

One diagram, five minutes, calm all the way through. Start at the top and answer honestly; the first "yes" or "no" is the road.

## The diagram

![Printer Rescue Flowchart — from "not printing" to fixed in a few calm steps](assets/flowchart.svg)

*(The same path, in text, below — the diagram is decorative help, this is the real thing.)*

## The flow, as a checklist

**Start: "It didn't print."**

1. **Does the printer have power and no error showing on its screen?**
   - **No** → fix the obvious (plug, outlet, error icon). If its screen shows a *specific* error (jam, ink, offline), follow that error first—trust the printer's own opinion.
2. **Can it make a copy or test page from its own panel?**
   - **No** → printer-side issue: check paper, supplies (chapter 7, fifth stop), or a phantom jam → sensor sweep.
   - **Yes** → computer-side. Move to step 3.
3. **Are there stuck jobs in the print queue?**
   - **Yes** → cancel all, resend. (This alone ends half of all mysteries.)
   - **No** → continue.
4. **Does the queue list the right printer—same name, not a duplicate "Copy 1"?**
   - **No** → select the real one, delete the impostor.
5. **Is the printer online on the network, on the same Wi-Fi as the device?**
   - **No** → chapter 3 setup again; set a DHCP reservation.
6. **Does a test print now produce fine text?**
   - **No, garbage** → driver reinstall (chapter 7, second stop).
   - **No, faded/streaky** → supplies & head-clean (chapter 7, fifth stop).
7. **Still stuck after all of that?** → restart printer (unplugged 30 s) → router → computer, then the escalation ladder in chapter 7.

## When to stop

You get to stop when:

- The page prints, or
- You've hit the escalation ladder and the next honest step is "search the model number + error," or
- Fifteen minutes have passed and tomorrow has a calmer forecast.

That third stop is loving and real: **some fixes are better tomorrow** (firmware updates, manufacturer escalations, or head-soak cycles that need hours anyway). Walking away isn't defeat; it's triage.
