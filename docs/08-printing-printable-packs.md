# Chapter 8: Printing the printable packs beautifully

This site ships [printable packs](printable-packs/printer-rescue-checklist.html): one-page checklists, planners, and worksheets designed to be printed and kept in a drawer. This chapter is how to make them look great on paper, with no invisible margins, cut-off checkboxes, or mystery scaling.

## What the packs are

| Pack | Pages | Good for |
| --- | --- | --- |
| [Printer Rescue Checklist](printable-packs/printer-rescue-checklist.html) | 1 | Taping inside a cabinet door; the calm path to a fix |
| [Ink & Toner Budget Planner](printable-packs/ink-budget-planner.html) | 1 | Running chapter 5's math on the real supplies you buy |
| [Weekend Maintenance Tick-Sheet](printable-packs/weekend-maintenance.html) | 1 | The five-minute monthly ritual from chapter 1, as a checkbox page |

Every pack is plain HTML with a dedicated print stylesheet. No accounts, no downloads with fonts, no plug-ins: open the page, press `Ctrl+P` (or `Cmd+P`), done.

## The three settings that matter in the Print dialog

1. **Paper size = the size you actually have.** `Letter` (US/Canada) or `A4` (almost everywhere else). Getting this wrong is the #1 cause of "everything is shifted".
2. **Scale = 100% / "Actual size".** The "Fit to page" and "Shrink to fit" options silently re-scale everything and eat your margins. Our designs are already sized correctly; choose *Actual size* and stand back.
3. **Margins = Default.** The packs already define their own safe zone inside the page. If you must change margins, keep them at their default.

**Skip:** headers and footers (the date/URL clutter) — untick "Headers and footers" for a clean sheet. **Background graphics:** leave ON for the shaded header to print if you want it; the design is legible either way.

## From your browser, step by step (Chrome/Edge, but Firefox and Safari are the same idea)

1. Open a pack page from the links above.
2. `Ctrl+P`. A preview appears on the right.
3. Check: Destination = your printer, Paper size = Letter/A4, **Scale = 100%**, Margins = Default, Headers/footers = off.
4. Look at the preview: does the footer's "cut here" line still have white around it? Then you're perfect. Print.
5. For a PDF instead of paper: set Destination to **Save as PDF**. Same settings, no printer involved.

## Phones and tablets

The phone print path re-flows pages, which *will* shift the layout. Two honest options:

- **Easiest:** open the pack on a computer and print from there.
- **On the go:** open the pack page in any mobile browser → Share → Print → choose your AirPrint/Default Print Service printer. If the layout is cramped, use "Save as PDF" from the same dialog, then print the PDF from your device's PDF viewer—that halts re-flowing.

## Beautiful-printing checklist (the short version)

- [ ] Paper size matches (Letter vs A4)
- [ ] Scale 100%, not "fit"
- [ ] Headers/footers off
- [ ] Preview shows nothing clipped
- [ ] Fresh, non-curled paper; one page at a time for cardstock
- [ ] 60–80gsm office paper for checklists; 120gsm+ for anything you'll write on with a marker

## Why the packs are built this way

The packs use:

- **A print stylesheet** (`@media print`) that hides site navigation, expands the useful area, and adds page-break rules so nothing splits in half.
- **A fixed-width chassis** sized to the printable zone of both Letter and A4, which is why both come out centered.
- **No webfonts.** Your installed fonts match the design, so the layout doesn't shift while loading or print while a font half-arrives.

If you'd like to tweak a pack for your own needs, view the page source and edit the HTML; it's plain, commented-by-structure markup, and re-saving as PDF gives you a custom sheet in two minutes.

> **Calm humor corner:** "Fit to page" is the printer's way of saying "I'll take it from here." Be kind to yourself and decline.
