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
    script = [
        {"speaker": "student", "text": f"Hello. I was told that the {place} could help me. I need to {goal}, but I have reached a problem and I am not sure which step should come next."},
        {"speaker": "staff", "text": f"Of course. Tell me what has happened so far. These requests usually have one general rule, but there may be another option if we understand your situation clearly."},
        {"speaker": "student", "text": f"The main issue is that {problem}. I checked the website twice, but its short message did not explain whether I should wait, start again, or speak to someone in person."},
        {"speaker": "staff", "text": f"That message is not very helpful. The important rule is that {rule}. It exists so that staff can treat similar requests in the same way and keep a clear record."},
        {"speaker": "student", "text": "I understand the reason for the rule. I am not asking you to ignore it; I just want to know whether there is a practical route that still lets me finish the task on time."},
        {"speaker": "staff", "text": f"There is. You can {solution}. That will give us the information we need without cancelling the work you have already completed."},
        {"speaker": "student", "text": "That sounds manageable. Will I need to pay anything or complete another long application? I have my student card and can open the campus portal on my phone."},
        {"speaker": "staff", "text": "There is no extra payment. The form is short, but use your university account so the system connects it to your record. Keep the confirmation page until everything is finished."},
        {"speaker": "student", "text": f"All right. So first I should {solution}, and then I should {next_step}. Is that the correct order?"},
        {"speaker": "staff", "text": "Yes. If the confirmation does not appear within an hour, do not send the same request several times. Bring the reference number here and we can find the original request."},
        {"speaker": "student", "text": "Good. I was worried that I would have to begin the whole process again. I will follow those steps now and save the reference number."},
        {"speaker": "staff", "text": "That should solve it. Read the final confirmation carefully because it will state the time and any item you need to bring. Come back if the details are different from what we discussed."},
    ]
    return {
        "id": f"catalog-conversation-{index:02d}", "kind": "conversation", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "defer_audio": True, "script": script,
        "questions": [
            _question("Why does the student visit the office?", ["To complain about a staff member", f"To {goal}", "To collect a course certificate", "To ask for a general campus map"], "B", f"The student says that they need to {goal}.", qtype="purpose"),
            _question("What is the main difficulty?", ["The office has moved", "The student forgot a password", problem.capitalize(), "A payment was made twice"], "C", f"The student clearly explains that {problem}.", qtype="detail"),
            _question("What solution does the staff member offer?", [solution.capitalize(), "Wait until the next semester", "Ask another student to complete it", "Cancel the request completely"], "A", f"The staff member recommends that the student {solution}.", qtype="process"),
            _question("What should the student do if no confirmation appears?", ["Submit several new requests", "Pay an additional charge", "Ignore the missing message", "Take the reference number to the office"], "D", "The staff member says the reference number can be used to find the original request.", qtype="inference"),
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
    lines = [
        f"Good morning. Today's topic is {subject}. This may sound like a narrow subject, but it connects everyday choices with larger systems. We will look at three main ideas, consider one practical example, and then discuss an important limit. The purpose is not to memorise technical language. It is to understand a process well enough to explain why a particular decision may work.",
        f"The first idea is that {first}. This matters because people often notice only the final result and miss the process that created it. When we separate cause from result, the subject becomes easier to analyse. It also helps us avoid a common mistake: assuming that one visible feature is responsible for every change we observe.",
        f"The second idea is that {second}. Think of this as another layer rather than a competing explanation. In real situations, several processes usually operate at the same time. Their strength may change with season, location, resources, or human behaviour. A useful explanation therefore describes conditions instead of promising that the same outcome will appear everywhere.",
        f"Our third idea is that {third}. This point expands the discussion beyond a single person or object. It shows why planners and researchers measure patterns over time. A quick photograph can show what exists today, but repeated observation reveals whether a change is stable, temporary, or simply the result of unusual conditions.",
        f"Consider {example}. At first, people involved in this example focused on the most obvious problem. After collecting information for several weeks, they discovered that the three ideas worked together. The project improved when they changed the order of their actions, explained the reason to users, and recorded what happened before and after the change.",
        f"The example also teaches us something about evidence. A successful result in one place is useful, but it is not a universal rule. We should ask who took part, how long the project lasted, and what was measured. Personal stories can suggest a question, while careful comparison tells us whether the suggested explanation is strong.",
        f"Now we need to recognise a limitation: {limitation}. This does not make the whole idea useless. Limits tell us where extra support, different timing, or another method is necessary. Good decisions rarely come from choosing between a perfect solution and a terrible one. They come from comparing realistic benefits, costs, and risks.",
        f"For students, a practical response is to {action}. Begin with a small observation and write down what you expect to happen. Then compare the result with your expectation. If they differ, do not hide the difference. It may reveal a missing factor and lead to a better question for the next round of work.",
        f"This way of thinking is valuable outside today's topic. It asks us to identify a process, connect several causes, test an example, and state a limit. These are also the moves you use in academic reading and listening questions. Main ideas describe the whole pattern, while details explain how individual parts support it.",
        f"To summarise, {subject} can be understood through three connected claims: {first}; {second}; and {third}. The case of {example} shows how those claims can guide action, while the fact that {limitation} reminds us to remain careful. The most useful next step is to {action}. Before our next meeting, try to explain the process to someone else in three sentences and include one reason, one example, and one limitation. In the next lecture, we will compare this approach with a case in which the first plan failed and the participants had to revise their assumptions.",
    ]
    script = [{"speaker": "lecturer", "text": line} for line in lines]
    return {
        "id": f"catalog-lecture-{index:02d}", "kind": "lecture", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "defer_audio": True,
        "note_scaffold": [f"Subject: {subject}", f"Idea 1: {first}", f"Idea 2: {second}", f"Idea 3: {third}", f"Example: {example}", f"Limit: {limitation}", f"Action: {action}"],
        "script": script,
        "questions": [
            _question("What is the lecture mainly about?", [f"The history of university courses about {subject}", f"Three connected ideas that explain {subject}", "Why personal stories are better than research", "A technical method students must memorise"], "B", f"The lecture organises {subject} around three connected ideas.", points=2, qtype="main_idea"),
            _question("Which statement is TRUE according to the lecture?", [first.capitalize(), "One visible feature always explains every result", "A single photograph proves a long-term pattern", "Conditions have no effect on outcomes"], "A", f"The first main point is that {first}.", points=2, qtype="true"),
            _question("Which statement is NOT TRUE according to the lecture?", ["Several processes may operate together", "Repeated observation can reveal stable patterns", "Limits can show where another method is needed", "A successful example creates a universal rule"], "D", "The lecturer warns that one successful example is not a universal rule.", points=2, qtype="not_true"),
            _question("Why does the lecturer mention the practical example?", ["To show how the three ideas can guide a real decision", "To prove that no measurements are necessary", "To replace the main explanation with a personal story", "To introduce a completely unrelated topic"], "A", f"The example of {example} shows the ideas working together.", points=2, qtype="cause"),
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
    paragraphs = [
        f"In many places, {subject} have moved from a small experiment to a practical part of everyday life. Supporters often describe them as a simple answer, yet their real value comes from several connected effects. The most immediate is that {first}. This visible result attracts attention, but it is only the beginning of the process.",
        f"A second effect is that {second}. This matters because a service may be technically available without being easy to use. Clear design and repeated experience reduce uncertainty. When people understand what is expected, they make fewer mistakes and are more willing to return. Over time, this reliability can become more important than an impressive launch.",
        f"There is also a social or educational layer: {third}. People do not simply receive a product or enter a space. They observe how others behave, exchange small pieces of information, and slowly develop shared expectations. These informal lessons are difficult to measure, but interviews often show that users remember them long after the first visit.",
        f"Consider {example}. At first, organisers measured only the number of users. Later they also recorded questions, repeated visits, and the times when problems occurred. The extra information changed their plan. Instead of expanding immediately, they improved signs, adjusted volunteer duties, and explained the system in shorter language. Use increased because the experience became clearer, not because the project became larger.",
        f"However, {limitation}. Ignoring this point can turn early success into disappointment. The strongest projects state what they cannot provide and collect evidence before promising more. A realistic next step is to {action}. This approach treats improvement as a continuing process: identify a need, try a limited response, observe its effects, and revise the design when the evidence suggests a better direction.",
        f"The wider lesson is not that every community must copy the same model. Local conditions affect cost, participation, space, and timing. The lesson is that practical systems work best when physical design, clear information, and human relationships support one another. A useful idea becomes sustainable only when people can understand it, maintain it, and adapt it without losing its original purpose. This takes patient observation, honest communication, and enough time for users to turn a new service into a familiar part of ordinary life.",
    ]
    return {
        "id": f"catalog-reading-standard-{index:02d}", "kind": "reading_standard", "title": title, "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True,
        "instructions": "Read the passage and choose the best answer according to the text.", "content": {"paragraphs": paragraphs},
        "questions": [
            _question("What is the main purpose of the passage?", [f"To argue that {subject} should be identical everywhere", f"To explain the connected benefits and limits of {subject}", "To describe a historical conflict between two cities", "To give technical instructions for professional researchers"], "B", f"The passage explains how {subject} work, including benefits and a limitation."),
            _question("According to paragraph 2, what supports repeated use?", ["An expensive launch event", "Removing every rule", "Clear design and a reliable experience", "Measuring only the number of users"], "C", "The paragraph links clarity and repeated experience with reliable use."),
            _question("Why did the organisers change their plan in the example?", ["They collected information beyond total user numbers", "They wanted the project to look larger", "Volunteers refused to speak to users", "The first location closed immediately"], "A", "Questions, repeat visits and problem times revealed what needed improvement."),
            _question("The word 'layer' in paragraph 3 is closest in meaning to _____.", ["additional aspect", "physical cover", "official limit", "final result"], "A", "Layer refers to another aspect of the system."),
            _question("What can be inferred about the writer's view of growth?", ["Every successful project should expand immediately", "Growth matters more than clear information", "Expansion should follow evidence and realistic planning", "Small projects cannot have social effects"], "C", "The writer recommends evidence and improvement before making larger promises."),
            _question("Which statement would the writer most likely agree with?", ["One model works in every local setting", "Good systems combine design, information and relationships", "Limitations should be hidden from users", "Informal learning has no lasting value"], "B", "The conclusion explicitly connects physical design, information and human relationships."),
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
    paragraphs = [
        f"Many small projects begin with a practical local need. {title} are one example. [[1]] This first feature explains why people notice the project and decide to try it.",
        f"Good organisation is necessary after the first interest appears. [[2]] Without this routine, users may lose confidence even when the original idea is useful.",
        f"The project can also become a place for learning. [[3]] In this way, participation produces knowledge as well as an immediate service.",
        f"Information collected during normal use supports later decisions. [[4]] Organisers can improve the system without guessing what participants want.",
        "Like most community projects, the idea works best when its limits are explained honestly. A small, reliable service is often more valuable than a large promise that cannot be maintained.",
    ]
    questions = []
    for gap, answer in enumerate(("A", "B", "C", "D"), start=1):
        questions.append({"stem": f"Which sentence best fits gap {gap}?", "options": options, "answer": answer, "points": 2, "qtype": "sentence_insertion", "rationale": f"Sentence {answer} develops the idea immediately before and after gap {gap}."})
    return {"id": f"catalog-reading-insertion-{index:02d}", "kind": "reading_insertion", "title": title, "topic": topic, "cefr": "B1+", "source": "seed", "published": True, "instructions": "Complete gaps 1-4 with the most suitable sentences A-E. There is one extra sentence.", "content": {"paragraphs": paragraphs, "sentence_options": options}, "questions": questions}


CLOZE_TOPICS = [
    "planning a weekly study schedule", "keeping a shared kitchen clean", "preparing for a short presentation", "using a campus bicycle safely", "starting a reading habit", "joining a student society", "reducing phone distractions", "cooking with seasonal vegetables", "organising digital notes", "walking to university", "learning from written feedback", "caring for indoor plants", "sharing tasks in a group", "visiting a museum effectively", "building an emergency kit", "using a reusable water bottle", "preparing for a job interview", "taking useful lecture notes", "protecting personal data", "volunteering at a local event", "choosing a quiet study place", "creating a realistic morning routine",
]


def _cloze_pack(index: int, topic: str) -> dict[str, Any]:
    text = f"Many students want to improve {topic}, but they sometimes begin with a plan that is too difficult to continue. A new routine is easier to build [[1]] the first step is clear and small. People [[2]] try to change everything at once often become tired before they see a result. It is therefore useful to choose one action and repeat it at a regular time. Progress should [[3]] once a week rather than judged after every attempt. This gives the routine enough time to become familiar. If a problem appears, the plan can be adjusted [[4]] being abandoned completely. Students should also notice the conditions that make the action easier. A routine is more likely to continue when the necessary materials [[5]] ready before the starting time."
    return {
        "id": f"catalog-cloze-{index:02d}", "kind": "cloze", "title": f"A Practical Guide to {topic.title()}", "topic": topic,
        "cefr": "B1+", "source": "seed", "published": True, "instructions": "Choose the option that best fits each gap.", "content": {"text": text},
        "questions": [
            _question("Gap 1", ["unless", "when", "although", "despite"], "B", "When introduces the condition that makes the routine easier.", qtype="connector"),
            _question("Gap 2", ["which", "whose", "who", "where"], "C", "Who refers to people.", qtype="relative_clause"),
            _question("Gap 3", ["review", "reviewed", "be reviewed", "reviewing"], "C", "The modal should requires the passive form be reviewed.", qtype="modal_passive"),
            _question("Gap 4", ["instead", "rather", "without", "except"], "C", "Without is followed by an -ing form and preserves the intended meaning.", qtype="preposition"),
            _question("Gap 5", ["prepare", "prepared", "are prepared", "have preparing"], "C", "Materials receive the action, so the passive form is required.", qtype="passive"),
        ],
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
    ("the history lecture", "the archive website", "the research essay", "the reading room", "the museum route"),
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
    questions = [
        _question(f"Although {event} is optional, students are advised to attend it before beginning {task}.", [f"Students cannot begin {task} unless they attend {event}.", f"Attending {event} is recommended but not required before {task} starts.", f"Only students who finished {task} may attend {event}.", f"The event and the task have both been cancelled."], "B", "The recommendation and the fact that attendance is optional are both preserved.", qtype="restatement"),
        _question(f"The coordinator simplified {guide} so that first-time users could follow it more easily.", [f"The guide was made clearer for people using it for the first time.", f"First-time users were asked to write a more difficult guide.", f"The coordinator removed the guide because nobody followed it.", f"Only experienced users are now able to understand the guide."], "A", "Simplifying the guide makes it easier for first-time users.", qtype="restatement"),
        _question(f"Mert did not notice the missing section of {task} until he read the feedback.", [f"Mert wrote the feedback before completing the missing section.", f"The feedback made Mert aware that part of the task was absent.", f"Mert refused to read feedback about the completed task.", f"The section disappeared after Mert read the feedback."], "B", "Reading the feedback caused Mert to recognise the missing section.", qtype="restatement"),
        _question(f"Because {place} becomes crowded after two o'clock, the group decided to meet there earlier.", [f"The group chose an earlier time to avoid the crowded period.", f"The place does not allow groups to enter before two.", f"The group prefers meeting when the place is busiest.", f"The meeting was moved to another day because the place closed."], "A", "The earlier meeting is a response to the place becoming crowded later.", qtype="restatement"),
        _question(f"The journey will be faster by {transport} unless there is an unexpected delay.", [f"An unexpected delay is the only stated condition that may prevent the transport from being faster.", f"The transport is always slower even when it leaves on time.", f"The journey was cancelled because the delay was expected.", f"Passengers must create a delay before using the transport."], "A", "Unless introduces the condition that could change the expected faster journey.", qtype="restatement"),
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
    ]
    number = 1
    for label, subject, topic in SPEAKING_DOMAINS:
        for suffix, prompt, bullets, followups in formats:
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
