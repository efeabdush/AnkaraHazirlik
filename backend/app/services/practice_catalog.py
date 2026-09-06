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


def _lexical_cycle(text: str, cycle: int) -> str:
    """Vary recurring genre language without changing its B1+ meaning."""
    replacements = (
        (),
        (
            ("For an individual,", "Seen by one participant,"),
            ("may be experienced as one simple moment: a need appears, a person uses the service, and a result follows.", "can look like a straightforward experience: a need arises, the service is used, and an outcome is noticed."),
            ("From the organiser's position, however, each moment belongs to a larger network of decisions.", "Staff see something more complex because every visit depends on decisions made earlier."),
            ("moves between these two viewpoints to show why both are necessary.", "uses both perspectives to give a fair account of the idea."),
            ("From the user's side, the main advantage is easy to state:", "Participants usually notice the clearest advantage first:"),
            ("Immediate usefulness matters because people rarely study the full structure before deciding whether to participate.", "This direct value matters; few people examine an entire system before trying it."),
            ("Their first experience shapes what they expect and what they tell others.", "That early encounter influences both later expectations and personal recommendations."),
            ("Behind that experience lies the way that", "The experience also depends on the fact that"),
            ("must make this process steady without creating rules that are harder than the problem they solve.", "need a reliable process, but its rules must not create a second obstacle."),
            ("The best procedures remain noticeable when guidance is needed and almost invisible when everything is working well.", "Good procedures offer direction at a difficult moment and stay out of the way at other times."),
            ("Individual actions can also combine into a collective effect because", "Separate choices may gradually produce a wider effect because"),
            ("illustrates this widening view.", "shows how the wider effect develops."),
            ("What began as separate choices gradually produced shared information, new habits, or a stronger sense of responsibility among participants.", "Repeated participation can spread knowledge, change habits, and create shared responsibility."),
            ("The system still faces a trade-off:", "A genuine limitation remains:"),
            ("A sensible response is to", "The proposed response is to"),
            ("even if that means rejecting a faster or more impressive change.", "although a quicker or more dramatic option may attract more attention."),
            ("The purpose is not to avoid risk completely but to keep the consequences visible and manageable.", "The aim is to recognise the risk early enough to manage its effects."),
            ("Neither viewpoint is sufficient alone.", "One perspective by itself gives an incomplete picture."),
            ("User stories show where value is felt, while system evidence reveals who is missing and what must be maintained.", "Personal accounts reveal direct value; operational evidence shows who is excluded and what requires continued work."),
            ("Combining them gives a more complete judgement of", "Considering both supports a more balanced judgement of"),
            ("prevents a few positive experiences from standing in for the whole picture.", "stops a handful of good experiences from representing everyone."),
            ("projects", "schemes"), ("project", "scheme"), ("services", "programmes"), ("service", "programme"),
            ("Organisers", "Staff teams"), ("organisers", "staff teams"), ("Users", "Participants"), ("users", "participants"),
            ("People", "Community members"), ("people", "community members"), ("benefits", "advantages"), ("benefit", "advantage"),
            ("difficulties", "obstacles"), ("difficulty", "obstacle"),
            ("information", "guidance"), ("However,", "Yet,"), ("For that reason,", "Consequently,"),
            ("At the same time,", "Meanwhile,"), ("This is why", "Therefore"),
        ),
        (
            ("For an individual,", "At the level of daily use,"),
            ("may be experienced as one simple moment: a need appears, a person uses the service, and a result follows.", "may seem simple: somebody has a need, tries the service, and observes a result."),
            ("From the organiser's position, however, each moment belongs to a larger network of decisions.", "Coordinators instead have to connect that moment with planning, access, and maintenance."),
            ("moves between these two viewpoints to show why both are necessary.", "compares these perspectives and explains what each one reveals."),
            ("From the user's side, the main advantage is easy to state:", "The direct positive effect is clear to a visitor:"),
            ("Immediate usefulness matters because people rarely study the full structure before deciding whether to participate.", "Direct usefulness is essential because most residents try an idea before they understand how it is organised."),
            ("Their first experience shapes what they expect and what they tell others.", "The first attempt then affects future use and what is said to neighbours."),
            ("Behind that experience lies the way that", "Supporting that visible outcome is the fact that"),
            ("must make this process steady without creating rules that are harder than the problem they solve.", "must keep the arrangement dependable without surrounding it with unnecessary rules."),
            ("The best procedures remain noticeable when guidance is needed and almost invisible when everything is working well.", "An effective procedure becomes clear when help is required but does not slow normal use."),
            ("Individual actions can also combine into a collective effect because", "A broader outcome can grow from many separate actions because"),
            ("illustrates this widening view.", "provides a concrete example of that development."),
            ("What began as separate choices gradually produced shared information, new habits, or a stronger sense of responsibility among participants.", "Over time, private choices may build common knowledge, different habits, and greater responsibility."),
            ("The system still faces a trade-off:", "The arrangement nevertheless has a limit:"),
            ("A sensible response is to", "A practical next step is to"),
            ("even if that means rejecting a faster or more impressive change.", "instead of selecting the fastest or most visible response."),
            ("The purpose is not to avoid risk completely but to keep the consequences visible and manageable.", "This does not remove uncertainty, but it makes the likely effects easier to control."),
            ("Neither viewpoint is sufficient alone.", "Daily experience and system evidence answer different questions."),
            ("User stories show where value is felt, while system evidence reveals who is missing and what must be maintained.", "Stories show where the value appears, whereas records identify missing groups and maintenance needs."),
            ("Combining them gives a more complete judgement of", "Together they allow a stronger assessment of"),
            ("prevents a few positive experiences from standing in for the whole picture.", "avoids treating a small number of satisfied visitors as the entire community."),
            ("projects", "initiatives"), ("project", "initiative"), ("services", "arrangements"), ("service", "arrangement"),
            ("Organisers", "Coordinators"), ("organisers", "coordinators"), ("Users", "Visitors"), ("users", "visitors"),
            ("People", "Residents"), ("people", "residents"), ("benefits", "positive effects"), ("benefit", "positive effect"),
            ("difficulties", "challenges"), ("difficulty", "challenge"),
            ("information", "details"), ("However,", "Nevertheless,"), ("For that reason,", "As a consequence,"),
            ("At the same time,", "In parallel,"), ("This is why", "That explains why"),
        ),
    )
    for original, replacement in replacements[cycle % len(replacements)]:
        text = text.replace(original, replacement)
    return text


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
    base_style = (index - 1) % len(styles)
    cycle = (index - 1) // len(styles)
    script = [{"speaker": speaker, "text": text} for speaker, text in styles[(base_style + cycle * 2) % len(styles)]]
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
        f"Good morning. Today we will use {subject} to examine how a visible result can depend on several less obvious processes.",
        f"Imagine that a classmate asks why {subject} deserves serious study. We will answer through evidence, one practical example, and an important limit.",
        f"Our subject today is {subject}. Listen for the relationship between three claims rather than trying to write down every sentence.",
        f"Today's question sounds simple: what makes {subject} work as it does? The answer becomes clearer when we compare purpose with actual use.",
        f"Let us begin with an everyday observation about {subject}, then widen the discussion to organisation, behaviour, and evidence.",
        f"This lecture treats {subject} as a case study. As you take notes, separate the central claim, the example, and the qualification.",
        f"A useful way into {subject} is to start with a local decision and ask what evidence would justify it.",
        f"Instead of listing facts about {subject}, today's talk follows the idea from an individual experience to a broader system.",
    )
    article_paragraphs, _ = _reading_paragraphs(index + 3, spec)
    lines = [openings[(index - 1) % len(openings)], *article_paragraphs]
    extensions = (
        f"Let us pause over the evidence. If we measured only whether {first}, we would miss the conditions behind that result. A stronger observation would record when {second}, who is affected when {third}, and whether the pattern changes over time. It would also compare ordinary days with unusual ones. This does not require a complicated experiment; it requires a question clear enough to be answered by more than one kind of evidence. In the case of {subject}, that distinction matters because a visible success may arrive before organisers understand the work needed to maintain it.",
        f"There is also a question of scale. What works in {example} may offer a useful possibility without becoming a set of instructions for every location. Another place could have different resources, expectations, or physical conditions. Before copying the example, decision-makers should identify which part depends on the fact that {first} and which part depends on local support. They can then test the proposal to {action} on a limited scale. Comparison becomes meaningful only when the original purpose and the new conditions are both stated clearly.",
        f"Now consider the viewpoint of someone directly affected by {subject}. That person may care about the immediate result and know little about the wider system. An organiser, by contrast, must think about repeated use, maintenance, and people who are currently excluded. Neither viewpoint is complete alone. Personal accounts can reveal why {second} matters, while records across time can test the claim that {third}. Bringing the two together prevents a small number of positive experiences from being mistaken for evidence that every part of the system is working.",
        f"A final issue is how to respond when the evidence is mixed. The fact that {limitation} does not automatically defeat the argument, just as one benefit does not prove it. The useful task is to locate the boundary: under which conditions does the benefit remain stronger than the difficulty? A carefully described limit can improve a recommendation by showing where extra support is needed. For {subject}, this leads back to the proposal to {action}. That step is modest enough to observe but meaningful enough to produce information for the next decision.",
    )
    lines.append(extensions[(index - 1) % len(extensions)])
    lines.append(
        f"Before moving to the conclusion, check the hierarchy in your notes. {first.capitalize()} is a direct claim, while the point that {third} widens the discussion. {example.capitalize()} belongs under evidence, and the statement that {limitation} belongs under limitation. Keeping those functions separate will make the four questions easier to answer. It will also prevent a memorable example from replacing the wider argument in your final summary."
    )
    summaries = (
        f"To conclude, connect the claim that {first} with the facts that {second} and {third}. Keep {limitation} beside the example in your notes, because it prevents a local result from becoming a universal promise.",
        f"Before we finish, reduce the lecture to three lines: the direct effect, the process that supports it, and the caution. The practical recommendation is to {action}; its value should be judged against evidence from the setting.",
        f"The main lesson is that {subject} cannot be explained by one attractive result. The example of {example} matters because it connects the separate claims, while the stated limit keeps the conclusion realistic.",
        f"In your notes, place {example} under evidence rather than under the main idea. The central argument joins {first}, {second}, and {third}, then qualifies that argument by recognising that {limitation}.",
    )
    lines.append(summaries[(index - 1) % len(summaries)])
    if sum(len(line.split()) for line in lines) < 620:
        lines.insert(
            -1,
            f"One last comparison will help: evidence that {first} describes an effect, whereas the proposal to {action} describes a response. Do not place them under the same heading in your notes.",
        )
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


READING_TOPIC_PARAGRAPHS = (
    "Food safety makes the community fridge different from an ordinary cupboard. Chilled products cannot remain outside while volunteers decide where they belong, and homemade food may require special rules. Some fridges solve this by accepting only sealed items with readable dates. Others work with nearby cafés at fixed collection times. These local choices influence how much food can be shared without creating a health risk.",
    "Restoring a stream also changes how rain moves through a neighbourhood. A straight concrete channel carries water away quickly, but that speed can increase pressure downstream. Bends, stones, and planted banks slow part of the flow. Engineers still need to prepare for unusually heavy rain, so the attractive park above the stream must remain connected to careful measurements below it.",
    "Peer teaching is most useful when the second student does more than listen politely. They need to interrupt an unclear explanation, request another example, and test the idea with a new question. This forces the speaker to reorganise knowledge instead of repeating a textbook sentence. The listener benefits too, because asking a precise question requires them to identify the exact point where understanding stopped.",
    "A photograph of a railway station, for example, may show clothing, luggage, signs, and expressions in remarkable detail. It cannot show who left five minutes earlier or why the crowd gathered. A newspaper report may answer some questions but introduce its own viewpoint. Historians therefore build an interpretation by comparing incomplete sources rather than asking one image to provide the whole event.",
    "The ability to buy an exact amount changes more than packaging. Someone trying a new ingredient can take a small quantity instead of paying for a full packet. On the other hand, shoppers must remember the weight of their empty container and may need more time at the till. Whether the system feels convenient depends on how these extra steps are designed.",
    "A campus garden follows the academic year poorly. Seedlings may need the most attention just as students leave for summer, and a new group may return without knowing what was planted. Simple labels and a seasonal notebook can carry knowledge between volunteers. Choosing a few strong plants is often wiser than creating an impressive garden that nobody can maintain in August.",
    "Pictures in repair guides deserve testing as carefully as words. A close photograph may show a screw clearly while hiding where it sits on the whole machine. A wider image gives orientation but may lose the small detail. Effective guides often alternate between the two and mark the relevant part. This lets beginners connect each action with the object in front of them.",
    "The collection itself must match local life. Camping equipment may be popular in one area, while cooking tools or carpet cleaners are more useful elsewhere. Loan records can guide future purchases, but a rarely borrowed item is not automatically a mistake; emergency equipment may be valuable precisely because people need it infrequently. Staff have to interpret the numbers alongside user requests.",
    "Plant choice affects whether a rain garden continues working. Species must survive both wet periods and days when the soil becomes dry. Ordinary garden soil may hold water too long, whereas a suitable mixture lets it pass slowly. Leaves and litter can also block the entrance from the road. Maintenance therefore involves the path of the water, not only the appearance of the plants.",
    "Serving size creates a particular comparison problem. One cereal may display values for thirty grams and another for forty-five, making the second appear to contain more of everything. A shopper who normally eats sixty grams needs to calculate both on the same basis. Clear front labels can direct attention, but the full table is still necessary when two products use different portions.",
    "A lasting study group develops a rhythm between meetings. Each member arrives with one question or section prepared, and the group finishes by deciding what will happen next. Without that link, every meeting begins with a new negotiation. Members may enjoy the company yet complete little work. A short written aim protects the academic purpose without removing friendly conversation entirely.",
    "The thirty-minute closure changes the space only at the busiest moment. Children can cross more freely, families wait near the entrance, and drivers learn to use another point. Enforcement matters because a sign alone may be ignored. Schools also have to consult residents and families with mobility needs, whose journeys may not fit the most common pattern.",
    "The sense of company is strongest when a programme appears regularly and the host speaks in an informal style. Yet the relationship moves in one direction: listeners may know the host's stories while the host knows nothing about them. Recognising this difference helps people enjoy the programme without treating every confident opinion as advice from a close friend.",
    "A recycling label on clothing can hide several physical difficulties. Thread, elastic, printed designs, and coatings may all require different treatment from the main fabric. Removing them costs time, and the remaining fibres may be too short for another strong garment. Designers can improve the situation before production by using components that are easier to separate and identify.",
    "Shade changes during the day and across the year. A bench comfortable in a spring afternoon may sit in full sun during July. Mature trees offer broad cooling but take years to grow, while a built cover works immediately and requires different maintenance. Mapping who uses each area at different hours helps planners choose where limited shade will have the greatest effect.",
    "Version labels are particularly important in shared work. If three students download a report called 'final', edit separate copies, and upload them again, useful changes can disappear. A short pattern containing the project, date, and version makes the order visible. The rule succeeds only when every member applies it, so the group should choose a format that is quick to type.",
    "A report about one altered bus route may seem too small for national media, yet it can explain why workers arrive late or why a shop loses customers. Repeated local reporting also preserves the earlier promises made by officials. When the route is reviewed months later, residents have more than memory. This continuity is valuable even when no single article attracts a large audience.",
    "Washing is the hidden centre of a shared cup scheme. A cup returned at a station must be collected, checked, cleaned, and sent back to a café before the supply runs low. If each business uses a different shape, stacking and transport become harder. A common design may feel less distinctive, but it allows the network to treat cups as one circulating supply.",
    "Standing changes pressure on the body but does not make movement unnecessary. A user may stand without changing position and develop discomfort in the feet or back. The useful feature is the ability to move between sitting, standing, and short walks according to the task. Reading a long article and joining a brief online meeting may call for different positions.",
    "Seed labels carry information that a commercial packet may not include. A gardener can record that beans survived strong wind, tomatoes ripened in a shaded yard, or a plant was especially vulnerable to insects. When seeds return with such notes, the library stores local experience as well as material. Poor labelling breaks that connection and turns an adapted collection into an uncertain mixture.",
    "Waiting information is useful even when it cannot shorten the delay. A patient who knows that a doctor is running twenty minutes late can sit down, make a call, or change another plan. Silence removes those small choices. Estimates need regular correction, however, because an old number that remains on a screen can feel less respectful than an honest message that timing is uncertain.",
    "Night trains combine transport and accommodation, which changes how travellers compare prices. A ticket may look expensive beside a flight until the cost of an airport journey and a hotel night is included. The comparison also depends on sleep quality and arrival time. For some passengers the train protects a working day; for others, a broken night's sleep removes that advantage.",
    "Debate often begins before a public artwork is installed. Residents may ask who selected it, what it cost, or why one history was represented instead of another. Explaining the process can build trust, but officials cannot require everyone to share the same interpretation. The open disagreement is part of public art's effect, provided that people have accurate information about the decision.",
)


def _reading_paragraphs(index: int, spec: tuple[str, ...]) -> tuple[list[str], tuple[str, str, list[str], int]]:
    """Write the same evidence through genuinely different B1+ discourse structures."""
    title, topic, subject, first, second, third, example, limitation, action = spec
    base_style = (index - 1) % 8
    style = (base_style + ((index - 1) // 8) * 3) % 8

    if style == 0:  # case study first
        paragraphs = [
            f"At {example}, an ordinary situation raised a larger question about {topic}. People liked the idea behind {subject}, but early reactions did not show whether it would remain useful. The organisers therefore watched what happened after the first excitement had passed. Their experience offers a practical way to understand both the value and the limits of the idea.",
            f"The most immediate result was that {first}. This mattered because it answered a visible local need rather than an imagined one. Yet the project team soon learned that a benefit is not self-sustaining. Someone still has to explain the system, notice failures, and make small corrections before a minor problem discourages users.",
            f"A less obvious finding concerned the way that {second}. In practice, this effect depended on consistent arrangements. When instructions changed without warning, people hesitated; when the process stayed clear, they adjusted their behaviour and returned with fewer questions. Reliability, rather than novelty, became the sign that the project was beginning to mature.",
            f"The project also revealed that {third}. This broader outcome developed gradually through repeated contact and observation. It could not be created by a single event or attractive sign. For that reason, the organisers treated comments and everyday behaviour as evidence, even when those details were harder to count than visitor numbers.",
            f"The case did not produce a perfect model. In particular, {limitation}. The team chose to {action}, accepting that a smaller improvement was more credible than a dramatic promise. This cautious decision made the project more resilient: it could respond to pressure without losing its original purpose.",
            f"The lesson is not that every place should copy {example}. Conditions connected with {subject} vary, and a solution that suits one group may fail elsewhere. The useful principle is to connect a clear benefit with dependable organisation, social learning, and honest limits. That approach turns an interesting experiment into something people can understand and improve over time.",
        ]
        vocab = ("resilient", "able to continue despite difficulty", ["popular for a very short time", "cheap to replace completely", "controlled by a single person"], 5)
    elif style == 1:  # question-led explainer
        paragraphs = [
            f"Why do some attempts involving {subject} become part of daily life while others are quickly forgotten? The answer is not simply money or publicity. Looking closely at {title.lower()} shows that several conditions must support one another. A visible advantage may bring people in, but a dependable process is what gives them a reason to come back.",
            f"Begin with the clearest advantage: {first}. It explains why the idea attracts attention in the first place. However, the result only matters if people can reach it without unnecessary confusion. A project may appear successful on its opening day and still lose support when users cannot tell what to do next.",
            f"This is where the fact that {second} becomes important. Clear arrangements reduce uncertainty and allow users to make sensible choices. They also make responsibility easier to trace when something goes wrong. Such practical details can seem dull beside a new idea, but they often determine whether the service earns trust.",
            f"There is another question: what do people learn from taking part? In this case, {third}. The effect may appear slowly as users watch one another and exchange advice. At {example}, for instance, the most useful changes came after organisers listened to recurring questions instead of assuming that silence meant satisfaction.",
            f"No arrangement can remove every difficulty. Here, {limitation}. Ignoring that fact would create an unrealistic expectation and eventually weaken support. A more sensible response is to {action}. This does not guarantee success, but it gives organisers a concrete action whose effects they can observe.",
            f"So the original question has a qualified answer. {subject.capitalize()} can last when a clear purpose, understandable routines, and opportunities for learning develop together. They become fragile when one early success is treated as proof that no adjustment is needed. Long-term value grows from attention to ordinary use, not from the size of the launch.",
        ]
        vocab = ("fragile", "easily weakened or damaged", ["certain to become larger", "difficult to explain in words", "supported by strong evidence"], 6)
    elif style == 2:  # misconception and correction
        paragraphs = [
            f"A common belief about {subject} is that the main idea is enough: introduce the service and people will naturally use it well. That belief is attractive because it makes change look simple. The evidence described in {title.lower()}, however, points to a more demanding conclusion. Benefits, routines, and human behaviour all shape the final result.",
            f"There is good reason for initial optimism, since {first}. This is not a minor achievement. Still, it is only one part of the picture. Measuring that result alone may hide whether the same people benefit repeatedly, whether newcomers understand the process, or whether the improvement continues after outside attention disappears.",
            f"The claim that {second} provides a second piece of evidence. It shows that design affects behaviour rather than merely presenting an opportunity. At the same time, {third}. Together, these points challenge the assumption that users are passive. People interpret a system, learn from it, and sometimes change it through the way they participate.",
            f"Consider {example}. Its organisers did not treat every positive comment as proof of success. They compared what people said with what they actually did, then looked for moments of confusion. This method exposed overlooked details and helped separate a real pattern from a temporary reaction.",
            f"The argument also has a boundary: {limitation}. Recognising this does not cancel the earlier benefits; it prevents them from being exaggerated. The proposed response is to {action}, so that improvement can be judged in a specific setting before anyone recommends a much larger scheme.",
            f"The strongest conclusion is therefore neither complete enthusiasm nor rejection. Work connected with {topic} benefits from curiosity, but also from careful testing. When supporters describe both achievements and weaknesses, other communities can decide what is relevant to them instead of copying a polished story with missing information.",
        ]
        vocab = ("overlooked", "not noticed or considered", ["deliberately advertised", "carefully measured", "impossible to change"], 4)
    elif style == 3:  # problem-solution progression
        paragraphs = [
            f"The discussion around {subject} usually starts with a problem in {topic}. Existing arrangements may waste time, space, or resources, while a promising alternative seems available. {title} examines what happens after that alternative is introduced. Solving the first problem is important, but it can reveal new questions about access, responsibility, and maintenance.",
            f"One part of the solution is that {first}. This gives the project a clear purpose and allows users to notice a direct improvement. If that purpose becomes vague, people may participate once without understanding why the activity should continue. A good starting point must therefore be simple enough to explain in a few sentences.",
            f"Operation is the next challenge. The fact that {second} can make the system more practical, but only when the arrangement is applied consistently. Users need to know what is expected, whom to contact, and how changes will be announced. These details turn an appealing idea into a usable service.",
            f"A third benefit reaches beyond the original problem: {third}. The example of {example} shows how this can happen through ordinary participation rather than a separate educational campaign. People gain information while pursuing their own goals, and their questions help organisers identify parts of the design that remain unclear.",
            f"Yet the solution has a constraint because {limitation}. Pretending otherwise may lead to rapid growth followed by frustration. The recommendation is to {action}. This measured step leaves room for evidence to guide the next decision instead of forcing every location to follow the same timetable.",
            f"Seen this way, {subject} are not a final answer but a tool that can be refined. Their value depends on matching the response to the local problem, communicating the procedure, and noticing unexpected effects. A realistic project does not promise to remove every difficulty; it makes the remaining difficulties easier to identify and address.",
        ]
        vocab = ("constraint", "a condition that limits what is possible", ["a reward offered to users", "a result nobody expected", "a method of public advertising"], 5)
    elif style == 4:  # observation report
        paragraphs = [
            f"An observation of {example} offers useful evidence about {subject}. Instead of asking only how many people appeared, the observers followed the project through several ordinary stages. They noted why users arrived, where they paused, what they asked, and whether they returned. This method produced a richer picture than a single total.",
            f"The first pattern supported the idea that {first}. People recognised this benefit quickly and often mentioned it when explaining their interest. The observation also showed, however, that awareness did not always lead to continued use. Some participants left when the next step was uncertain or required information they did not have.",
            f"A second pattern concerned the fact that {second}. Small organisational choices affected whether the experience felt manageable. Clear guidance reduced repeated errors, while inconsistent messages created extra work for both users and organisers. The quality of the process was therefore visible in behaviour, not only in survey answers.",
            f"The observers also recorded signs that {third}. These signs were scattered across conversations and repeated visits, so they would have been missed by a narrow measurement. The report describes this outcome as significant because it connected individual use with wider knowledge or social contact.",
            f"The findings remain provisional. Since {limitation}, the same outcome cannot be assumed in every setting. The report recommends that organisers {action} and then compare the result with the earlier pattern. A follow-up of this kind can show whether a change is useful or merely creates a different problem.",
            f"Overall, the observation supports {subject} without presenting them as a universal answer. It demonstrates why evidence should include actions, questions, and difficulties as well as simple numbers. This balanced record gives future organisers something practical to work with while keeping uncertainty visible.",
        ]
        vocab = ("provisional", "not yet final or certain", ["accepted without any evidence", "too expensive to continue", "designed only for experts"], 5)
    elif style == 5:  # weak-versus-strong comparison
        paragraphs = [
            f"Two projects can use the label {subject} and still produce very different experiences. One may focus on appearance and quick growth; the other may begin on a smaller scale and pay close attention to daily use. The contrast helps explain why {title.lower()} is less about a fashionable idea than about the system built around it.",
            f"Both versions may achieve the basic result that {first}. In the weaker version, this early success becomes the only measure and later problems are treated as complaints. In the stronger version, the same benefit is viewed as a starting point. Organisers ask who can reach it, who cannot, and what makes participation continue.",
            f"The difference becomes clearer when we consider how {second}. A dependable project makes the relevant process visible and predictable. By contrast, a poorly organised one expects each person to discover the rules alone. Confusion then looks like a failure by users even when the design caused it.",
            f"The stronger approach also makes room for the fact that {third}. At {example}, shared experience produced information that no organiser could have prepared in advance. Participants did more than receive a service: their behaviour revealed which details mattered in practice.",
            f"Neither version can escape the reality that {limitation}. The difference lies in the response. Choosing to {action} acknowledges the limit and creates a manageable next step. Ignoring it may make the project seem ambitious, but the result is less likely to endure.",
            f"This comparison suggests a useful test for projects connected with {topic}. Ask whether the design learns from people or merely counts them. A durable system keeps its purpose clear while changing the parts that create unnecessary difficulty. Size alone cannot provide that balance.",
        ]
        vocab = ("endure", "continue to exist successfully", ["attract attention immediately", "cost less than expected", "remain completely unchanged"], 5)
    elif style == 6:  # development over time
        paragraphs = [
            f"Ideas involving {subject} often pass through three stages. At first, attention centres on what is new. Later, everyday problems test the original plan. Finally, organisers must decide which parts deserve to become permanent. The development of {title.lower()} can be understood through this movement from enthusiasm to experience and then revision.",
            f"During the opening stage, the strongest argument is that {first}. It gives people an immediate reason to support the proposal. Early success can also attract partners or volunteers, although it may encourage organisers to expand before they understand how the service behaves on an ordinary day.",
            f"The second stage reveals why {second}. Procedures that appeared unimportant during a small trial become essential as more people arrive. Meanwhile, {third}. This effect may not have been part of the original goal, but it can become one of the most valuable reasons to continue.",
            f"At {example}, the transition between these stages was not smooth. Questions that seemed isolated began to form a pattern. Once organisers compared experiences rather than handling each problem separately, they could distinguish a weakness in communication from a weakness in the idea itself.",
            f"The final decision has to consider that {limitation}. One practical option is to {action}. This choice may look modest, yet it protects the project from a premature commitment that would be difficult to reverse.",
            f"Development of {subject} does not end when a project becomes permanent. Conditions change, new users arrive, and old instructions may lose their relevance. The mature approach is therefore adaptive: it preserves the main benefit while continuing to review evidence and explain limitations openly.",
        ]
        vocab = ("premature", "happening before the proper time", ["based on long experience", "unlikely to affect anyone", "carefully explained to the public"], 5)
    else:  # individual experience widening into a system view
        paragraphs = [
            f"For an individual, {subject} may be experienced as one simple moment: a need appears, a person uses the service, and a result follows. From the organiser's position, however, each moment belongs to a larger network of decisions. {title} moves between these two viewpoints to show why both are necessary.",
            f"From the user's side, the main advantage is easy to state: {first}. Immediate usefulness matters because people rarely study the full structure before deciding whether to participate. Their first experience shapes what they expect and what they tell others.",
            f"Behind that experience lies the way that {second}. Organisers must make this process steady without creating rules that are harder than the problem they solve. The best procedures remain noticeable when guidance is needed and almost invisible when everything is working well.",
            f"Individual actions can also combine into a collective effect because {third}. {example.capitalize()} illustrates this widening view. What began as separate choices gradually produced shared information, new habits, or a stronger sense of responsibility among participants.",
            f"The system still faces a trade-off: {limitation}. A sensible response is to {action}, even if that means rejecting a faster or more impressive change. The purpose is not to avoid risk completely but to keep the consequences visible and manageable.",
            f"Neither viewpoint is sufficient alone. User stories show where value is felt, while system evidence reveals who is missing and what must be maintained. Combining them gives a more complete judgement of {subject} and prevents a few positive experiences from standing in for the whole picture.",
        ]
        vocab = ("trade-off", "a balance in which one benefit requires accepting a disadvantage", ["a rule with no practical purpose", "a result shared equally by everyone", "an error that can never be corrected"], 5)

    extensions = (
        f"This way of reading the case also changes what counts as success. A high number on one day may look impressive, but it cannot show whether {first} continues or whether {limitation} has become more serious. Organisers need evidence from quiet periods as well as busy ones. They should also ask whether the people who stop using {subject} faced the same obstacle. Such questions do not make the project unnecessarily complicated. They protect it from decisions based on the easiest information to collect and make the next adjustment easier to explain.",
        f"Responsibility is another part of the answer. Users can contribute observations, yet they should not be expected to repair every weakness themselves. Organisers must decide who checks the system, who responds when {limitation}, and how that response will be communicated. Without this division of work, even people who support {subject} may become uncertain. A modest but clearly managed service can therefore create more confidence than a larger one whose procedures remain unclear. The difference becomes visible only after the first period of enthusiasm.",
        f"Language can strengthen or weaken the false belief as well. Calling {subject} a complete solution hides the choices and labour behind them. Describing the project as a testable response is more accurate. It invites people to examine whether {first}, whether {second}, and what happens when {limitation}. This wording may sound less exciting, but it allows criticism to improve the design instead of appearing to attack the whole idea. Honest description is therefore part of the evidence, not merely a public-relations decision.",
        f"The order of the response matters. Trying to solve every difficulty at once makes it hard to discover which change caused a result. A limited step such as the proposal to {action} creates a clearer comparison. Organisers can record the situation before the change, observe what happens afterwards, and ask users about any new obstacle. If the benefit that {first} becomes stronger without increasing confusion, the next stage has some support. If not, the design can be revised before resources are committed on a much larger scale.",
        f"The observation also has to include people whose experience differs from the majority. A process may look smooth because confident users complete it without asking for help, while others leave silently. Watching only successful participation would therefore produce a misleading result. Notes about unclear instructions, abandoned attempts, or repeated requests can reveal where access breaks down. In relation to {subject}, these details help explain not only whether the project functions but for whom it functions. That distinction is essential before the findings are used elsewhere.",
        f"A comparison should also consider time. The weaker version may initially move faster because it postpones maintenance, training, or explanation. The stronger one invests effort before a visible problem appears. Over several months, those positions can reverse: repeated confusion slows the first project, while familiar routines make the second easier to operate. This is why the fact that {second} should not be treated as a minor detail. It shapes the cost and effort of future participation even when both projects look similar on opening day.",
        f"Each stage produces a different kind of question. During the trial, organisers ask whether people recognise the benefit. During regular operation, they ask whether responsibilities remain manageable. Before expansion, they ask how {limitation} could affect a larger group. Answers collected at one stage cannot automatically settle the next. A useful review keeps the stages separate and records why a decision was made. Later teams can then understand which conditions supported the result rather than seeing only the final version of {subject}. This history also prevents an old solution from being repeated after local conditions have changed.",
        f"Feedback connects the personal and organisational views. A comment such as 'this was difficult' is useful but incomplete until someone identifies the step, condition, or instruction involved. Organisers can invite more precise reports without demanding long forms from every user. Patterns across several short comments may point to the same barrier. At the same time, direct observation can test whether the barrier appears in practice. Combining these sources makes decisions about {subject} more grounded and reduces the risk of treating the loudest opinion as the experience of everyone. It also lets quiet users influence the design without requiring them to attend a formal meeting.",
    )
    paragraphs.insert(-1, extensions[style])
    lexical_cycle = (index - 1) // 8
    paragraphs = [_lexical_cycle(paragraph, lexical_cycle) for paragraph in paragraphs]
    return paragraphs, vocab


def _reading_pack(index: int, spec: tuple[str, ...]) -> dict[str, Any]:
    title, topic, subject, first, second, third, example, limitation, action = spec
    paragraphs, (word, meaning, vocab_distractors, vocab_paragraph) = _reading_paragraphs(index, spec)
    paragraphs.insert(-1, READING_TOPIC_PARAGRAPHS[index - 1])
    main_stems = (
        f"What is the main purpose of the passage about {subject}?",
        f"Which option best summarises the writer's discussion of {subject}?",
        f"What does the writer mainly aim to show through {title.lower()}?",
        f"Which statement expresses the central idea of the passage?",
    )
    questions = [
        _choice_question(main_stems[index % len(main_stems)], f"The value of {subject} depends on benefits, organisation, and honest limits", [f"Every place should copy one fixed model of {subject}", f"The disadvantages of {subject} always outweigh their benefits", f"Only specialists can understand or use {subject}"], "The text balances practical benefits with organisation, evidence, and limitations.", rotation=index, qtype="main_idea"),
        _choice_question(f"Which direct benefit of {subject} is identified in the passage?", first.capitalize(), [second.capitalize(), limitation.capitalize(), "A guarantee that every local problem will disappear"], f"The passage directly states that {first}.", rotation=index + 1, qtype="detail"),
        _choice_question(f"What does the passage say about the role of organisation in {subject}?", second.capitalize(), ["Rules should change whenever a new user arrives", "Publicity can replace a dependable process", "Organisation matters only after a project has failed"], f"The text identifies the fact that {second}.", rotation=index + 2, qtype="detail"),
        _choice_question(f"Why does the writer mention {example}?", "To illustrate how the main ideas appear in a practical setting", ["To prove that the same design will succeed everywhere", "To introduce a historical event unrelated to the topic", "To show that observation is less useful than publicity"], "The example turns the general argument into an observable situation.", rotation=index + 3, qtype="example"),
        _choice_question(f"The word '{word}' in paragraph {vocab_paragraph} is closest in meaning to _____.", meaning, vocab_distractors, f"In this context, {word} means {meaning}.", rotation=index + 4, qtype="vocabulary"),
        _choice_question(f"What can be inferred from the writer's recommendation to {action}?", "Improvement should respond to evidence from the actual setting", ["A larger project is always more reliable", "Limitations should be hidden until participation rises", "The first version of a project should never be changed"], "The recommendation is presented as a measured response to evidence and local limits.", rotation=index + 5, qtype="inference"),
    ]
    question_orders = (
        (1, 2, 3, 4, 5, 0), (0, 3, 1, 4, 2, 5), (3, 1, 2, 5, 4, 0), (2, 1, 4, 3, 5, 0),
    )
    ordered_questions = [questions[position] for position in question_orders[(index - 1) % len(question_orders)]]
    return {
        "id": f"catalog-reading-standard-{index:02d}", "kind": "reading_standard", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True,
        "instructions": "Read the passage and choose the best answer according to the text.", "content": {"paragraphs": paragraphs},
        "questions": ordered_questions,
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
    facts = [a + ".", b + ".", c + ".", d + "."]
    option_orders = (
        (2, 4, 0, 3, 1), (1, 3, 4, 0, 2), (4, 0, 3, 1, 2), (3, 2, 1, 4, 0),
        (0, 4, 2, 1, 3), (2, 1, 3, 0, 4), (1, 0, 4, 2, 3), (4, 3, 0, 2, 1),
    )
    pool = [*facts, extra + "."]
    cycle = (index - 1) // len(option_orders)
    option_order = option_orders[(index - 1) % len(option_orders)]
    option_order = option_order[cycle:] + option_order[:cycle]
    options = {letter: pool[position] for letter, position in zip(("A", "B", "C", "D", "E"), option_order, strict=True)}
    answer_for_fact = {position: next(letter for letter, text in options.items() if text == pool[position]) for position in range(4)}

    role_orders = (
        (0, 1, 2, 3), (0, 2, 1, 3), (1, 0, 3, 2), (0, 3, 2, 1),
        (2, 0, 1, 3), (0, 1, 3, 2), (3, 0, 2, 1), (1, 2, 0, 3),
    )
    role_order = role_orders[(index - 1) % len(role_orders)]
    style = (index - 1) % 8

    contexts = (
        (
            (f"{title} began as a response to an ordinary need connected with {topic}. The organisers wanted the purpose to be visible from the first visit. [[gap]] This immediate function gave residents a reason to try the idea, although it did not answer every question about long-term operation.", f"The opening paragraph defines what attracts users."),
            (f"Once the first visitors arrived, attention moved from the idea to its daily routine. A shared service can lose trust quickly if nobody knows who is responsible. [[gap]] The procedure made each use safer and gave the next person a more predictable experience.", f"The paragraph moves from responsibility to a dependable operating procedure."),
            (f"The project created an opportunity for learning as well as practical use. New participants watched how more experienced people behaved and asked short questions. [[gap]] In this way, knowledge about {topic} travelled through participation rather than through a formal lesson.", f"The missing sentence identifies the educational benefit developed afterwards."),
            (f"After several months, the organisers looked beyond attendance figures. They compared repeated requests, common mistakes, and changes in demand. [[gap]] This wider evidence helped them decide what to keep, what to explain again, and what not to expand.", f"The paragraph requires the result revealed by records of ordinary use."),
        ),
        (
            (f"People first noticed {title} because it offered a concrete answer to a local problem. [[gap]] Without that clear benefit, the project would have been only an attractive display. With it, users could immediately connect the new idea to their own lives.", f"The missing sentence supplies the project's concrete first benefit."),
            (f"Popularity brought a less exciting challenge: the system had to work consistently on quiet days as well as busy ones. Organisers divided tasks and made the sequence visible. [[gap]] As a result, small faults were discovered before they became reasons for people to stop taking part.", f"The sentence describes the routine that supports consistent operation."),
            (f"Not every outcome could be counted. Some appeared in the way experienced users spoke to newcomers or explained a choice. [[gap]] That exchange gave the project an educational value which had not been part of the original publicity.", f"The gap needs the fact about learning or shared understanding."),
            (f"Meanwhile, everyday use produced information for future decisions. A record of what happened was more useful than a general claim that the idea was popular. [[gap]] Organisers could then change the design according to an observed pattern rather than one loud opinion.", f"The paragraph develops the evidence produced over time."),
        ),
        (
            (f"Before {title} existed, people dealt with the same need separately. This often required more effort and made useful resources harder to notice. [[gap]] The project therefore joined individual choices into a service with a recognisable public purpose.", f"The opening contrast calls for the sentence explaining the immediate function."),
            (f"Bringing many users together also created responsibility. An unclear handover could affect someone who arrived much later. [[gap]] This practice connected one person's action with the quality of the next person's experience.", f"The surrounding sentences focus on a specific responsibility or checking routine."),
            (f"Participation gradually changed what people knew about {topic}. Advice no longer remained with a small group of experts. [[gap]] Even brief contact could help a newcomer make a better decision on a later visit.", f"The sentence must explain how knowledge or awareness is shared."),
            (f"The accumulated experience had another use. Instead of guessing which part deserved investment, the organisers studied actual behaviour. [[gap]] The finding turned scattered actions into guidance for the next version of the project.", f"The missing idea is the broader information created by use."),
        ),
        (
            (f"A visitor may understand {title} through a single action, but the scheme has a wider aim related to {topic}. [[gap]] That result is the doorway into the project: it explains why someone would participate before learning about the system behind it.", f"The first gap needs the user-facing purpose."),
            (f"Behind the simple action is a chain of small decisions. Equipment, information, or responsibility must pass from one stage to another without becoming uncertain. [[gap]] The rule is valuable because it protects the whole chain, not because organisers enjoy adding restrictions.", f"The paragraph needs the operational rule that protects continued use."),
            (f"Repeated participation can then alter understanding. People see examples, compare methods, and discuss mistakes in a practical setting. [[gap]] The learning is informal, but it may influence behaviour outside the project as well.", f"The gap develops the informal learning described on both sides."),
            (f"From the organiser's viewpoint, these separate experiences form a pattern. Questions and choices reveal which parts of the service are working. [[gap]] Such evidence gives future planning a stronger basis than enthusiasm alone.", f"The missing sentence states what the pattern of use reveals."),
        ),
        (
            (f"Supporters of {title} sometimes begin with a broad promise about {topic}. A better explanation starts with the exact service people receive. [[gap]] Stating this clearly makes the project easier to judge and prevents expectations from growing beyond its real purpose.", f"The missing sentence gives the exact, limited benefit offered to users."),
            (f"A useful idea still requires maintenance. When several people participate, yesterday's small uncertainty can become tomorrow's repeated problem. [[gap]] The routine distributes responsibility and makes changes easier to trace.", f"The gap must contain the maintenance or checking arrangement."),
            (f"There is also a human effect that formal descriptions often miss. Participants bring different experience and notice one another's solutions. [[gap]] The service consequently becomes a place where practical knowledge is exchanged.", f"The paragraph points directly to a learning or community outcome."),
            (f"Good records keep this social experience from remaining anecdotal. Organisers can examine which needs appear frequently and which are rare. [[gap]] They can use that information to resist unnecessary expansion as well as to support a useful change.", f"The missing sentence describes information obtained from participation."),
        ),
        (
            (f"Imagine encountering {title} for the first time. The name may be interesting, but a user still needs to know what problem it solves. [[gap]] Once this purpose is understood, the remaining instructions have a reason rather than feeling like unrelated rules.", f"The sentence answers the first-time user's question about purpose."),
            (f"The next visit tests whether the project is dependable. People should not have to invent a different method each time they use a shared resource. [[gap]] Consistency reduces doubt and allows attention to remain on the activity itself.", f"The missing fact is the repeated procedure that creates consistency."),
            (f"A further effect appears when users meet or observe one another. Someone who came only for a practical result may leave with a new idea. [[gap]] This additional value can continue even when the original task is complete.", f"The gap requires the sentence about knowledge, confidence, or social exchange."),
            (f"Finally, organisers need to learn from the service instead of merely keeping it open. They collect signs of demand and recurring difficulty. [[gap]] The evidence can guide a careful adjustment and show whether the original aim still fits local needs.", f"The final gap needs the result that accumulated use makes visible."),
        ),
        (
            (f"The future of {title} can be discussed only after its present function is clear. [[gap]] This basic contribution explains why the idea deserves attention in debates about {topic}. It is a starting claim, not proof that every version will succeed.", f"The paragraph asks for the project's present practical contribution."),
            (f"Success also depends on what happens between one user and the next. A gap in responsibility may remain invisible until it causes harm or confusion. [[gap]] By making that step regular, organisers protect both trust and resources.", f"The missing sentence names the procedure between uses."),
            (f"The project can influence people in ways that appear later. Participants may carry a method, fact, or question into another setting. [[gap]] This is why an evaluation should consider learning and social behaviour, not just completed transactions.", f"The gap needs the wider learning effect."),
            (f"Long-term planning requires another kind of evidence. Patterns across many ordinary decisions show where the service is most valuable. [[gap]] The same evidence may also reveal that one popular feature receives more attention than a quieter but important need.", f"The sentence describes the knowledge created from recorded use."),
        ),
        (
            (f"When a new scheme connected with {topic} is introduced, people often ask whether it is worth their time. {title} gives a direct answer. [[gap]] This outcome is visible enough to attract interest without requiring users to understand every organisational detail first.", f"The missing sentence is the visible outcome that attracts participation."),
            (f"The organisational details become important soon afterwards. A project shared by many people cannot depend on memory or goodwill alone. [[gap]] The agreed practice reduces avoidable disagreement and gives organisers a clear point at which to check the system.", f"The gap requires the specific agreed practice or safeguard."),
            (f"Use also creates contact with unfamiliar experience. People notice how others approach the same need and may explain their choices. [[gap]] The result is a modest form of public learning rooted in action.", f"The missing sentence develops the exchange of knowledge."),
            (f"Those actions leave useful traces. Over time, they show demand, repeated obstacles, or changes in behaviour. [[gap]] Instead of relying on an early impression, the organisers can base the next decision on this record.", f"The sentence must state what the traces reveal."),
        ),
    )

    paragraphs = []
    rationales = []
    context_style = (style + cycle * 3) % len(contexts)
    for gap, role in enumerate(role_order, start=1):
        paragraph, rationale = contexts[context_style][role]
        paragraph = paragraph.replace("[[gap]]", f"[[{gap}]]")
        if title not in paragraph and topic not in paragraph:
            role_closers = (
                f"This is the part that gives {title} its immediate purpose.",
                f"Here it protects the daily operation of {title}.",
                f"For {title}, the effect extends beyond a single task.",
                f"This lets the team judge the future of {title}.",
            )
            paragraph += " " + role_closers[role]
        paragraphs.append(_lexical_cycle(paragraph, cycle))
        rationales.append(rationale)
    conclusions = (
        f"The experience of {title} shows why projects linked to {topic} need both a clear purpose and patient organisation. Not every difficulty can be removed, but limits should be explained rather than hidden. A modest service that learns from use is more valuable than a large promise that cannot be maintained.",
        f"No single feature guarantees the future of {title}. Direct usefulness brings people in, routines protect trust, shared experience creates learning, and records support revision. Keeping these functions distinct allows organisers to see which part needs attention when circumstances connected with {topic} change.",
        f"The project is therefore best understood as an adjustable system, not a finished object. Its value comes from the relationship between individual action and collective evidence. If organisers remain honest about capacity, {title} can improve without losing sight of the local need that produced it.",
        f"This layered view prevents two opposite mistakes: rejecting {title} after one problem or treating early popularity as complete proof. Both reactions ignore how services develop. Careful observation gives communities a stronger basis for deciding what role the project should play in {topic}.",
    )
    paragraphs.append(conclusions[(index - 1) % len(conclusions)])

    questions = []
    for gap, role in enumerate(role_order, start=1):
        answer = answer_for_fact[role]
        questions.append({"stem": f"Which sentence best fits gap {gap}?", "options": options, "answer": answer, "points": 2, "qtype": "sentence_insertion", "rationale": rationales[gap - 1]})
    return {"id": f"catalog-reading-insertion-{index:02d}", "kind": "reading_insertion", "title": title, "topic": topic, "cefr": "B1+", "source": "seed", "published": True, "instructions": "Complete gaps 1-4 with the most suitable sentences A-E. There is one extra sentence.", "content": {"paragraphs": paragraphs, "sentence_options": options}, "questions": questions}


CLOZE_TOPICS = [
    "planning a weekly study schedule", "keeping a shared kitchen clean", "preparing for a short presentation", "using a campus bicycle safely", "starting a reading habit", "joining a student society", "reducing phone distractions", "cooking with seasonal vegetables", "organising digital notes", "walking to university", "learning from written feedback", "caring for indoor plants", "sharing tasks in a group", "visiting a museum effectively", "building an emergency kit", "using a reusable water bottle", "preparing for a job interview", "taking useful lecture notes", "protecting personal data", "volunteering at a local event", "choosing a quiet study place", "creating a realistic morning routine",
]


CLOZE_CONTEXTS = [
    ("A Week That Fits on Paper", "When every deadline feels urgent, students often react to the nearest task and forget the rest of the week. A realistic schedule creates distance from that pressure. It shows where study time is actually available and prevents one demanding course from silently taking over every evening.", "The schedule should still leave room for delay, rest, and unexpected work. Reviewing it on Sunday evening is more useful than following a plan that no longer matches reality."),
    ("Sharing a Kitchen", "A shared kitchen can become tense even when nobody intends to be inconsiderate. Different ideas about cleanliness are usually part of the problem: one person washes a pan immediately, while another thinks that doing it later is perfectly acceptable. Specific agreements are easier to follow than general requests to be tidy.", "A fair system should distribute unpleasant jobs as well as quick ones. If the arrangement stops working, housemates can change the routine without turning one forgotten task into a judgement about someone's character."),
    ("Turning Notes into a Short Presentation", "A short presentation is difficult for a surprising reason: the speaker has little time to decide what the audience truly needs. Trying to include every fact makes the main point harder to recognise. A clear opening, two or three supporting ideas, and a brief conclusion usually communicate more than a crowded set of slides.", "Rehearsing aloud reveals sentences that look fine on paper but are hard to say naturally. It also allows the speaker to adjust the amount of information before facing the audience."),
    ("A Safer Ride Across Campus", "Campus bicycles are convenient for journeys between distant buildings, yet familiarity can make riders careless. A route that appears safe in daylight may contain poor lighting, heavy traffic, or wet surfaces later in the day. Basic checks and a suitable route reduce risks before the bicycle begins to move.", "Safety also depends on predictable behaviour around pedestrians. Slowing down near entrances and signalling a turn give other people time to respond, which matters more than arriving one minute earlier."),
    ("Making Reading an Ordinary Habit", "Many people buy a book with genuine enthusiasm and then wait for a long, quiet evening that never arrives. Reading becomes more regular when it is attached to a situation that already happens each day. Ten minutes after breakfast can be easier to protect than an ambitious promise to finish several chapters at night.", "Progress should be measured by returning to the book, not by reading at the same speed every day. A difficult chapter may require patience, while an engaging one may naturally lead to a longer session."),
    ("Finding a Place in a Student Society", "Joining a student society can make a large university feel smaller, but the first meeting is not always comfortable. Existing members may already know one another and use terms that a newcomer has never heard. Asking about one current activity is often an easier entrance than trying to speak to the whole room.", "Regular participation matters more than making a perfect first impression. Taking responsibility for one manageable task gives other members a clear reason to contact the newcomer again."),
    ("Putting the Phone Outside the Task", "Phone distractions are not caused only by weak self-control. Notifications, bright icons, and the possibility of a new message repeatedly invite the mind to change direction. Even a quick check can leave part of a person's attention on the conversation that has just appeared.", "A useful strategy changes the environment before concentration is required. Moving the phone out of reach or allowing calls from selected contacts reduces interruption without pretending that the device can be ignored in every situation."),
    ("Cooking with What the Season Offers", "Seasonal vegetables are often fresher and less expensive, but unfamiliar produce can be difficult to use. Instead of searching for a complicated recipe, a cook can begin with a familiar method such as roasting, soup, or a simple pan dish. One new ingredient is easier to understand when the rest of the meal is predictable.", "Taste and texture vary from one harvest to another, so exact cooking times may need adjustment. Paying attention to the food is more reliable than following a number without checking the result."),
    ("Notes That Can Be Found Again", "Digital notes solve the problem of carrying paper, but they can create a different problem when files have unclear names and live in several applications. The value of a note depends on whether it can be found at the moment it is needed. A small system for titles, dates, and subjects improves later searching.", "Organisation should not take longer than the studying itself. A simple pattern used consistently is usually more effective than an impressive structure that requires constant maintenance."),
    ("Walking the Useful Part of the Journey", "Walking to university may sound unrealistic when the entire route is long. However, the choice is not always between walking every kilometre and taking transport from door to door. Students can walk one safe section and use a bus or train for the rest.", "Comfortable shoes, weather, and the time of the first class all affect whether the plan remains practical. The best routine is one that can survive an ordinary busy morning, not only a perfect day."),
    ("Reading Feedback Without Defending Every Sentence", "Written feedback can feel personal because it appears beside work that required time and effort. Yet comments are most useful when the learner separates the quality of the current draft from their ability as a whole. Looking for repeated issues often reveals a clearer priority than correcting every mark immediately.", "After revising, the learner can compare the two versions and write one rule in their own words. This turns feedback into a tool that can influence the next task rather than a list that disappears with the grade."),
    ("What an Indoor Plant Is Telling You", "Indoor plants rarely fail because their owners do not care. More often, people respond to a yellow leaf by adding water, although too much water may be the original problem. Light, drainage, temperature, and season should be considered together before changing the routine.", "Keeping a brief record of watering can prevent guesses based on memory. A plant that grows slowly may still be healthy, so new leaves and firm stems are often better signs than rapid growth alone."),
    ("Dividing Group Work", "Group members sometimes divide a project by giving each person an equal number of tasks. Equal numbers do not always mean equal effort, especially when one task depends on research completed by someone else. The group needs to discuss sequence, difficulty, and responsibility together.", "Short progress checks can expose a delay while there is still time to respond. They should help the group reorganise work, not become meetings in which everyone simply says that everything is fine."),
    ("A Museum Visit with a Question", "Walking through every room of a museum does not guarantee a meaningful visit. Large collections quickly become tiring when each object receives the same amount of attention. Choosing one question before entering gives the visitor a reason to compare particular objects and read selected labels carefully.", "Photographs can support memory, but only when the museum permits them and the visitor also spends time looking directly. A few written observations may preserve more understanding than dozens of unexamined images."),
    ("An Emergency Kit for Likely Problems", "An emergency kit should respond to the risks of its location rather than copy an endless list from the internet. A student residence, a family car, and a rural home may require different supplies. Water, light, basic first aid, and essential contact information provide a sensible foundation.", "Items with expiry dates need occasional checking, and everyone in the household should know where the kit is stored. Equipment cannot help during an emergency if it is hidden behind objects nobody can move quickly."),
    ("Using a Reusable Bottle", "Buying a reusable bottle feels like an environmental action, but the benefit develops through repeated use. If the bottle is inconvenient to carry, difficult to clean, or too small for the day, it may remain at home while disposable bottles continue to be purchased.", "Choosing a practical design and creating a washing routine matter more than owning the most fashionable model. Refill points along a normal route make the new habit easier to maintain."),
    ("Preparing Evidence for a Job Interview", "Job interviews ask candidates to describe qualities such as teamwork or responsibility, but general claims are rarely convincing. A short example from study, volunteering, or part-time work gives the interviewer something concrete to evaluate. The example should explain the situation, the action taken, and the result.", "Preparation is not the same as memorising a speech. Candidates need enough structure to answer clearly while remaining able to respond to the exact wording of the question."),
    ("Lecture Notes That Record Relationships", "Students who try to write every word of a lecture often miss the connection between ideas. Useful notes select claims, examples, contrasts, and causes. Space on the page can show these relationships before the student has time to write a full sentence.", "Soon after class, unclear abbreviations should be completed while the explanation is still familiar. This short review makes later study faster and reveals any gap that requires another source."),
    ("Small Decisions That Protect Personal Data", "Personal data is often lost through ordinary actions rather than highly technical attacks. Reusing a password, opening an unexpected attachment, or approving a login request without reading it can give another person access. A few repeatable checks reduce this risk considerably.", "Security advice must remain practical or people will ignore it. Password managers, software updates, and a second login step provide stronger protection without requiring users to become computer experts."),
    ("Being Useful at a Local Event", "Volunteers sometimes arrive at an event expecting to choose an exciting role, while organisers urgently need help with simple tasks. Asking where the greatest need is can be more valuable than waiting for the perfect assignment. Clear instructions protect both visitors and the volunteer.", "At the end of the event, a brief handover prevents unfinished work from being forgotten. Volunteers should also report problems honestly so that the next event can be organised more effectively."),
    ("Choosing a Quiet Place", "A quiet study place is not automatically an effective one. A room may have no conversation but still contain uncomfortable seating, poor light, or constant movement near the door. The right environment depends on the task and on the kind of distraction a particular student finds difficult.", "Testing two locations with the same short task can produce better evidence than relying on preference alone. The aim is not perfect silence but a place where attention can return quickly after a minor interruption."),
    ("A Morning Routine That Survives Monday", "An ideal morning routine often contains exercise, reading, a careful breakfast, and several other goals. Such a plan may work once and then collapse on the first difficult day. A realistic routine protects the few actions that have the greatest effect on the rest of the morning.", "Preparing one item the night before can remove an early decision. The routine can grow later, but it should first become reliable enough to continue when motivation is low."),
]


CLOZE_VARIANT_BY_TOPIC = (0, 3, 4, 4, 5, 7, 0, 4, 1, 5, 2, 0, 3, 4, 1, 5, 4, 2, 1, 7, 6, 0)

CLOZE_BODIES = (
    "The first version should be tested [[1]] the student has an ordinary week, not during a holiday. Students [[2]] fill every free hour may discover that the plan leaves no space for travel or rest. At the weekend, completed tasks and missed tasks should [[3]] together. A missed session can be moved [[4]] treating the whole week as a failure. The next plan will be easier to begin if books and notes [[5]] in advance.",
    "Housemates should first discuss [[1]] everyone means the same thing by 'clean'. A person [[2]] standard is different may not realise that others are annoyed. If the group [[3]] on a few clear rules when they moved in, several later arguments might have been prevented. [[4]] having busy schedules, everyone can complete one regular job. The agreement can be placed near the fridge [[5]] nobody has to depend on memory.",
    "The speaker should decide on the central message [[1]] choosing pictures or colours. Someone who ignored the time limit may later wish they [[2]] the task instructions more carefully. [[3]] a first rehearsal can feel uncomfortable, it shows whether the talk is too long. The difficult parts can then be practised [[4]]. [[5]], the final presentation may contain good information but still feel rushed.",
    "A rider should inspect the brakes and tyres [[1]] leaving the bicycle station. After an accident, a careless rider may wish they [[2]] the route conditions earlier. [[3]] a helmet cannot prevent every injury, it offers important protection. Near busy buildings, cyclists need to move [[4]] and expect pedestrians to change direction. [[5]], a short and familiar journey can become dangerous very quickly.",
    "Readers may be used [[1]] choosing a book only when they have a free afternoon. [[2]] that perfect moment arrives, several weeks may already have passed. The daily target does not have to [[3]] large. In fact, the first target should not be [[4]] demanding to repeat every day. Ten regular minutes can create steady progress, [[5]] a large weekend target is easy to postpone.",
    "Attending one meeting allows a newcomer to understand the group [[1]] making a long commitment. Some students dislike [[2]] expected to speak immediately in front of everyone. A welcoming introduction has often [[3]] to stronger participation. If committee members [[4]] newcomers' questions after the meeting, they can improve the next event. Students should accept a regular role [[5]] the schedule fits their other responsibilities.",
    "A phone is easier to ignore [[1]] it is placed beyond the user's reach. People [[2]] keep every notification active must repeatedly decide whether to look at the screen. The settings should [[3]] before a demanding task begins. Important contacts can still be allowed through [[4]] opening the door to every alert. Concentration improves when the required documents [[5]] on the computer before the phone is put away.",
    "A cook should check what is already available [[1]] buying several new ingredients. Someone who wasted vegetables may wish they [[2]] storage advice sooner. [[3]] a seasonal product may look unfamiliar, it can often be prepared with a simple method. The heat and cooking time should be adjusted [[4]] after the food is checked. [[5]], a useful ingredient may be rejected merely because the first attempt was unsuccessful.",
    "A naming system needs to be easy enough [[1]] even when a student is in a hurry. Files [[2]] belong to the same course can share a short subject code. Once a document [[3]], its final date should appear in the title. This gives the student a clearer record [[4]] than labels such as 'new' or 'final'. Extra folders should not be created [[5]] they make searching faster.",
    "Students may be used [[1]] taking transport for the entire journey. [[2]] they notice how little they move during the day, the habit may be well established. The whole journey does not have to [[3]] on foot. Starting with one safe section keeps the change from becoming [[4]] tiring. Walking also gives some light exercise, [[5]] taking a bus may still be sensible in bad weather.",
    "Instead of [[1]] every correction as a separate failure, a learner can search for a repeated pattern. A comment [[2]] identifies the reason for an error is more useful than a mark alone. One weak paragraph can [[3]] first and used as a model for the rest. The changes should be made [[4]] the writer can still remember their original purpose. This early review matters [[5]] delayed feedback is easier to misunderstand or forget.",
    "The plant should be moved only [[1]] the owner has considered light, water, and temperature. People [[2]] react to every yellow leaf may change the conditions too often. The watering routine should [[3]] after the soil is checked. One adjustment can then be observed [[4]] several possible causes being mixed together. A useful comparison is possible only if an observation sheet and matching labels [[5]] first.",
    "Before the project begins, the group should decide [[1]] every task has a clear owner. Members [[2]] work depends on earlier research need realistic deadlines. If the team [[3]] on the order of the tasks from the start, one delay would not have surprised everyone. [[4]] having different roles, members still need to share progress. A brief weekly check keeps the plan visible [[5]] problems can be discussed while there is time.",
    "Visitors should choose a purpose [[1]] trying to see the entire collection. Someone who became tired halfway through may wish they [[2]] the museum map at the entrance. [[3]] famous objects attract attention, a less crowded room can offer a calmer experience. A few related displays can be examined [[4]] when the visitor is not rushing. [[5]], the visit may become a race through rooms that nobody remembers clearly.",
    "An emergency list should be simple enough [[1]] under pressure. Supplies [[2]] have an expiry date need regular attention. Once a monthly check [[3]], the next inspection date can be recorded. The kit should contain necessary supplies [[4]] than every product suggested online. Nothing should be added [[5]] someone in the household understands its purpose and use.",
    "People may be used [[1]] buying a drink whenever they leave home. [[2]] they count those purchases, many disposable bottles may already have been used. The first routine must not [[3]] complicated by extra rules. The bottle should not be [[4]] large to fit in an ordinary bag. A practical design can become part of daily life, [[5]] an unsuitable one may remain unused in a cupboard.",
    "Candidates should read the job description [[1]] selecting examples from their experience. A person who gives only general answers may wish they [[2]] two specific situations beforehand. [[3]] prepared examples provide confidence, they should not sound like memorised speeches. Answers can be delivered [[4]] when the candidate listens to the exact question. [[5]], a polished response may fail to show the ability the interviewer asked about.",
    "Instead of [[1]] complete sentences as the only useful form, students can record relationships between key ideas. A symbol [[2]] marks a cause or contrast saves time during a fast explanation. The visibility of important definitions can [[3]] with a box or colour. Notes should be checked [[4]] the lecture is still easy to remember. This review is valuable [[5]] unclear abbreviations may make no sense several days later.",
    "A password manager should be simple enough [[1]] on every important device. Accounts [[2]] contain private information need different passwords. Once a second login step [[3]], unexpected approval requests become a warning sign. The manager stores complex passwords [[4]] than asking the user to remember similar versions. A link in a surprising message should not be opened [[5]] its source has been checked separately.",
    "Volunteers can discover what an event needs [[1]] demanding their preferred role. New helpers may feel uncomfortable about [[2]] given only a routine task, but these jobs are often essential. Clear explanations have [[3]] to better cooperation at many events. If organisers [[4]] concerns during the day, they can correct small problems quickly. A volunteer should change roles only [[5]] another person is ready to take over the first task.",
    "[[1]] complete silence nor a fashionable design guarantees useful study. Possible locations should [[2]] by doing the same short task in each one. A library [[3]] suits careful reading may not suit an online discussion. The student should [[4]] choose according to the work planned for that day. Evidence from direct experience is usually more reliable [[5]] a general review written by someone with different needs.",
    "A morning habit becomes easier [[1]] it begins with one dependable action. People [[2]] try to copy a long routine from social media may run out of time. After several days, the order should [[3]] calmly. A late morning can be managed [[4]] abandoning the most important step. The routine is more likely to survive if clothes, food, or study materials [[5]] the night before.",
)

CLOZE_EXTENSIONS = (
    "A plan with visible free time is often easier to trust than one that fills every hour.",
    "Writing the agreement down can prevent the same discussion from returning every few days.",
    "One final practice without slides checks whether the argument itself is clear enough to follow.",
    "A helmet and working lights remain necessary even when the journey is short and familiar.",
    "Keeping the book in a visible place can make the next reading session easier to begin.",
    "New members can also ask whom to contact when they are unable to attend an activity.",
    "The goal is to make checking deliberate rather than allowing it to interrupt every quiet moment.",
    "Recording a successful combination makes it easier to use the same vegetable confidently next time.",
    "Old files should occasionally be removed so that search results remain useful instead of crowded.",
    "On unsafe or exhausting days, using transport for a larger part of the route is a reasonable adjustment.",
    "A learner does not have to accept every suggestion, but each decision should have a clear reason.",
    "Changing several conditions together makes it difficult to discover what the plant actually needed.",
    "Dependencies between tasks should appear on the plan before individual deadlines are agreed.",
    "Taking a short break can restore attention before the visitor moves to a different section.",
    "A paper copy of key telephone numbers remains helpful if a phone battery has run out.",
    "After several weeks, the environmental benefit depends far more on repetition than on the original purchase.",
    "Preparing one question for the interviewer also shows serious interest in the position and its responsibilities.",
    "Symbols and arrows are valuable only if the student can still understand them during revision. Leaving space beside a main idea also makes later additions easier to place.",
    "Unexpected requests should be confirmed through a separate channel before any private information is shared. A genuine organisation will not object to a careful security check.",
    "Knowing the purpose of a task makes even routine work feel connected to the event as a whole.",
    "Students may use different places for deep reading, discussion, and short administrative tasks.",
    "A consistent starting point matters more than completing a long list in exactly the same order.",
)


CLOZE_VARIANTS = [
    {
        "text": "People often begin {topic} with an ambitious plan. Progress is easier [[1]] the first action is small and clear. Learners [[2]] change everything at once may become tired before results appear. The plan should [[3]] at the end of each week, not after every attempt. A difficult day can then be examined [[4]] the whole routine being abandoned. Success is also more likely when the necessary materials [[5]] before the chosen starting time.",
        "questions": [
            (["unless", "when", "despite", "whereas"], "B", "When introduces the condition that makes progress easier.", "connector"),
            (["which", "whose", "who", "where"], "C", "Who refers to people.", "relative_clause"),
            (["review", "reviewed", "be reviewed", "reviewing"], "C", "Should requires be plus the past participle for this passive meaning.", "modal_passive"),
            (["instead", "rather", "without", "except"], "C", "Without is followed by an -ing form.", "preposition"),
            (["prepare", "prepared", "are prepared", "have preparing"], "C", "The plural subject receives the action, so a passive form is needed.", "passive"),
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
            (["who", "where", "whose", "that"], "D", "That refers to the preceding noun and introduces a defining clause.", "relative_clause"),
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
            (["careful", "more carefully", "most careful", "carefulness"], "B", "An adverb is needed to describe how the action is performed.", "adverb"),
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
    variant = CLOZE_VARIANTS[CLOZE_VARIANT_BY_TOPIC[index - 1]]
    title, introduction, conclusion = CLOZE_CONTEXTS[index - 1]
    text = f"{introduction} {CLOZE_BODIES[index - 1]} {conclusion}"
    if len(text.split()) < 155:
        text += " " + CLOZE_EXTENSIONS[index - 1]
    questions = []
    for gap, (options, answer, rationale, qtype) in enumerate(variant["questions"], start=1):
        correct = options[("A", "B", "C", "D").index(answer)]
        distractors = [option for option in options if option != correct]
        questions.append(_choice_question(f"Gap {gap}", correct, distractors, rationale, rotation=index + gap, qtype=qtype))
    return {
        "id": f"catalog-cloze-{index:02d}", "kind": "cloze", "title": title, "topic": topic,
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
    pattern = index - 1
    selected = [
        styles[(pattern // (4 ** offset) + pattern + offset) % len(styles)][offset]
        for offset in range(5)
    ]
    order_patterns = (
        (0, 1, 2, 3, 4), (2, 0, 4, 1, 3), (1, 3, 0, 4, 2), (4, 2, 1, 3, 0),
        (3, 1, 4, 0, 2), (0, 4, 3, 2, 1),
    )
    selected = [selected[position] for position in order_patterns[(index - 1) % len(order_patterns)]]
    questions = [
        _choice_question(original, correct, distractors, rationale, rotation=index + offset, qtype="restatement")
        for offset, (original, correct, distractors, rationale) in enumerate(selected)
    ]
    title_stems = ("Meaning in Context", "Same Idea, New Structure", "Following the Exact Meaning", "Sentence Equivalence")
    return {"id": f"catalog-restatement-{index:02d}", "kind": "restatement", "title": f"{title_stems[(index - 1) % len(title_stems)]}: {event.title()}", "topic": event.removeprefix("the "), "cefr": "B1+", "source": "seed", "published": True, "instructions": "Choose the option that best restates the meaning of the original sentence.", "content": {"intro": "Read each original sentence carefully. Choose the option with the closest meaning."}, "questions": questions}


SPEAKING_CARD_GROUPS = [
    ("learning", [
        ("Your Study Plan", "Talk about a study plan that works well for you.", ["when you usually study", "how you organise the work", "why this plan is useful"], ["Why do some students find plans difficult to follow?", "Should every student use the same study method?", "How can a student study effectively before an exam?"]),
        ("A Difficult Subject", "Talk about a subject that you find difficult.", ["which subject it is", "what makes it difficult", "how you try to improve"], ["Why are some subjects harder than others?", "How can teachers support struggling students?", "Is difficulty always a reason to avoid a subject?"]),
        ("Exam Week", "Talk about how you prepare for a busy exam week.", ["which tasks you do first", "how you protect your energy", "what you avoid during the week"], ["Do exams show everything a student knows?", "How can universities reduce exam stress?", "Why do some students leave revision until the last day?"]),
        ("Studying Together", "Talk about a time when studying with someone helped you.", ["who you studied with", "what you worked on", "how the other person helped"], ["When is group study more useful than studying alone?", "What can make a study group ineffective?", "Should stronger students help their classmates?"]),
    ]),
    ("campus life", [
        ("A Campus Place", "Talk about a place on campus that you often use.", ["where it is", "what you do there", "why you choose that place"], ["What makes a campus comfortable for students?", "Which campus facilities are most important?", "How could unused campus areas be improved?"]),
        ("A Crowded Campus", "Talk about a crowded area at your university.", ["when it becomes crowded", "which problems it creates", "what could make it better"], ["Why do people dislike crowded places?", "Should universities limit access to busy areas?", "How can students behave responsibly in a crowd?"]),
        ("A Campus Event", "Talk about a university event you would like to attend.", ["what kind of event it is", "who might enjoy it", "what you could learn there"], ["Why are campus events important?", "How can organisers attract more students?", "Should all university events be free?"]),
        ("A New Student", "Talk about how you would help a new student on campus.", ["what you would show them", "which advice you would give", "how you would make them feel welcome"], ["What is difficult about starting university?", "Who should guide new students?", "Do orientation programmes solve every problem?"]),
    ]),
    ("wellbeing", [
        ("A Healthier Day", "Talk about one change that could make your daily life healthier.", ["which habit you would change", "how you would begin", "what benefit you expect"], ["Why are healthy habits difficult to maintain?", "Should universities teach students about wellbeing?", "Can a small change have a lasting effect?"]),
        ("Better Sleep", "Talk about what helps you get enough sleep.", ["what your evening is usually like", "which things disturb your sleep", "what you do the next morning"], ["Why do many young people sleep too little?", "How does poor sleep affect learning?", "Should people stop using phones before bed?"]),
        ("Simple Exercise", "Talk about a form of exercise that suits student life.", ["what the activity is", "where it can be done", "why students might enjoy it"], ["Why do some people avoid exercise?", "Are team sports better than individual activities?", "How can a city encourage people to move more?"]),
        ("A Food Choice", "Talk about a food choice that is important to you.", ["what you usually choose", "what influences your decision", "how the choice affects your day"], ["Why is healthy food sometimes less convenient?", "Should university cafeterias change their menus?", "How much should price influence food choices?"]),
    ]),
    ("technology", [
        ("An App You Use", "Talk about an app that makes one task easier for you.", ["which task it supports", "how often you use it", "what its main weakness is"], ["Do useful apps always save time?", "Why do some apps become popular quickly?", "What information should an app never collect?"]),
        ("Phone-Free Time", "Talk about a situation when you prefer not to use your phone.", ["where you are", "why the phone would be distracting", "how you feel without it"], ["Why is it hard to put a phone away?", "Should phones be allowed in every class?", "Can people relax properly while staying online?"]),
        ("Learning Online", "Talk about a digital tool that can help someone learn.", ["what the tool teaches", "how a learner uses it", "what a teacher still needs to do"], ["Can online tools replace classroom teaching?", "How can learners check online information?", "Why do some people lose motivation in online courses?"]),
        ("An App for Students", "Talk about an app you would design for university students.", ["which problem it would solve", "how students would use it", "what would keep it simple"], ["Which student problems can technology solve?", "What could make the app unsuccessful?", "Should universities develop their own apps?"]),
    ]),
    ("responsibility", [
        ("A Shared Chore", "Talk about a task you share with people at home.", ["what the task involves", "how the work is divided", "what happens when someone forgets"], ["Why should household work be shared?", "Should children have regular responsibilities?", "What is the fairest way to divide unpleasant tasks?"]),
        ("Keeping a Promise", "Talk about a promise that was important to keep.", ["who you made it to", "what you had to do", "why keeping it mattered"], ["Why do people sometimes break promises?", "Are all promises equally important?", "How can trust be repaired after a broken promise?"]),
        ("Unequal Work", "Talk about a time when work was not shared fairly.", ["what the group was doing", "why the division was unfair", "how the group handled it"], ["Why do some people avoid responsibility?", "Should a leader give everyone an exact role?", "How can a group discuss unfairness calmly?"]),
        ("A Responsible Student", "Talk about what it means to be a responsible university student.", ["which duties matter most", "how responsibility affects others", "what students often forget"], ["Does responsibility increase with age?", "Should universities punish every irresponsible action?", "Can a responsible person still make mistakes?"]),
    ]),
    ("travel", [
        ("A Memorable Journey", "Talk about a journey that you remember clearly.", ["where you travelled", "what happened on the way", "why the journey stayed in your mind"], ["Why can travelling change a person's view?", "Is the journey sometimes more valuable than the destination?", "What makes travel stressful?"]),
        ("A Travel Problem", "Talk about a problem you had while travelling.", ["where the problem occurred", "how you reacted", "what you would do differently now"], ["How should travellers prepare for unexpected problems?", "When should a traveller ask local people for help?", "Does technology make travel safer?"]),
        ("A New Place", "Talk about a place you would like to visit for the first time.", ["which destination you have in mind", "what you want to see", "how you would prepare for the visit"], ["Why do people choose unfamiliar destinations?", "Is it better to travel with a plan?", "How can visitors respect local culture?"]),
        ("Better Transport", "Talk about a public transport change your city needs.", ["which route or service should change", "who would benefit", "why the change is practical"], ["Why do some people avoid public transport?", "Should students pay less for transport?", "How can cities reduce traffic without causing new problems?"]),
    ]),
    ("communication", [
        ("Helpful Feedback", "Talk about a comment that helped you improve your work.", ["who gave the comment", "what they suggested", "what you changed afterwards"], ["Why can feedback feel uncomfortable?", "What makes criticism useful?", "Should teachers give feedback in public?"]),
        ("Giving Advice", "Talk about how you would give feedback to a friend.", ["which point you would mention first", "how you would stay respectful", "what help you would offer"], ["Is honesty always the best approach?", "Why do people react differently to advice?", "When is it better to say nothing?"]),
        ("Unfair Criticism", "Talk about a time when criticism seemed unfair.", ["what the criticism was", "how you responded", "what you learned from the situation"], ["How can someone respond without becoming angry?", "Can unfair comments still contain useful information?", "Who should decide whether criticism is fair?"]),
        ("Learning from Errors", "Talk about how feedback can turn a mistake into progress.", ["which mistake could be discussed", "what useful detail feedback adds", "how the next attempt can improve"], ["Why do some people hide their mistakes?", "Should every error be corrected immediately?", "How can a classroom make mistakes feel safer?"]),
    ]),
    ("community", [
        ("A Neighbourhood Problem", "Talk about a problem in the area where you live.", ["what residents experience", "why the problem continues", "which solution could work"], ["Who should solve local problems first?", "How can residents make their voices heard?", "Why do some local projects fail?"]),
        ("A Safer Street", "Talk about one way to make a street near you safer.", ["where the street is", "which danger people face", "what should be changed"], ["Who is most responsible for road safety?", "Do stricter rules always prevent accidents?", "How can pedestrians help keep streets safe?"]),
        ("A Quiet Public Place", "Talk about a public place where people should behave quietly.", ["which place you mean", "why quiet is important there", "how noise should be managed"], ["Why are shared spaces difficult to manage?", "Should every public place have noise rules?", "How can staff enforce rules politely?"]),
        ("Local Volunteers", "Talk about a volunteer activity that could help your neighbourhood.", ["what volunteers would do", "who needs the support", "how people could join"], ["Why do people volunteer without payment?", "Should universities reward volunteer work?", "What makes a volunteer project last?"]),
    ]),
    ("planning", [
        ("A Busy Day", "Talk about how you manage a day with many tasks.", ["how you choose priorities", "where you keep your plan", "what you do if plans change"], ["Why do people often plan too much?", "Is a written schedule useful for everyone?", "How should people handle an unfinished task?"]),
        ("Wasting Time", "Talk about something that often wastes your time.", ["when it usually happens", "why it is hard to stop", "what could reduce the problem"], ["Is all unplanned time wasted time?", "How does social media affect time management?", "Why do simple tasks sometimes take too long?"]),
        ("A Deadline", "Talk about a time when you had to finish something quickly.", ["what had to be completed", "how you used the available time", "whether you met the deadline"], ["Do deadlines improve the quality of work?", "When should someone ask for more time?", "How can teams prevent last-minute problems?"]),
        ("Time to Rest", "Talk about how you make time for rest during a busy week.", ["which activity helps you relax", "when you take a break", "how rest improves your work"], ["Why do some people feel guilty while resting?", "Can a break become too long?", "Should workplaces protect employees' free time?"]),
    ]),
    ("personal development", [
        ("A New Skill", "Talk about a skill you would like to learn.", ["which ability you want to develop", "why it interests you", "how you could practise it"], ["Which skills take the longest to learn?", "Is natural ability more important than practice?", "How can adults find time to learn?"]),
        ("A Hard Skill", "Talk about something that took you a long time to learn.", ["why it was difficult", "what kept you practising", "when you noticed progress"], ["Why do learners sometimes give up early?", "Does slow progress mean someone lacks ability?", "What role does patience play in learning?"]),
        ("Teaching a Skill", "Talk about a skill you could teach another person.", ["who might need the skill", "how you would explain the first step", "which mistake you would warn them about"], ["Does teaching help the teacher learn too?", "What makes instructions easy to follow?", "When is a demonstration better than an explanation?"]),
        ("A Future Skill", "Talk about a skill that students may need in the future.", ["what the skill allows people to do", "why demand may grow", "where students could learn it"], ["Which current skills may become less useful?", "Should universities change courses more often?", "Can technology predict future job needs accurately?"]),
    ]),
    ("environment", [
        ("Using Less Plastic", "Talk about one way you can use less plastic.", ["which item you would replace", "what you would use instead", "why the change may be difficult"], ["Should shops charge more for plastic products?", "Can individual choices protect the environment?", "Why is convenient packaging so common?"]),
        ("Saving Water", "Talk about how people can avoid wasting water at home.", ["where water is often wasted", "which habit should change", "how families can notice progress"], ["Why should cities teach people about water use?", "Should heavy users pay more?", "How can old buildings save water?"]),
        ("A Greener Campus", "Talk about an environmental improvement for your campus.", ["what should be added or changed", "how students could take part", "which benefit would appear first"], ["Should green projects receive more university funding?", "How can campuses reduce energy use?", "Why do environmental campaigns lose attention?"]),
        ("Travelling Green", "Talk about an environmentally friendly way to travel.", ["which type of trip it suits", "what makes it cleaner", "what may stop people choosing it"], ["Can public transport meet everyone's needs?", "Should short car journeys be discouraged?", "How could cleaner travel become more affordable?"]),
    ]),
    ("communication", [
        ("A Useful Conversation", "Talk about a conversation that helped you understand something.", ["who you spoke with", "what you discussed", "what became clearer"], ["Why do some conversations change our opinions?", "Is face-to-face communication always clearer?", "How can someone ask better questions?"]),
        ("A Difficult Conversation", "Talk about a conversation that was difficult but necessary.", ["what needed to be discussed", "why starting was hard", "how the conversation ended"], ["Should difficult topics be discussed immediately?", "How can people disagree respectfully?", "When can a written message be more suitable?"]),
        ("Listening Well", "Talk about a person who is a good listener.", ["how the person behaves", "how you feel while speaking", "what others can learn from them"], ["Why do people interrupt each other?", "Can listening be taught?", "How does careful listening prevent conflict?"]),
        ("A Misunderstanding", "Talk about a misunderstanding you were able to solve.", ["what caused the confusion", "how you discovered it", "what solved the problem"], ["Why are messages easily misunderstood online?", "Should people explain their intentions more clearly?", "What is the best first response to confusion?"]),
    ]),
    ("teamwork", [
        ("A Successful Team", "Talk about a group that worked well together.", ["what the group wanted to achieve", "how members divided the work", "why the result was successful"], ["What qualities does a good team need?", "Can friends always work well together?", "How should a team celebrate success?"]),
        ("Group Conflict", "Talk about a disagreement that can happen in group work.", ["what people may disagree about", "how the conflict affects the task", "how members could solve it"], ["Should a leader make the final decision?", "Why do quiet members get ignored?", "Can conflict ever improve a project?"]),
        ("Choosing a Leader", "Talk about the person you would choose to lead a student project.", ["which qualities the person has", "how they treat group members", "why you would trust them"], ["Is experience necessary for leadership?", "Should leaders do more work than others?", "How can a group replace an ineffective leader?"]),
        ("An Online Team", "Talk about how a group can work together online.", ["which tools the group needs", "how members stay in contact", "what problem may occur"], ["Is online teamwork less personal?", "How can a group include members in different places?", "When is an in-person meeting still necessary?"]),
    ]),
    ("public services", [
        ("A Useful Service", "Talk about a public service that you use.", ["what the service provides", "who uses it most", "what could be improved"], ["Why do public services differ between cities?", "Should every service be free?", "How can users report a problem effectively?"]),
        ("The City Library", "Talk about how a public library can serve young people.", ["which resources they need", "what activities could be offered", "how the library could attract them"], ["Are libraries still necessary in the digital age?", "Should libraries remain open later?", "What makes a public place welcoming?"]),
        ("A Health Centre", "Talk about what makes a local health centre easy to use.", ["how patients get information", "what reduces waiting", "how staff can help nervous visitors"], ["Why do people delay asking for medical help?", "Should basic health advice be available online?", "How can public clinics improve communication?"]),
        ("City Information", "Talk about how a city should inform people during an emergency.", ["which information is urgent", "where updates should appear", "how messages can stay clear"], ["Why do false reports spread during emergencies?", "Should people rely on social media for warnings?", "How can information reach people without internet access?"]),
    ]),
    ("technology", [
        ("Your Screen Time", "Talk about how screen time affects your daily routine.", ["when you use screens most", "which activity takes the longest", "what limit might help you"], ["Is all screen time equally harmful?", "Why are digital habits difficult to measure?", "Should parents control teenagers' screen use?"]),
        ("An Online Break", "Talk about a time when taking a break from the internet would help.", ["how long the break would last", "what you would do instead", "what might be difficult at first"], ["Can people study properly without internet access?", "Why do notifications demand attention?", "Should workplaces contact staff after work hours?"]),
        ("Social Media Choice", "Talk about how you decide what to share on social media.", ["which details you keep private", "who may see a post", "what you check before sharing"], ["Why do people share personal moments online?", "Can an old post cause future problems?", "Should platforms remove misleading content?"]),
        ("Digital Messages", "Talk about one rule that makes online communication better.", ["which behaviour the rule concerns", "why it is needed", "how people could follow it"], ["Why do online discussions become rude?", "Are emojis helpful or confusing?", "Should anonymous comments be allowed?"]),
    ]),
    ("culture", [
        ("A Cultural Event", "Talk about a cultural event you attended or watched.", ["where it took place", "what people did", "what you found interesting"], ["Why do cultural events bring people together?", "Should cities spend money on festivals?", "How can an event welcome international visitors?"]),
        ("A Family Tradition", "Talk about a tradition in your family.", ["when it happens", "who takes part", "why it is meaningful to you"], ["Why do some traditions disappear?", "Should traditions change with society?", "Can a new activity become a tradition quickly?"]),
        ("Another Culture", "Talk about something you would like to learn about another culture.", ["which culture interests you", "what you want to understand", "how you could learn respectfully"], ["Can films teach people accurately about a culture?", "Why do cultural misunderstandings happen?", "How does travel affect cultural knowledge?"]),
        ("A Local Festival", "Talk about a festival that could represent your town or city.", ["what it would celebrate", "which activities it would include", "who would be invited"], ["What makes a festival successful?", "How can festivals support local businesses?", "Should traditional festivals include modern activities?"]),
    ]),
    ("decision making", [
        ("A Quick Decision", "Talk about a decision you had to make quickly.", ["why there was little time", "which options you considered", "what happened after your choice"], ["When are quick decisions necessary?", "Why can too many options be unhelpful?", "Should people trust their first reaction?"]),
        ("Changing Your Mind", "Talk about a time when you changed your mind.", ["what you believed at first", "which information affected you", "how your final view was different"], ["Why do people refuse to change an opinion?", "Does changing your mind show weakness?", "Whose opinions influence young people most?"]),
        ("Asking for Advice", "Talk about someone you consult before an important choice.", ["who the person is", "why you value their opinion", "how you make the final decision"], ["Can advice make a decision more confusing?", "Should parents influence adult children's choices?", "When should professional advice be preferred?"]),
        ("Choosing a Course", "Talk about how a student should choose an optional course.", ["which information they should read", "what personal interest matters", "who could answer their questions"], ["Should career value decide every course choice?", "Why do students drop a course?", "How can universities describe courses more clearly?"]),
    ]),
    ("daily life", [
        ("A Cheap Weekend", "Talk about an enjoyable weekend plan that costs little money.", ["where you would go", "who you would invite", "what you would do together"], ["Why do people connect enjoyment with spending?", "What free activities can cities provide?", "Is planning necessary for a relaxing weekend?"]),
        ("A Free Campus Activity", "Talk about a free activity your university could offer.", ["what students would do", "where it would happen", "why people would join"], ["Should student clubs receive university funding?", "How can a new activity become popular?", "Why do students avoid some free events?"]),
        ("Fun Without Money", "Talk about something you enjoy doing without spending money.", ["how the activity became your interest", "when you usually do it", "what makes it enjoyable"], ["Are hobbies becoming too expensive?", "Can simple activities reduce stress?", "Why do interests change over time?"]),
        ("Travelling on a Budget", "Talk about how a student can take an affordable trip.", ["which costs can be reduced", "what should be booked early", "what should not be sacrificed"], ["Is cheap travel always uncomfortable?", "How can travellers avoid hidden costs?", "Should students borrow money for a holiday?"]),
    ]),
    ("learning", [
        ("A Useful Mistake", "Talk about a mistake that taught you something important.", ["what you were trying to do", "what went wrong", "how you used the lesson later"], ["Why are mistakes useful for learning?", "Do schools sometimes make students fear errors?", "When should the same mistake be forgiven?"]),
        ("A Classroom Error", "Talk about how a student should react after giving a wrong answer.", ["how they may feel", "what they can ask the teacher", "how they can remember the correction"], ["Should teachers correct every spoken mistake?", "Why do some students avoid answering questions?", "How can classmates respond kindly?"]),
        ("Helping After a Mistake", "Talk about how you would help a friend who made a serious mistake.", ["how you would listen", "which practical help you could give", "what the friend must do personally"], ["Can too much help prevent responsibility?", "Why is admitting a mistake difficult?", "Should friends always defend each other?"]),
        ("Fear of Failure", "Talk about a situation where fear of failure can stop progress.", ["what the person wants to attempt", "what they are afraid of", "which first step could help"], ["Why do people compare their progress with others?", "Can failure improve confidence later?", "How should success be measured?"]),
    ]),
    ("work", [
        ("An Ideal Workplace", "Talk about a workplace where you would feel comfortable.", ["what the space is like", "how people communicate", "which rule is important to you"], ["Does a comfortable office improve performance?", "Should employees help choose workplace rules?", "What causes stress at work?"]),
        ("Your First Job", "Talk about what you would expect from your first full-time job.", ["which tasks you hope to do", "what you want to learn", "what support you may need"], ["Should a first job offer a high salary or useful experience?", "Why do new employees need feedback?", "How long should someone stay in an unsuitable job?"]),
        ("Working from Home", "Talk about whether working from home would suit you.", ["where you would work", "how you would stay focused", "what you might miss"], ["Which jobs cannot be done from home?", "Does remote work weaken teamwork?", "Should employees choose where they work?"]),
        ("A Good Manager", "Talk about the qualities you want in a manager.", ["how they give instructions", "how they respond to problems", "how they treat employees"], ["Can a friendly manager still be effective?", "Should managers admit their own mistakes?", "What makes employees trust a leader?"]),
    ]),
    ("community", [
        ("Helping a Neighbour", "Talk about a simple way neighbours can help each other.", ["who may need help", "what others could do", "how privacy can be respected"], ["Why do some neighbours rarely speak?", "Is community life weaker in large cities?", "When should help come from professionals?"]),
        ("Student Volunteers", "Talk about a volunteer project for university students.", ["which need it would address", "what students would contribute", "how the project would be organised"], ["What do volunteers learn from service?", "Should volunteer work count towards a degree?", "How can projects avoid wasting resources?"]),
        ("Support in a Crisis", "Talk about how a community can respond to a difficult event.", ["which help is needed first", "how information should be shared", "how support can continue later"], ["Why do people cooperate during a crisis?", "Who should coordinate donations?", "How can communities prepare before trouble occurs?"]),
        ("A Community Project", "Talk about a small project that could improve local life.", ["what the project would create", "who could take part", "how its success would be seen"], ["Why are small projects easier to begin?", "Should local businesses provide support?", "How can residents keep a project active?"]),
    ]),
    ("daily life", [
        ("An Object You Use", "Talk about an everyday object that is useful to you.", ["what the object is", "when you use it", "why another object cannot replace it easily"], ["Why do people become attached to objects?", "Are modern products designed to last?", "Which everyday item has changed most over time?"]),
        ("A Special Gift", "Talk about an object that someone gave you.", ["who gave it to you", "when you received it", "why you have kept it"], ["Does a valuable gift need to be expensive?", "Why do people keep objects they never use?", "Is giving an experience better than giving an item?"]),
        ("Repair or Replace", "Talk about an item you would try to repair instead of replacing.", ["what is wrong with it", "who could repair it", "why keeping it is worthwhile"], ["Why are many products difficult to repair?", "Should repair services be cheaper?", "When is replacement the safer choice?"]),
        ("One Daily Item", "Talk about one item that every student should carry.", ["what the item is", "which situations it helps with", "why it is a sensible choice"], ["Do people carry too many things each day?", "How have bags changed because of technology?", "Should useful design be more important than appearance?"]),
    ]),
    ("personal development", [
        ("A Personal Goal", "Talk about a goal you hope to reach.", ["why the goal matters", "what you have already done", "what your next step will be"], ["Why are personal goals sometimes abandoned?", "Should goals always have a deadline?", "How can other people support progress?"]),
        ("One Small Step", "Talk about a small action that could move you towards a larger goal.", ["which goal it supports", "how often you would do it", "what could make it a habit"], ["Why can small steps be powerful?", "How should someone track gradual progress?", "When is a bigger change necessary?"]),
        ("Staying Motivated", "Talk about what helps you continue when progress is slow.", ["which situation tests your motivation", "what you tell yourself", "who or what encourages you"], ["Does motivation matter more than discipline?", "Why do rewards sometimes stop working?", "Can competition help people continue?"]),
        ("A Different Goal", "Talk about a goal that a person may need to change.", ["why the original goal no longer fits", "which signs show this", "how a new direction could be chosen"], ["Is changing a goal the same as giving up?", "How often should people review their plans?", "Can an unrealistic goal still be useful?"]),
    ]),
]


def _speaking_packs() -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    number = 1
    for topic, group in SPEAKING_CARD_GROUPS:
        for title, prompt, bullets, followups in group:
            cards.append({
                "id": f"catalog-speaking-{number:03d}",
                "kind": "speaking_card",
                "title": title,
                "topic": topic,
                "cefr": "B1+",
                "source": "seed",
                "published": True,
                "instructions": "Read the card aloud and think for one minute. Then speak about the topic and cover all three points.",
                "content": {"prompt": prompt, "bullets": bullets, "followups": followups},
                "questions": [],
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
