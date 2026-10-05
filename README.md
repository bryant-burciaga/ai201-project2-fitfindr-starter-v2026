# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is an agent that helps with thrifting. Users can give it a plain-language
request like "vintage graphic tee under $30" and it searches a listings
dataset, picks the best match, suggests how to style it with your existing
wardrobe, and writes a short social-media-style caption about the find. If
nothing in the data matches the request, it stops and tells you what to
change instead of guessing.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### search_listings
- Does: searches listings by keyword, optional size and max price
- Inputs: description (str), size (str or None), max_price (float or None)
- Returns: list of listing dicts, best match first
- Empty case: returns an empty list

### suggest_outfit
- Does: suggests outfits pairing a new item with the user's wardrobe
- Inputs: new_item (dict), wardrobe (dict with "items" key)
- Returns: a string with 1-2 outfit suggestions
- Empty case: if wardrobe has no items, gives general styling advice instead

### create_fit_card
- Does: writes a short social-caption-style blurb about the item and outfit
- Inputs: outfit (str), new_item (dict)
- Returns: a 2-4 sentence caption string
- Empty case: if outfit is empty/blank, returns a message saying so instead of calling the model

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

## Planning Loop

Branch rule: if search_listings returns an empty list, the loop puts a
specific message in session["error"] and stops before calling
suggest_outfit. Otherwise it takes the first search result and continues
through suggest_outfit and create_fit_card.

This lives in agent.py, in the run_agent() function.

---

## Sample Run

### Per-tool terminal tests

Command: `./.venv/bin/python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"`

Output: [{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', ...}]  (6 listings total, truncated here for README length — full output confirmed in terminal)

Command: `./.venv/bin/python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"`

Output: **Outfit 1: Casual Streetwear**
Pair the vintage Levi's 501s with the white ribbed tank top tucked in, layering the oversized grey crewneck sweatshirt on top for an effortless, textured look. Finish the outfit with the chunky white sneakers and the black crossbody bag for an easy, everyday vibe.

**Outfit 2: Edgy Contrast**
Style the medium wash jeans with the black cropped zip hoodie to play with proportions, cinched at the waist using the brown leather belt. Ground the look with the black combat boots and throw on the vintage black denim jacket for a cool, double-denim aesthetic.

Command: `./.venv/bin/python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"`

Output: Found my holy grail denim on Depop for just $38! Honestly obsessed with the wash on these vintage 501s. Paired them with crisp white sneakers and I'm officially never taking them off.
### Full agent run

Command: `./.venv/bin/python agent.py`

Output: === A query the data can match ===
  found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  outfit:   **Outfit 1: Casual Y2K Contrast**
Pair the butterfly baby tee with your baggy dark-wash straight-leg jeans for a classic early-2000s silhouette. Cinch the waist with your brown leather belt, and finish the look with chunky white sneakers and the black crossbody bag.

**Outfit 2: Edgy Streetwear Mix**
Layer the feminine graphic tee underneath your black cropped zip hoodie for a balanced, textured look paired with your wide-leg khaki trousers. Ground the outfit with your black combat boots to lean into an effortless vintage-meets-modern aesthetic.
  fit card: Obsessed with this little butterfly tee I scored on Depop for just $18! 🦋 It's so easy to dress down with baggy denim and chunky sneakers, or layer under a zip hoodie with combat boots for when I want a more edgy vibe. Which fit are we feeling more?

=== A query it can't ===
  stopped: No listings matched 'designer ballgown' under $5 in size XXS. Try a broader description, a higher price, or a different size.
  fit_card is None — it should still be None here

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

I used claude extensively on this particular project, in particular to help with implementing the three tool funcitons in tools.py, the planning loop in agent.py, and working with the README and all of the different TODOs in the starter code. I did end up using a keyword matching approached that I asked claude for help on in the search_listings and helped to make sure all the words in the title, description, style, etc. all worked. I also used it to help with testing all of the different loops to help complete all the milestones. 


**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
