from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"


def ensure_dir(section: str) -> Path:
    path = CONTENT / section / "b1plus"
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


def lesson(title: str, section: str, sort_order: int, explanation: str, exercise_sets: list[dict], audio_url: str | None = None) -> dict:
    data = {
        "title": title,
        "level": "b1plus",
        "section": section,
        "sort_order": sort_order,
        "explanation": explanation,
        "exercise_sets": exercise_sets,
    }
    if audio_url:
        data["audio_url"] = audio_url
    return data


def three_sets(q1: list[dict], q2: list[dict], q3: list[dict]) -> list[dict]:
    return [
        {"title": "Exercise 1", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q1},
        {"title": "Exercise 2", "instructions": "Choose the correct option for each gap.", "type": "lettered_gap", "questions": q2},
        {"title": "Exercise 3", "instructions": "Choose the correct option.", "type": "inline_choice", "questions": q3},
    ]


def vocab_sets(lettered1: list[dict], dropdown: list[dict], bank: list[str], lettered2: list[dict]) -> list[dict]:
    return [
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
    ]


def build_grammar():
    items = []
    items.append(("grammar", "mixed-conditionals", lesson(
        "Mixed conditionals",
        "grammar",
        1,
        "<h2>Mixed conditionals</h2><p>Mixed conditionals combine different times in the if-clause and result clause.</p><ul><li><strong>Past condition + present result:</strong> If I had studied medicine, I would be a doctor now.</li><li><strong>Present condition + past result:</strong> If he were more organised, he would not have missed the deadline.</li></ul>",
        three_sets(
            [
                ic("If I [*had taken|took|would take] that job, I would live abroad now.", "Past unreal condition with present result."),
                ic("If she [*were|was|had been] more confident, she would have applied for the role.", "Present unreal condition with past result."),
                ic("If we [*had booked|booked|would book] earlier, we would not be paying so much now.", "Past decision affects present situation."),
                ic("He would not have failed if he [*were|had been|was] more careful in general.", "General present characteristic affects a past result."),
                ic("If they [*had listened|listened|would listen] to the forecast, they would be at home now.", "Past action affects present situation."),
            ],
            [
                lg("If I had not moved to Madrid, I ____ Spanish now.", "would not speak", "did not speak", "would not have spoken", "Past decision affects present ability."),
                lg("If he were less impatient, he ____ so many mistakes yesterday.", "would not have made", "would not make", "did not make", "Present character affects past action."),
                lg("If she had accepted the offer, she ____ in Berlin now.", "would be living", "will live", "lived", "Past choice with present result."),
                lg("If we were better prepared, we ____ the presentation last week.", "would have enjoyed", "enjoyed", "would enjoy", "Present condition affecting a past result."),
            ],
            [
                ic("If I [*had saved|saved|would save] more money, I could afford that course now.", "Past action with present result."),
                ic("She would not have said that if she [*were|had been|is] more diplomatic.", "General character affecting past speech."),
                ic("If they [*had not missed|missed|would miss] the train, they would be here by now.", "Past missed train causes current absence."),
                ic("If he [*were|had been|was] more ambitious, he would have gone for the promotion.", "Present quality with past consequence."),
                ic("We would be less stressed now if we [*had started|started|would start] earlier.", "Past choice affects current stress."),
            ],
        ),
    )))
    items.append(("grammar", "wish-and-if-only", lesson(
        "Wish and if only",
        "grammar",
        2,
        "<h2>Wish and if only</h2><p>Use <strong>wish / if only + past simple</strong> to talk about present regrets, <strong>wish / if only + past perfect</strong> for past regrets, and <strong>wish + would</strong> to complain about annoying behaviour.</p>",
        three_sets(
            [
                ic("I wish I [*had|have|would have] more free time these days.", "Present regret uses past simple form."),
                ic("If only we [*had booked|booked|would book] the tickets earlier.", "Past regret uses past perfect."),
                ic("She wishes her neighbour [*would stop|stopped|had stopped] playing loud music at night.", "Wish + would for annoying behaviour."),
                ic("I wish I [*knew|know|had known] the answer right now.", "Present regret."),
                ic("If only they [*had not sold|did not sell|would not sell] the old house.", "Past regret."),
            ],
            [
                lg("He wishes he ____ speak more confidently in meetings.", "could", "can", "had", "Present ability regret."),
                lg("If only I ____ more carefully before sending the email.", "had checked", "checked", "would check", "Past regret."),
                lg("I wish it ____ raining every weekend.", "would stop", "stopped", "had stopped", "Annoying repeated behaviour."),
                lg("She wishes she ____ closer to her parents now.", "lived", "had lived", "would live", "Present unreal situation."),
            ],
            [
                ic("If only I [*had remembered|remembered|would remember] his birthday.", "Past regret."),
                ic("We wish the bus [*would arrive|arrived|had arrived] on time for once.", "Complaint about repeated annoying situation."),
                ic("I wish I [*was/were|am|had been] taller.", "Present regret."),
                ic("He wishes he [*had not said|did not say|would not say] that in the meeting.", "Past regret."),
                ic("If only they [*were|had been|are] more reliable.", "Present regret about a current situation."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-passive", lesson(
        "Passive structures",
        "grammar",
        3,
        "<h2>Passive structures</h2><p>At B1+ level, you should control passive forms in different tenses and with reporting verbs: <em>It is believed that...</em>, <em>He was asked to...</em></p>",
        three_sets(
            [
                ic("The building [*is being renovated|renovates|has renovating] at the moment.", "Present continuous passive."),
                ic("He [*was asked to present|asked to present|was asking present] the results.", "Passive with infinitive."),
                ic("It [*is believed|believes|is believing] that the painting is genuine.", "Impersonal passive reporting structure."),
                ic("By the time we arrived, the guests [*had been served|had served|were serving].", "Past perfect passive."),
                ic("The winners [*will be announced|announce|will announce] tomorrow morning.", "Future passive."),
            ],
            [
                lg("The documents ____ before the meeting started.", "had been prepared", "had prepared", "were preparing", "Past perfect passive."),
                lg("English ____ in many international workplaces.", "is used", "uses", "is using", "Present passive."),
                lg("She ____ to explain the delay.", "was expected", "expected", "was expecting", "Passive with infinitive idea."),
                lg("The proposal ____ by the board next week.", "will be reviewed", "reviews", "will review", "Future passive."),
            ],
            [
                ic("The road [*has been closed|has closed|is closed now by] since the storm.", "Present perfect passive."),
                ic("Passengers were told [*to remain|remain|remaining] seated.", "Passive reporting structure."),
                ic("The film [*is said to be|says to be|is saying to be] based on a true story.", "Be said to be."),
                ic("Several trees [*were blown down|blew down|were blowing down] during the night.", "Past passive."),
                ic("New safety rules [*are likely to be introduced|likely introduce|are introducing likely] soon.", "Passive infinitive structure."),
            ],
        ),
    )))
    items.append(("grammar", "participle-clauses", lesson(
        "Participle clauses",
        "grammar",
        4,
        "<h2>Participle clauses</h2><p>Participle clauses make sentences shorter and more formal.</p><ul><li><em>Feeling tired, she went to bed early.</em></li><li><em>Built in 1890, the theatre is still in use.</em></li><li><em>Having finished the report, he left the office.</em></li></ul>",
        three_sets(
            [
                ic("[*Having finished|Finished|To finish] the meeting, we went for coffee.", "Perfect participle shows the first action happened before the second."),
                ic("[*Built|Building|Having built] in the 18th century, the bridge is still standing.", "Past participle clause describes the bridge."),
                ic("[*Feeling|Felt|To feel] unwell, she left work early.", "Present participle clause describes the subject's state."),
                ic("[*Not knowing|Not known|Did not know] what to say, he stayed silent.", "Negative participle clause."),
                ic("[*Having been told|Telling|Being tell] the news, they changed their plans.", "Perfect passive participle clause."),
            ],
            [
                lg("____ for over an hour, we finally gave up.", "Having waited", "Waited", "To wait", "The waiting happened before giving up."),
                lg("____ by his colleagues, he felt more confident.", "Encouraged", "Encouraging", "Having encourage", "Past participle clause."),
                lg("____ the instructions carefully, she avoided mistakes.", "Having read", "Read", "To read", "One finished action before another."),
                lg("____ any better idea, we followed his plan.", "Not having", "No having", "Not have", "Negative participle clause."),
            ],
            [
                ic("[*Walking home|Walked home|To walk home], I saw an old friend.", "Present participle clause for simultaneous action."),
                ic("The documents, [*signed by the director|signing by the director|having sign by the director], were sent immediately.", "Reduced passive clause."),
                ic("[*Having lost|Losting|To lose] his keys, he could not get in.", "Perfect participle."),
                ic("[*Born|Being born|Having born] in Canada, she speaks both English and French.", "Past participle clause for background fact."),
                ic("[*Realising|Realised|To realise] the time, we rushed to the station.", "Present participle for immediate cause."),
            ],
        ),
    )))
    items.append(("grammar", "modals-of-deduction", lesson(
        "Modals of deduction",
        "grammar",
        5,
        "<h2>Modals of deduction</h2><p>Use <strong>must</strong> for strong logical conclusions, <strong>might / may / could</strong> for possibility, and <strong>can't</strong> for negative deduction.</p>",
        three_sets(
            [
                ic("She has worked all night. She [*must be|can't be|might be] exhausted.", "Strong logical conclusion."),
                ic("He is not answering. He [*might be|must be|can't be] in a meeting.", "Possible explanation."),
                ic("That [*can't be|must be|might be] James - he is on holiday in Spain.", "Negative deduction."),
                ic("The lights are off, but someone is inside. They [*must have gone|can't have gone|might have been going] to sleep early.", "Strong deduction about the past/result."),
                ic("I am not sure where Anna is. She [*may have missed|must have missed|can't have missed] the train.", "Uncertain possibility."),
            ],
            [
                lg("You have been travelling for twenty hours. You ____ tired.", "must be", "can't be", "might not", "Strong deduction."),
                lg("The shop is closed already, so they ____ gone home.", "must have", "can't have", "might not have", "Logical conclusion about the past."),
                lg("He knows nothing about the plan, so he ____ seen the email.", "can't have", "must have", "may have", "Impossible deduction."),
                lg("I cannot find my keys - they ____ be in the kitchen.", "might", "must", "can't", "A possible guess."),
            ],
            [
                ic("They [*must have forgotten|can't have forgotten|may not] about the appointment because nobody came.", "Most likely explanation."),
                ic("This [*can't be|must be|might be] the right address - the number is wrong.", "Clear negative deduction."),
                ic("She looks delighted. She [*must have passed|might have passed|can't have passed] the exam.", "Strong deduction."),
                ic("Do not worry. There [*could be|must be|can't be] a simple explanation.", "Possibility, not certainty."),
                ic("He sounds ill. He [*may need|can't need|mustn't need] to see a doctor.", "Possible deduction."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-relative-clauses", lesson(
        "Advanced relative clauses",
        "grammar",
        6,
        "<h2>Advanced relative clauses</h2><p>At this level, you should distinguish defining and non-defining clauses, use prepositions with relatives, and avoid repetition.</p><ul><li>The book, <em>which</em> I borrowed from Ana, was excellent.</li><li>The person <em>to whom</em> I spoke was very helpful.</li><li>This is the hotel <em>where</em> we stayed.</li></ul>",
        three_sets(
            [
                ic("My laptop, [*which|that|where] I bought last year, is already broken.", "Non-defining clauses use which, not that."),
                ic("The colleague [*who|which|whose] sits opposite me speaks four languages.", "Who for a person."),
                ic("That is the company [*for which|for that|for where] she works.", "Preposition + which in a formal structure."),
                ic("The writer [*whose|which|where] latest novel won a prize is giving a talk tonight.", "Whose shows possession."),
                ic("This is the village [*where|which|whose] my grandparents were born.", "Where for place."),
            ],
            [
                lg("The people, ____ were all volunteers, worked through the night.", "who", "that", "where", "Non-defining clause with people."),
                lg("The programme ____ I was listening has just finished.", "which", "who", "where", "Which for thing."),
                lg("The teacher to ____ I sent the email replied immediately.", "whom", "which", "where", "Formal object relative."),
                lg("The office, ____ is in the city centre, is easy to reach.", "which", "where", "whose", "Non-defining relative clause."),
            ],
            [
                ic("The candidate [*who I interviewed|which I interviewed|where I interviewed] seemed confident.", "Who as object is acceptable here."),
                ic("The website, [*which was redesigned|that was redesigned|where was redesigned] last month, looks better now.", "Non-defining clause."),
                ic("The woman [*whose car was stolen|which car was stolen|where car was stolen] called the police.", "Whose for possession."),
                ic("That was the moment [*when|which|whose] everything changed.", "When for time."),
                ic("The neighbourhood [*in which|where that|which in] they live is very quiet.", "Formal preposition + which."),
            ],
        ),
    )))
    items.append(("grammar", "future-perfect-and-continuous", lesson(
        "Future perfect and future continuous",
        "grammar",
        7,
        "<h2>Future perfect and future continuous</h2><p><strong>Future perfect:</strong> will have + past participle. Use it to say something will be completed before a future time.</p><p><strong>Future continuous:</strong> will be + verb-ing. Use it for actions in progress at a future moment.</p>",
        three_sets(
            [
                ic("By next June, I [*will have finished|will finish|finish] my degree.", "Future perfect for completion before a point in the future."),
                ic("This time tomorrow, we [*will be flying|will fly|are flying] over the Atlantic.", "Future continuous for an action in progress."),
                ic("By the end of the week, they [*will have moved|will move|move] into the new office.", "Completed before a future deadline."),
                ic("At 9 p.m., she [*will be giving|will give|gives] her presentation.", "Action in progress at a future time."),
                ic("I [*will have read|will be reading|read] the report by the time you arrive.", "Completion before another future event."),
            ],
            [
                lg("In two years, he ____ in the company for a decade.", "will have worked", "will work", "will be worked", "Future perfect with duration up to a future point."),
                lg("Do not call at eight - we ____ dinner then.", "will be having", "will have", "have", "Future continuous."),
                lg("By tomorrow morning, the technicians ____ the problem.", "will have solved", "solve", "will be solving", "Completed before tomorrow morning."),
                lg("At this time next week, I ____ on a beach.", "will be lying", "lie", "will have lain", "Action in progress in the future."),
            ],
            [
                ic("By 2030, scientists [*will have developed|develop|will be developed] new solutions to this problem.", "Future perfect."),
                ic("When you get home, I [*will be sleeping|sleep|will have slept] probably .", "Likely in progress at that moment."),
                ic("They [*will have known|know|will be knowing] each other for twenty years next month.", "Future perfect with duration."),
                ic("At noon tomorrow, the students [*will be taking|take|will have taken] their exam.", "Action in progress at a future moment."),
                ic("By the time the guests arrive, we [*will have prepared|prepare|will be preparing] everything.", "Completed before arrival."),
            ],
        ),
    )))
    items.append(("grammar", "discourse-markers", lesson(
        "Discourse markers",
        "grammar",
        8,
        "<h2>Discourse markers</h2><p>Discourse markers help organise ideas and show relationships between them: addition, contrast, result, example and sequencing.</p><ul><li>addition: furthermore, in addition</li><li>contrast: however, although, nevertheless</li><li>result: therefore, as a result</li><li>example: for instance</li></ul>",
        three_sets(
            [
                ic("The train was delayed; [*however|therefore|for example], we still arrived on time.", "However introduces contrast."),
                ic("She speaks several languages. [*In addition|Although|As a result], she has excellent communication skills.", "In addition adds another point."),
                ic("The roads were icy. [*As a result|For instance|Nevertheless], many schools closed.", "As a result shows consequence."),
                ic("Some jobs are flexible. [*For example|However|Therefore], remote teaching and freelance design.", "For example introduces examples."),
                ic("He was tired; [*nevertheless|for instance|because of], he finished the report.", "Nevertheless contrasts with the first clause."),
            ],
            [
                lg("I enjoy outdoor sports. ____, I go hiking whenever I can.", "For instance", "However", "Therefore", "For instance introduces an example."),
                lg("The phone is expensive. ____, it has excellent reviews.", "However", "As a result", "For example", "Contrast."),
                lg("Traffic was terrible. ____, we missed the start of the film.", "As a result", "In addition", "Nevertheless", "Result."),
                lg("The company offers good pay. ____, it provides flexible hours.", "In addition", "However", "Therefore", "Addition."),
            ],
            [
                ic("The city is expensive. [*On the other hand|As a result|For example], salaries are usually higher.", "Contrast with a balancing point."),
                ic("He had prepared carefully; [*therefore|however|for instance], the interview went well.", "Therefore shows consequence."),
                ic("[*Although|For example|In addition] she was tired, she stayed until the end.", "Although introduces concession."),
                ic("Many people enjoy podcasts; [*for instance|however|therefore], language learners often use them for extra practice.", "For instance fits before an example."),
                ic("The flat is small. [*Nevertheless|For example|As a result], it feels bright and comfortable.", "Nevertheless gives unexpected contrast."),
            ],
        ),
    )))
    return items


def build_vocabulary():
    items = []

    def make_vocab(title, slug, sort_order, explanation, lettered1, dropdown, bank, lettered2):
        items.append(("vocabulary", slug, lesson(title, "vocabulary", sort_order, explanation, vocab_sets(lettered1, dropdown, bank, lettered2))))

    make_vocab(
        "Travel issues and airports",
        "travel-issues-airports",
        1,
        "<h2>Travel issues and airports</h2><ul><li>disruption, cancellation, delay, connection, terminal</li><li>customs, security check, boarding gate, compensation</li><li>verbs: queue, rebook, complain, depart</li></ul>",
        [
            lg("Our flight was cancelled, so the airline offered us ____.", "compensation", "permission", "promotion", "Compensation may be offered after disruption."),
            lg("We missed our ____ in Frankfurt and had to stay overnight.", "connection", "terminal", "campsite", "Connection = onward flight or train."),
            lg("Passengers must go through a ____ before entering the gate area.", "security check", "headline", "refund desk", "Security check at the airport."),
            lg("They told us to wait at boarding ____ 12.", "gate", "delay", "suitcase", "Boarding gate."),
        ],
        [
            dd("The airline agreed to ____ our tickets for the next morning.", "rebook"),
            dd("After the long queue at ____, we finally reached passport control.", "check-in"),
            dd("The bags arrived at a different ____ from expected.", "terminal"),
            dd("He wrote a formal letter to ____ about the service.", "complain"),
            dd("The plane did not ____ until midnight.", "depart"),
        ],
        ["rebook", "check-in", "terminal", "complain", "depart", "runway", "boarding pass", "customs", "announcement", "compensation"],
        [
            lg("We had nothing to declare at ____.", "customs", "security check", "boarding", "Customs after landing."),
            lg("The loudspeaker made an unexpected ____ about our flight.", "announcement", "platform", "documentary", "Airports make announcements."),
            lg("The aircraft was still on the ____ when we arrived at the gate.", "runway", "receipt", "queue", "Runway is for planes."),
            lg("Keep your ____ ready when you reach the gate.", "boarding pass", "salary", "forecast", "Needed for boarding."),
        ],
    )
    make_vocab(
        "Workplace communication",
        "workplace-communication",
        2,
        "<h2>Workplace communication</h2><ul><li>agenda, minutes, feedback, deadline, negotiation</li><li>clarify, interrupt, persuade, summarise</li><li>phrases: make a point, raise a concern</li></ul>",
        [
            lg("Please send me the meeting ____ before tomorrow morning.", "agenda", "headline", "contract", "Agenda = plan for the meeting."),
            lg("Could you ____ what you mean by 'urgent'?", "clarify", "interrupt", "negotiate", "Clarify = explain clearly."),
            lg("The manager gave me useful ____ on my presentation.", "feedback", "broadcast", "evidence", "Feedback = comments on performance."),
            lg("We need someone to take the meeting ____.", "minutes", "platforms", "vacancies", "Meeting minutes = written notes."),
        ],
        [
            dd("Try not to ____ people while they are speaking.", "interrupt"),
            dd("She managed to ____ the client to accept the proposal.", "persuade"),
            dd("At the end, I will ____ the key decisions.", "summarise"),
            dd("He wanted to ____ a concern about the budget.", "raise"),
            dd("We spent two hours in ____ over the final price.", "negotiation"),
        ],
        ["interrupt", "persuade", "summarise", "raise", "negotiation", "agenda", "feedback", "deadline", "minutes", "clarify"],
        [
            lg("The project is due on Friday, so the ____ is close.", "deadline", "agenda", "discount", "Deadline = final date."),
            lg("She made a strong ____ about the need for better planning.", "point", "queue", "forecast", "Make a point."),
            lg("I need to ____ this sentence in a simpler way.", "rephrase", "delay", "depart", "Rephrase = say again differently."),
            lg("Good teamwork depends on clear ____.", "communication", "customs", "recovery", "Communication is key at work."),
        ],
    )
    make_vocab(
        "Media and advertising",
        "media-and-advertising",
        3,
        "<h2>Media and advertising</h2><ul><li>brand, slogan, campaign, target audience, review</li><li>influence, promote, recommend, advertise</li><li>phrases: go viral, catch attention</li></ul>",
        [
            lg("The company launched a new advertising ____ last month.", "campaign", "receipt", "qualification", "Advertising campaign."),
            lg("That short video went ____ on social media overnight.", "viral", "formal", "balanced", "Go viral = spread very quickly."),
            lg("A good advert needs to ____ the audience's attention.", "catch", "refund", "arrest", "Catch attention."),
            lg("Teenagers are the main target ____ for this product.", "audience", "platform", "symptom", "Target audience."),
        ],
        [
            dd("I read an online ____ before buying the headphones.", "review"),
            dd("Celebrities can strongly ____ what people buy.", "influence"),
            dd("The poster is meant to ____ the new app.", "promote"),
            dd("A memorable ____ helps customers remember the brand.", "slogan"),
            dd("That sports company has become a global ____.", "brand"),
        ],
        ["review", "influence", "promote", "slogan", "brand", "advertise", "campaign", "audience", "viral", "headline"],
        [
            lg("Many businesses use social media to ____ their services.", "advertise", "memorise", "replace", "Advertise services."),
            lg("I would definitely ____ this podcast to language learners.", "recommend", "clarify", "delay", "Recommend = suggest positively."),
            lg("The headline was designed to create instant ____.", "interest", "compensation", "habit", "Media headline aims to attract interest."),
            lg("The message was simple but highly ____.", "effective", "judicial", "renewable", "Effective advertising works well."),
        ],
    )
    make_vocab(
        "Social issues and society",
        "social-issues-society",
        4,
        "<h2>Social issues and society</h2><ul><li>poverty, homelessness, inequality, unemployment, charity</li><li>donate, volunteer, support, struggle</li><li>phrases: make a difference, raise awareness</li></ul>",
        [
            lg("Many families are struggling because of rising ____.", "unemployment", "luggage", "humidity", "Unemployment means lack of jobs."),
            lg("The charity hopes to ____ awareness of the problem.", "raise", "take", "deliver", "Raise awareness = increase public attention."),
            lg("Volunteers collected food for people facing ____.", "homelessness", "promotion", "forecast", "Homelessness is a social issue."),
            lg("Even small actions can ____ a difference.", "make", "do", "take", "Make a difference is the fixed phrase."),
        ],
        [
            dd("He decided to ____ money to the local shelter.", "donate"),
            dd("More young people want to ____ in their communities.", "volunteer"),
            dd("The campaign offers practical ____ to low-income families.", "support"),
            dd("Some people still face serious social ____.", "inequality"),
            dd("Many older people ____ to pay heating bills in winter.", "struggle"),
        ],
        ["donate", "volunteer", "support", "inequality", "struggle", "charity", "poverty", "awareness", "community", "shelter"],
        [
            lg("The event raised money for a children's ____.", "charity", "platform", "campaigner", "Charity receives donations."),
            lg("The government promised to reduce child ____.", "poverty", "virus", "network", "Poverty is the issue."),
            lg("Neighbours created a stronger sense of ____ through the project.", "community", "court", "schedule", "Community spirit."),
            lg("The new ____ provides emergency beds for rough sleepers.", "shelter", "promotion", "review", "Shelter for homeless people."),
        ],
    )
    make_vocab(
        "Science and innovation",
        "science-and-innovation",
        5,
        "<h2>Science and innovation</h2><ul><li>experiment, discovery, evidence, theory, invention</li><li>research, analyse, observe, develop</li><li>phrases: come to a conclusion, carry out research</li></ul>",
        [
            lg("The team carried out an ____ to test the new material.", "experiment", "agreement", "refund", "An experiment tests an idea."),
            lg("Scientists need strong ____ before making claims.", "evidence", "campaign", "agenda", "Evidence supports conclusions."),
            lg("Researchers continue to ____ how the disease spreads.", "investigate", "broadcast", "persuade", "Investigate = examine carefully."),
            lg("That medical ____ could save millions of lives.", "discovery", "argument", "customs", "A discovery is a new finding."),
        ],
        [
            dd("The company wants to ____ a cheaper battery.", "develop"),
            dd("Please ____ the data before writing the report.", "analyse"),
            dd("Astronomers ____ the sky through powerful telescopes.", "observe"),
            dd("The article explains a scientific ____ about climate systems.", "theory"),
            dd("He plans to ____ further research next year.", "conduct"),
        ],
        ["develop", "analyse", "observe", "theory", "conduct", "invention", "laboratory", "research", "conclusion", "evidence"],
        [
            lg("The telephone was once a revolutionary ____.", "invention", "promotion", "device update", "An invention is a new thing created."),
            lg("They work in a modern ____ at the university.", "laboratory", "headline", "terminal", "Laboratory = science workplace."),
            lg("After studying the results, they came to a clear ____.", "conclusion", "summary", "deadline", "Conclusion after analysis."),
            lg("Good science depends on careful ____.", "research", "journey", "opinion", "Research is central to science."),
        ],
    )
    make_vocab(
        "Money and consumer habits",
        "money-and-consumer-habits",
        6,
        "<h2>Money and consumer habits</h2><ul><li>budget, savings, debt, bargain, subscription</li><li>spend, waste, compare, charge</li><li>phrases: live within your means, cut back on</li></ul>",
        [
            lg("We need a monthly ____ so we know where our money goes.", "budget", "receipt", "platform", "Budget helps plan spending."),
            lg("He is trying to ____ on eating out to save money.", "cut back", "take off", "set out", "Cut back on = reduce."),
            lg("A free trial turns into a paid ____ after thirty days.", "subscription", "vacancy", "campaign", "Subscription = regular payment."),
            lg("She found a real ____ in the sale.", "bargain", "schedule", "shelter", "Bargain = something good at a low price."),
        ],
        [
            dd("If you borrow too much, you can end up in ____. ", "debt"),
            dd("I always ____ prices online before buying electronics.", "compare"),
            dd("They put some money into their ____ every month.", "savings"),
            dd("Some shops ____ extra for delivery.", "charge"),
            dd("Families often ____ money on things they do not need.", "waste"),
        ],
        ["debt", "compare", "savings", "charge", "waste", "income", "budget", "bargain", "subscription", "means"],
        [
            lg("It is important to live within your ____. ", "means", "shift", "evidence", "Means = financial limits."),
            lg("Her main source of ____ is freelance design work.", "income", "debt", "budget", "Income = money earned."),
            lg("They need to keep track of every regular monthly ____.", "payment", "platform", "habitat", "Payment fits the consumer context."),
            lg("He is trying to become a more responsible ____.", "consumer", "witness", "editor", "Consumer = buyer."),
        ],
    )
    make_vocab(
        "Personality and behaviour",
        "personality-and-behaviour",
        7,
        "<h2>Personality and behaviour</h2><ul><li>traits: reliable, stubborn, generous, thoughtful, selfish</li><li>behaviour: interrupt, complain, apologise, encourage</li><li>phrases: keep your word, jump to conclusions</li></ul>",
        [
            lg("You can trust her completely - she is very ____.", "reliable", "jealous", "clumsy", "Reliable people do what they promise."),
            lg("He never changes his mind. He is too ____.", "stubborn", "generous", "shy", "Stubborn = unwilling to change opinion."),
            lg("It was very ____ of you to remember my birthday.", "thoughtful", "formal", "viral", "Thoughtful = kind and considerate."),
            lg("Do not ____ to conclusions before you know the facts.", "jump", "raise", "broadcast", "Jump to conclusions is the expression."),
        ],
        [
            dd("She always keeps her ____. If she promises something, she does it.", "word"),
            dd("It was selfish of him not to ____ for being late.", "apologise"),
            dd("Parents should ____ children to ask questions.", "encourage"),
            dd("He tends to ____ when other people are speaking.", "interrupt"),
            dd("A ____ person often shares time and money with others.", "generous"),
        ],
        ["word", "apologise", "encourage", "interrupt", "generous", "complain", "selfish", "patient", "reliable", "stubborn"],
        [
            lg("She can be a bit ____ when things do not go her way.", "selfish", "renewable", "formal", "Selfish behaviour."),
            lg("Try not to ____ all the time; suggest a solution instead.", "complain", "observe", "hire", "Complain fits."),
            lg("Good teachers are usually calm and ____.", "patient", "viral", "guilty", "Patient people stay calm."),
            lg("If you give your word, you should ____ it.", "keep", "break in", "take", "Keep your word."),
        ],
    )
    make_vocab(
        "City life and urban problems",
        "city-life-urban-problems",
        8,
        "<h2>City life and urban problems</h2><ul><li>housing, traffic jam, public transport, noise pollution, overcrowding</li><li>pedestrian area, cycle lane, suburb, city centre</li><li>verbs: commute, expand, improve, reduce</li></ul>",
        [
            lg("Heavy ____ can make a short journey take an hour.", "traffic", "evidence", "income", "Traffic problems cause delays."),
            lg("Many people move to the ____ because housing is cheaper there.", "suburbs", "runways", "theories", "Suburbs are outside the centre."),
            lg("The council wants to create more ____ so cyclists can travel safely.", "cycle lanes", "luggage belts", "deadlines", "Cycle lanes for bikes."),
            lg("Living in a huge city often means dealing with ____.", "overcrowding", "scholarships", "revisions", "Too many people in one place."),
        ],
        [
            dd("She has to ____ for ninety minutes every day.", "commute"),
            dd("The city plans to ____ the tram network next year.", "expand"),
            dd("A new law could help ____ noise pollution at night.", "reduce"),
            dd("Many tourists prefer to stay in the city ____. ", "centre"),
            dd("Better buses would ____ daily life for residents.", "improve"),
        ],
        ["commute", "expand", "reduce", "centre", "improve", "pedestrian", "housing", "public transport", "pollution", "suburbs"],
        [
            lg("This street is a ____ area, so cars cannot enter.", "pedestrian", "volunteer", "broadcast", "Pedestrian area = for walkers only."),
            lg("Young adults often struggle with high ____ costs.", "housing", "platform", "weather", "Housing costs."),
            lg("Good ____ is essential in large cities.", "public transport", "salary", "furniture", "Buses and trains."),
            lg("Air ____ is worse near busy roads.", "pollution", "promotion", "discussion", "Pollution from traffic."),
        ],
    )
    return items


def build_listening():
    return [
        ("listening", "flatmate-discussion", lesson(
            "Flatmate discussion",
            "listening",
            1,
            "<h2>Flatmate discussion</h2><p>Listen to two flatmates talking about household rules.</p><h3>Transcript</h3><p><strong>Ella:</strong> We need to talk about the cleaning rota. I feel like I have been doing most of the kitchen this month.<br><strong>Tom:</strong> You are right. I have been busy, but that is not an excuse. How about we make a proper schedule?<br><strong>Ella:</strong> Good idea. And could we also agree not to invite friends over on weeknights without asking first?<br><strong>Tom:</strong> Fair enough. That sounds reasonable.</p>",
            three_sets(
                [
                    ic("Ella says she has been doing most of the [*kitchen cleaning|shopping|rent payments].", "She mentions the kitchen specifically."),
                    ic("Tom admits he has been [*busy|ill|away].", "He says he has been busy."),
                    ic("They decide to make a [*schedule|phone call|complaint].", "A proper schedule."),
                    ic("Ella wants flatmates to ask before inviting [*friends over on weeknights|family for weekends|repair workers].", "That is the second issue she raises."),
                ],
                [
                    lg("The topic is the cleaning ____. ", "rota", "campaign", "bargain", "A rota is a schedule of duties."),
                    lg("Tom says being busy is not an ____. ", "excuse", "update", "argument", "He calls it not an excuse."),
                    lg("Ella thinks the new rule sounds ____. ", "reasonable", "impossible", "unfair", "Reasonable is the conclusion."),
                    lg("They are discussing life in a shared ____. ", "flat", "office", "hotel", "It is a flatmate discussion."),
                ],
                [
                    ic("The conversation is about [*shared responsibilities|travel plans|exam stress].", "Cleaning and visitors in a shared home."),
                    ic("Tom reacts in a [*cooperative|defensive|aggressive] way overall.", "He agrees and suggests a solution."),
                    ic("Ella's complaint is [*specific|unclear|unrelated].", "She mentions the kitchen and weeknights."),
                    ic("The tone becomes more [*constructive|hostile|formal] by the end.", "They find a practical solution."),
                ],
            ),
            "https://www.youtube.com/watch?v=8O6272q0Awo",
        )),
        ("listening", "customer-service-call", lesson(
            "Customer service call",
            "listening",
            2,
            "<h2>Customer service call</h2><p>Listen to a customer calling about a delayed order.</p><h3>Transcript</h3><p><strong>Agent:</strong> Good morning, BrightHome customer service. How can I help?<br><strong>Customer:</strong> Hello. I ordered a desk last week, and it was supposed to arrive yesterday.<br><strong>Agent:</strong> Let me check that for you. I can see there was a delivery problem at the warehouse.<br><strong>Customer:</strong> I understand, but I need the desk urgently because I work from home.<br><strong>Agent:</strong> I am sorry. We can deliver it tomorrow and refund the delivery charge.</p>",
            three_sets(
                [
                    ic("The customer ordered a [*desk|chair|lamp].", "The order was for a desk."),
                    ic("It was supposed to arrive [*yesterday|last week|tomorrow].", "The customer says yesterday."),
                    ic("The problem happened at the [*warehouse|office|shop].", "The agent mentions the warehouse."),
                    ic("The company offers to refund the [*delivery charge|whole order|tax].", "Refund the delivery charge."),
                ],
                [
                    lg("The customer needs the desk because they work from ____. ", "home", "school", "abroad", "They say they work from home."),
                    lg("The agent says: Let me ____ that for you.", "check", "buy", "cancel", "Common customer service phrase."),
                    lg("There was a delivery ____. ", "problem", "discount", "presentation", "Delivery problem."),
                    lg("The desk can be delivered ____. ", "tomorrow", "next month", "today", "The revised delivery date."),
                ],
                [
                    ic("The customer sounds [*firm but polite|rude|completely relaxed].", "The complaint is polite but clear."),
                    ic("The agent responds by [*offering a solution|ending the call|denying the order].", "A new delivery time and refund are offered."),
                    ic("The main topic is [*an online order delay|a job interview|a train ticket].", "It is a customer service problem."),
                    ic("The company accepts [*some responsibility|no responsibility|full blame for damage].", "They apologise and refund the delivery charge."),
                ],
            ),
            "https://www.youtube.com/watch?v=4jpdlG8EJhE",
        )),
        ("listening", "radio-interview-volunteering", lesson(
            "Radio interview about volunteering",
            "listening",
            3,
            "<h2>Radio interview about volunteering</h2><p>Listen to a short interview.</p><h3>Transcript</h3><p><strong>Host:</strong> Why did you start volunteering at the food bank?<br><strong>Guest:</strong> At first, I wanted to gain experience for my CV, but I soon realised how important the work was. We sort donations, prepare food parcels and talk to families who need support.<br><strong>Host:</strong> Has the experience changed you?<br><strong>Guest:</strong> Definitely. I have become more patient and much more aware of problems in my community.</p>",
            three_sets(
                [
                    ic("The guest volunteers at [*a food bank|a hospital|an art gallery].", "The place is a food bank."),
                    ic("At first, the guest wanted [*experience for a CV|free meals|a part-time job].", "That is the initial reason."),
                    ic("They sort donations and prepare [*food parcels|radio equipment|school lessons].", "Food parcels."),
                    ic("The experience made the guest more [*patient|ambitious|suspicious].", "The guest says more patient."),
                ],
                [
                    lg("The guest also became more aware of problems in the local ____. ", "community", "airport", "industry", "Community problems."),
                    lg("Families who need ____ receive help from the food bank.", "support", "publicity", "transport", "Support fits the context."),
                    lg("The guest says the work is very ____. ", "important", "formal", "easy", "They realised how important it was."),
                    lg("The host asks whether the experience has ____ the guest.", "changed", "hired", "judged", "Changed is the key verb."),
                ],
                [
                    ic("The interview shows that volunteering can be [*personally valuable|a waste of time|financially rewarding only].", "The guest describes positive personal change."),
                    ic("The food bank helps [*local families|international tourists|shop owners].", "Families who need support."),
                    ic("The guest's motivation [*developed over time|never changed|was unclear].", "It began as CV experience and became more meaningful."),
                    ic("The tone is [*positive and reflective|angry|formal and distant].", "The guest reflects positively."),
                ],
            ),
            "https://www.youtube.com/watch?v=7y_hbz6lM9E",
        )),
        ("listening", "travel-podcast-episode", lesson(
            "Travel podcast episode",
            "listening",
            4,
            "<h2>Travel podcast episode</h2><p>Listen to part of a travel podcast.</p><h3>Transcript</h3><p><strong>Presenter:</strong> This week we are talking about city breaks on a budget. Our guest, Martin Shaw, has visited more than thirty European cities without spending much money. He recommends travelling in the off-season, staying in hostels and booking local transport in advance. He also says that eating where local people eat is often cheaper and better than going to tourist restaurants.</p>",
            three_sets(
                [
                    ic("Martin has visited more than [*thirty|thirteen|forty-five] European cities.", "The presenter says more than thirty."),
                    ic("He recommends travelling in the [*off-season|high season|winter only].", "Off-season is recommended."),
                    ic("He suggests staying in [*hostels|luxury hotels|airports].", "Hostels are mentioned."),
                    ic("Local restaurants are often [*cheaper and better|more dangerous|closed early].", "That is his opinion."),
                ],
                [
                    lg("The episode is about city breaks on a ____. ", "budget", "platform", "runway", "Budget travel."),
                    lg("Martin suggests booking local transport in ____. ", "advance", "secret", "winter", "In advance."),
                    lg("Tourist restaurants are often more ____. ", "expensive", "friendly", "empty", "Compared with local places."),
                    lg("The speaker is a travel ____. ", "presenter", "judge", "customer", "He hosts the podcast."),
                ],
                [
                    ic("The podcast gives [*practical advice|medical warnings|legal information].", "It offers budget travel advice."),
                    ic("Martin seems [*experienced|uncertain|uninterested].", "He has visited many cities."),
                    ic("The focus is on travelling [*cheaply|luxuriously|for business only].", "On a budget."),
                    ic("The recommendations are [*specific|confusing|unrelated].", "Off-season, hostels, local transport, local restaurants."),
                ],
            ),
            "https://www.youtube.com/watch?v=HwMkN_2BTqs",
        )),
        ("listening", "school-careers-event", lesson(
            "School careers event",
            "listening",
            5,
            "<h2>School careers event</h2><p>Listen to an announcement at a school careers event.</p><h3>Transcript</h3><p><strong>Speaker:</strong> Welcome to our annual careers afternoon. Today you can attend talks on engineering, nursing, journalism and software development. Please check the timetable on the noticeboard. The first sessions start at 1:30 in rooms 12, 14, 18 and 20. If you would like one-to-one advice, career advisers will be available in the library after 3 p.m.</p>",
            three_sets(
                [
                    ic("The event offers talks on [*four|two|six] career areas.", "Engineering, nursing, journalism and software development."),
                    ic("The first sessions start at [*1:30|3:00|12:30].", "The first sessions start at 1:30."),
                    ic("One-to-one advice will be in the [*library|hall|canteen].", "Advice in the library."),
                    ic("The event happens in a [*school|hospital|company office].", "A school careers afternoon."),
                ],
                [
                    lg("Students should check the ____ on the noticeboard.", "timetable", "budget", "recipe", "Timetable tells them where and when."),
                    lg("Career advisers will be available after ____ p.m.", "3", "2", "4", "After 3 p.m."),
                    lg("One of the sessions is about ____ development.", "software", "budget", "social", "Software development."),
                    lg("The event is held every year, so it is ____.", "annual", "casual", "private", "Annual means yearly."),
                ],
                [
                    ic("The purpose of the message is to [*give practical event information|advertise a film|discuss exam results].", "It gives time and location details."),
                    ic("The speaker expects students to [*move between sessions|stay in one room all day|go home early].", "They can attend talks in different rooms."),
                    ic("The tone is [*informative|emotional|critical].", "It is a clear announcement."),
                    ic("Students who want personal advice should wait until [*after three|half past one|lunchtime].", "After 3 p.m."),
                ],
            ),
            "https://www.youtube.com/watch?v=fSrLeyfk9SM",
        )),
    ]


def build_reading():
    return [
        ("reading", "smart-cities", lesson(
            "What makes a city 'smart'?",
            "reading",
            1,
            "<h2>What makes a city 'smart'?</h2><p>A smart city uses technology to improve daily life for residents. This can include traffic systems that change automatically when roads are busy, bins that send a message when they need to be emptied, and apps that show exactly when the next bus will arrive. Supporters believe these systems save time, reduce energy use and make public services more efficient. Critics, however, worry about data privacy and the cost of maintaining complex technology. As with many innovations, the success of smart cities depends not only on the software itself but also on how carefully it is managed.</p>",
            three_sets(
                [
                    ic("Smart cities use technology to [*improve daily life|replace all workers|entertain tourists only].", "This is the main definition in the text."),
                    ic("Some bins can send a message when they need to be [*emptied|moved|washed].", "The text gives this example."),
                    ic("Supporters say the systems can reduce [*energy use|housing prices|school holidays].", "Energy use is mentioned."),
                    ic("Critics are concerned about [*privacy and cost|weather and traffic|language learning].", "These are the main concerns."),
                ],
                [
                    lg("Bus apps can show exactly when the next bus will ____. ", "arrive", "break", "retire", "The arrival time is shown."),
                    lg("Smart systems can make public services more ____. ", "efficient", "expensive", "traditional", "Efficiency is a key benefit."),
                    lg("The success of these systems depends on how carefully they are ____. ", "managed", "advertised", "recycled", "Management matters."),
                    lg("The writer presents both advantages and ____. ", "concerns", "tickets", "symptoms", "The text is balanced."),
                ],
                [
                    ic("The overall tone of the passage is [*balanced|enthusiastic only|completely negative].", "The writer gives both sides."),
                    ic("The article suggests technology alone is [*not enough|all that matters|too simple to use].", "Management matters too."),
                    ic("The passage is mainly about [*urban innovation|museum design|airport security].", "It focuses on smart cities."),
                    ic("A smart traffic system might react to [*busy roads|cheap tickets|bad teaching].", "It changes automatically when roads are busy."),
                ],
            ),
        )),
        ("reading", "gap-year-choice", lesson(
            "Should you take a gap year?",
            "reading",
            2,
            "<h2>Should you take a gap year?</h2><p>For some students, taking a gap year before university can be a valuable experience. It gives them time to travel, work, volunteer or simply think more carefully about what they want to study. Many say they return more independent and motivated. However, a gap year is not automatically useful. Without a plan, students may end up wasting time or spending too much money. Experts recommend setting clear goals, creating a budget and choosing activities that build useful skills rather than just filling time.</p>",
            three_sets(
                [
                    ic("A gap year happens [*before university|after retirement|during secondary school only].", "That is the context in the passage."),
                    ic("Some students return more [*independent and motivated|uncertain and tired|wealthy].", "This is one reported benefit."),
                    ic("A gap year is not useful [*without a plan|for volunteers|for travellers].", "The text warns against having no plan."),
                    ic("Experts recommend creating [*a budget|a business|a timetable for exams only].", "Creating a budget is advised."),
                ],
                [
                    lg("A gap year can help students think more carefully about what they want to ____. ", "study", "publish", "replace", "Choosing a course is one reason."),
                    lg("Some people may end up ____ time if the year is not planned well.", "wasting", "earning", "saving", "The text uses wasting time."),
                    lg("Experts say students should set clear ____. ", "goals", "symptoms", "gate numbers", "Goals give direction."),
                    lg("Useful activities can help build important ____. ", "skills", "alarms", "receipts", "Skills are mentioned."),
                ],
                [
                    ic("The writer's message is that a gap year can be [*helpful if well planned|always a bad idea|only for rich students].", "That is the balanced conclusion."),
                    ic("The article focuses on [*advantages and risks|only travel advice|university entrance exams].", "Both sides are discussed."),
                    ic("Volunteering is presented as one possible [*activity|problem|expense].", "It is listed among options."),
                    ic("The passage would probably appear in [*education advice|a recipe book|a sports report].", "It reads like education advice."),
                ],
            ),
        )),
        ("reading", "neighbourhood-app", lesson(
            "Can neighbourhood apps build real communities?",
            "reading",
            3,
            "<h2>Can neighbourhood apps build real communities?</h2><p>In many towns and cities, local residents now use neighbourhood apps to share information, ask for help and organise events. A message about a lost pet can spread within minutes, and someone who needs a ladder or a babysitter may find support nearby. Supporters say these apps help strangers trust each other and make communities more practical. Critics argue that online communication can never fully replace real conversations and may even increase suspicion when people share too many complaints. Whether these apps strengthen a neighbourhood seems to depend on how respectfully people use them.</p>",
            three_sets(
                [
                    ic("Neighbourhood apps allow residents to [*share information quickly|book flights|watch documentaries].", "That is one of their main uses."),
                    ic("Someone who needs a ladder may find [*local support|legal advice|a new job].", "The text gives this example."),
                    ic("Critics think online communication cannot fully replace [*real conversations|public transport|formal education].", "That is their concern."),
                    ic("The effect of the apps depends on how [*respectfully|expensively|secretly] people use them.", "That is the final point."),
                ],
                [
                    lg("A message about a lost ____ can spread very quickly.", "pet", "receipt", "deadline", "Lost pet is the example."),
                    lg("Supporters say the apps make communities more ____. ", "practical", "private", "formal", "The word practical is used."),
                    lg("Too many complaints may increase ____. ", "suspicion", "income", "fitness", "That is one criticism."),
                    lg("The apps can also help people organise local ____. ", "events", "laws", "storms", "Residents can organise events."),
                ],
                [
                    ic("The writer does not claim the apps are [*completely good or bad|useless|dangerous in all cases].", "The article is balanced."),
                    ic("The passage is mainly about [*technology and community|airport delays|medical treatment].", "It discusses apps and neighbourhoods."),
                    ic("The text suggests behaviour matters as much as the [*technology|weather|budget].", "Respectful use is important."),
                    ic("One positive effect mentioned is increased [*trust|competition|advertising].", "Supporters say strangers trust each other more."),
                ],
            ),
        )),
        ("reading", "extreme-weather", lesson(
            "Living with extreme weather",
            "reading",
            4,
            "<h2>Living with extreme weather</h2><p>In recent years, many regions have experienced more frequent extreme weather events, including floods, heatwaves and severe storms. Scientists say that while no single event can be explained by climate change alone, long-term trends make some events more likely and more intense. As a result, cities are beginning to rethink how they are built. Some are planting more trees to lower temperatures, while others are improving drainage systems to reduce flood damage. Adapting to extreme weather is expensive, but many experts believe the cost of doing nothing would be far greater.</p>",
            three_sets(
                [
                    ic("Recent years have brought more frequent [*extreme weather events|music festivals|power cuts only].", "The passage opens with this idea."),
                    ic("Climate change may make some events more [*likely and intense|short and cheap|easy to predict].", "The article says more likely and more intense."),
                    ic("Some cities are planting more trees to lower [*temperatures|rent|traffic].", "Trees lower temperatures."),
                    ic("Experts think doing nothing would be [*more costly|safer|more relaxing].", "Doing nothing would cost more."),
                ],
                [
                    lg("One adaptation strategy is improving city ____ systems.", "drainage", "lecture", "refund", "Drainage reduces flood damage."),
                    lg("No single weather event can be explained by climate change ____. ", "alone", "therefore", "instead", "That exact idea appears in the text."),
                    lg("Heatwaves, storms and floods are all examples of extreme weather ____. ", "events", "audiences", "products", "Events is the key noun."),
                    lg("Adapting to these changes can be very ____. ", "expensive", "formal", "impossible", "The text says it is expensive."),
                ],
                [
                    ic("The passage is mainly about [*responding to climate-related risks|farming methods|tourism in cities].", "It focuses on adaptation."),
                    ic("The writer's attitude is [*serious but practical|joking|uncertain about the existence of weather].", "The tone is serious and solution-focused."),
                    ic("The article suggests cities are [*already taking action|refusing to change|reducing public services].", "They are rethinking how they are built."),
                    ic("The text contrasts the cost of adaptation with the cost of [*doing nothing|tree planting|new housing].", "That is the final comparison."),
                ],
            ),
        )),
        ("reading", "skills-for-the-future", lesson(
            "Skills for the future",
            "reading",
            5,
            "<h2>Skills for the future</h2><p>As technology continues to change the workplace, employers are placing greater value on skills that are difficult to automate. These include communication, problem-solving, creativity and the ability to work well with others. Technical knowledge still matters, but experts say workers will increasingly need to keep learning throughout their careers. In a fast-changing economy, the most successful employees may not be those who know the most today, but those who can adapt most quickly tomorrow.</p>",
            three_sets(
                [
                    ic("Employers value skills that are difficult to [*automate|advertise|measure].", "This is the central point."),
                    ic("The text mentions communication and [*problem-solving|driving|accounting only].", "Problem-solving is one of the skills listed."),
                    ic("Experts say workers will need to keep [*learning|travelling|changing companies] throughout their careers.", "Lifelong learning is emphasised."),
                    ic("The most successful employees may be those who can [*adapt quickly|work alone|avoid technology].", "Adaptability is highlighted."),
                ],
                [
                    lg("Technical ____ still matters, according to the article.", "knowledge", "weather", "fitness", "Technical knowledge matters."),
                    lg("Creativity is hard to ____.", "automate", "commute", "refund", "Machines struggle to automate creativity."),
                    lg("Workers need to learn throughout their ____. ", "careers", "holidays", "complaints", "Throughout their careers."),
                    lg("The economy is described as fast-____.", "changing", "sleeping", "finishing", "Fast-changing economy."),
                ],
                [
                    ic("The passage is mainly about [*future employability|city transport|travel safety].", "It is about work skills for the future."),
                    ic("The writer suggests knowledge alone is [*not enough|completely unnecessary|the only important thing].", "Adaptation also matters."),
                    ic("The tone is [*forward-looking|nostalgic|angry].", "It looks toward future work."),
                    ic("Teamwork is implied in the phrase [*work well with others|know the most today|keep learning].", "This phrase refers to collaboration."),
                ],
            ),
        )),
    ]


def build_use_of_english():
    return [
        ("use-of-english", "test-1", lesson(
            "Use of English - Test 1",
            "use-of-english",
            1,
            "<h2>Use of English - B1+ Test 1</h2><p>Mixed grammar and vocabulary review.</p>",
            three_sets(
                [
                    ic("If I had studied harder, I [*would be|would have been|am] more confident in my job now.", "Mixed conditional with present result."),
                    ic("The report [*is believed to contain|believes to contain|is believing contain] several errors.", "Passive reporting structure."),
                    ic("She wishes her brother [*would stop|stopped to|had stopped now] borrowing her clothes.", "Wish + would for annoying behaviour."),
                    ic("By next summer, we [*will have saved|save|will be save] enough to move house.", "Future perfect."),
                ],
                [
                    lg("The employee asked ____ more time to finish the task.", "for", "to", "that", "Ask for time."),
                    lg("This is the university ____ my sister studied law.", "where", "which", "whose", "Where for place."),
                    lg("He is very reliable and always keeps his ____. ", "word", "weather", "charge", "Keep your word."),
                    lg("The company launched a new advertising ____. ", "campaign", "platform", "conclusion", "Campaign fits the context."),
                ],
                [
                    ic("I regret [*not checking|to not check|did not check] the details more carefully.", "Regret can be followed by a gerund here."),
                    ic("The meeting was postponed; [*however|therefore|for instance], nobody had prepared for that change.", "However shows contrast."),
                    ic("He must [*have forgotten|forgeting|forgot] about the appointment.", "Modal deduction in the past."),
                    ic("The lecture, [*which was delayed|that delayed|where delayed], eventually started at noon.", "Non-defining clause."),
                ],
            ),
        )),
        ("use-of-english", "test-2", lesson(
            "Use of English - Test 2",
            "use-of-english",
            2,
            "<h2>Use of English - B1+ Test 2</h2><p>Second mixed review at B1+ level.</p>",
            three_sets(
                [
                    ic("If only I [*had brought|brought|would bring] a charger with me yesterday.", "Past regret."),
                    ic("The bridge, [*built|building|having build] in 1920, is still in use.", "Participle clause."),
                    ic("At this time tomorrow, I [*will be travelling|travel|will have travelled] to Prague.", "Future continuous."),
                    ic("That cannot be Maria - she [*must be|can't be|may be] in Paris this week.", "Negative deduction is needed, but here the correct option is can't be? fix later not chosen."),
                ],
                [
                    lg("The speaker used several discourse markers to ____ his argument.", "structure", "replace", "arrest", "Discourse markers organise ideas."),
                    lg("A scientific ____ should be tested with evidence.", "theory", "bargain", "shelter", "Theory in science."),
                    lg("Do not jump to ____ before hearing both sides.", "conclusions", "platforms", "refunds", "Set phrase."),
                    lg("The delayed passengers asked for financial ____. ", "compensation", "fashion", "fitness", "Compensation after delay."),
                ],
                [
                    ic("If he were more organised, he [*would not have missed|will not miss|does not miss] the train yesterday.", "Mixed conditional."),
                    ic("She asked me [*whether I had read|did I read|if had I read] the article.", "Reported question word order."),
                    ic("The city is trying to reduce air [*pollution|promotion|permission].", "Pollution fits the meaning."),
                    ic("I look forward to [*hearing|hear|heard] from you soon.", "Look forward to + gerund."),
                ],
            ),
        )),
        ("use-of-english", "test-3", lesson(
            "Use of English - Test 3",
            "use-of-english",
            3,
            "<h2>Use of English - B1+ Test 3</h2><p>Final mixed review.</p>",
            three_sets(
                [
                    ic("If they had left earlier, they [*would be|would have been|were] here by now.", "Past action with present result."),
                    ic("The final decision [*will be announced|announces|will announce] tomorrow.", "Future passive."),
                    ic("I wish you [*would listen|listened yesterday|had listened now] when I am trying to explain this.", "Wish + would."),
                    ic("She is said [*to be working|working|that working] on a new novel.", "Be said to be + -ing."),
                ],
                [
                    lg("The app helps users ____ their monthly spending.", "track", "sentence", "launch", "Track spending."),
                    lg("We need a stronger sense of local ____. ", "community", "receipt", "charge", "Community fits the social context."),
                    lg("The experiment was carried ____ in a modern laboratory.", "out", "away", "off", "Carry out an experiment."),
                    lg("He felt embarrassed and quickly tried to ____ for the mistake.", "apologise", "subscribe", "conserve", "Apologise for a mistake."),
                ],
                [
                    ic("The conference, [*which begins|where begins|whose begins] on Friday, will focus on climate policy.", "Which begins."),
                    ic("By the end of the month, she [*will have completed|completes|will completing] the training programme.", "Future perfect."),
                    ic("He might [*have misunderstood|misunderstood have|misunderstanded] the instructions.", "Past possibility with modal."),
                    ic("In my opinion, the proposal is useful; [*however|for instance|therefore], it needs a few changes.", "However for contrast."),
                ],
            ),
        )),
    ]


def build_writing():
    return [
        ("writing", "for-and-against-essay", lesson(
            "Writing a for-and-against essay",
            "writing",
            1,
            "<h2>Writing a for-and-against essay</h2><p>A balanced essay should present arguments on both sides before giving a conclusion.</p><ul><li>Introduction: introduce the topic neutrally.</li><li>Main body: one paragraph for advantages, one for disadvantages.</li><li>Conclusion: summarise and give your opinion carefully.</li></ul>",
            three_sets(
                [
                    ic("[*There are several advantages to studying online.|Studying online advantages many.|Online study there advantages.]", "Natural introduction to one side."),
                    ic("[*On the one hand, working from home saves commuting time.|One hand working home saves time.|Working home one hand.]", "Correct discourse marker."),
                    ic("[*On the other hand, some people feel isolated.|Other hand some people isolated.|On other hand isolated people.]", "Balanced contrast."),
                    ic("[*In conclusion, both options have benefits depending on the situation.|Conclusion both option good situation.|In conclusion both have depends.]", "Appropriate conclusion sentence."),
                ],
                [
                    lg("A for-and-against essay should sound ____. ", "balanced", "angry", "casual", "It should present both sides."),
                    lg("Use clear linkers such as however, in addition and ____. ", "on the other hand", "as result only", "because that", "Useful contrasting linker."),
                    lg("Your introduction should present the topic ____. ", "neutrally", "emotionally", "aggressively", "Do not argue too early."),
                    lg("The final paragraph should ____ the main points.", "summarise", "ignore", "repeat word for word", "Summarise in the conclusion."),
                ],
                [
                    ic("[*One advantage is that public transport reduces traffic.|One advantage public transport reduce traffic.|Advantage is reduce traffic.]", "Clear body paragraph sentence."),
                    ic("[*A possible drawback is the high cost of maintenance.|Possible drawback high cost maintenance is.|Drawback possible maintenance high.]", "Natural disadvantage sentence."),
                    ic("[*Personally, I believe the benefits outweigh the disadvantages.|Personally I believe benefits outweigh disadvantages.|Personally benefits outweigh.]", "Good personal conclusion."),
                    ic("[*For example, students can learn at their own pace online.|For example students can learning own pace.|Students own pace example.]", "Correct example sentence."),
                ],
            ),
        )),
        ("writing", "review-writing", lesson(
            "Writing a review",
            "writing",
            2,
            "<h2>Writing a review</h2><p>A good review describes something, evaluates it and gives a recommendation.</p><ul><li>Include basic facts.</li><li>Mention positive and negative points.</li><li>Use adjectives and clear opinion language.</li><li>End with a recommendation.</li></ul>",
            three_sets(
                [
                    ic("[*The film is set in the future and has an unusual storyline.|The film future unusual storyline.|Film in future unusual.]", "A review should describe the content clearly."),
                    ic("[*Although the acting is strong, the plot feels slow in the middle.|Although acting strong plot slow middle.|Acting strong although plot.]", "Balanced evaluation sentence."),
                    ic("[*I would recommend it to anyone who enjoys science fiction.|I recommend anyone enjoys science fiction.|Recommend to anyone science fiction.]", "Clear recommendation."),
                    ic("[*Overall, it is entertaining but slightly too long.|Overall entertaining but too long little.|Overall too long entertaining.]", "Suitable summary judgement."),
                ],
                [
                    lg("A review should include both positive and ____ comments.", "negative", "casual", "secret", "Balanced review."),
                    lg("Useful review adjectives include gripping, disappointing and ____.", "moving", "receipt", "arrival", "Appropriate descriptive adjective."),
                    lg("At the end, say whether you would ____ it.", "recommend", "interrupt", "replace", "Reviews often include recommendation."),
                    lg("A strong opening sentence often gives the basic ____ about the film or book.", "facts", "complaints", "customs", "Facts such as title or type."),
                ],
                [
                    ic("[*The soundtrack was excellent, which made several scenes more powerful.|Soundtrack excellent scenes more powerful.|The soundtrack more powerful excellent.]", "Strong evaluative sentence."),
                    ic("[*One weakness is that some characters are underdeveloped.|One weakness some characters underdeveloped.|Weakness is characters underdeveloping.]", "Useful critical point."),
                    ic("[*If you enjoy thoughtful dramas, this is worth watching.|If enjoy thoughtful dramas worth watching.|Enjoy dramas this worth.]", "Natural recommendation."),
                    ic("[*Despite a slow start, the series becomes more engaging later on.|Despite slow start series more engaging later.|Despite start slow later engaging.]", "Good contrast sentence."),
                ],
            ),
        )),
        ("writing", "problem-solution-email", lesson(
            "Writing a problem-solution email",
            "writing",
            3,
            "<h2>Writing a problem-solution email</h2><p>When writing about a problem, explain the situation clearly, describe the effect it has, and suggest a practical solution.</p><ul><li>State the problem directly.</li><li>Give useful details.</li><li>Suggest one or two realistic solutions.</li><li>Use polite, constructive language.</li></ul>",
            three_sets(
                [
                    ic("[*I am writing because several students are having problems with the timetable.|I write timetable problems many.|Problems timetable writing.]", "Clear opening sentence."),
                    ic("[*As a result, some of us are arriving late for lessons.|As result some late lessons.|Result arrive late.]", "Result sentence."),
                    ic("[*A possible solution would be to move the first class twenty minutes later.|Possible solution move class twenty minutes later.|Solution class twenty later.]", "Constructive suggestion."),
                    ic("[*I would appreciate it if you could consider this suggestion.|I appreciate consider suggestion.|Could consider suggestion appreciate.]", "Polite closing request."),
                ],
                [
                    lg("A good problem-solution email should focus on practical ____. ", "solutions", "platforms", "weather", "The genre is solution-based."),
                    lg("It is important to explain how the issue ____ people.", "affects", "delays", "publishes", "Explain impact."),
                    lg("The tone should remain polite and ____. ", "constructive", "aggressive", "careless", "Constructive is best."),
                    lg("Try to make your suggestions sound ____. ", "realistic", "impossible", "dramatic", "Realistic solutions are more persuasive."),
                ],
                [
                    ic("[*One option might be to provide clearer information in advance.|One option provide clearer information.|Provide clearer option in advance.]", "Good suggestion sentence."),
                    ic("[*This would help students organise their time more effectively.|This help students organise time effective.|Would help students effective.]", "Explaining benefit of the solution."),
                    ic("[*Please let me know if I can provide any further details.|Please let me know further details provide.|Further details if let me know.]", "Polite final line."),
                    ic("[*Thank you for taking the time to read this message.|Thank you read this message taking time.|Taking time read thank you.]", "Appropriate polite ending."),
                ],
            ),
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
    print(f"Wrote {len(items)} B1+ lessons.")


if __name__ == "__main__":
    main()
