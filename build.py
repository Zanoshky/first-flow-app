#!/usr/bin/env python3
"""Builds the guide pages in docs/ from the bodies below. Run after any edit and commit docs/. Fails on any dash.

The look is the Zanoshky Standard, the same as firstflow.zanoski.com: docs/tokens.css is a copy of the house
tokens (never edit it here), docs/style.css maps them to First Flow's rose looks and holds the guide's own parts. Both are inlined into every page so no
stylesheet holds up the first paint. Every screenshot in docs/img is a real capture of the app."""
import re
from pathlib import Path

D = Path(__file__).parent / "docs"
REPO = "https://github.com/Zanoshky/first-flow-app"
PLAY = "https://play.google.com/store/apps/details?id=com.zanoshky.firstflow&amp;referrer=utm_source%3Dgithub%26utm_medium%3Dguide%26utm_campaign%3Dfirst-flow-2026-11"
SITE = "https://firstflow.zanoski.com"
MAIL = "support@zanoski.com"
NAV = [("index.html", "Home"), ("guide.html", "Guide"), ("faq.html", "Questions"), ("report.html", "Report a bug")]

CSS = "\n".join((D / f).read_text() for f in ("tokens.css", "style.css"))
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s*\n\s*", "\n", CSS).strip()


def shot(img, alt, name, line, lazy=True):
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    stem = img.rsplit(".", 1)[0]
    # The jpg stays for the README on GitHub; pages pick a small webp, about half the bytes.
    src = f'srcset="img/{stem}-300.webp 300w, img/{stem}-540.webp 540w" sizes="(min-width: 840px) 260px, 45vw"'
    return (f'<figure><img src="img/{img}" {src} alt="{alt}" width="540" height="1200" {load}>'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure>')


def tv(img, alt, name, line):
    stem = img.rsplit(".", 1)[0]
    src = f'srcset="img/{stem}-480.webp 480w, img/{stem}-960.webp 960w" sizes="(min-width: 1140px) 540px, (min-width: 640px) 48vw, 100vw"'
    return (f'<li><figure class="tv"><img src="img/{img}" {src} alt="{alt}" width="960" height="540" loading="lazy" decoding="async">'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure></li>')


def page(name, title, desc, body):
    for bad in ("\u2014", "\u2013", " - "):
        if bad in body:
            raise SystemExit(f"{name}: dash {bad!r} in copy")
    nav = "".join(f'<a class="hide-s" href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    foot = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in
                   [(SITE, "Home"), ("index.html", "User guide"), ("faq.html", "Questions"), ("report.html", "Report a bug"),
                    (f"{SITE}/privacy", "Privacy"), (f"{SITE}/terms", "Terms")])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · First Flow user guide</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fbf5f3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#120a0e" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title} · First Flow user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/jetbrains-mono-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/icon.svg" alt="" width="34" height="34"><span>First Flow</span></a>
    <nav aria-label="Guide pages">{nav}<a class="key" href="{PLAY}">Get the app</a></nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>First Flow by <a href="https://zanoski.com">Marko Zanoski</a></span>
    <nav aria-label="Footer">{foot}</nav>
    <p class="lic">Guide text and images are shared under CC BY 4.0. The First Flow app itself is proprietary.</p>
  </div>
</footer>
</body>
</html>
"""
    (D / name).write_text(html)
    print(name)


HOME_ALT = "First Flow Home in Dusk: Good evening, A gentle evening, How long do you have?, Warrior II as the pose of the day in its arch, the 5 min, 10 min and Full flow lengths, the Steady, Slow and Calm paces and a big Begin key, with Home, Poses, Science and Settings in the bar."
FLOW_ALT = "The flow in Blush, paused before Mountain, pose 1 of 20 with 21:57 left: the figure stands in its arch, the breath ring shows 2, and under it Paused, Tap play when you are ready, with previous, play and next keys."
POSE_ALT = "The Mountain pose page in Blush, 01 of 20: the figure stands tall, Tadasana under the name, a Hold 5 breaths chip with five breath dots, and the How to steps."
POSES_ALT = "Poses in Dusk: 20 gentle poses, in the order you flow them. Tap one to learn it. Cards for Mountain, Tree, Chair and Standing Forward Fold, each with its number, Sanskrit name and hold."
SCIENCE_ALT = "Science page 1 of 4 in Dusk: Slow breathing, 10 or fewer breaths a minute, a chart that marks Steady and Slow, Calm, and a short summary of the research."
DONE_ALT = "The done screen in Blush: Corpse Pose in its arch, Flow complete, Well done., Stay in the quiet a little longer, then rise slowly, 20 poses, 22 minutes and 141 breaths, then the card A little ritual, Shall I remind you tomorrow?"
WIDGET_ALT = "An Android home screen with the First Flow widget: the pose of the day, Standing Forward Fold, the line 5 min, Steady, Done today, and a Begin key."
SETTINGS_ALT = "Settings in Dusk: Look set to Dusk, then Practice with Breath pace, Get ready time, Sound and Daily reminder, the note that yoga should never hurt, and Privacy."
SOUND_ALT = "The Sound page in Dusk: Singing bowls and Voice guide switched on, then Under the flow with Calm music chosen over Singing bowl bath and Silence."
PRIVACY_ALT = "Privacy in Dusk: red ban chips No ads, No tracking, No analytics, No crash reports, No error reports, No account, No AI and No internet, then the Notifications and Run at start up permissions and Internet, location, contacts, camera and microphone denied by design."
LOOK_ALT = "The Look page in Dusk: Follow the phone, Blush, Dusk and Black tiles, with Dusk chosen."

page("index.html", "Home", "The user guide for First Flow, gentle beginner yoga for Android phones, tablets and TVs.", f"""
    <p class="lbl">User guide</p>
    <h1>First Flow</h1>
    <p class="lede">New to yoga? Press Begin and First Flow guides you through 20 gentle beginner poses, one breath at a time, with a breath ring, soft singing bowls and a warm voice. Pay once, no ads, no account, works fully offline. On phones, tablets, Android TV and Google TV.</p>
    <div class="keys">
      <a class="key filled" href="guide.html">Read the guide</a>
      <a class="key tonal" href="report.html">Report a bug or ask for a feature</a>
    </div>
    <ul class="shots">
      <li>{shot("home.jpg", HOME_ALT, "Home", "Pick a length and a pace.", lazy=False)}</li>
      <li>{shot("flow.jpg", FLOW_ALT, "The flow", "One breath at a time.")}</li>
      <li>{shot("pose.jpg", POSE_ALT, "A pose", "Steps and an easier way in.")}</li>
      <li>{shot("done.jpg", DONE_ALT, "Well done", "Poses, minutes and breaths.")}</li>
    </ul>
    <ul class="tvshots">
      {tv("tv-home.jpg", "First Flow Home on a TV with the side rail on the left, Warrior II as the pose of the day, Full flow and Steady chosen, 22 min and 20 poses, and Begin in focus.", "On a TV", "Begin is in focus: press OK.")}
      {tv("tv-flow.jpg", "The flow on a TV holding Mountain, pose 1 of 20: the figure on the left, the breath ring beside Breathe out, Up next, Tree, the pause key in focus and the hint OK pauses, Back ends the flow.", "The flow on a TV", "OK pauses, Back ends.")}
    </ul>
""")

page("guide.html", "Guide", "How to use First Flow: Home, the guided flow, Poses, Science and Settings, the widget, the reminder and Android TV.", f"""
    <p class="lbl">Guide</p>
    <h1>How First Flow works</h1>

    <div class="with-shot">
      <div class="doc">
        <h2>Start in one tap</h2>
        <p>First Flow opens on Home. It greets you by the time of day, shows the pose of the day in its arch, and asks how long you have. Pick a length, pick a pace, and press Begin.</p>
        <dl class="rows plate">
          <div><dt>5 min and 10 min</dt><dd>A new mix of standing, floor and seated poses each time.</dd></div>
          <div><dt>Full flow</dt><dd>All 20 poses in order, about 20 minutes.</dd></div>
          <div><dt>Steady</dt><dd>4 in and 4 out.</dd></div>
          <div><dt>Slow</dt><dd>5 in and 5 out.</dd></div>
          <div><dt>Calm</dt><dd>4 in and 6 out, a longer out breath to settle you.</dd></div>
        </dl>
        <p style="margin-top:16px">Tap the pose of the day to read about it.</p>

        <h2>Four sections in the bar</h2>
        <p>The bar at the foot of the screen has Home, Poses, Science and Settings. Tap one to go there, or tap the one you are on to go back to its top. The three dots at the top right open More, with Add the widget.</p>
      </div>
      {shot("home.jpg", HOME_ALT, "Home", "Length, pace and Begin.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>The flow</h2>
        <p>Each pose starts with a short Get ready time to move into it (5, 7 or 10 seconds, set in Settings), then you hold it for a few slow breaths. The breath ring fills as you breathe in and empties as you breathe out, and its number counts the seconds left in this breath. The words say Breathe in or Breathe out, and which breath of the hold you are on.</p>
        <p>Poses that work one side at a time give each side its turn: Hold, first side, then Switch sides, then the second side. Near the end of a pose you see what is up next.</p>
        <dl class="rows plate">
          <div><dt>Pause and play</dt><dd>The big round key in the middle.</dd></div>
          <div><dt>Previous and next</dt><dd>The keys on each side go back a pose or skip ahead.</dd></div>
          <div><dt>End the flow</dt><dd>The cross at the top left.</dd></div>
        </dl>
        <p style="margin-top:16px">The screen stays on while the flow runs. A call or another app playing sound pauses it, and so does pulling out headphones; press play when you are ready.</p>
      </div>
      {shot("flow.jpg", FLOW_ALT, "The flow", "The ring follows your breath.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Well done</h2>
        <p>At the end you see how many poses, minutes and breaths you gave yourself. After a short flow, Another mix starts a fresh one; after the full flow, Flow again starts over.</p>
        <p>On a phone, First Flow may ask once: Shall I remind you tomorrow? Pick Morning, Midday, Evening or another time and tap Yes, remind me, or Not now. After two Not now it never asks again.</p>
      </div>
      {shot("done.jpg", DONE_ALT, "Well done", "And a gentle reminder, if you like.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Poses</h2>
        <p>Poses lists all 20 in the order you flow them: Mountain, Tree, Chair, Standing Forward Fold, Warrior I, Warrior II, Triangle, Low Lunge, Plank, Downward Facing Dog, Cobra, Cat, Cow, Child's Pose, Easy Seat, Butterfly, Seated Forward Fold, Bridge, Knees to Chest and Corpse Pose.</p>
        <p>Tap a pose to open its page: its Sanskrit name, how long you hold it, three short How to steps in plain words, and an easier option, so you can go at your own pace. Start the flow here begins the flow from that pose. Previous and next take you to the poses around it.</p>
      </div>
      {shot("poses.jpg", POSES_ALT, "Poses", "All 20, in flow order.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Science</h2>
        <p>Science has four short pages, one finding each, with a clear chart: slow breathing at 10 or fewer breaths a minute, heart and breath at 6 a minute, the long out breath, and a little every day. The charts mark the pace you chose. Turn the pages with Previous and Next, or swipe.</p>
        <p>First Flow is a gentle practice, not a treatment. Stop if anything hurts, and ask a doctor if you are unsure.</p>
      </div>
      {shot("science.jpg", SCIENCE_ALT, "Science", "Four findings, four charts.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>The widget</h2>
        <p>The home screen widget shows the pose of the day and begins your flow in one tap. It grows with its size, from a slim bar to the pose large with its Sanskrit name. Add it from Settings, Widget, or from More, or touch and hold your home screen, pick Widgets, then First Flow.</p>

        <h2>The daily reminder</h2>
        <p>Off until you turn it on, from the done screen or in Settings, Daily reminder. One gentle note a day at the time you choose, and none on days you have already flowed. On Android 13 and newer, Android asks for notifications only after you say yes.</p>
      </div>
      {shot("widget.jpg", WIDGET_ALT, "The widget", "Begin from your home screen.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Settings</h2>
        <p>Settings is the last item in the bar: cards of rows, each saying what is set now. A row opens its own small page; Back takes you to the hub where you left it. Privacy, Help and About sit at the end.</p>
        <p><strong>New in 1.12:</strong> Settings is tidier. About and the widget have pages of their own, and Privacy, Help and About sit at the end.</p>
        <dl class="rows plate">
          <div><dt>Look</dt><dd>Follow the phone (Blush by day, Dusk at night), Blush (warm white paper with deep rose), Dusk (deep plum, nearly black, with rose), or Black (true black for OLED, with rose).</dd></div>
          <div><dt>Language</dt><dd>Pick the language of First Flow, or follow the phone. The page lists every language the app has words for, each named in itself. Pose names and cues follow your pick, and the voice guide stays in English.</dd></div>
          <div><dt>Breath pace</dt><dd>Steady, Slow or Calm. Every pace is under ten breaths a minute, the slow breathing the research studies.</dd></div>
          <div><dt>Get ready time</dt><dd>5, 7 or 10 seconds before each pose to find your shape.</dd></div>
          <div><dt>Sound</dt><dd>Singing bowls, a soft ring at each new step; the Voice guide, a warm voice that reads each pose and its cues; and under the flow Calm music, a Singing bowl bath, or Silence.</dd></div>
          <div><dt>Daily reminder</dt><dd>A gentle note each day, and its time.</dd></div>
          <div><dt>Widget</dt><dd>Opens its own page, where you add the widget to your home screen.</dd></div>
          <div><dt>Privacy</dt><dd>The promises as red ban chips, the two permissions and why, where your practice is kept, and the privacy policy in full.</dd></div>
          <div><dt>Help</dt><dd>This guide, the report page and the privacy policy.</dd></div>
          <div><dt>About</dt><dd>Opens its own page, last in the list: the version. Every pose, voice clip and track ships inside the app, so nothing is ever fetched or sent.</dd></div>
        </dl>
      </div>
      {shot("settings.jpg", SETTINGS_ALT, "Settings", "Look, practice, privacy and help.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Sound</h2>
        <p>Soft singing bowls mark each step, never each breath. The voice guide is a warm recorded voice, not the phone's robot voice, and it never says the same line twice in a row. Music ducks while the voice speaks. Every sound ships inside the app.</p>
      </div>
      {shot("sound.jpg", SOUND_ALT, "Sound", "Bowls, voice and what plays under.")}
    </div>

    <div class="doc">
      <h2>On Android TV and Google TV</h2>
      <p>First Flow runs on Android TV and Google TV too: start with one press, pause and move through the flow with the remote, and scan links with your phone.</p>
      <dl class="rows plate">
        <div><dt>The side rail</dt><dd>Home, Poses, Science and Settings sit in a rail on the left instead of the bar.</dd></div>
        <div><dt>Begin in focus</dt><dd>Home opens with Begin in focus, so OK starts the flow. A ring of light shows where you are.</dd></div>
        <div><dt>The flow on the remote</dt><dd>OK pauses, Back ends the flow. The remote's media keys work from anywhere in the flow: play and pause, next or fast forward for the next pose, previous or rewind for the one before.</dd></div>
        <div><dt>Open on your phone</dt><dd>A TV has no browser, so links in Settings (this guide, the report page, the privacy policy) end in a QR tag and open a QR code. Point your phone's camera at it to open the page there.</dd></div>
        <div><dt>Not on a TV</dt><dd>The daily reminder, the widget and More. Dusk is where a TV starts; Follow the phone reads Follow the TV.</dd></div>
      </dl>
    </div>
    <ul class="tvshots">
      {tv("tv-home.jpg", "First Flow Home on a TV with the side rail on the left, Warrior II as the pose of the day, Full flow and Steady chosen, 22 min and 20 poses, and Begin in focus.", "Home on a TV", "Begin is in focus.")}
      {tv("tv-flow.jpg", "The flow on a TV holding Mountain, pose 1 of 20: the figure on the left, the breath ring beside Breathe out, Up next, Tree, the pause key in focus and the hint OK pauses, Back ends the flow.", "The flow", "OK pauses, Back ends.")}
      {tv("tv-poses.jpg", "Poses on a TV: a list on the left with Warrior II in focus, and on the right its figure, Hold 5 breaths each side and Start the flow here.", "Poses", "A list beside a preview.")}
      {tv("tv-settings.jpg", "Settings on a TV in two columns: Look, Practice with breath pace, get ready time and sound, Privacy, and Help with a QR code and the report and privacy rows.", "Settings", "Links open as QR codes.")}
    </ul>

    <div class="with-shot">
      <div class="doc">
        <h2>Privacy</h2>
        <p>No ads, no tracking, no analytics, no crash reports, no account, no AI and no internet. First Flow does not even ask for internet access, so Android does not let it reach the network. It asks for two things, both for the reminder: notifications, only after you say yes to it, and running at start up, to set the reminder again after a restart or an update. Your look, pace, sounds and reminder time stay in the app's own storage on your phone. See the <a href="{SITE}/privacy">privacy policy</a>.</p>

        <h2>Accessibility</h2>
        <p>First Flow works with TalkBack and large text. Every figure has a spoken description, and the flow says each step aloud; the voice guide stays quiet while TalkBack runs, so you never hear two voices. Touch targets are at least 48 dp, words keep a 7 to 1 contrast, and with Android's animations off the breathing art keeps still.</p>

        <h2>Go easy</h2>
        <p>Yoga should never hurt. Stop if you feel pain, and ask your doctor first if you have a health condition, are pregnant, injured or recovering. First Flow is not a medical device and does not diagnose, treat, cure, or prevent any medical condition.</p>
      </div>
      {shot("privacy.jpg", PRIVACY_ALT, "Privacy", "Every promise and permission.")}
    </div>
""")

page("faq.html", "Questions", "Answers to common questions about First Flow, and what to try when something does not work.", f"""
    <div class="doc">
    <p class="lbl">Questions</p>
    <h1>Questions and fixes</h1>

    <h2>I hear no sound</h2>
    <p>First Flow plays through your media volume, so turn that up. Then check Settings, Sound: Singing bowls and the Voice guide are switches, and Silence under the flow leaves only the bowls and the voice. A call or another app playing sound pauses the flow, and so does pulling out headphones; press play to go on.</p>

    <h2>The voice is quiet</h2>
    <p>The voice guide may be off in Settings, Sound. It also stays quiet while TalkBack runs, so you never hear two voices; TalkBack still says each step.</p>

    <h2>The screen turns off</h2>
    <p>First Flow keeps the screen on while the flow runs. When you pause, the phone may turn the screen off as usual.</p>

    <h2>My reminder does not come</h2>
    <p>The reminder is off until you turn it on. If Android's notifications for First Flow are off, the switch stays off and Settings says so: turn them on in your phone settings. There is no reminder on days you have already flowed, and it may come a few minutes after the time you set. It is set again after a restart or an update.</p>

    <h2>Where is the reminder on my TV?</h2>
    <p>Not there, on purpose: a TV shows almost no notifications. The widget and More are not on a TV either.</p>

    <h2>How do I add the widget?</h2>
    <p>Settings, Widget, Add the widget, or the three dots at the top, then Add the widget. Or touch and hold your home screen, pick Widgets, then First Flow. Some home screens do not hold widgets.</p>

    <h2>Does it need the internet?</h2>
    <p>No. It works fully offline and cannot connect at all: every pose, voice clip and track ships inside the app.</p>

    <h2>Will my settings move to a new phone?</h2>
    <p>Only through Android's own backup, if you use it. Android may then copy your settings to your own Google account; we never see that copy.</p>

    <h2>The look does not change at night</h2>
    <p>Only Follow the phone switches between Blush by day and Dusk at night, as your phone does. Pick it in Settings, Look.</p>

    <h2>A pose feels too hard</h2>
    <p>Every pose has an easier option on its page. Go easy, listen to your body, and stop if anything hurts. If you have a health condition or are pregnant, ask your doctor before you start. You can also pick a slower pace or a longer get ready time in Settings.</p>

    <h2>Is it a medical app?</h2>
    <p>No. First Flow is not a medical device and does not diagnose, treat, cure, or prevent any medical condition.</p>

    <h2>On a TV, how do I open a link?</h2>
    <p>A TV has no browser, so a link opens a QR code. Point your phone's camera at it to open the page on your phone.</p>

    <h2>Refunds</h2>
    <p>First Flow is sold through Google Play, so refunds follow Google Play's refund policy.</p>
    </div>
""")

page("report.html", "Report a bug", "How to report a First Flow bug or ask for a feature on GitHub.", f"""
    <div class="doc" style="max-width:none">
    <p class="lbl">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p style="margin-top:16px">Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <div class="cards">
      <div class="card plate"><h2 class="h3">Bug report</h2><p>Something does not work, sounds wrong, or crashes.</p><a class="key filled" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></div>
      <div class="card plate"><h2 class="h3">Feature request</h2><p>A pose, a sound or something you would like First Flow to do.</p><a class="key tonal" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></div>
    </div>
    </div>
    <div class="doc">
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="faq.html">questions and fixes</a> page.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>

    <h2>What helps</h2>
    <dl class="rows plate">
      <div><dt>App version</dt><dd>Settings, About, or Android settings, Apps, First Flow.</dd></div>
      <div><dt>Device and Android version</dt><dd>Android settings, About phone (on a TV, Settings, System, About).</dd></div>
      <div><dt>Which screen</dt><dd>Home, the flow, the done screen, Poses, a pose by name, Science, Settings, the widget, the reminder, or the TV rail and remote.</dd></div>
      <div><dt>Steps</dt><dd>What you did, one step per line, so we can do the same.</dd></div>
      <div><dt>Expected and actual</dt><dd>What you thought would happen, and what happened.</dd></div>
      <div><dt>A picture or a recording</dt><dd>A screenshot or a short screen recording. Drag it into the form.</dd></div>
    </dl>
    <p style="margin-top:16px">Issues on GitHub are public. Before you attach a screenshot, crop or cover anything private.</p>

    <h2>Other ways</h2>
    <p>Prefer not to use GitHub? Write to <span class="mail">{MAIL}</span> (<a href="mailto:{MAIL}">write an email</a>).</p>
    </div>
""")
