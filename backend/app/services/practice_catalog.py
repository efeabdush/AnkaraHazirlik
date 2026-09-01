from __future__ import annotations

"""Deterministic, original B1+ practice packs used to extend the starter library.

The short metadata lists keep the repository reviewable.  The builders turn each
entry into a complete validated pack with its own text, questions and rationales.
"""

from typing import Any


def _question(stem: str, options: list[str], answer: str, rationale: str, *, points: int = 1, qtype: str = "detail") -> dict[str, Any]:
    return {
        "stem": stem,
        "options": dict(zip(("A", "B", "C", "D"), options, strict=True)),
        "answer": answer,
        "points": points,
        "qtype": qtype,
        "rationale": rationale,
    }


def _choice_question(
    stem: str,
    correct: str,
    distractors: list[str],
    rationale: str,
    *,
    rotation: int = 0,
    points: int = 1,
    qtype: str = "detail",
) -> dict[str, Any]:
    """Place the correct option at a changing position so packs do not share an answer pattern."""
    choices = [correct, *distractors]
    shift = rotation % len(choices)
    choices = choices[shift:] + choices[:shift]
    answer = ("A", "B", "C", "D")[choices.index(correct)]
    return _question(stem, choices, answer, rationale, points=points, qtype=qtype)


CONVERSATION_SPECS = [
    ("Changing a Laboratory Session", "course scheduling", "science office", "move a laboratory session", "the new time conflicts with a language class", "changes require the instructor's approval", "join Friday's group after the instructor signs the form", "email the signed form before Wednesday noon"),
    ("Collecting a Student Travel Card", "student transport", "transport desk", "collect a discounted travel card", "the online record shows an old address", "the address must match a recent document", "show a digital bank statement and update the record", "return before the desk closes at four"),
    ("Borrowing a Camera", "media equipment", "media centre", "borrow a camera for a class project", "all standard cameras are booked", "advanced cameras require a short safety workshop", "attend the workshop and reserve a returned camera", "confirm the reservation by six this evening"),
    ("Joining a Conversation Club", "language practice", "language centre", "join an English conversation club", "the beginner group is already full", "students may try a higher group before registering", "visit Tuesday's intermediate session as a guest", "tell the coordinator after the trial session"),
    ("Replacing a Lost Library Card", "library services", "library help desk", "replace a lost library card", "the student needs books for tomorrow", "a replacement card takes two working days", "use a temporary digital pass meanwhile", "upload a photograph before leaving the desk"),
    ("Booking a Music Practice Room", "campus facilities", "arts building office", "book a piano room", "the requested room is reserved for an exam", "practice bookings are limited to ninety minutes", "choose the smaller room from three to four thirty", "check in with a student card ten minutes early"),
    ("Correcting a Course Registration", "course registration", "registrar's office", "add a missing elective", "the system says the class is closed", "late additions need both departments to agree", "ask the receiving department to release one reserved place", "bring the approval message by Friday"),
    ("Finding a Volunteer Placement", "community volunteering", "volunteer office", "find a weekend volunteer role", "the animal shelter needs weekday helpers", "new volunteers must attend an introduction", "choose the Saturday food-bank team instead", "complete the health form online tonight"),
    ("Returning a Damaged Book", "library responsibility", "circulation desk", "return a book with water damage", "the book became wet during a bus journey", "staff must assess damage before charging a fee", "leave the book for inspection and borrow a digital copy", "check the decision in the library account tomorrow"),
    ("Applying for a Campus Job", "student employment", "career desk", "apply for a campus café job", "the student has no formal work reference", "one academic reference is accepted for first jobs", "ask a tutor and submit a short skills statement", "send both items before Monday morning"),
    ("Changing a Meal Plan", "campus dining", "dining office", "switch to a smaller meal plan", "the normal change period has ended", "medical or financial reasons can be reviewed late", "submit a budget explanation for a special review", "keep the current card until a decision arrives"),
    ("Reporting a Noisy Residence Room", "student housing", "residence reception", "report repeated night-time noise", "the student does not want a conflict with neighbours", "staff first record incidents before arranging mediation", "use the quiet-hours form for three nights", "meet the residence adviser on Friday"),
    ("Printing a Large Poster", "academic presentation", "print centre", "print a research poster", "the uploaded file has the wrong dimensions", "large posters must use the official template size", "resize the file at the design computer", "submit the corrected PDF before five"),
    ("Rescheduling an Adviser Meeting", "academic advising", "department office", "move an adviser appointment", "the student has a compulsory seminar", "same-day changes cannot be made online", "take a cancellation slot on Thursday morning", "reply to the office message within one hour"),
    ("Using the Bicycle Repair Station", "sustainable transport", "campus security desk", "use the bicycle repair station", "the tyre pump is locked after dark", "equipment keys are borrowed with identification", "leave a student card and collect the key", "return the key before the night shift changes"),
    ("Joining a Research Survey", "research participation", "psychology office", "join a paid research survey", "the student's timetable misses the listed sessions", "participants must complete both parts in one week", "take an early online part and a Saturday interview", "book both parts through the same account"),
    ("Requesting Exam Arrangements", "assessment support", "student support office", "request a quieter exam room", "the supporting letter has not arrived", "temporary arrangements can cover one assessment", "ask for temporary approval while the letter is processed", "submit the online request forty-eight hours early"),
    ("Collecting a Club Event Key", "student clubs", "activities office", "collect a hall key for a club event", "the named organiser is ill", "only a registered committee member may sign", "update the responsible person's name in the club portal", "bring identification before the office closes"),
    ("Extending a Laptop Loan", "technology loans", "IT help desk", "extend a laptop loan", "another student has reserved the device", "renewals are possible only without a waiting list", "return this laptop and borrow a short-term model", "back up personal files before returning it"),
    ("Getting Feedback on a CV", "career preparation", "career centre", "get feedback on a CV", "all individual appointments are full", "the weekly clinic accepts six walk-in students", "arrive early at Wednesday's clinic", "bring a printed copy and one job advertisement"),
    ("Moving a Sports Class", "sports membership", "sports centre", "change a swimming lesson", "the evening group has reached its limit", "members may exchange places through a waiting list", "join the list and attend Monday's open practice", "answer the text message within thirty minutes"),
    ("Sending a Parcel from Campus", "campus post", "mail room", "send a project model to another city", "the box is larger than the standard shelf", "oversized parcels need a printed label and collection booking", "buy a stronger box and schedule a courier collection", "leave the labelled parcel before two"),
]


def _conversation_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    title, topic, place, goal, problem, rule, solution, next_step = spec
    styles = (
        [
            ("student", f"Hi. I am trying to {goal}, and the website sent me to the {place}. Could I check what I need to do?"),
            ("staff", f"Certainly. Before we look at the form, tell me what stopped you while you were trying to {goal}."),
            ("student", f"The problem is that {problem}. The online page lists several choices, but none seems to match my situation."),
            ("staff", f"In this case the key condition is that {rule}. That is why the normal online route did not work."),
            ("student", f"That makes sense. I still need to finish this soon, so is there an alternative that follows the {place}'s rules?"),
            ("staff", f"Yes. The quickest valid option is to {solution}. It keeps your earlier work on the system."),
            ("student", f"After that, should I {next_step}, or will the system contact me automatically?"),
            ("staff", f"You should {next_step}. Save the confirmation in case the update is delayed."),
        ],
        [
            ("staff", f"Good afternoon, {place}. How can I help?"),
            ("student", f"I hoped to {goal}, but I discovered that {problem}. I am worried I have left it too late."),
            ("staff", f"Let me check. Our normal policy says that {rule}, although there is a route for cases like yours."),
            ("student", f"I read that rule, but I could not tell whether it meant I had to cancel my plan to {goal}."),
            ("staff", f"No cancellation is necessary. You can {solution}; that gives the {place} enough evidence to continue."),
            ("student", f"Great. What happens to my request to {goal} once I have done that?"),
            ("staff", f"Then {next_step}. Please do not create a second request while the first one is being checked."),
            ("student", f"Understood. I will {solution} today and keep the reference number until the process is complete."),
        ],
        [
            ("student", f"Excuse me, I have a question about how to {goal}. Someone at reception said the {place} handles it."),
            ("staff", f"That is right. Are you starting a new request to {goal}, or has something gone wrong with an existing one?"),
            ("student", f"It is an existing request. {problem.capitalize()}, and I do not want to submit incorrect information."),
            ("staff", f"You were right to pause. We have to make sure that {rule}; otherwise the request may be rejected later."),
            ("student", f"What can I do without losing the time I have already spent trying to {goal}?"),
            ("staff", f"You can {solution}. We will attach that step to the same request rather than opening a new file."),
            ("student", f"Will that be enough for me to {goal}?"),
            ("staff", f"Yes, provided that you also {next_step}. Check the final message for the exact time and location."),
        ],
        [
            ("student", f"Hello. I have come to the {place} because I need to {goal} before the end of the week."),
            ("staff", f"All right. Show me the message you received and the {place} can work out why the request stopped."),
            ("student", f"Here it is. It seems to say that {problem}, but it does not give me another button to press."),
            ("staff", f"The button disappears because {rule}. The message should explain that more clearly."),
            ("student", f"Is there still a way to {goal} this week?"),
            ("staff", f"There should be. First, {solution}. That lets us review the exception without changing the deadline."),
            ("student", f"And what should I do about {goal} while the review is taking place?"),
            ("staff", f"Please {next_step}. If you hear nothing by the stated time, contact the {place} with this reference code."),
        ],
        [
            ("staff", f"Welcome to the {place}. What are you hoping to arrange today?"),
            ("student", f"I want to {goal}. I prepared everything listed online, but {problem}."),
            ("staff", f"That detail changes the procedure. The rule is that {rule}, so I cannot approve the original route at this desk."),
            ("student", f"I see. Could you suggest a practical option for {goal} rather than making me start from the beginning?"),
            ("staff", f"The best option is to {solution}. It was designed for exactly this kind of delay or mismatch."),
            ("student", f"Do I need to bring anything else to the {place} afterwards?"),
            ("staff", f"For now, just {next_step}. The confirmation will say if an original document is needed later."),
            ("student", f"Thanks. I will follow that order for {goal} and check the confirmation before I leave campus."),
        ],
        [
            ("student", f"Could I get some advice? I need to {goal}, but {problem}, and two web pages seem to give different instructions."),
            ("staff", f"Use the guidance from the {place}. The deciding rule is that {rule}; the other page only describes ordinary cases."),
            ("student", f"So which part of the process for {goal} should I complete first? I do not want the deadline to pass while I wait."),
            ("staff", f"Start by trying to {solution}. That creates a dated record of the problem."),
            ("student", f"Once the record appears, can I continue with my plan to {goal}?"),
            ("staff", f"Yes. Your next action is to {next_step}. There is no need to repeat the first form."),
            ("student", f"That is much clearer. I will save both the record and the final reply from the {place}."),
            ("staff", f"Good idea. If the details about {goal} change, use the same reference number so the {place} can see the full history."),
        ],
    )
    script = [{"speaker": speaker, "text": text} for speaker, text in styles[(index - 1) % len(styles)]]
    script.extend([
        {"speaker": "student", "text": f"Before I leave, could you confirm that following these steps will keep my request to {goal} active? I may need to explain the process to my course tutor."},
        {"speaker": "staff", "text": f"It will remain active. Keep the message from the {place}, follow the stated deadline, and quote the same reference number if you need further help."},
    ])
    return {
        "id": f"catalog-conversation-{index:02d}", "kind": "conversation", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "defer_audio": True, "script": script,
        "questions": [
            _choice_question(f"Why does the student contact the {place}?", f"To {goal}", ["To complain about a staff member", "To collect an unrelated certificate", "To ask for a campus map"], f"The student says that they need to {goal}.", rotation=index, qtype="purpose"),
            _choice_question(f"Which difficulty affects the plan to {goal}?", problem.capitalize(), ["The office has moved", "The student forgot every password", "A payment was made twice"], f"The student explains that {problem}.", rotation=index + 1, qtype="detail"),
            _choice_question(f"How does the {place} suggest continuing the request?", solution.capitalize(), ["Wait until the next semester", "Ask another student to complete it", "Cancel the request completely"], f"The staff member recommends that the student {solution}.", rotation=index + 2, qtype="process"),
            _choice_question(f"Which follow-up step completes the plan to {goal}?", next_step.capitalize(), ["Send the same request several times", "Ignore all confirmation messages", "Pay an unmentioned extra charge"], f"The required follow-up is to {next_step}.", rotation=index + 3, qtype="inference"),
        ],
    }


LECTURE_SPECS = [
    ("How Urban Trees Cool Neighbourhoods", "urban environment", "urban trees", "shade reduces the heat stored by roads", "leaves release water into the air", "connected green routes support wildlife", "a school street with young trees", "trees need water and long-term care", "map the hottest walking routes first"),
    ("Why Habits Depend on Cues", "behaviour and learning", "daily habits", "a cue starts an automatic routine", "a small reward helps the routine continue", "changing the environment is easier than relying on willpower", "placing a book on a pillow before bedtime", "strong routines take time to replace", "change one cue and measure the result"),
    ("The Hidden Work of Soil", "environmental science", "healthy soil", "tiny organisms break down old material", "soil spaces store water and air", "plant roots protect the surface from erosion", "a campus garden after heavy rain", "damaged soil recovers slowly", "avoid covering every open area with concrete"),
    ("How Maps Shape Decisions", "visual information", "maps", "designers choose which details to include", "colour can make one pattern appear stronger", "scale changes the questions a map can answer", "a bus map that simplifies real streets", "every map leaves some information out", "check the map's purpose before trusting it"),
    ("Why People Remember Stories", "communication", "stories and memory", "events create a meaningful sequence", "characters give facts an emotional connection", "concrete scenes help listeners rebuild information", "a safety lesson told through one worker's day", "a dramatic story can hide weak evidence", "combine a clear story with accurate data"),
    ("The Science of Everyday Fermentation", "food science", "fermentation", "microorganisms change sugars into new substances", "acid can protect food from harmful microbes", "temperature affects speed and flavour", "yoghurt thickening in a warm container", "poor hygiene can make a batch unsafe", "control temperature and use clean tools"),
    ("How Public Benches Change a Street", "public space", "public seating", "seats allow older people to rest", "their position influences social contact", "visible activity can make a place feel safer", "benches near a busy neighbourhood market", "bad placement may block paths", "observe how different users move first"),
    ("Why Background Noise Affects Study", "attention", "background noise", "unpredictable speech takes attention from reading", "steady sounds are easier for the brain to ignore", "task type changes how much noise matters", "students comparing a café and a quiet room", "complete silence is uncomfortable for some people", "match the sound environment to the task"),
    ("The Journey of Recycled Glass", "materials", "glass recycling", "colour sorting protects material quality", "crushed glass melts at a lower temperature", "closed-loop recycling can happen many times", "bottles collected from a campus café", "mixed ceramics can damage equipment", "sort carefully before transport"),
    ("How Bees Navigate", "animal behaviour", "bee navigation", "the sun provides a changing compass", "landmarks guide the final part of a journey", "movement inside the hive shares location information", "bees finding flowers behind a building", "weather can hide important signals", "protect varied feeding areas close together"),
    ("Why Small Museums Use Objects", "history education", "museum objects", "physical details make the past concrete", "personal objects connect large events to ordinary lives", "careful labels guide observation", "a worn suitcase in a migration display", "an object cannot explain its full history alone", "compare the object with several records"),
    ("What Makes a Queue Feel Fair", "social behaviour", "queues", "clear order reduces uncertainty", "visible progress makes waiting easier", "explanations improve acceptance of delays", "students waiting at a registration desk", "priority needs can require a different order", "show both the rule and expected waiting time"),
    ("How Wetlands Reduce Flood Risk", "ecology", "wetlands", "plants slow moving water", "soft ground stores water temporarily", "wetlands filter some pollutants", "a river park during spring rain", "very large floods can exceed their capacity", "protect natural flood areas before building barriers"),
    ("Why We Misjudge Food Portions", "health behaviour", "food portions", "large plates change visual comparison", "packages suggest a normal serving size", "distraction reduces awareness of eating", "snacks shared during a film", "individual energy needs are different", "serve a first portion before sitting down"),
    ("The Value of Dark Skies", "environment and astronomy", "dark skies", "artificial light hides faint stars", "night lighting changes animal behaviour", "careful lamp design saves energy", "a town replacing upward-facing street lamps", "some lighting is necessary for safety", "direct warm light only where it is needed"),
    ("How Translation Changes with Context", "language", "translation", "one word can carry several meanings", "social relationships influence polite choices", "the purpose of a text shapes the best version", "translating a warning and a friendly invitation", "literal accuracy can produce an unnatural message", "read the whole situation before choosing words"),
    ("Why Local Markets Matter", "local economy", "local markets", "small producers meet customers directly", "seasonal goods travel shorter distances", "markets create regular social contact", "a weekly square used by farmers and residents", "prices and supply may change quickly", "support reliable transport and simple stall rules"),
    ("How Sleepy Drivers Misread Risk", "road safety", "driver fatigue", "slow reactions delay braking", "tired people may not notice their own decline", "short microsleeps remove awareness completely", "a late journey after a long workday", "coffee offers only temporary help", "stop in a safe place and rest"),
    ("Why Handwriting Can Support Learning", "study skills", "handwriting", "slower writing encourages selection", "personal layouts can show relationships", "physical movement adds another memory cue", "a student summarising a complex diagram", "typing is better for some access needs", "choose the method that matches the learning goal"),
    ("The Design of Emergency Messages", "risk communication", "emergency messages", "the first line must state the action", "short sentences reduce reading effort", "specific locations prevent unnecessary panic", "a flood warning sent to one district", "too many alerts can reduce attention", "test messages with real users"),
    ("How Shared Tools Build Communities", "community resources", "tool libraries", "borrowing reduces the cost of rare tasks", "instruction sessions improve safety", "members exchange practical knowledge", "neighbours borrowing a carpet cleaner", "maintenance requires time and money", "track condition and train volunteers"),
    ("Why Some Buildings Are Reused", "architecture", "building reuse", "existing structures save construction material", "old layouts can support new creative uses", "familiar buildings preserve local memory", "a factory becoming a public library", "repairs may reveal hidden costs", "compare long-term value rather than first price"),
    ("How Colour Influences Wayfinding", "design", "wayfinding colours", "consistent colour marks related routes", "contrast helps signs remain readable", "too many colours create confusion", "hospital visitors following a blue line", "colour meanings differ across settings", "combine colour with words and symbols"),
    ("Why Citizen Science Needs Care", "research methods", "citizen science", "many volunteers can collect wide-area data", "simple instructions improve consistency", "local observers notice unusual changes", "residents recording birds in city parks", "uncontrolled methods can create unreliable results", "train participants and check a sample"),
]


def _lecture_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    title, topic, subject, first, second, third, example, limitation, action = spec
    openings = (
        f"Good morning. Today we are examining {subject}, beginning with an everyday observation and then building a three-part explanation.",
        f"Imagine that a classmate asks why {subject} deserves serious study. Today's lecture offers an answer through causes, evidence, and limits.",
        f"Our subject today is {subject}. Rather than treating it as an isolated fact, we will trace how several parts of the process influence one another.",
        f"Today's question is simple to ask but harder to answer: what makes {subject} work as it does? We will test three connected claims.",
        f"Let us begin with {subject}. You may already know the visible result, but the less visible process is more useful for academic listening.",
        f"This lecture uses {subject} as a case study. Listen for a first cause, a supporting process, a wider effect, and one reason for caution.",
    )
    lines = [
        openings[(index - 1) % len(openings)] + f" The aim is not to memorise a list. It is to follow the argument about {subject} and decide which details support its central claim most clearly.",
        f"The first claim is that {first}. In discussions of {subject}, people often jump directly to the outcome and overlook this starting mechanism. Separating the mechanism from the outcome lets us ask better questions: when does it operate, who notices it first, and what evidence would show that it has changed?",
        f"A second process is equally important: {second}. It does not replace the first claim about {first}; the two can strengthen or weaken one another. For {subject}, location, timing, available resources, and human behaviour may alter the balance. That is why a careful explanation states its conditions instead of promising an identical result everywhere.",
        f"The third claim widens the frame: {third}. This moves our attention beyond a single person or moment. Researchers studying {subject} therefore compare patterns over time. One photograph or one interview may capture a useful detail, but repeated observation is needed to distinguish a stable pattern from an unusual day.",
        f"A practical illustration is {example}. The people involved first measured only the most visible outcome. Later, they recorded when problems appeared, which users returned, and what changed after each adjustment. They then saw that {first}, {second}, and {third} were connected rather than separate explanations.",
        f"The case of {example} also shows why evidence must be interpreted carefully. A positive result can suggest that an approach deserves another trial, but it cannot prove that every setting will behave like this one. We still need to know who participated, how long observation continued, and which alternative explanations were considered.",
        f"There is an important limit to the argument: {limitation}. In the context of {subject}, this is not a reason to abandon the whole idea. A stated limit shows where extra support, different timing, or another method may be necessary. Honest limits make a recommendation more useful because they prevent a local success from becoming an unrealistic promise.",
        f"One reasonable response is to {action}. A small trial should begin with a written expectation and a simple measure. Afterwards, compare what actually happened with that expectation. If the result is different, the gap may reveal a missing factor in our explanation of {subject}, not merely a failed project.",
        f"Notice the structure of today's argument about {subject}: a mechanism, a second process, a wider effect, an example, and a qualification. Academic listening questions often follow the same structure. A main-idea question asks for the entire pattern, whereas a detail or inference question asks how one part supports or limits that pattern.",
        f"To conclude, {subject} becomes clearer when we connect three claims: {first}; {second}; and {third}. The example of {example} demonstrates how those claims can guide a decision, while {limitation} keeps the conclusion realistic. The next step is to {action}. Try summarising this lecture in three sentences: one cause, one example, and one caution. Then compare your summary with the evidence in your notes. If a claim has no supporting detail, return to that section and listen for the condition or limitation you may have missed. This final check separates a convincing explanation from a list of facts that merely sound relevant.",
    ]
    script = [{"speaker": "lecturer", "text": line} for line in lines]
    return {
        "id": f"catalog-lecture-{index:02d}", "kind": "lecture", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "defer_audio": True,
        "note_scaffold": [f"Subject: {subject}", f"Idea 1: {first}", f"Idea 2: {second}", f"Idea 3: {third}", f"Example: {example}", f"Limit: {limitation}", f"Action: {action}"],
        "script": script,
        "questions": [
            _choice_question(f"Which option best summarises the lecture about {subject}?", f"It connects three processes, an example, and a limit concerning {subject}", [f"It gives a complete history of {subject}", "It argues that personal stories are stronger than evidence", "It teaches a technical list that must be memorised"], f"The lecture organises {subject} around connected claims, evidence, and a limitation.", rotation=index, points=2, qtype="main_idea"),
            _choice_question(f"Which claim does the lecturer make about {subject}?", first.capitalize(), ["One visible feature explains every result", "A single observation proves a permanent pattern", "Local conditions never affect the outcome"], f"The first stated claim is that {first}.", rotation=index + 1, points=2, qtype="true"),
            _choice_question(f"Which statement contradicts the lecturer's argument about {subject}?", "One successful example creates a universal rule", ["Several processes may operate together", "Repeated observation can reveal stable patterns", "Limits can show where another method is needed"], "The lecturer explicitly warns that a local success is not a universal rule.", rotation=index + 2, points=2, qtype="not_true"),
            _choice_question(f"What purpose does the example of {example} serve?", "To show how the three claims can guide a real decision", ["To prove that measurements are unnecessary", "To replace the main explanation with a personal story", "To introduce a topic unrelated to the lecture"], f"The example of {example} shows the claims working together.", rotation=index + 3, points=2, qtype="cause"),
        ],
    }


READING_SPECS = [
    ("Why Community Fridges Need More Than Food", "food sharing", "community fridges", "they make surplus food available locally", "clear labels protect safety", "regular volunteers build trust", "a neighbourhood fridge beside a library", "unpredictable donations make planning difficult", "publish simple rules and a daily check"),
    ("The Return of Small Urban Streams", "urban ecology", "restored city streams", "open water creates cooler public space", "plants slow rainwater", "local wildlife returns gradually", "a concrete channel changed into a park", "maintenance continues after construction", "monitor water quality with residents"),
    ("What Students Gain from Peer Teaching", "learning", "peer teaching", "explaining reveals gaps in understanding", "questions force flexible examples", "shared responsibility increases attention", "two students preparing for a biology quiz", "confident speakers can dominate", "rotate roles and use a time limit"),
    ("Why Old Photographs Need Context", "history", "historical photographs", "images preserve visual detail", "the photographer chooses a viewpoint", "captions influence interpretation", "a crowded station shown during a migration period", "events outside the frame remain invisible", "compare the image with written records"),
    ("How Refill Shops Change Buying Habits", "sustainable shopping", "refill shops", "customers reuse containers", "buying exact amounts can reduce waste", "visible quantities encourage planning", "a student buying only one week's rice", "some products cost more at first", "compare price per unit and actual use"),
    ("The Quiet Value of Campus Gardens", "campus life", "campus gardens", "green areas offer short mental breaks", "shared work connects different groups", "planting demonstrates seasonal change", "a small garden behind a residence hall", "volunteers may disappear during holidays", "design a simple summer care plan"),
    ("Why Repair Instructions Often Fail", "communication", "repair instructions", "writers assume hidden knowledge", "unclear pictures hide orientation", "missing safety steps create risk", "a guide for replacing a bicycle brake pad", "too much detail can overwhelm beginners", "test each step with a first-time user"),
    ("How Libraries Lend More Than Books", "public services", "libraries of things", "shared items lower occasional costs", "borrowing reduces storage needs", "workshops teach safe use", "a library lending drills and sewing machines", "damaged equipment requires a budget", "charge no fee but record condition carefully"),
    ("Why Rain Gardens Appear Beside Roads", "water management", "rain gardens", "shallow planted areas collect runoff", "soil filters some pollution", "slow release protects drains", "a garden beside a supermarket car park", "blocked soil reduces performance", "inspect the inlet after heavy storms"),
    ("The Challenge of Clear Food Labels", "consumer information", "food labels", "short names are easy to notice", "serving sizes affect comparisons", "front labels simplify complex nutrition", "two cereals using different portion sizes", "simple scores may hide useful detail", "read both the front and full table"),
    ("What Makes a Study Group Last", "study habits", "study groups", "a shared goal keeps meetings focused", "prepared members create useful discussion", "regular times reduce planning effort", "four classmates reviewing one unit weekly", "social conversation can replace study", "finish each meeting with assigned tasks"),
    ("Why Some Streets Become School Streets", "transport", "school streets", "temporary closures reduce traffic danger", "walking becomes more attractive", "quieter entrances improve social contact", "cars restricted for thirty minutes", "families with access needs require exceptions", "plan alternative drop-off points"),
    ("How Podcasts Create a Sense of Company", "media", "spoken podcasts", "a regular voice becomes familiar", "informal language feels direct", "listeners choose private moments to listen", "a commuter following one weekly programme", "familiarity can be mistaken for friendship", "keep a critical view of claims"),
    ("Why Clothes Are Hard to Recycle", "materials", "textile recycling", "mixed fibres are difficult to separate", "buttons and zips require extra work", "fabric quality falls after repeated processing", "a shirt made from cotton and plastic", "collection alone does not create a market", "design garments with fewer mixtures"),
    ("The Role of Shade in Public Parks", "urban design", "park shade", "shade extends comfortable visiting hours", "different trees cool spaces unevenly", "covered seats help sensitive visitors", "a playground empty at midday", "dense shade may prevent grass growth", "map sun movement before planting"),
    ("Why Names Matter in Digital Files", "digital skills", "file naming", "consistent names improve searching", "dates support correct ordering", "version labels prevent accidental replacement", "a group writing several report drafts", "very long names become difficult to scan", "agree on one short pattern first"),
    ("How Local News Builds Knowledge", "media literacy", "local news", "small reports explain nearby decisions", "regular coverage creates public memory", "local sources notice practical effects", "changes to one bus line", "limited staff cannot cover every issue", "support several independent sources"),
    ("Why Reusable Cups Need a System", "waste reduction", "reusable cup schemes", "return points make reuse convenient", "deposits encourage cups to come back", "shared washing ensures hygiene", "a cup borrowed at one café and returned at another", "missing cups raise replacement costs", "use one design across many shops"),
    ("The Benefits and Limits of Standing Desks", "work habits", "standing desks", "changing position reduces long sitting", "easy adjustment supports different tasks", "short standing periods can increase alertness", "a student alternating during revision", "standing all day creates other discomfort", "change position rather than choose one forever"),
    ("How Seed Libraries Share Local Knowledge", "gardening", "seed libraries", "gardeners exchange adapted seeds", "labels preserve planting experience", "returning seeds keeps the collection active", "beans grown successfully in a windy area", "cross-pollination can change varieties", "teach simple saving methods"),
    ("Why Waiting Information Reduces Stress", "service design", "waiting information", "estimated times reduce uncertainty", "visible order increases fairness", "updates let people make small choices", "patients receiving a delay message", "incorrect estimates damage trust", "update the estimate when conditions change"),
    ("How Night Trains Compete with Flights", "travel", "night trains", "sleeping uses travel time efficiently", "city-centre stations reduce transfers", "rail can produce lower emissions", "a student arriving before a morning meeting", "tickets and routes remain limited", "coordinate services across borders"),
    ("Why Public Art Invites Debate", "culture", "public art", "art changes familiar surroundings", "open locations reach accidental audiences", "different interpretations create discussion", "a sculpture placed in a market square", "communities may disagree about cost", "explain selection without controlling interpretation"),
]


def _reading_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    title, topic, subject, first, second, third, example, limitation, action = spec
    leads = (
        f"Across many towns, {subject} have grown from small experiments into services people meet in ordinary life.",
        f"It is easy to describe {subject} as a single clever idea, but their long-term value depends on a connected system.",
        f"Public interest in {subject} often begins with one visible benefit, while the less visible work determines whether that interest lasts.",
        f"When {subject} first appear, attention usually goes to novelty; later, users begin to judge reliability, clarity, and social value.",
        f"A useful way to understand {subject} is to look beyond their immediate function and examine what helps people trust them.",
    )
    paragraphs = [
        leads[(index - 1) % len(leads)] + f" The first benefit is that {first}. This outcome attracts support for {subject}, yet it tells us only what users see at the beginning of the process.",
        f"A second effect is that {second}. For {subject}, availability alone does not guarantee confident use. People also need understandable rules and a predictable experience. When the design explains what is expected, users make fewer avoidable mistakes and are more likely to return. Reliability can eventually matter more than an impressive public launch.",
        f"The subject has a social or educational dimension as well: {third}. People using {subject} observe one another, exchange practical information, and gradually form shared expectations. These informal lessons are difficult to count, but interviews can reveal how they influence behaviour long after a first visit.",
        f"The case of {example} makes these connections concrete. Organisers initially counted only total users. Later they recorded repeat visits, common questions, and the moments when difficulties appeared. That evidence led them to adjust signs, responsibilities, and explanations before expanding. The experience improved because {subject} became easier to understand, not simply because the project became larger.",
        f"A serious qualification is that {limitation}. If this limit is hidden, early enthusiasm for {subject} may turn into disappointment. A realistic response is to {action}. This treats improvement as an evidence cycle: identify a need, test a limited response, observe what changes, and revise the design before making a larger promise.",
        f"The broader lesson from {subject} is not that every community should copy one model. Cost, space, participation, and timing differ. Durable projects connect physical design, clear information, and human relationships while stating their limits honestly. People can then understand the service, maintain it, and adapt it without losing the original purpose. This slower form of development may attract less attention than a rapid launch, but it produces information that later decisions can use. It also gives organisers time to notice who is excluded, which explanation remains unclear, and whether the original goal still matches the needs of the people using {subject}. Those questions keep improvement connected to evidence rather than publicity.",
    ]
    return {
        "id": f"catalog-reading-standard-{index:02d}", "kind": "reading_standard", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True,
        "instructions": "Read the passage and choose the best answer according to the text.", "content": {"paragraphs": paragraphs},
        "questions": [
            _choice_question(f"What is the writer's main purpose in discussing {subject}?", f"To explain connected benefits and limits of {subject}", [f"To demand that {subject} be identical everywhere", "To describe a conflict between two cities", "To give technical instructions only for researchers"], f"The passage explains how {subject} work, including benefits and a limitation.", rotation=index),
            _choice_question(f"According to paragraph 2, what encourages people to use {subject} again?", "Clear design and a reliable experience", ["An expensive launch event", "Removing every rule", "Counting only first-time users"], "The paragraph connects clarity and reliability with repeated use.", rotation=index + 1),
            _choice_question(f"Why did the organisers revise their plan in the example of {example}?", "They collected information beyond total user numbers", ["They wanted the project to look larger", "Volunteers refused to speak to users", "The first location closed immediately"], "Repeat visits, questions, and problem times showed what needed improvement.", rotation=index + 2),
            _choice_question("The phrase 'a social or educational dimension' is closest in meaning to _____.", "an additional aspect involving people and learning", ["a physical cover around the service", "an official financial limit", "the final measurable result"], "Dimension refers to another aspect of the subject.", rotation=index + 3),
            _choice_question(f"What can be inferred about expanding {subject}?", "Expansion should follow evidence and realistic planning", ["Every successful project should expand immediately", "Growth matters more than clear information", "Small projects cannot create social effects"], "The writer recommends testing and improvement before larger promises.", rotation=index + 4, qtype="inference"),
            _choice_question(f"Which statement best matches the writer's view of {subject}?", "Strong systems combine design, information, and relationships", ["One model works in every local setting", "Limitations should be hidden from users", "Informal learning has no lasting value"], "The conclusion connects physical design, information, and human relationships.", rotation=index + 5),
        ],
    }


INSERTION_TOPICS = [
    ("Community Tool Sheds", "shared tools", "Residents borrow tools that they only need occasionally", "Volunteers inspect each item before and after a loan", "Short workshops teach safe use", "The records also show which tools the neighbourhood needs most", "A tool may be unavailable when a borrower needs it"),
    ("Pocket Parks", "small urban parks", "Unused corners are changed into small green spaces", "Local residents often help choose the design", "Simple seating creates a place for short visits", "Even a tiny park can connect two walking routes", "Large sports fields can fit into every pocket park"),
    ("Book Exchange Shelves", "public book sharing", "Open shelves let people take and leave books freely", "A local helper removes damaged material", "Children's books are placed where young readers can reach them", "The changing collection reflects neighbourhood interests", "Every donated book must remain forever"),
    ("Campus Clothes Swaps", "clothing reuse", "Students bring clean clothes they no longer wear", "Items are organised by type rather than price", "Unclaimed clothes go to a local charity", "The event makes second-hand choices feel social", "Only new designer clothing is accepted"),
    ("Quiet Hours in Shared Homes", "shared housing", "Housemates agree on periods with less noise", "The agreement works best when needs are discussed first", "Visible reminders prevent repeated arguments", "Guests should also be told about the rule", "A single person should choose every quiet hour"),
    ("Water Refill Maps", "public water access", "Digital maps show where bottles can be filled", "Users report broken or missing fountains", "Regular updates make the map trustworthy", "Businesses may add their taps to the network", "Old information always improves a map"),
    ("Neighbourhood Walking Groups", "community exercise", "People meet for regular walks at an easy pace", "Rotating routes keep the activity interesting", "A named leader checks that nobody is left behind", "Conversation is often as important as exercise", "Members are tested on speed every week"),
    ("Library Seed Corners", "seed sharing", "Gardeners take small packets of local seeds", "Labels record when and where plants grew well", "Members return seeds after a successful season", "Workshops explain how to keep varieties healthy", "All seeds grow equally well in every climate"),
    ("Repairable School Furniture", "product design", "Desks are built with replaceable parts", "Standard screws make repairs easier", "Students learn why maintenance matters", "A damaged surface no longer requires a whole new desk", "Repairable furniture must be thrown away sooner"),
    ("Digital Noticeboards", "campus information", "One screen collects changing campus announcements", "Messages expire automatically after their event", "Clear categories help viewers scan quickly", "Urgent notices can appear without covering everything else", "Every message should use a different design"),
    ("Rainwater Barrels", "water saving", "Roof water is stored for garden use", "A covered barrel prevents insects and dirt", "An overflow pipe directs extra water safely", "The stored supply reduces demand during dry weeks", "Drinking the water without treatment is always safe"),
    ("Community Translation Teams", "language access", "Bilingual volunteers help explain local information", "A second reader checks important translations", "Plain language makes the source easier to translate", "Feedback reveals words that confuse new residents", "Automatic translation never needs review"),
    ("Shared Study Calendars", "group planning", "Team members record deadlines in one place", "Colour labels separate different tasks", "Automatic reminders reduce forgotten work", "The calendar also shows when workloads overlap", "A calendar completes the work for the team"),
    ("Food Waste Diaries", "household waste", "Families record which food they throw away", "Patterns become visible after several weeks", "Shopping lists can then match real use", "The diary turns a general problem into specific choices", "One day of notes proves a permanent pattern"),
    ("Accessible Event Guides", "inclusive events", "Guides describe entrances, seating and sound levels", "Specific details help visitors plan independently", "Organisers update the guide when a room changes", "The same information can reveal design improvements", "Vague promises are more useful than measurements"),
    ("Street Tree Adoption", "urban tree care", "Residents volunteer to water young street trees", "Simple schedules prevent both neglect and overwatering", "City staff still handle technical care", "Local attention helps damage get reported quickly", "Volunteers should cut large branches themselves"),
    ("Borrowable Picnic Kits", "shared leisure equipment", "Parks lend reusable plates and cups", "A deposit encourages users to return the kit", "Central washing protects hygiene", "Families can hold events without buying disposable items", "Missing pieces have no effect on the scheme"),
    ("Public Piano Projects", "public music", "Old pianos are placed in supervised public spaces", "Local artists decorate the instruments", "Playing creates unexpected social contact", "Regular tuning keeps the experience enjoyable", "Rain improves an outdoor piano"),
    ("Campus Leftover Alerts", "food sharing", "Cafés announce safe surplus food near closing time", "Students receive alerts only for chosen locations", "Collection times remain short and clear", "Usage data helps kitchens plan future quantities", "Surplus food can wait outdoors all night"),
    ("Slow Checkout Lanes", "inclusive services", "Some shops offer lanes without pressure to hurry", "Staff receive extra communication training", "Clear signs let customers choose the service", "The lane supports people who need more processing time", "Every shopper is forced to use the slow lane"),
    ("Window Bird Markers", "wildlife safety", "Visible patterns help birds notice large windows", "Markers must cover enough of the glass", "Outside placement reduces reflections more effectively", "Simple designs can protect birds without blocking daylight", "One small sticker protects an entire building"),
    ("Local History Walks", "place-based learning", "Residents create routes around meaningful locations", "Personal memories add detail to official records", "Old photographs encourage comparison", "The walk turns ordinary streets into evidence", "Only famous buildings can carry history"),
    ("Reusable Moving Boxes", "waste reduction", "Strong boxes are rented for house moves", "Labels can be removed and used again", "Collection saves customers a return journey", "Repeated use spreads the production cost", "Cardboard is never used in moving"),
    ("Study Buddy Check-ins", "student support", "Students arrange brief weekly progress talks", "Each person states one realistic next action", "The partner asks questions rather than controlling the plan", "Regular contact makes difficulties easier to notice", "Partners should complete each other's assignments"),
]


def _insertion_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    title, topic, a, b, c, d, extra = spec
    options = {"A": a + ".", "B": b + ".", "C": c + ".", "D": d + ".", "E": extra + "."}
    transitions = (
        ("This practical starting point", "A reliable routine", "A learning benefit", "Evidence from ordinary use"),
        ("The first visible advantage", "The organisational foundation", "The shared knowledge created", "The record of real behaviour"),
        ("This immediate function", "A clear operating habit", "The project's educational side", "Information gathered over time"),
        ("The feature that attracts users", "The rule that protects trust", "The experience participants exchange", "The pattern organisers can measure"),
    )[(index - 1) % 4]
    paragraphs = [
        f"A local need often gives {title} their first group of users. [[1]] {transitions[0]} explains why the idea feels relevant to people interested in {topic}, rather than merely decorative.",
        f"Initial interest is not enough to keep {title} useful. [[2]] {transitions[1]} helps participants know what will happen and protects confidence when several people share the same service.",
        f"Participation in {title} can produce more than an immediate result. [[3]] {transitions[2]} allows practical knowledge about {topic} to move between organisers, experienced users, and newcomers.",
        f"Decisions about the future of {title} should come from observation. [[4]] {transitions[3]} shows which parts work well and where users still face confusion or unnecessary effort.",
        f"Like most projects connected with {topic}, {title} work best when their limits are stated honestly. A small and dependable service is more valuable than a large promise that organisers cannot maintain.",
    ]
    questions = []
    for gap, answer in enumerate(("A", "B", "C", "D"), start=1):
        questions.append({"stem": f"Which sentence completes gap {gap} in the text about {title}?", "options": options, "answer": answer, "points": 2, "qtype": "sentence_insertion", "rationale": f"Sentence {answer} develops the idea immediately before and after gap {gap} in the {topic} passage."})
    return {"id": f"catalog-reading-insertion-{index:02d}", "kind": "reading_insertion", "title": title, "topic": topic, "cefr": "B1+", "source": "seed", "published": True, "instructions": "Complete gaps 1-4 with the most suitable sentences A-E. There is one extra sentence.", "content": {"paragraphs": paragraphs, "sentence_options": options}, "questions": questions}


CLOZE_TOPICS = [
    "planning a weekly study schedule", "keeping a shared kitchen clean", "preparing for a short presentation", "using a campus bicycle safely", "starting a reading habit", "joining a student society", "reducing phone distractions", "cooking with seasonal vegetables", "organising digital notes", "walking to university", "learning from written feedback", "caring for indoor plants", "sharing tasks in a group", "visiting a museum effectively", "building an emergency kit", "using a reusable water bottle", "preparing for a job interview", "taking useful lecture notes", "protecting personal data", "volunteering at a local event", "choosing a quiet study place", "creating a realistic morning routine",
]


CLOZE_VARIANTS = [
    {
        "text": "People often begin {topic} with an ambitious plan. Progress is easier [[1]] the first action is small and clear. Learners [[2]] change everything at once may become tired before results appear. The plan should [[3]] at the end of each week, not after every attempt. A difficult day can then be examined [[4]] the whole routine being abandoned. Success is also more likely when the necessary materials [[5]] before the chosen starting time.",
        "questions": [
            (["unless", "when", "despite", "whereas"], "B", "When introduces the condition that makes progress easier.", "connector"),
            (["which", "whose", "who", "where"], "C", "Who refers to people.", "relative_clause"),
            (["review", "reviewed", "be reviewed", "reviewing"], "C", "Should requires be plus the past participle for this passive meaning.", "modal_passive"),
            (["instead", "rather", "without", "except"], "C", "Without is followed by an -ing form.", "preposition"),
            (["prepare", "prepared", "are prepared", "have preparing"], "C", "Materials receive the action, so a passive form is needed.", "passive"),
        ],
    },
    {
        "text": "A short checklist can make {topic} less confusing. It must be simple enough [[1]] in a busy moment. Tasks [[2]] depend on another person should be marked clearly. Once an item [[3]], the date can be added beside it. This creates a useful record [[4]] than a vague feeling of progress. The list should not be expanded [[5]] a new item is genuinely necessary.",
        "questions": [
            (["to use", "using", "used", "use"], "A", "Enough is followed by the infinitive: simple enough to use.", "infinitive"),
            (["what", "that", "where", "whose"], "B", "That introduces a defining relative clause about tasks.", "relative_clause"),
            (["completes", "has completed", "has been completed", "was completing"], "C", "The item receives the action, so present perfect passive is required.", "perfect_passive"),
            (["rather", "quite", "more", "so"], "A", "Rather than forms the comparison used here.", "comparison"),
            (["unless", "because of", "in spite", "during"], "A", "Unless means except if and introduces the required condition.", "connector"),
        ],
    },
    {
        "text": "Useful feedback can improve {topic}, but only if it leads to action. Instead of [[1]] every comment as criticism, learners can separate advice from personal opinion. A suggestion [[2]] includes an example is usually easier to apply. Some weaknesses can [[3]] immediately, while others require several attempts. Notes should be reviewed [[4]] the work is still fresh in the learner's mind. This process matters [[5]] memory alone often hides small but repeated errors.",
        "questions": [
            (["treat", "treated", "treating", "to treated"], "C", "Instead of is followed by an -ing form.", "gerund"),
            (["who", "where", "whose", "that"], "D", "That refers to the suggestion and introduces a defining clause.", "relative_clause"),
            (["improve", "be improved", "improved", "improving"], "B", "Can takes be plus the past participle for passive meaning.", "modal_passive"),
            (["while", "until", "despite", "unless"], "A", "While expresses that the work remains fresh at that time.", "connector"),
            (["because", "although", "unless", "whereas"], "A", "Because introduces the reason the process matters.", "connector"),
        ],
    },
    {
        "text": "At the start of {topic}, a group should decide [[1]] each member understands the same goal. People [[2]] responsibilities are unclear may complete the same task twice. If everyone [[3]] on a division of work earlier, this confusion could have been avoided. [[4]] having different skills, members still need a shared record of decisions. The record should be brief [[5]] everyone can check it quickly before a meeting.",
        "questions": [
            (["whether", "despite", "unless", "whose"], "A", "Whether introduces the question of shared understanding.", "noun_clause"),
            (["who", "whose", "which", "whom"], "B", "Whose expresses possession of responsibilities.", "relative_clause"),
            (["agrees", "has agreed", "had agreed", "would agree"], "C", "The third conditional requires past perfect in the if-clause.", "conditional"),
            (["Because", "Despite", "Although", "Therefore"], "B", "Despite is followed by the -ing phrase having different skills.", "connector"),
            (["even though", "so that", "as if", "rather than"], "B", "So that introduces the purpose of keeping the record brief.", "purpose"),
        ],
    },
    {
        "text": "Good preparation makes {topic} more manageable. Important information should be collected [[1]] a final decision is made. A learner who arrives unprepared may wish they [[2]] the instructions earlier. [[3]] the first attempt is imperfect, it can still reveal what needs attention. The next attempt should then be planned [[4]] instead of being rushed. [[5]], the same preventable difficulty may appear again.",
        "questions": [
            (["before", "since", "during", "until"], "A", "Before establishes the correct order of the two actions.", "time_clause"),
            (["checked", "have checked", "had checked", "would check"], "C", "Wish about an earlier past action takes past perfect.", "wish_clause"),
            (["Although", "Because", "Unless", "Therefore"], "A", "Although introduces a contrast with the useful result.", "connector"),
            (["careful", "more carefully", "most careful", "carefulness"], "B", "An adverb is needed to describe how the attempt is planned.", "adverb"),
            (["Otherwise", "Moreover", "For instance", "Similarly"], "A", "Otherwise states what may happen if the advice is not followed.", "linker"),
        ],
    },
    {
        "text": "People working on {topic} sometimes expect motivation to remain constant. They may be used [[1]] acting only when they feel enthusiastic. [[2]] they notice that energy changes from day to day, the routine may already have become difficult. A fixed time reduces the number of decisions that must [[3]]. The task should not be made [[4]] complicated to begin. A short repeatable action is useful, [[5]] a dramatic plan is often abandoned after a few days.",
        "questions": [
            (["for", "to", "with", "by"], "B", "Be used to is followed by a noun or -ing form.", "preposition"),
            (["By the time", "Although", "As soon as", "In case"], "A", "By the time shows that one situation may already exist when another is noticed.", "time_clause"),
            (["make", "be made", "made", "making"], "B", "Must takes be plus the past participle for passive meaning.", "modal_passive"),
            (["enough", "such", "too", "so much"], "C", "Too plus adjective means more complicated than is helpful.", "degree"),
            (["whereas", "because", "unless", "therefore"], "A", "Whereas contrasts a short action with a dramatic plan.", "contrast"),
        ],
    },
    {
        "text": "When several methods for {topic} are available, choosing one can be difficult. [[1]] the cost nor the popularity of a method proves that it is suitable. Options should be [[2]] according to the learner's actual goal. A method [[3]] works well for a friend may require different resources. The learner should [[4]] test a small version before making a long commitment. Evidence from that trial is usually more useful [[5]] a general recommendation online.",
        "questions": [
            (["Either", "Neither", "Both", "Not only"], "B", "Neither pairs with nor to reject both factors.", "correlative"),
            (["compare", "comparing", "be compared", "to compare"], "C", "Should requires passive be compared because options receive the action.", "modal_passive"),
            (["who", "where", "which", "whose"], "C", "Which refers to the method.", "relative_clause"),
            (["therefore", "however", "otherwise", "although"], "A", "Therefore introduces the logical recommendation from the previous point.", "linker"),
            (["that", "then", "as", "than"], "D", "The comparative more useful is followed by than.", "comparison"),
        ],
    },
    {
        "text": "A small trial is often the safest way to begin {topic}. It allows people to identify difficulties [[1]] risking the whole project. Users may dislike [[2]] asked to follow rules that have not been explained. Clear communication has therefore [[3]] to better participation in many trials. If organisers [[4]] questions early, they can adjust the design before expanding it. A larger version should be launched only [[5]] the first results are reliable.",
        "questions": [
            (["without", "except", "beside", "although"], "A", "Without is followed by an -ing form and means the risk is avoided.", "preposition"),
            (["be", "been", "being", "to being"], "C", "Dislike is followed by an -ing form; passive meaning requires being asked.", "gerund_passive"),
            (["lead", "led", "leading", "leads"], "B", "Has takes the past participle led.", "present_perfect"),
            (["collect", "collected", "will collect", "had collecting"], "A", "The first conditional uses present simple in the if-clause.", "conditional"),
            (["provided that", "despite", "in case of", "whereas"], "A", "Provided that introduces the necessary condition for expansion.", "connector"),
        ],
    },
]


def _cloze_pack(index: int, topic: str) -> dict[str, Any]:
    variant = CLOZE_VARIANTS[(index - 1) % len(CLOZE_VARIANTS)]
    cycle = (index - 1) // len(CLOZE_VARIANTS)
    leads = (
        f"This short text focuses on the practical side of {topic}.",
        f"The following advice treats {topic} as a process that can be tested and improved.",
        f"Successful {topic} depends on decisions made before, during, and after an attempt.",
    )
    text = f"{leads[cycle % len(leads)]} {variant['text'].format(topic=topic)}"
    questions = []
    for gap, (options, answer, rationale, qtype) in enumerate(variant["questions"], start=1):
        correct = options[("A", "B", "C", "D").index(answer)]
        distractors = [option for option in options if option != correct]
        questions.append(_choice_question(f"Gap {gap}", correct, distractors, rationale, rotation=index + gap, qtype=qtype))
    return {
        "id": f"catalog-cloze-{index:02d}", "kind": "cloze", "title": f"A Practical Guide to {topic.title()}", "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "instructions": "Choose the option that best fits each gap.", "content": {"text": text},
        "questions": questions,
    }


RESTATEMENT_TOPICS = [
    ("the library workshop", "the online guide", "the final report", "the study room", "the morning bus"),
    ("the volunteer event", "the safety briefing", "the application form", "the community hall", "the evening train"),
    ("the language club", "the practice recording", "the group presentation", "the media room", "the campus shuttle"),
    ("the garden project", "the planting guide", "the progress diary", "the equipment shed", "the weekend service"),
    ("the career seminar", "the example CV", "the interview task", "the advice office", "the early appointment"),
    ("the recycling campaign", "the sorting poster", "the results summary", "the collection point", "the delivery vehicle"),
    ("the photography course", "the camera manual", "the final portfolio", "the editing lab", "the city tram"),
    ("the cooking class", "the recipe video", "the shared meal", "the training kitchen", "the market bus"),
    ("the history lecture", "the archive website", "the research essay", "the reading room", "the museum shuttle"),
    ("the sports programme", "the exercise plan", "the fitness record", "the training hall", "the late ferry"),
    ("the coding workshop", "the setup guide", "the team project", "the computer lab", "the express bus"),
    ("the design exhibition", "the visitor map", "the reflection paper", "the main gallery", "the local train"),
    ("the debate society", "the topic sheet", "the opening speech", "the meeting room", "the direct coach"),
    ("the music rehearsal", "the practice notes", "the concert plan", "the performance hall", "the night bus"),
    ("the science fair", "the experiment guide", "the display board", "the project space", "the regional train"),
    ("the book discussion", "the chapter summary", "the response paper", "the quiet lounge", "the campus minibus"),
    ("the first-aid course", "the emergency card", "the skills test", "the practice room", "the morning metro"),
    ("the film screening", "the discussion guide", "the review assignment", "the small cinema", "the last tram"),
    ("the field trip", "the route notes", "the observation report", "the meeting point", "the university coach"),
    ("the entrepreneurship talk", "the planning template", "the business proposal", "the conference room", "the airport bus"),
    ("the peer-mentoring session", "the question list", "the action plan", "the support centre", "the regular shuttle"),
    ("the environmental survey", "the data guide", "the findings poster", "the research office", "the river ferry"),
    ("the theatre workshop", "the scene outline", "the group performance", "the rehearsal studio", "the city bus"),
    ("the mathematics clinic", "the example sheet", "the weekly assignment", "the tutorial room", "the suburban train"),
]


def _restatement_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    event, guide, task, place, transport = spec
    styles = (
        [
            (f"Although {event} is optional, students are advised to attend it before beginning {task}.", f"Attending {event} is recommended but not required before {task} starts.", [f"Students cannot begin {task} unless they attend {event}.", f"Only students who finished {task} may attend {event}.", "Both activities have been cancelled."], "The recommendation and optional status are both preserved."),
            (f"The coordinator simplified {guide} so that first-time users could follow it more easily.", "The guide was made clearer for people using it for the first time.", ["New users were asked to write a harder guide.", "The guide was removed because nobody followed it.", "Only experienced users can now understand the guide."], "Simplifying the guide makes it easier for first-time users."),
            (f"Mert did not notice the missing section of {task} until he read the feedback.", "The feedback made Mert aware that part of the task was absent.", ["Mert wrote the feedback before the missing section.", "Mert refused to read feedback about the task.", "The section disappeared after the feedback was read."], "Reading the feedback caused Mert to recognise the missing section."),
            (f"Because {place} becomes crowded after two o'clock, the group decided to meet there earlier.", "The group chose an earlier time to avoid the crowded period.", ["The place does not allow entry before two.", "The group prefers meeting at the busiest time.", "The meeting moved to another day because the place closed."], "The earlier meeting avoids the later crowded period."),
            (f"The journey will be faster by {transport} unless there is an unexpected delay.", "Only an unexpected delay may prevent this transport option from being faster.", ["The transport is always slower even when on time.", "The journey was cancelled because a delay was expected.", "Passengers must create a delay before travelling."], "Unless introduces the condition that could change the expected result."),
        ],
        [
            (f"The organisers postponed {event} because too few students had registered by Friday.", f"Insufficient registration by Friday caused {event} to be delayed.", [f"The event took place early because registration was full.", "Students registered only after the event ended.", "Friday's event attracted more students than expected."], "The cause and the postponement are preserved."),
            (f"Students may use {place} only after a supervisor has checked their booking.", f"A supervisor must confirm the booking before students can enter {place}.", ["Students check the supervisor's booking after entering.", "No booking is needed when a supervisor is absent.", "The place can be used before any check takes place."], "The required check must happen before use."),
            (f"Selin completed {task} on time despite losing access to {guide} for two days.", f"Losing access to {guide} did not prevent Selin from finishing {task} by the deadline.", ["Selin missed the deadline because the guide was unavailable.", "The guide was available throughout the task.", "Selin stopped the task for two days after finishing it."], "Despite shows that the difficulty did not change the successful result."),
            (f"The revised version of {guide} is not as detailed as the original, but it is easier to use.", f"The new guide contains less detail yet is more user-friendly.", ["The original guide was shorter and easier.", "Both versions contain exactly the same detail.", "The revision became harder because more detail was added."], "Both the reduced detail and improved usability are retained."),
            (f"If the group misses {transport}, it will have to arrive after the opening session.", f"Catching {transport} is necessary for the group to arrive before the opening session ends.", ["The opening session begins only after the group arrives.", "Missing the transport will make the group arrive earlier.", "The group has decided not to attend the opening session."], "The conditional consequence is expressed without changing its meaning."),
        ],
        [
            (f"Not until the reminder arrived did Ayşe remember that she had signed up for {event}.", f"The reminder caused Ayşe to recall her registration for {event}.", ["Ayşe registered only after the event reminder ended.", "The reminder made Ayşe cancel an event she remembered.", "Ayşe sent the reminder to everyone who registered."], "The reminder is the point at which she remembers."),
            (f"The tutor suggested using {guide} rather than searching for several unrelated sources.", f"The tutor preferred the guide to a collection of unconnected sources.", ["The tutor said the guide should never be used.", "Several unrelated sources were written by the tutor.", "The guide contains no information from any source."], "Rather than expresses the tutor's preference."),
            (f"As long as the main argument remains clear, minor changes can be made to {task}.", f"Small revisions to {task} are acceptable provided that its main argument stays clear.", ["No changes are allowed even when the argument is clear.", "The main argument must be removed before revision.", "Only major changes can make the argument clearer."], "As long as and provided that express the same condition."),
            (f"Hardly anyone was using {place} when the group first arrived.", f"The place was almost empty at the time of the group's arrival.", ["The group arrived because the place was completely closed.", "A large crowd was already using the place.", "The group left before anyone could arrive."], "Hardly anyone means almost nobody."),
            (f"By the time {transport} reached the station, the rain had already stopped.", "The rain ended before the transport arrived at the station.", ["The rain began after the transport left the station.", "The transport stopped because the rain continued.", "The station closed before either event happened."], "Past perfect marks the rain ending as the earlier event."),
        ],
        [
            (f"Students who miss {event} can watch the recording, provided that they submit a short reflection.", f"A reflection is required from students who replace attendance at {event} with the recording.", ["Only students at the live event may write a reflection.", "The recording is unavailable to anyone who missed the event.", "Submitting a reflection prevents students from watching."], "The condition attached to using the recording is preserved."),
            (f"No sooner had Deniz opened {guide} than he found the section he needed.", f"Deniz located the required section immediately after opening the guide.", ["Deniz closed the guide before finding any section.", "The required section was added much later.", "Deniz searched several guides without success."], "No sooner ... than shows that the second event followed immediately."),
            (f"The lecturer asked for {task} to be shortened without removing its main example.", f"The task should become shorter while keeping the central example.", ["The main example must be removed to shorten the task.", "The lecturer requested a longer task with more examples.", "The task cannot be edited in any way."], "Both shortening and retaining the example are required."),
            (f"Unless the booking is extended, the group must leave {place} at four.", f"The group can stay after four only if it receives a longer booking.", ["The group may stay indefinitely without a booking.", "Extending the booking forces the group to leave earlier.", "The place always closes before four."], "Only if expresses the same necessary condition as unless."),
            (f"The group chose {transport} mainly because it was more reliable, not because it was cheaper.", f"Reliability, rather than price, was the main reason for choosing the transport.", ["The group selected the cheapest but least reliable option.", "Price and reliability had no influence on the choice.", "The transport was rejected because it cost less."], "The main reason and the rejected reason are both retained."),
        ],
    )
    selected = styles[(index - 1) % len(styles)]
    questions = [
        _choice_question(original, correct, distractors, rationale, rotation=index + offset, qtype="restatement")
        for offset, (original, correct, distractors, rationale) in enumerate(selected)
    ]
    return {"id": f"catalog-restatement-{index:02d}", "kind": "restatement", "title": f"Restatement Practice {index:02d}", "topic": event.removeprefix("the "), "cefr": "B1+", "source": "seed", "published": True, "instructions": "Choose the option that best restates the meaning of the original sentence.", "content": {"intro": "Read each original sentence carefully. Choose the option with the closest meaning."}, "questions": questions}


SPEAKING_DOMAINS = [
    ("Study Routine", "your study routine", "learning"), ("Campus Place", "a useful place on campus", "campus life"),
    ("Healthy Choice", "a healthy choice you make", "wellbeing"), ("Useful App", "an app that supports daily life", "technology"),
    ("Shared Responsibility", "a responsibility shared with other people", "teamwork"), ("Travel Experience", "a journey that taught you something", "travel"),
    ("Helpful Feedback", "feedback that changed your work", "learning"), ("Local Problem", "a problem in your neighbourhood", "community"),
    ("Time Management", "the way you manage a busy day", "planning"), ("New Skill", "a skill worth learning", "personal development"),
    ("Environmental Habit", "an environmental habit", "sustainability"), ("Important Conversation", "a conversation you remember", "communication"),
    ("Team Project", "a project completed with a team", "teamwork"), ("Public Service", "a public service people need", "community"),
    ("Digital Balance", "a way to balance online and offline time", "technology"), ("Cultural Event", "a cultural event you experienced", "culture"),
    ("Difficult Decision", "a difficult decision", "decision making"), ("Affordable Activity", "an enjoyable low-cost activity", "daily life"),
    ("Learning Mistake", "a mistake that helped you learn", "learning"), ("Future Workplace", "a workplace you would enjoy", "work"),
    ("Community Support", "a way people support one another", "community"), ("Useful Object", "an everyday object you value", "daily life"),
    ("Personal Goal", "a goal you want to reach", "personal development"),
]


def _speaking_packs() -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    formats = [
        ("A Memorable Example", "Talk about a memorable example of {subject}.", ["what happened", "who or what was involved", "why you still remember it"], ["What makes an experience memorable?", "How can people learn from this kind of experience?", "Would your response be different now?"]),
        ("One Useful Change", "Talk about one change you would make to {subject}.", ["what you would change", "why the change is needed", "what result you expect"], ["Why can small changes be effective?", "Who should be involved in the decision?", "What difficulty might appear first?"]),
        ("A Choice to Explain", "Explain an important choice connected with {subject}.", ["what the choices are", "which option you prefer", "what evidence supports your choice"], ["Why might another person choose differently?", "Which factor matters most in this decision?", "Can the best choice change over time?"]),
        ("A Realistic Plan", "Describe a realistic future plan involving {subject}.", ["what you want to do", "which steps you would take", "how you would measure progress"], ["What could interrupt the plan?", "Who could provide useful support?", "When should a plan be revised?"]),
        ("A Problem and Response", "Describe a problem related to {subject} and explain how you would respond.", ["what causes the problem", "who is affected", "which response is realistic"], ["What should happen first?", "Which response would be ineffective?", "How would you know the problem is improving?"]),
        ("Advice for Someone", "Give practical advice to someone dealing with {subject}.", ["what the person should understand", "two actions they can take", "one mistake they should avoid"], ["Why might the advice be difficult to follow?", "How could the advice be adapted?", "Who else could help?"]),
        ("Past and Present", "Compare how you experienced {subject} in the past with how you experience it now.", ["what was different before", "what caused the change", "which situation you prefer"], ["Do people always change in the same direction?", "What may change again in the future?", "Which difference matters most?"]),
        ("Benefits and Limits", "Discuss both the benefits and the limits of {subject}.", ["one important benefit", "one realistic limitation", "how to keep a fair balance"], ["Who receives the greatest benefit?", "Can the limitation be reduced?", "When might the balance change?"]),
        ("A Specific Recommendation", "Make a specific recommendation about {subject}.", ["what you recommend", "which evidence supports it", "who should act on it"], ["What objection might someone raise?", "How would you answer that objection?", "What is the first practical step?"]),
        ("An Unexpected Lesson", "Explain an unexpected lesson you learned through {subject}.", ["what you expected at first", "what actually happened", "how the lesson changed you"], ["Why was the result surprising?", "Could someone learn this without the experience?", "How will you use the lesson later?"]),
        ("Two Possible Futures", "Describe two possible future outcomes connected with {subject}.", ["what could go well", "what could go wrong", "which action would influence the outcome"], ["Which outcome is more likely?", "Who has the most influence?", "What early sign would you watch?"]),
        ("Explain It to a Newcomer", "Explain {subject} to someone experiencing it for the first time.", ["what they need to know first", "what may confuse them", "how they can prepare"], ["Which detail is easiest to misunderstand?", "What example would make it clearer?", "What question should the newcomer ask?"]),
    ]
    number = 1
    for domain_index, (label, subject, topic) in enumerate(SPEAKING_DOMAINS):
        start = (domain_index * 4) % len(formats)
        selected_formats = [formats[(start + offset) % len(formats)] for offset in range(4)]
        for suffix, prompt, bullets, followups in selected_formats:
            cards.append({
                "id": f"catalog-speaking-{number:03d}", "kind": "speaking_card", "title": f"{label}: {suffix}", "topic": topic,
                "cefr": "B1+", "source": "seed", "published": True,
                "instructions": "Read the card, think for one minute, then cover all three points and answer the follow-up questions.",
                "content": {"prompt": prompt.format(subject=subject), "bullets": bullets, "followups": followups}, "questions": [],
            })
            number += 1
    return cards


def build_practice_catalog() -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    packs.extend(_conversation_pack(i, spec) for i, spec in enumerate(CONVERSATION_SPECS, start=1))
    packs.extend(_lecture_pack(i, spec) for i, spec in enumerate(LECTURE_SPECS, start=1))
    packs.extend(_reading_pack(i, spec) for i, spec in enumerate(READING_SPECS, start=1))
    packs.extend(_insertion_pack(i, spec) for i, spec in enumerate(INSERTION_TOPICS, start=1))
    packs.extend(_cloze_pack(i, topic) for i, topic in enumerate(CLOZE_TOPICS, start=1))
    packs.extend(_restatement_pack(i, spec) for i, spec in enumerate(RESTATEMENT_TOPICS, start=1))
    packs.extend(_speaking_packs())
    return packs


EXPECTED_EXTRA_COUNTS = {
    "conversation": 22,
    "lecture": 24,
    "reading_standard": 23,
    "reading_insertion": 24,
    "cloze": 22,
    "restatement": 24,
    "speaking_card": 92,
}


def _assert_catalog_shape() -> None:
    packs = build_practice_catalog()
    counts = {kind: sum(pack["kind"] == kind for pack in packs) for kind in EXPECTED_EXTRA_COUNTS}
    if counts != EXPECTED_EXTRA_COUNTS:
        raise RuntimeError(f"Practice catalog count mismatch: {counts}")
    ids = [pack["id"] for pack in packs]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Practice catalog contains duplicate IDs")


_assert_catalog_shape()
