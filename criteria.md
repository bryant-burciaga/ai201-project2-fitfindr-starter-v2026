# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. The item that matched is the item that gets styled

Given a query that matches at least one listing, the "id" of
session["selected_item"] after the run is the same id that was passed into
suggest_outfit — checked by comparing ids directly — in 5 of 5 tries.

**Why this target:**

This is a plain dictionary lookup with no model call involved, so there's
no randomness to account for. If the session correctly carries the item
once, it should carry it every time.







---

## 4. Fit cards aren't identical copies of each other

Given the same item run through create_fit_card three separate times, the
three captions are not word-for-word identical to each other — in at least
2 of 3 tries.

**Why this target:**

TEMPERATURE is set to 0.9, so real variation is expected, but not
guaranteed on every single call — the model could still land on similar
phrasing by chance for a short caption. 2 of 3 leaves room for that without
letting the test pass if caching or a stuck temperature setting is quietly
producing the same caption every time.


---

## 5. A bad search gives a specific reason, not a dead end

Given a query that matches nothing in the listings data, the message in
session["error"] names at least one concrete thing the user could change
(price, size, or wording) rather than just saying no results were found —
5 of 5 tries.

**Why this target:**

This is plain string-building with no model call, so it should be
consistent every time. I care about this one because "no results" with
nothing else is a dead end for the user — the whole point of the branch
message is to tell them what to try next.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
