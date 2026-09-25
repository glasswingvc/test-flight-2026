# Test Flight 2026: Submissions

This is where every Test Flight team hands in its project. You build in your own GitHub repo. When you're ready, one person on your team adds a single file here that describes your team and links to your code.

Questions on the day: find any Glasswing staffer on the floor.


## Sunday deadlines

1:00 PM. First PR due. Open your submission pull request (Step 4 below) by 1:00. We use it to set the order teams present in, and we'll share that order before 2:00. If your check is still red at 1:00, find a staffer and we'll help you fix it.

2:00 PM. Code freeze. We judge the latest commit on your repo's main branch as of 2:00. You can keep pushing code between 1:00 and 2:00.

Show and tell runs 2:00 to 4:30 PM. Every team shows the judges what they built, running live. No slides, decks or videos needed. Be back at 275 Newbury Street by 2:00 if you've been building somewhere else.


## Step 1. Make your team repo

One person on the team does this on Saturday, once your team is set.

1. Go to github.com/glasswingvc/test-flight-starter
2. Click "Use this template", then "Create a new repository". Make it under your own GitHub account.
3. Set it to Public, so judges can open it. Keep it public until awards wrap on Sunday.
4. Add your teammates under Settings, then Collaborators. They need to accept the invite from their email or GitHub notifications before they can push.

The starter is optional. Any public GitHub repo works as long as the README covers the sections in Step 3.


## Step 2. Keep your keys out of GitHub

If an API key ends up in a public repo, bots find it within minutes and start using it.

Put keys in a file called .env. The starter repo already keeps that file out of GitHub. If you push a key by accident, tell a staffer right away so we can delete it and give you a new one.


## Step 3. Fill in your README

Judges read your README while you present and again afterward. The starter has these sections ready:

- The problem, and who inside a company has it
- Who pays for this and why they'd buy it
- How it works, and where the AI does something regular software couldn't
- What's real and what's mocked
- How to run it
- Anything built before this weekend

Judges score four things equally: customer problem, business case, operational fit and AI differentiation.


## Starting from scratch or bringing a project

Both are fine. Most teams start from scratch. Either way, judges score what you build this weekend.

If you start from scratch, there's nothing extra to do. Put `prior_work: none` in your submission file.

If you bring existing code, do two things:

1. Before you write anything new, commit your existing code exactly as it was before the weekend, with the commit message `prior work`. That lets judges see what you added this weekend.
2. In your submission file, describe what you brought under `prior_work`.

Open-source libraries, public models and APIs don't count as prior work.


## Step 4. Open your first PR (by 1:00 PM Sunday)

One person per team does this in the browser. No git commands needed.

1. Go to github.com/glasswingvc/test-flight-2026 and open the `submissions` folder.
2. Open `_TEMPLATE.yml` and copy everything in it.
3. Go back to the `submissions` folder. Click "Add file", then "Create new file". Stay inside the submissions folder when you do this.
4. Name the file after your team, all lowercase with hyphens instead of spaces. Example: `ledgerline.yml`
5. Paste the template and fill it in. The `slug` line must match your file name without `.yml`.
6. Click "Commit changes", then "Propose changes", then "Create pull request" (you'll click it twice).

About a minute later a check runs on your submission. If you've never contributed to a public GitHub repo before, it may say it's waiting for approval. A staffer will start it for you.

- Green check: you're done. A staffer will merge it.
- Red X: click "Details" to see what to fix, then edit your file (see below). The check runs again on its own.

To edit your file before it's merged: open your pull request, go to the "Files changed" tab, click the "..." menu on your file and choose "Edit file".

To edit your file after it's merged: open it in the `submissions` folder, click the pencil icon and propose the change. That opens a new pull request, which is fine.

Your first PR is due at 1:00. Edits to it are fine until 2:00.


## Example submission file

```yaml
team_name: Ledgerline
slug: ledgerline
members:
  - name: Alex Rivera
    github: arivera
  - name: Priya Nair
    github: priyanair
repo: https://github.com/arivera/ledgerline
description: >
  Matches supplier invoices to purchase orders and contracts, and flags the
  ones that don't line up.
customer: Accounts payable teams at mid-size manufacturers
live_url: ""
prior_work: none
```

Example team. Names and handles are made up.

| Field | What to put |
|---|---|
| team_name | Your team's name |
| slug | Your file name without `.yml` |
| members | Name and GitHub handle for each person, 1 to 6 people. No emails or phone numbers, since this repo is public. |
| repo | Link to your public GitHub repo |
| description | What it does and for whom, one or two sentences (280 characters max) |
| customer | Who inside a company would use it |
| live_url | Optional. Where a judge can try it |
| prior_work | `none`, or what you brought in from before the weekend |


## Rules

- One submission file per team. Only add or edit your own file. Follow-up pull requests that edit your own file are fine.
- Each person is on one team only.
- Keep your team repo public until awards wrap on Sunday.
- Only the submission file goes in this repo. Your code stays in your own repo.


## Your code is yours

Glasswing does not own your code or anything you build at Test Flight. It stays in your own GitHub repo, under your own account.

Shortly after the event, we'll delete this submissions repo, which removes our links to your code. Submitting creates a copy (a fork) of this repo under your account, and you can delete that too. Once awards wrap on Sunday, you're free to make your repo private.


## If the check goes red

| Message | Fix |
|---|---|
| something is required | A field in the template is still blank. Fill it in |
| slug does not match file name | Make the file name and the slug line match, all lowercase |
| repo is not reachable, private or empty | Make your repo public, check the link and push at least one commit |
| description is too long | Cut it to 280 characters |
| duplicate member | Someone is also listed on another team's file. Sort it out with that team or find a staffer |
| exactly one submission file, or files outside submissions/ | Your pull request should only add or edit your own file inside the submissions folder |
| YAML could not be parsed | Usually a tab instead of spaces, or a colon inside a value. Put quotes around the value |
