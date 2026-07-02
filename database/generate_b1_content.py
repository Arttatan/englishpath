from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"


def ensure_dir(section: str) -> Path:
    path = CONTENT / section / "b1"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(section: str, slug: str, data: dict) -> None:
    path = ensure_dir(section) / f"{slug}.json"
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def ic(text: str, feedback: str) -> dict:
    return {"text": text, "feedback": feedback}


def lg(sentence: str, correct: str, wrong1: str, wrong2: str, feedback: str) -> dict:
    return {"text": f"{sentence} | *{correct} | {wrong1} | {wrong2}", "feedback": feedback}


def dd(sentence: str, answer: str, feedback: str = "") -> dict:
    return {"text": f"{sentence} | {answer}", "feedback": feedback}


def lesson(title: str, level: str, section: str, sort_order: int, explanation: str, exercise_sets: list[dict], audio_url: str | None = None) -> dict:
    data = {
        "title": title,
        "level": level,
        "section": section,
        "sort_order": sort_order,
        "explanation": explanation,
        "exercise_sets": exercise_sets,
    }
    if audio_url:
        data["audio_url"] = audio_url
    return data


def grammar_lesson(title: str, sort_order: int, explanation: str, q1: list[dict], q2: list[dict], q3: list[dict]) -> dict:
    return lesson(
        title,
        "b1",
        "grammar",
        sort_order,
        explanation,
        [
            {"title": "Exercise 1", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q1},
            {"title": "Exercise 2", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": q2},
            {"title": "Exercise 3", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q3},
        ],
    )


def vocab_lesson(title: str, sort_order: int, explanation: str, lettered1: list[dict], dropdown: list[dict], bank: list[str], lettered2: list[dict]) -> dict:
    return lesson(
        title,
        "b1",
        "vocabulary",
        sort_order,
        explanation,
        [
            {"title": "Exercise 1", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": lettered1},
            {
                "title": "Exercise 2",
                "instructions": "Choose the correct option. Use each option ONLY ONCE.",
                "type": "dropdown_gap",
                "use_once": True,
                "word_bank": bank,
                "questions": dropdown,
            },
            {"title": "Exercise 3", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": lettered2},
        ],
    )


def skill_lesson(title: str, section: str, sort_order: int, explanation: str, q1: list[dict], q2: list[dict], q3: list[dict], audio_url: str | None = None) -> dict:
    return lesson(
        title,
        "b1",
        section,
        sort_order,
        explanation,
        [
            {"title": "Exercise 1", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q1},
            {"title": "Exercise 2", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": q2},
            {"title": "Exercise 3", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q3},
        ],
        audio_url=audio_url,
    )


def build_grammar() -> list[tuple[str, str, dict]]:
    out = []
    out.append(
        (
            "grammar",
            "present-perfect-continuous",
            grammar_lesson(
                "Present perfect continuous",
                2,
                "<h2>Present perfect continuous</h2><p><strong>have / has been + verb-ing</strong></p><p>We use it for actions that started in the past and continue now, or actions that have recently stopped and have a visible result.</p><ul><li>I have been working here for six years.</li><li>She is tired because she has been studying all day.</li></ul>",
                [
                    ic("I [*have been waiting|have waited|am waiting] for the bus for half an hour.", "For half an hour suggests an activity continuing until now."),
                    ic("She is wet because it [*has been raining|has rained|rained] all afternoon.", "Visible result plus duration."),
                    ic("How long [*have you been learning|have you learnt|are you learning] English?", "We ask about duration with the present perfect continuous."),
                    ic("They [*have been living|live|are living] in Dublin since January.", "Since January shows an unfinished period."),
                    ic("He is exhausted because he [*has been running|has run|ran] for an hour.", "Current result after an activity."),
                ],
                [
                    lg("We ____ on this project all week.", "have been working", "worked", "are working", "All week points to an unfinished activity."),
                    lg("Why are your hands dirty? I ____ in the garden.", "have been digging", "dug", "am digging", "Recent activity with present result."),
                    lg("She ____ too much coffee recently.", "has been drinking", "drank", "has drunk", "Recently plus repeated activity."),
                    lg("It ____ since early morning.", "has been snowing", "snowed", "is snowing", "Since early morning shows duration."),
                ],
                [
                    ic("We [*have been trying|tried|are trying] to call you all day.", "All day suggests duration up to now."),
                    ic("He [*has been teaching|taught|teaches] at this school for ten years.", "For ten years shows continuity."),
                    ic("My eyes hurt because I [*have been looking|looked|have looked] at the screen too long.", "Current effect after an activity."),
                    ic("They [*have been travelling|travelled|are travelling] around South America since May.", "Since May suggests a continuing journey."),
                    ic("I [*have not been sleeping|did not sleep|am not sleeping] well recently.", "Recently plus repeated ongoing problem."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "past-perfect",
            grammar_lesson(
                "Past perfect",
                3,
                "<h2>Past perfect</h2><p><strong>had + past participle</strong></p><p>We use the past perfect to show that one action happened before another past action.</p><ul><li>When I arrived, they had already left.</li><li>She was nervous because she had never flown before.</li></ul>",
                [
                    ic("When we got to the station, the train [*had left|left|has left].", "The train left before we got there."),
                    ic("She was upset because she [*had lost|lost|has lost] her keys.", "The loss happened before the feeling."),
                    ic("I [*had never seen|never saw|have never seen] snow before I moved to Norway.", "Before another past moment."),
                    ic("By the time he called, I [*had finished|finished|have finished] dinner.", "By the time signals earlier past action."),
                    ic("They [*had already booked|already booked|have already booked] the tickets when I asked.", "Already booked before the asking."),
                ],
                [
                    lg("After she ____ the report, she went home.", "had sent", "sent", "has sent", "Sending happened before going home."),
                    lg("We realised we ____ there before.", "had been", "were", "have been", "Past perfect for earlier experience."),
                    lg("He ____ dinner before the guests arrived.", "had prepared", "prepared", "has prepared", "Preparation happened first."),
                    lg("I was tired because I ____ very little the night before.", "had slept", "slept", "have slept", "Earlier past cause."),
                ],
                [
                    ic("The film started after everyone [*had sat down|sat down|has sat down].", "The sitting happened before the start."),
                    ic("She did not want dessert because she [*had eaten|ate|has eaten] too much.", "Earlier action caused the later decision."),
                    ic("I knew the city because I [*had visited|visited|have visited] it before.", "Visit happened before the knowing."),
                    ic("By 2015, they [*had moved|moved|have moved] three times.", "By + past year often takes past perfect."),
                    ic("The teacher was angry because no one [*had done|did|has done] the homework.", "Homework should have been done earlier."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "future-forms-b1",
            grammar_lesson(
                "Future forms review",
                4,
                "<h2>Future forms review</h2><p>Use <strong>will</strong> for predictions and spontaneous decisions, <strong>going to</strong> for plans and evidence, <strong>present continuous</strong> for arranged future events, and <strong>present simple</strong> for timetables.</p>",
                [
                    ic("Look at those clouds! It [*is going to rain|will rain|rains] soon.", "Evidence now suggests going to."),
                    ic("I think people [*will work|are working|work] fewer hours in the future.", "Prediction with will."),
                    ic("We [*are meeting|meet|will meet] the clients at 10 tomorrow.", "Arrangement with present continuous."),
                    ic("The train [*leaves|is leaving|will leave] at 6:45.", "Timetable with present simple."),
                    ic("I forgot my wallet. I [*will go|am going to go|go] back for it.", "Spontaneous decision with will."),
                ],
                [
                    lg("She ____ to Berlin next Friday. Everything is booked.", "is flying", "flies", "will fly", "Arrangement already made."),
                    lg("I am sure you ____ the exam.", "will pass", "are passing", "pass", "Prediction."),
                    lg("We ____ a new flat this summer.", "are going to buy", "buy", "will buying", "Plan or intention."),
                    lg("The lesson ____ at half past nine.", "starts", "is starting", "will starts", "Schedule or timetable."),
                ],
                [
                    ic("They [*are going to open|will opening|open] a new branch next year.", "Planned future action."),
                    ic("I am thirsty. I [*will get|am getting|get] some water.", "Immediate decision."),
                    ic("The conference [*begins|is going to begin|will beginning] on Monday.", "Fixed programme."),
                    ic("What time [*are you leaving|do you leave|will you leaves] tomorrow?", "Personal arrangement."),
                    ic("He [*is not going to stay|will not staying|does not stay] in that job for long.", "Decision or intention about the future."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "modals-obligation-advice",
            grammar_lesson(
                "Modals of obligation and advice",
                5,
                "<h2>Modals of obligation and advice</h2><p><strong>must / have to</strong> express obligation, <strong>mustn't</strong> expresses prohibition, <strong>don't have to</strong> means no necessity, and <strong>should / ought to</strong> express advice.</p>",
                [
                    ic("You [*mustn't|don't have to|shouldn't to] park here. It is illegal.", "Mustn't means prohibition."),
                    ic("I [*have to|mustn't|should] wear a uniform at work.", "External rule or necessity."),
                    ic("You [*don't have to|mustn't|ought] come if you are busy.", "No necessity."),
                    ic("He [*should|must|has to] see a dentist about that tooth.", "Advice, not a rule."),
                    ic("We [*had to|must|should] cancel the trip because of the storm.", "Past obligation uses had to."),
                ],
                [
                    lg("Students ____ hand in the project by Friday.", "have to", "should", "don't have to", "It is a requirement."),
                    lg("You ____ tell anyone. It is a secret.", "mustn't", "don't have to", "ought", "You are not allowed to tell anyone."),
                    lg("We ____ hurry; there is plenty of time.", "don't have to", "mustn't", "had to", "No necessity."),
                    lg("She ____ eat less sugar if she wants to feel better.", "should", "mustn't", "has to not", "Advice."),
                ],
                [
                    ic("Passengers [*must show|must showing|show must] their tickets.", "Must + base verb."),
                    ic("You [*ought to apologise|ought apologise|ought apologising] for what you said.", "Ought to + base verb."),
                    ic("I [*didn't have to|mustn't|shouldn't] work yesterday because it was a public holiday.", "No necessity in the past."),
                    ic("They [*have to get|must getting|should to get] up early on weekdays.", "Have to + base verb."),
                    ic("You [*should not ignore|must not to ignore|ought ignore] his advice.", "Should not + base verb."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "relative-clauses",
            grammar_lesson(
                "Relative clauses",
                6,
                "<h2>Relative clauses</h2><p>We use <strong>who</strong> for people, <strong>which</strong> for things, <strong>where</strong> for places, and <strong>whose</strong> for possession. We often use relative clauses to add information: <em>The woman who lives next door is a doctor.</em></p>",
                [
                    ic("The man [*who|which|where] helped me was very kind.", "Who refers to a person."),
                    ic("This is the book [*which|who|whose] I told you about.", "Which refers to a thing."),
                    ic("That is the house [*where|who|whose] I grew up.", "Where refers to a place."),
                    ic("She is the writer [*whose|which|where] novels have won prizes.", "Whose shows possession."),
                    ic("The café [*which|who|whose] opened last month is already popular.", "Which refers to the café."),
                ],
                [
                    lg("I know someone ____ can repair your laptop.", "who", "which", "where", "Who for people."),
                    lg("This is the park ____ we first met.", "where", "who", "whose", "Where for places."),
                    lg("The company ____ products I buy is based in Sweden.", "whose", "where", "which", "Whose products."),
                    lg("The film ____ we saw last night was disappointing.", "which", "who", "where", "Which for things."),
                ],
                [
                    ic("Do you remember the teacher [*who taught|which taught|where taught] us maths?", "Who for a person."),
                    ic("The office [*where she works|who she works|whose she works] is in the city centre.", "Where she works."),
                    ic("I met a girl [*whose brother|which brother|where brother] is a pilot.", "Whose brother."),
                    ic("The phone [*which I bought|who I bought|where I bought] was expensive.", "Which for the object."),
                    ic("That is the restaurant [*where they got married|which they got married|whose they got married] .", "Where for place."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "gerunds-and-infinitives",
            grammar_lesson(
                "Gerunds and infinitives",
                7,
                "<h2>Gerunds and infinitives</h2><p>Some verbs are followed by a gerund (<strong>-ing</strong>): enjoy, avoid, consider. Others are followed by an infinitive with <strong>to</strong>: decide, hope, plan, want. Some can take both with a change of meaning.</p>",
                [
                    ic("I enjoy [*reading|to read|read] before bed.", "Enjoy is followed by a gerund."),
                    ic("She decided [*to leave|leaving|leave to] early.", "Decide takes to + infinitive."),
                    ic("We avoid [*using|to use|use] plastic bags.", "Avoid takes a gerund."),
                    ic("He promised [*to call|calling|calls] me later.", "Promise takes an infinitive."),
                    ic("They suggested [*going|to go|go] by train.", "Suggest is followed by a gerund."),
                ],
                [
                    lg("I hope ____ from you soon.", "to hear", "hearing", "hear", "Hope takes an infinitive."),
                    lg("She finished ____ the kitchen before dinner.", "cleaning", "to clean", "clean", "Finish is followed by a gerund."),
                    lg("We agreed ____ outside the station.", "to meet", "meeting", "meet", "Agree takes an infinitive."),
                    lg("Do you mind ____ the window?", "opening", "to open", "open", "Mind takes a gerund."),
                ],
                [
                    ic("I would like [*to learn|learning|learn] Italian next year.", "Would like + infinitive."),
                    ic("He kept [*talking|to talk|talk] during the film.", "Keep + gerund."),
                    ic("They want [*to move|moving|move] to a bigger house.", "Want + infinitive."),
                    ic("She denied [*breaking|to break|break] the vase.", "Deny is followed by a gerund."),
                    ic("We plan [*to start|starting|start] earlier tomorrow.", "Plan + infinitive."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "conditionals-review",
            grammar_lesson(
                "Conditionals review",
                8,
                "<h2>Conditionals review</h2><p>Use the zero conditional for facts, the first conditional for real future possibilities, the second conditional for imaginary present or future situations, and the third conditional for unreal past situations.</p>",
                [
                    ic("If you heat water to 100C, it [*boils|will boil|would boil].", "Zero conditional for scientific facts."),
                    ic("If she studies hard, she [*will pass|would pass|passes] the exam.", "First conditional."),
                    ic("If I were taller, I [*would play|will play|played] basketball.", "Second conditional."),
                    ic("If they had left earlier, they [*would have caught|would catch|caught] the train.", "Third conditional."),
                    ic("If you [*press|will press|pressed] this button, the machine starts.", "Zero conditional."),
                ],
                [
                    lg("If I ____ more time, I would travel more.", "had", "have", "will have", "Second conditional if-clause."),
                    lg("If he had listened, he ____ that mistake.", "would not have made", "will not make", "did not make", "Third conditional result."),
                    lg("If the weather is nice, we ____ to the beach.", "will go", "would go", "go", "First conditional result."),
                    lg("If babies are hungry, they ____ .", "cry", "will cry", "would cry", "General truth."),
                ],
                [
                    ic("If I [*had known|knew|would know] about the meeting, I would have come.", "Third conditional."),
                    ic("We [*will stay|would stay|stayed] inside if the storm gets worse.", "First conditional."),
                    ic("If she [*were|was|is] more confident, she would speak in public.", "Second conditional form."),
                    ic("If you mix yellow and blue, you [*get|will get|would get] green.", "Zero conditional result."),
                    ic("They would be happier if they [*lived|live|had lived] closer to their family.", "Second conditional."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "reported-questions-and-commands",
            grammar_lesson(
                "Reported questions and commands",
                9,
                "<h2>Reported questions and commands</h2><p>In reported questions, we use statement word order and usually backshift the tense: <em>He asked where I lived.</em> For commands and requests, we use <strong>tell / ask + object + to + verb</strong>: <em>She told me to wait.</em></p>",
                [
                    ic("He asked me where I [*lived|live|did I live].", "Reported questions use statement word order."),
                    ic("She wanted to know if I [*had finished|finished|have finished] the report.", "Backshift after wanted to know."),
                    ic("The teacher told us [*to be|be|being] quiet.", "Tell + object + to + verb."),
                    ic("My mother asked me [*not to stay|to not stay|not stay] out late.", "Negative command: not to + verb."),
                    ic("They asked [*whether|that|to] we were ready.", "Whether or if introduces reported yes/no questions."),
                ],
                [
                    lg("He asked ____ I was late.", "why", "that", "to", "Why introduces an open question."),
                    lg("She told me ____ the door behind me.", "to lock", "locking", "lock", "Tell someone to do something."),
                    lg("The manager asked us ____ the customers.", "to call", "calling", "call", "Request or instruction."),
                    lg("I asked him ____ he needed any help.", "whether", "that", "what", "Whether for yes/no question."),
                ],
                [
                    ic("She asked me what time the train [*left|did leave|leaves].", "No question word order in reported speech."),
                    ic("He told the children [*not to run|to not run|not run] in the corridor.", "Negative command structure."),
                    ic("The doctor asked whether I [*was feeling|am feeling|felt to be] better.", "Backshifted form is natural."),
                    ic("We wanted to know where they [*had gone|did go|have gone].", "Backshift in reported question."),
                    ic("The note told visitors [*to switch off|switch off|switching off] their phones.", "To + infinitive after told."),
                ],
            ),
        )
    )
    out.append(
        (
            "grammar",
            "article-use-b1",
            grammar_lesson(
                "Articles: a, an, the, zero article",
                10,
                "<h2>Articles review</h2><p>Use <strong>a / an</strong> for one non-specific thing, <strong>the</strong> for something specific or already known, and no article for many plural or uncountable nouns in a general sense.</p>",
                [
                    ic("She bought [*a|the|zero] new laptop yesterday.", "A introduces one non-specific singular noun."),
                    ic("Can you close [*the|a|zero] window? It is cold.", "The because both speakers know which window."),
                    ic("[*Music|The music|A music] helps me relax.", "No article for music in general."),
                    ic("He is [*an|a|the] honest man.", "An before a vowel sound."),
                    ic("We visited [*the|a|zero] British Museum while we were in London.", "The with names like the British Museum."),
                ],
                [
                    lg("I need ____ advice about my CV.", "some", "an", "the", "Advice is uncountable and often takes no article or some."),
                    lg("They went to ____ school by bus.", "zero", "the", "a", "No article in the general expression go to school."),
                    lg("Could you pass me ____ salt, please?", "the", "a", "zero", "Specific object on the table."),
                    lg("She wants to become ____ engineer.", "an", "a", "the", "An before engineer."),
                ],
                [
                    ic("I saw [*a|the|zero] man outside your house, but I did not recognise him.", "First mention of man."),
                    ic("The man was carrying [*a|the|zero] umbrella.", "First mention of umbrella."),
                    ic("[*The|A|Zero] sun was setting when we arrived.", "The sun is unique."),
                    ic("Children should not spend all day on [*zero|the|a] social media.", "No article for social media in general."),
                    ic("She works in [*a|the|zero] hospital near the station.", "A hospital, one of many."),
                ],
            ),
        )
    )
    return out


def build_vocabulary() -> list[tuple[str, str, dict]]:
    out = []
    out.append(("vocabulary", "travel-and-holidays", vocab_lesson(
        "Travel and holidays",
        1,
        "<h2>Travel and holidays</h2><ul><li>accommodation: hostel, resort, campsite, guesthouse</li><li>travel words: delay, departure, luggage, boarding pass, platform</li><li>holiday verbs: explore, book, check in, set off</li></ul>",
        [
            lg("We stayed in a small ____. It was cheap but clean.", "guesthouse", "platform", "suitcase", "A guesthouse is a type of accommodation."),
            lg("The flight was cancelled because of a long ____.", "delay", "check-in", "resort", "Delay means waiting longer than planned."),
            lg("Please show your ____ before you enter the plane.", "boarding pass", "platform", "resort", "You need a boarding pass at the gate."),
            lg("They want to ____ the old town on foot.", "explore", "queue", "delay", "Explore means discover a place."),
        ],
        [
            dd("We need to ____ in online before the flight.", "check"),
            dd("Our train leaves from ____ 6.", "platform"),
            dd("Do not leave your ____ unattended.", "luggage"),
            dd("They are staying at a beach ____ this summer.", "resort"),
            dd("We decided to ____ a car to see the island.", "hire"),
        ],
        ["check", "platform", "luggage", "resort", "hire", "hostel", "departure", "passport", "excursion", "campsite"],
        [
            lg("The backpackers slept in a youth ____.", "hostel", "receipt", "forecast", "A hostel is cheap shared accommodation."),
            lg("We ____ at dawn to avoid the traffic.", "set off", "took off", "gave up", "Set off means start a journey."),
            lg("I booked an ____ to visit the caves.", "excursion", "arrival", "signal", "An excursion is a short organised trip."),
            lg("Our ____ time is 18:40.", "departure", "arrival gate", "boarding", "Departure is when you leave."),
        ],
    )))
    out.append(("vocabulary", "work-and-careers", vocab_lesson(
        "Work and careers",
        2,
        "<h2>Work and careers</h2><ul><li>workplace: deadline, shift, promotion, contract, training</li><li>people: applicant, employer, colleague, manager</li><li>verbs: apply, resign, negotiate, supervise</li></ul>",
        [
            lg("She got a ____, so now she manages a bigger team.", "promotion", "deadline", "contract", "A promotion is a move to a higher position."),
            lg("I work the night ____, from 10 p.m. to 6 a.m.", "shift", "training", "salary", "A shift is a set working period."),
            lg("He missed the project ____, and the client was unhappy.", "deadline", "promotion", "office", "A deadline is the latest time to finish something."),
            lg("You should ____ for the role before Friday.", "apply", "retire", "supervise", "Apply for a job."),
        ],
        [
            dd("She signed a two-year ____ with the company.", "contract"),
            dd("Our ____ wants the report by noon.", "manager"),
            dd("The company offers safety ____ for new staff.", "training"),
            dd("He decided to ____ because he had found a better job.", "resign"),
            dd("The best ____ had relevant experience and strong references.", "applicant"),
        ],
        ["contract", "manager", "training", "resign", "applicant", "salary", "employer", "bonus", "colleague", "vacancy"],
        [
            lg("The ____ offered her a flexible schedule.", "employer", "employee", "applicant", "Employer = company or boss."),
            lg("He earns a good ____, but he works long hours.", "salary", "shift", "vacancy", "Salary = regular pay."),
            lg("A job ____ appeared on the company website this morning.", "vacancy", "deadline", "supervisor", "Vacancy = open position."),
            lg("My closest ____ helped me learn the new system.", "colleague", "employer", "contract", "Colleague = coworker."),
        ],
    )))
    out.append(("vocabulary", "technology-and-media", vocab_lesson(
        "Technology and media",
        3,
        "<h2>Technology and media</h2><ul><li>digital words: device, update, password, privacy, account</li><li>media words: headline, article, channel, broadcast, documentary</li><li>verbs: stream, upload, subscribe, scroll</li></ul>",
        [
            lg("Remember to install the latest security ____.", "update", "channel", "documentary", "Software update."),
            lg("I changed my social media ____ after the hack.", "password", "headline", "scroll", "Password protects your account."),
            lg("We watched a nature ____ last night.", "documentary", "account", "privacy", "A documentary is factual TV or film."),
            lg("She likes to ____ music instead of downloading it.", "stream", "scroll", "print", "Stream audio online."),
        ],
        [
            dd("This newspaper ____ sounds surprising, but the article is more balanced.", "headline"),
            dd("Please do not share your banking ____ with anyone.", "details"),
            dd("I ____ to that science channel on YouTube.", "subscribe"),
            dd("The company promised to improve user ____.", "privacy"),
            dd("He spent an hour ____ through short videos.", "scrolling"),
        ],
        ["headline", "details", "subscribe", "privacy", "scrolling", "account", "broadcast", "device", "article", "editor"],
        [
            lg("The football match will be ____ live at 8 p.m.", "broadcast", "uploaded", "streamed off", "Broadcast means sent on TV or radio."),
            lg("I read an interesting ____ about climate change.", "article", "device", "network", "Article = written text in a paper or online."),
            lg("This ____ is too old to run the new app.", "device", "headline", "broadcast", "A phone or tablet is a device."),
            lg("Log out of your ____ when you use a public computer.", "account", "scroll", "documentary", "Account = personal online profile."),
        ],
    )))
    out.append(("vocabulary", "health-and-lifestyle", vocab_lesson(
        "Health and lifestyle",
        4,
        "<h2>Health and lifestyle</h2><ul><li>health words: symptoms, treatment, recovery, balanced diet, stress</li><li>verbs: recover, improve, avoid, stretch</li><li>phrases: get enough sleep, stay hydrated</li></ul>",
        [
            lg("A doctor looked at my ____ and said it was probably flu.", "symptoms", "contract", "headline", "Symptoms are signs of illness."),
            lg("Walking every day can ____ your mood.", "improve", "delay", "broadcast", "Improve means make better."),
            lg("She needs more time for ____ after the operation.", "recovery", "privacy", "training", "Recovery = time to get better."),
            lg("A ____ includes fruit, vegetables and protein.", "balanced diet", "screen time", "deadline", "Balanced diet = healthy eating."),
        ],
        [
            dd("Too much ____ at work can make you tired and irritable.", "stress"),
            dd("The doctor recommended a new ____ for his back pain.", "treatment"),
            dd("You should ____ before running to protect your muscles.", "stretch"),
            dd("Try to ____ sugary drinks if you want more energy.", "avoid"),
            dd("Athletes need to ____ during hot weather.", "stay hydrated"),
        ],
        ["stress", "treatment", "stretch", "avoid", "stay hydrated", "recover", "sleep", "habit", "vitamin", "routine"],
        [
            lg("It took her a month to fully ____ from the virus.", "recover", "improve", "avoid", "Recover from an illness."),
            lg("You should try to get ____ sleep every night.", "enough", "balanced", "hydrated", "Common phrase: get enough sleep."),
            lg("This exercise has become a healthy ____.", "habit", "symptom", "treatment", "Habit = repeated behaviour."),
            lg("Citrus fruit contains a lot of vitamin ____. ", "C", "D", "B12", "Vitamin C is common in citrus fruit."),
        ],
    )))
    out.append(("vocabulary", "crime-and-law", vocab_lesson(
        "Crime and law",
        5,
        "<h2>Crime and law</h2><ul><li>crime words: theft, robbery, suspect, witness, evidence</li><li>legal words: judge, lawyer, court, prison, fine</li><li>verbs: steal, arrest, accuse, sentence</li></ul>",
        [
            lg("The police found enough ____ to continue the investigation.", "evidence", "headline", "vacancy", "Evidence supports a case."),
            lg("A ____ saw the accident and called emergency services.", "witness", "judge", "suspect", "A witness sees an event."),
            lg("The shop was closed after a violent ____.", "robbery", "promotion", "documentary", "Robbery involves stealing with force."),
            lg("The officer decided to ____ the man at the scene.", "arrest", "broadcast", "resign", "Arrest = take into police custody."),
        ],
        [
            dd("The ____ listened to both sides before making a decision.", "judge"),
            dd("He had to pay a large ____ for parking illegally.", "fine"),
            dd("A defence ____ represented the accused man.", "lawyer"),
            dd("The police questioned the main ____ all afternoon.", "suspect"),
            dd("She was found guilty in ____.", "court"),
        ],
        ["judge", "fine", "lawyer", "suspect", "court", "prison", "theft", "crime", "sentence", "evidence"],
        [
            lg("He went to ____ for six months.", "prison", "court", "evidence", "Prison is where criminals are kept."),
            lg("Bike ____ has increased in the area recently.", "theft", "witness", "sentence", "Theft = stealing."),
            lg("The judge will ____ the defendant tomorrow.", "sentence", "steal", "delay", "Sentence = give punishment."),
            lg("She was accused of a serious ____. ", "crime", "contract", "routine", "Crime = illegal act."),
        ],
    )))
    out.append(("vocabulary", "education-and-learning", vocab_lesson(
        "Education and learning",
        6,
        "<h2>Education and learning</h2><ul><li>study words: assignment, revision, scholarship, attendance, qualification</li><li>verbs: revise, memorise, concentrate, submit</li><li>phrases: take notes, hand in work</li></ul>",
        [
            lg("I need to finish this history ____ by tomorrow.", "assignment", "recovery", "documentary", "Assignment = piece of work."),
            lg("She won a ____ to study abroad.", "scholarship", "promotion", "symptom", "Scholarship = financial support."),
            lg("Good ____ is important if you want to understand lectures.", "concentration", "evidence", "crime", "Concentration means focused attention."),
            lg("Please ____ your essay before midnight.", "submit", "stream", "sentence", "Submit = formally hand in."),
        ],
        [
            dd("I usually ____ my notes before an exam.", "revise"),
            dd("The university checks student ____ every week.", "attendance"),
            dd("He wrote down key ideas so he could ____ notes later.", "review"),
            dd("This course gives you a recognised ____.", "qualification"),
            dd("It is easier to learn when you actively ____ with the material.", "engage"),
        ],
        ["revise", "attendance", "review", "qualification", "engage", "memorise", "lecture", "assignment", "scholarship", "deadline"],
        [
            lg("Some students try to ____ whole paragraphs word for word.", "memorise", "delay", "resign", "Memorise = learn by heart."),
            lg("The professor gave an interesting ____ on climate policy.", "lecture", "attendance", "signal", "Lecture = formal talk."),
            lg("You should ____ your homework on time.", "hand in", "set off", "grow up", "Hand in = give to the teacher."),
            lg("I cannot ____ when the room is noisy.", "concentrate", "broadcast", "decorate", "Concentrate = focus."),
        ],
    )))
    out.append(("vocabulary", "environment-and-climate", vocab_lesson(
        "Environment and climate",
        7,
        "<h2>Environment and climate</h2><ul><li>climate words: drought, flood, emissions, renewable energy, habitat</li><li>verbs: reduce, protect, recycle, conserve</li><li>phrases: carbon footprint, global warming</li></ul>",
        [
            lg("This region often suffers from summer ____ because it hardly rains.", "drought", "flood", "breeze", "Drought = long period without rain."),
            lg("Factories are trying to reduce carbon ____.", "emissions", "habitats", "witnesses", "Emissions are gases released into the air."),
            lg("Solar and wind are forms of ____ energy.", "renewable", "delayed", "furnished", "Renewable energy can be replaced naturally."),
            lg("We should ____ natural habitats for wild animals.", "protect", "broadcast", "promote", "Protect habitats."),
        ],
        [
            dd("Heavy rain caused a serious ____ in the village.", "flood"),
            dd("Riding a bike can lower your carbon ____.", "footprint"),
            dd("National parks help ____ rare species.", "conserve"),
            dd("Global ____ is changing weather patterns worldwide.", "warming"),
            dd("Many birds lose their ____ when forests disappear.", "habitat"),
        ],
        ["flood", "footprint", "conserve", "warming", "habitat", "recycle", "pollution", "renewable", "plastic", "drought"],
        [
            lg("Try to ____ glass, paper and metal whenever possible.", "recycle", "delay", "resign", "Recycle materials."),
            lg("Air ____ can damage human health.", "pollution", "promotion", "qualification", "Pollution affects air quality."),
            lg("We need to cut down on single-use ____.", "plastic", "lecture", "receipt", "Plastic waste is a major issue."),
            lg("A long ____ damaged farmers' crops this year.", "drought", "storm", "bargain", "Drought affects crops."),
        ],
    )))
    out.append(("vocabulary", "relationships-and-emotions", vocab_lesson(
        "Relationships and emotions",
        8,
        "<h2>Relationships and emotions</h2><ul><li>relationship words: trust, argument, support, respect, misunderstanding</li><li>emotions: relieved, embarrassed, jealous, proud, anxious</li><li>verbs: upset, forgive, encourage, disappoint</li></ul>",
        [
            lg("A good friendship is built on mutual ____.", "trust", "evidence", "schedule", "Trust is essential in relationships."),
            lg("I felt really ____ after passing my driving test.", "relieved", "guilty", "delayed", "Relieved = less worried after something ends."),
            lg("They had an ____ about money but solved it calmly.", "argument", "update", "promotion", "Argument = disagreement."),
            lg("Her parents always ____ her to keep trying.", "encourage", "sentence", "arrest", "Encourage = give support."),
        ],
        [
            dd("He felt ____ when he forgot his best friend's birthday.", "embarrassed"),
            dd("She was very ____ of her daughter after the performance.", "proud"),
            dd("A simple ____ caused the whole problem.", "misunderstanding"),
            dd("If someone hurts you, it can be hard to ____ them.", "forgive"),
            dd("My friends gave me a lot of ____ when I moved house.", "support"),
        ],
        ["embarrassed", "proud", "misunderstanding", "forgive", "support", "respect", "anxious", "jealous", "trust", "encourage"],
        [
            lg("You should show ____ for other people's opinions.", "respect", "flood", "device", "Respect matters in relationships."),
            lg("He felt ____ before the interview and could not relax.", "anxious", "proud", "renewable", "Anxious = worried."),
            lg("Some children get ____ when a new baby arrives.", "jealous", "balanced", "furnished", "Jealous about attention."),
            lg("The bad news really ____ her.", "upset", "updated", "revised", "Upset = make sad or worried."),
        ],
    )))
    return out


def build_listening() -> list[tuple[str, str, dict]]:
    return [
        ("listening", "moving-house", skill_lesson(
            "Moving house",
            "listening",
            1,
            "<h2>Moving house</h2><p>Listen to two friends talking about a recent move.</p><h3>Transcript</h3><p><strong>Sam:</strong> How is the new flat?<br><strong>Nina:</strong> Much better than the old one. It is closer to work, but it is smaller.<br><strong>Sam:</strong> Was it difficult to move?<br><strong>Nina:</strong> Yes, especially carrying the boxes up three flights of stairs. But the neighbours were friendly and helped us.</p>",
            [
                ic("Nina says the new flat is [*closer to work|bigger|more expensive].", "She says it is closer to work."),
                ic("The new flat is [*smaller|larger|farther away].", "She says it is smaller."),
                ic("Moving was difficult because of the [*stairs|weather|traffic].", "They had to carry boxes upstairs."),
                ic("The neighbours were [*friendly|noisy|angry].", "They helped with the move."),
            ],
            [
                lg("Nina thinks the new flat is ____ than the old one.", "better", "worse", "older", "She says it is much better."),
                lg("They carried the boxes up three flights of ____. ", "stairs", "lifts", "roads", "The boxes went up the stairs."),
                lg("The neighbours ____ them with the move.", "helped", "ignored", "phoned", "They were helpful."),
                lg("The move was difficult, ____.", "especially carrying boxes", "especially finding work", "especially buying furniture", "That was the hardest part."),
            ],
            [
                ic("The conversation is mainly about [*a recent move|a holiday|a job interview].", "They discuss a new flat."),
                ic("Nina compares the new flat with the [*old one|next one|office].", "She compares it with the old flat."),
                ic("Sam asks whether it was [*difficult|cheap|safe] to move.", "That is his second question."),
                ic("The tone is [*positive overall|completely negative|formal].", "Despite the difficulties, Nina likes the new flat."),
            ],
            "https://www.youtube.com/watch?v=8O6272q0Awo",
        )),
        ("listening", "missing-luggage", skill_lesson(
            "Missing luggage",
            "listening",
            2,
            "<h2>Missing luggage</h2><p>Listen to a passenger reporting a problem at the airport.</p><h3>Transcript</h3><p><strong>Passenger:</strong> Excuse me, my suitcase did not arrive on the belt.<br><strong>Agent:</strong> I am sorry to hear that. Can I see your baggage tag?<br><strong>Passenger:</strong> Yes, here it is. It is a large black case with a red ribbon.<br><strong>Agent:</strong> We will track it and contact you as soon as possible.</p>",
            [
                ic("The missing item is a [*suitcase|passport|laptop].", "The passenger mentions a suitcase."),
                ic("The suitcase is [*black|blue|red].", "It is a large black case."),
                ic("It has a [*red ribbon|yellow sticker|green strap].", "Red ribbon."),
                ic("The agent says they will [*track it|replace it immediately|call the police].", "They will track the suitcase."),
            ],
            [
                lg("The suitcase did not arrive on the ____. ", "belt", "platform", "shelf", "Suitcases arrive on the baggage belt."),
                lg("The agent asks to see the baggage ____. ", "tag", "receipt", "signal", "You use a baggage tag to identify luggage."),
                lg("The case is described as large and ____. ", "black", "heavy", "silver", "The suitcase is black."),
                lg("The airline will contact the passenger as soon as ____. ", "possible", "tomorrow", "check-in", "Common phrase: as soon as possible."),
            ],
            [
                ic("This conversation happens at [*an airport|a hotel|a station].", "Baggage belt and baggage tag show the location."),
                ic("The passenger sounds [*calm but worried|angry and rude|happy].", "They politely explain the issue."),
                ic("The agent offers [*help|a free ticket|food].", "The agent will track the bag."),
                ic("The problem was noticed after the flight had [*arrived|left|been cancelled].", "The bag did not come out after arrival."),
            ],
            "https://www.youtube.com/watch?v=4jpdlG8EJhE",
        )),
        ("listening", "office-presentation", skill_lesson(
            "Office presentation",
            "listening",
            3,
            "<h2>Office presentation</h2><p>Listen to a manager speaking before a team presentation.</p><h3>Transcript</h3><p><strong>Manager:</strong> Thanks for coming. Our client wants a short presentation on Friday. Anna, can you prepare the sales figures? Mark, please update the slides. We only have two days, so we need to work efficiently. If we finish by Thursday afternoon, we can practise once before the meeting.</p>",
            [
                ic("The presentation is for [*a client|new employees|investors only].", "The manager says our client wants it."),
                ic("The presentation is on [*Friday|Thursday|Monday].", "It is on Friday."),
                ic("Anna must prepare the [*sales figures|slides|room].", "She is asked to prepare the sales figures."),
                ic("The team has [*two days|one week|one day] to work on it.", "We only have two days."),
            ],
            [
                lg("Mark is asked to update the ____. ", "slides", "client", "figures", "He has to update the slides."),
                lg("The team should work ____. ", "efficiently", "quietly", "late", "The manager uses the word efficiently."),
                lg("If they finish by Thursday afternoon, they can ____. ", "practise once", "go home early", "meet the client", "The manager mentions one practice run."),
                lg("The manager begins by saying ____. ", "thanks for coming", "please sit down quietly", "who is absent", "Those are the opening words."),
            ],
            [
                ic("The tone of the manager is [*organised and practical|angry and impatient|confused].", "The instructions are clear and structured."),
                ic("The team wants time to [*practise|travel|eat lunch] before the meeting.", "They can practise once."),
                ic("The presentation is described as [*short|informal|optional].", "The client wants a short presentation."),
                ic("The meeting will happen after they have [*prepared the material|met the client already|changed departments].", "They need to prepare first."),
            ],
            "https://www.youtube.com/watch?v=7y_hbz6lM9E",
        )),
        ("listening", "doctor-appointment-b1", skill_lesson(
            "Doctor appointment",
            "listening",
            4,
            "<h2>Doctor appointment</h2><p>Listen to a patient talking to a doctor.</p><h3>Transcript</h3><p><strong>Doctor:</strong> How long have you had the pain?<br><strong>Patient:</strong> For about ten days. It started after I helped a friend move house.<br><strong>Doctor:</strong> Does it hurt all the time?<br><strong>Patient:</strong> Mostly in the morning. It gets better when I walk around.<br><strong>Doctor:</strong> I think you have strained a muscle. I will prescribe painkillers and some rest.</p>",
            [
                ic("The patient has had the pain for [*about ten days|ten weeks|two days].", "The patient says about ten days."),
                ic("The pain started after [*helping a friend move|playing football|driving to work].", "It started after moving house."),
                ic("It hurts most in the [*morning|evening|night].", "Mostly in the morning."),
                ic("The doctor thinks it is [*a strained muscle|a broken bone|the flu].", "That is the diagnosis."),
            ],
            [
                lg("The pain gets better when the patient ____. ", "walks around", "sits down", "goes to sleep", "Movement helps."),
                lg("The doctor will prescribe ____. ", "painkillers", "antibiotics", "exercise equipment", "The doctor mentions painkillers."),
                lg("The pain started after helping a friend move ____. ", "house", "office", "furniture shop", "Move house."),
                lg("The doctor also recommends some ____. ", "rest", "travel", "surgery", "Rest is recommended."),
            ],
            [
                ic("The patient probably has [*a minor injury|a serious infection|food poisoning].", "A strained muscle is a minor injury."),
                ic("The doctor asks about the [*duration|cost|address] of the pain first.", "How long have you had the pain?"),
                ic("The patient says the pain is [*not constant|constant|gone].", "Mostly in the morning, so not constant."),
                ic("The conversation is [*medical|legal|social].", "It is a doctor appointment."),
            ],
            "https://www.youtube.com/watch?v=fSrLeyfk9SM",
        )),
        ("listening", "weekend-radio-show", skill_lesson(
            "Weekend radio show",
            "listening",
            5,
            "<h2>Weekend radio show</h2><p>Listen to a short radio introduction.</p><h3>Transcript</h3><p><strong>Presenter:</strong> Good morning and welcome back to City Weekend. In today's programme, we will speak to a local chef about affordable meals, review a new exhibition at the art gallery, and hear listeners' tips for saving money while travelling. Stay with us after the break for a live interview with a young musician from Manchester.</p>",
            [
                ic("The programme will speak to [*a local chef|a doctor|a football coach].", "The presenter mentions a local chef."),
                ic("There will be a review of [*an exhibition|a film|a train station].", "A new exhibition at the art gallery."),
                ic("Listeners will share tips about [*saving money while travelling|buying houses|studying abroad].", "Travel money-saving tips."),
                ic("The final live interview is with [*a young musician|a teacher|an actor].", "A young musician from Manchester."),
            ],
            [
                lg("The show is called City ____. ", "Weekend", "Morning", "Travel", "City Weekend is the programme title."),
                lg("The chef talks about ____ meals.", "affordable", "healthy only", "luxury", "Affordable meals."),
                lg("The interview with the musician is after the ____. ", "break", "gallery", "news", "After the break."),
                lg("The gallery exhibition is described as ____. ", "new", "closing", "international", "It is a new exhibition."),
            ],
            [
                ic("The programme is probably on [*radio|television only|a podcast with no host].", "The style is a radio introduction."),
                ic("The presenter uses the word [*welcome|goodbye|sorry] near the start.", "Good morning and welcome back."),
                ic("The topics are [*varied|all about sport|all political].", "Food, art, travel, music."),
                ic("The tone is [*friendly and informative|formal and legal|negative].", "Friendly radio tone."),
            ],
            "https://www.youtube.com/watch?v=HwMkN_2BTqs",
        )),
    ]


def build_reading() -> list[tuple[str, str, dict]]:
    return [
        ("reading", "remote-work-trend", skill_lesson(
            "The rise of remote work",
            "reading",
            1,
            "<h2>The rise of remote work</h2><p>In the past, most office workers had to travel to work every day. Today, many companies allow at least part of the week to be spent working from home. Supporters say remote work saves time, reduces commuting stress and helps people balance family life with work. However, critics argue that it can make teamwork harder and may leave some people feeling isolated. Experts suggest that the most successful companies combine flexible working with regular face-to-face meetings.</p>",
            [
                ic("Remote work can reduce [*commuting stress|holiday costs|crime].", "The text mentions commuting stress."),
                ic("Some critics believe remote work makes [*teamwork harder|pay higher|cities quieter].", "That is one criticism."),
                ic("Workers may feel [*isolated|more athletic|richer] when working remotely.", "Isolation is mentioned."),
                ic("Experts recommend combining flexibility with [*face-to-face meetings|shorter holidays|more travel].", "That is the suggested solution."),
            ],
            [
                lg("In the past, most office workers had to ____ to work every day.", "travel", "apply", "retire", "They had to travel in daily."),
                lg("Remote work can help people ____ family life with work.", "balance", "replace", "cancel", "Balance family life with work."),
                lg("The most successful companies often use a ____ approach.", "mixed", "silent", "strictly remote only", "The text supports a combination."),
                lg("The article presents both ____ and disadvantages.", "benefits", "broadcasts", "platforms", "It gives both sides."),
            ],
            [
                ic("The main purpose of the text is to [*discuss a trend|sell software|describe one employee].", "It discusses remote work in general."),
                ic("The writer sounds [*balanced|angry|completely negative].", "Both benefits and drawbacks are shown."),
                ic("Remote work is presented as [*popular but not perfect|impossible for most jobs|only useful for managers].", "That summarises the passage."),
                ic("The passage is mainly about [*working life|sport|medicine].", "It focuses on work."),
            ],
        )),
        ("reading", "community-garden", skill_lesson(
            "The community garden project",
            "reading",
            2,
            "<h2>The community garden project</h2><p>Two years ago, an empty piece of land behind the library was turned into a community garden. At first, only a few volunteers joined the project, but now more than fifty local residents help there every month. The garden produces vegetables, herbs and flowers, and local schools sometimes bring children to learn about nature. Organisers say the project has improved the area because neighbours now know each other better and spend more time outdoors.</p>",
            [
                ic("The garden was created [*behind the library|next to a school|on a farm].", "It was behind the library."),
                ic("At first, only [*a few volunteers|fifty residents|schoolchildren] joined.", "Only a few volunteers at first."),
                ic("The garden grows [*vegetables, herbs and flowers|only trees|fruit only].", "These three are listed."),
                ic("The project has helped neighbours [*know each other better|move away|work indoors].", "That is one social benefit."),
            ],
            [
                lg("The land used to be ____ before the project began.", "empty", "busy", "private farmland", "It was an empty piece of land."),
                lg("More than fifty residents help there every ____. ", "month", "day", "year", "Every month."),
                lg("Schools bring children to learn about ____. ", "nature", "law", "history", "The visits are educational."),
                lg("The organisers think the project has improved the ____. ", "area", "weather", "budget", "It improved the local area."),
            ],
            [
                ic("The text suggests the project has both [*social and environmental benefits|financial losses only|no educational value].", "It mentions community and nature learning."),
                ic("The number of volunteers has [*grown|fallen|stayed the same].", "From a few to over fifty."),
                ic("The garden is an example of a [*local initiative|national law|private company].", "It is a community project."),
                ic("The tone of the text is [*positive|critical|uncertain].", "The project is described positively."),
            ],
        )),
        ("reading", "second-hand-shopping", skill_lesson(
            "Why second-hand shopping is growing",
            "reading",
            3,
            "<h2>Why second-hand shopping is growing</h2><p>Buying second-hand clothes and furniture used to be seen by some people as a last resort. Today, it has become much more popular, especially among younger consumers. Some shoppers want to save money, while others are trying to reduce waste and avoid fast fashion. Online marketplaces have also made it easier to find unusual items in good condition. For many people, second-hand shopping now feels both practical and environmentally responsible.</p>",
            [
                ic("Second-hand shopping is especially popular among [*younger consumers|retired doctors|small children].", "The text says younger consumers."),
                ic("People buy second-hand items partly to [*save money|travel faster|learn history].", "Saving money is one reason."),
                ic("Online marketplaces make it easier to find [*unusual items|new food|jobs].", "Unusual items in good condition."),
                ic("The text links second-hand shopping with [*reducing waste|more pollution|higher salaries].", "Environmental responsibility is highlighted."),
            ],
            [
                lg("Second-hand shopping used to be seen as a last ____. ", "resort", "minute", "chance sale", "That phrase appears in the text."),
                lg("Some people want to avoid fast ____. ", "fashion", "service", "shopping bag", "Fast fashion is mentioned."),
                lg("Items can often be found in good ____. ", "condition", "salary", "attendance", "Good condition."),
                lg("For many people, second-hand shopping is practical and environmentally ____. ", "responsible", "delayed", "formal", "Environmentally responsible."),
            ],
            [
                ic("The passage mainly explains [*reasons for a trend|how to open a shop|why furniture is expensive].", "It explains why second-hand shopping is growing."),
                ic("The writer's attitude seems [*supportive|mocking|confused].", "The final sentence is positive."),
                ic("The text mentions both [*financial and environmental motives|only fashion advice|only charity work].", "Both motives appear."),
                ic("The trend is described as [*more common than before|almost finished|limited to one city].", "It has become much more popular."),
            ],
        )),
        ("reading", "teen-volunteer-project", skill_lesson(
            "A teenage volunteer project",
            "reading",
            4,
            "<h2>A teenage volunteer project</h2><p>Last summer, a group of teenagers in Bristol decided to spend their school holiday helping older people in their neighbourhood. They did small jobs such as carrying shopping, tidying gardens and teaching basic smartphone skills. At the end of the programme, both the volunteers and the residents said they had learned a lot from each other. Several teenagers even decided to continue volunteering during the school year because the experience had made them more confident.</p>",
            [
                ic("The volunteers helped [*older people|tourists|their teachers].", "They helped older people in the neighbourhood."),
                ic("One of the tasks was teaching [*smartphone skills|driving|cooking].", "Basic smartphone skills."),
                ic("The project took place during the [*summer holiday|winter term|weekend only].", "Last summer during the school holiday."),
                ic("Some teenagers continued because they felt more [*confident|famous|wealthy].", "The experience made them more confident."),
            ],
            [
                lg("The teenagers carried shopping and tidied ____. ", "gardens", "platforms", "resorts", "They tidied gardens."),
                lg("At the end, both groups said they had learned from ____ other.", "each", "one", "all", "Each other is the phrase used."),
                lg("Several students chose to continue ____ during the school year.", "volunteering", "travelling", "teaching maths", "They continued volunteering."),
                lg("The project happened in ____. ", "Bristol", "London", "Leeds", "The city is Bristol."),
            ],
            [
                ic("The text focuses on the [*benefits of volunteering|problems with smartphones|cost of holidays].", "It is about a volunteer project."),
                ic("The relationship between volunteers and residents is shown as [*mutually helpful|tense|formal and distant].", "They learned from each other."),
                ic("The passage is [*mainly positive|mainly negative|unclear].", "The outcome is positive."),
                ic("The volunteers worked with people from their own [*neighbourhood|country only|workplace].", "Their neighbourhood."),
            ],
        )),
        ("reading", "city-bike-scheme", skill_lesson(
            "The city bike scheme",
            "reading",
            5,
            "<h2>The city bike scheme</h2><p>Three years ago, the city council introduced a bike-sharing scheme to reduce traffic and improve air quality. At first, residents were uncertain whether people would use it, but the number of journeys has increased every year. Users unlock bikes with a mobile app and can leave them at stations across the city. Although some people still prefer cars, the scheme has helped many commuters travel more cheaply and quickly, especially during rush hour.</p>",
            [
                ic("The bike scheme was introduced to reduce [*traffic|crime|noise from concerts].", "Traffic reduction is one aim."),
                ic("Users unlock bikes with [*a mobile app|a paper ticket|cash].", "They use a mobile app."),
                ic("The number of journeys has [*increased|fallen|stayed the same].", "It has increased every year."),
                ic("The scheme is especially useful during [*rush hour|holidays|the night].", "Rush hour is mentioned."),
            ],
            [
                lg("The city council introduced the scheme ____ years ago.", "three", "two", "five", "The text says three years ago."),
                lg("People can leave bikes at stations across the ____. ", "city", "country", "road", "The stations are across the city."),
                lg("At first, some residents were ____. ", "uncertain", "enthusiastic", "angry", "They were uncertain whether it would work."),
                lg("The scheme helps people travel more cheaply and ____. ", "quickly", "carefully", "politely", "More cheaply and quickly."),
            ],
            [
                ic("The text is about [*public transport innovation|a sports competition|road safety laws only].", "It describes a bike-sharing scheme."),
                ic("The writer presents the scheme as [*largely successful|a complete failure|too expensive to continue].", "Use has increased every year."),
                ic("The scheme affects both [*transport and air quality|education and housing|law and crime].", "Both aims are mentioned."),
                ic("Some people still [*prefer cars|do not own phones|avoid commuting].", "The passage notes that some still prefer cars."),
            ],
        )),
    ]


def build_use_of_english() -> list[tuple[str, str, dict]]:
    return [
        ("use-of-english", "test-1", skill_lesson(
            "Use of English - Test 1",
            "use-of-english",
            1,
            "<h2>Use of English - B1 Test 1</h2><p>Mixed grammar and vocabulary review.</p>",
            [
                ic("I [*have been working|worked|am working] here since 2019.", "Present perfect continuous for duration."),
                ic("If I had seen the message, I [*would have replied|would reply|replied] sooner.", "Third conditional."),
                ic("The report [*was written|wrote|was writing] by our team leader.", "Passive form."),
                ic("She suggested [*meeting|to meet|meet] after work.", "Suggest takes a gerund."),
            ],
            [
                lg("He told me ____ be late.", "not to", "to not", "not", "Reported command."),
                lg("This is the woman ____ brother works with me.", "whose", "who", "where", "Whose for possession."),
                lg("You do not have to come, but you ____ let me know.", "should", "mustn't", "would", "Advice."),
                lg("We ran ____ of coffee this morning.", "out", "up", "off", "Phrasal verb run out of."),
            ],
            [
                ic("I do not mind [*waiting|to wait|wait] a few more minutes.", "Mind takes a gerund."),
                ic("The shop gave me a full [*refund|broadcast|promotion] after the complaint.", "Refund fits the context."),
                ic("By the time we arrived, the film [*had started|started|has started].", "Past perfect."),
                ic("If he [*were|was|is] more organised, he would miss fewer deadlines.", "Second conditional."),
            ],
        )),
        ("use-of-english", "test-2", skill_lesson(
            "Use of English - Test 2",
            "use-of-english",
            2,
            "<h2>Use of English - B1 Test 2</h2><p>More mixed B1 practice.</p>",
            [
                ic("She asked me where I [*had bought|did buy|have bought] the jacket.", "Reported question with backshift."),
                ic("This app is [*more reliable|reliabler|most reliable] than the old one.", "Comparative long adjective."),
                ic("We [*used to live|were used to live|use to living] near the station.", "Used to for past state."),
                ic("You [*mustn't|don't have to|shouldn't to] use your phone during the exam.", "Mustn't for prohibition."),
            ],
            [
                lg("He promised ____ me as soon as he arrived.", "to call", "calling", "call", "Promise + infinitive."),
                lg("I know the café ____ serves excellent coffee.", "which", "where", "whose", "Which for things."),
                lg("The weather was awful, but we ____ managed to finish the walk.", "still", "yet", "already", "Still works in this sentence."),
                lg("She has been studying ____ six o'clock.", "since", "for", "during", "Since for a starting point."),
            ],
            [
                ic("The city has introduced a bike scheme to reduce [*traffic|lecture|trust].", "Traffic fits the context."),
                ic("I [*would not have gone|did not go|would not go] there if I had known the truth.", "Third conditional."),
                ic("They [*have never travelled|never travelled|are never travelling] abroad before.", "Present perfect for experience."),
                ic("He needs to [*hand in|set off|grow up] the assignment by Friday.", "Hand in homework."),
            ],
        )),
        ("use-of-english", "test-3", skill_lesson(
            "Use of English - Test 3",
            "use-of-english",
            3,
            "<h2>Use of English - B1 Test 3</h2><p>Final B1 mixed review.</p>",
            [
                ic("The museum [*was opened|opened by|was opening] in 1890.", "Passive form."),
                ic("If you [*had listened|listened|would listen], you would have understood.", "Third conditional if-clause."),
                ic("She avoids [*eating|to eat|eat] dairy products.", "Avoid takes a gerund."),
                ic("I think they [*will probably arrive|probably arrive will|arrive probably] late.", "Natural future order."),
            ],
            [
                lg("We have lived here ____ more than ten years.", "for", "since", "from", "For + period."),
                lg("The woman ____ spoke to you is our new manager.", "who", "whose", "where", "Who for person."),
                lg("You do not need a ticket, but you ____ reserve a seat online.", "can", "mustn't", "had to", "Can for possibility/option."),
                lg("My phone battery had run ____ before I got home.", "out", "off", "away", "Run out = finish."),
            ],
            [
                ic("He said he [*would help|will help|helps] us the next day.", "Reported speech."),
                ic("This route is [*less crowded|more fewer crowded|the less crowded] than the motorway.", "Correct comparative structure."),
                ic("The suitcase did not arrive, so the airline promised to [*track|book|resign] it.", "Track luggage."),
                ic("I [*had been waiting|waited|was waited] for over an hour when she finally called.", "Past perfect continuous context."),
            ],
        )),
    ]


def build_writing() -> list[tuple[str, str, dict]]:
    return [
        ("writing", "opinion-paragraph", skill_lesson(
            "Writing an opinion paragraph",
            "writing",
            1,
            "<h2>Writing an opinion paragraph</h2><p>At B1 level, an opinion paragraph should include a clear point, one or two supporting reasons, and a short conclusion.</p><ul><li>Opening: <em>In my opinion, ...</em></li><li>Support: <em>Firstly, ... Secondly, ...</em></li><li>Conclusion: <em>For these reasons, ...</em></li></ul>",
            [
                ic("[*In my opinion, online learning can be very effective.|My opinion online learning very effective.|Online learning, I opinion effective.]", "Clear opinion opening."),
                ic("[*Firstly, it is flexible and saves travel time.|First, flexible and save travel.|Firstly is flexible save travel.]", "A full supporting sentence."),
                ic("[*For these reasons, I believe schools should offer both options.|These reasons schools both options.|Because these reasons schools.]", "Strong concluding sentence."),
                ic("[*However, some students learn better in a classroom.|However some students better classroom.|However, classroom better some students.]", "Balanced linking sentence."),
            ],
            [
                lg("A paragraph should have one clear main ____. ", "idea", "shift", "refund", "Good paragraphs focus on one main idea."),
                lg("Use linking words such as firstly, ____, and however.", "secondly", "finally only", "meanwhile not", "Secondly is a common linker."),
                lg("Support your opinion with clear ____. ", "reasons", "platforms", "witnesses", "Reasons explain your point."),
                lg("A short conclusion should ____ the main idea.", "summarise", "ignore", "copy", "Conclusions summarise."),
            ],
            [
                ic("[*On the one hand, social media helps us stay in touch.|One hand social media stay touch.|Social media one hand touch.]", "Correct discussion phrase."),
                ic("[*For example, students can revise using videos.|For example students can revising videos.|Example students revise using.]", "Good example sentence."),
                ic("[*I agree to some extent, but there are disadvantages too.|I agree some extent but disadvantages too are.|Agree some extent disadvantages.]", "Balanced B1 expression."),
                ic("[*As a result, many people prefer working from home.|As result many people prefering home work.|Result many home.]", "As a result introduces consequence."),
            ],
        )),
        ("writing", "email-of-complaint", skill_lesson(
            "Writing an email of complaint",
            "writing",
            2,
            "<h2>Writing an email of complaint</h2><p>A good complaint email is polite, clear and specific.</p><ul><li>State what happened.</li><li>Explain the problem.</li><li>Say what you would like the company to do.</li><li>Use polite but firm language.</li></ul>",
            [
                ic("[*I am writing to complain about a laptop I bought from your website.|I write complain your laptop website.|Complain laptop from website.]", "Clear formal opening."),
                ic("[*When I switched it on, the screen went black after two minutes.|When switched on screen black two minutes.|It black after two minute.]", "Specific explanation of the problem."),
                ic("[*I would like a full refund or a replacement.|I want refund now immediately.|Give replacement refund.]", "Polite but firm request."),
                ic("[*I have attached a copy of the receipt for reference.|Attached receipt reference copy I have.|Receipt copy attach.]", "Useful supporting detail."),
            ],
            [
                lg("A complaint email should remain ____. ", "polite", "angry", "vague", "Being polite is important."),
                lg("You should explain the problem as clearly as ____. ", "possible", "angry", "formal", "Common phrase."),
                lg("It helps to include proof, such as a ____. ", "receipt", "headline", "lecture", "Receipts show what you bought."),
                lg("At the end, ask the company to take ____. ", "action", "holiday", "travel", "Action is the expected response."),
            ],
            [
                ic("[*I look forward to hearing from you soon.|I wait hear you soon.|Hear from you I look.]", "Correct closing line."),
                ic("[*Unfortunately, the product stopped working after one day.|Unfortunate product stop one day.|Stopped after day product.]", "Natural formal complaint sentence."),
                ic("[*Could you please let me know how you intend to resolve this matter?|Please tell me now resolve matter.|Resolve matter how now?]", "Polite request for action."),
                ic("[*I hope this issue can be resolved quickly.|Hope issue resolved quickly.|This issue quickly resolved hope.]", "Good final sentence."),
            ],
        )),
        ("writing", "story-with-linkers", skill_lesson(
            "Writing a story with linkers",
            "writing",
            3,
            "<h2>Writing a story with linkers</h2><p>At B1 level, stories are easier to follow when you use time linkers and sequence words such as <em>suddenly, while, afterwards, eventually, in the end</em>. Use past simple for main events and past continuous for background action.</p>",
            [
                ic("[*While I was waiting for the bus, I noticed a wallet on the ground.|While waiting bus I noticed wallet.|I noticed wallet while wait bus.]", "Good background plus event structure."),
                ic("[*Suddenly, a man ran towards me and asked if I had seen his wallet.|Suddenly a man run to me ask wallet.|A man suddenly wallet ask.]", "Suddenly introduces an unexpected event."),
                ic("[*In the end, I returned it and he thanked me warmly.|In the end I return it he thank me.|End I returned and thanked.]", "A clear ending sentence."),
                ic("[*Afterwards, I felt proud that I had done the right thing.|Afterwards I proud I right thing done.|Proud afterwards right thing.]", "Natural reflective sentence."),
            ],
            [
                lg("Use the past ____ for the main actions in a story.", "simple", "continuous only", "perfect always", "Main events usually use past simple."),
                lg("Words like suddenly and eventually help show the ____. ", "sequence", "forecast", "receipt", "They organise the story."),
                lg("A story often becomes more interesting when something ____. ", "unexpected happens", "formal appears", "passive is used", "Unexpected events create interest."),
                lg("The final sentence can express how the writer ____. ", "felt", "resigned", "broadcast", "A story can end with a feeling."),
            ],
            [
                ic("[*At first, I thought someone had dropped it by mistake.|At first I think someone drop it.|First I thought someone mistake.]", "Good opening reflection."),
                ic("[*A few minutes later, the owner arrived looking worried.|Few minutes later owner arrived worry.|Owner arrived worry few minutes.]", "Time linker used correctly."),
                ic("[*Because I had kept the wallet safe, nothing was missing.|Because I kept wallet safe nothing missing was.|Wallet safe because nothing.]", "Clear cause and result."),
                ic("[*It was an ordinary day that turned into a memorable experience.|It was ordinary day into memorable.|Ordinary day memorable experience turned.]", "Strong story ending."),
            ],
        )),
    ]


def main() -> None:
    items = []
    items.extend(build_grammar())
    items.extend(build_vocabulary())
    items.extend(build_listening())
    items.extend(build_reading())
    items.extend(build_use_of_english())
    items.extend(build_writing())

    for section, slug, data in items:
        write_json(section, slug, data)

    print(f"Wrote {len(items)} B1 lessons.")


if __name__ == "__main__":
    main()
