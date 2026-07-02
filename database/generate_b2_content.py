from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
LEVEL = "b2"


def ensure_dir(section: str) -> Path:
    path = CONTENT / section / LEVEL
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
        "level": LEVEL,
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
    items.append(("grammar", "inversion-negative-adverbials", lesson(
        "Inversion with negative adverbials",
        "grammar",
        1,
        "<h2>Inversion with negative adverbials</h2><p>After negative or restrictive adverbials at the start of a sentence, we use inversion (auxiliary before subject), like in questions.</p><ul><li><em>Never have I seen such a crowd.</em></li><li><em>Not only did she apologise, but she also offered compensation.</em></li><li><em>Hardly had we arrived when the meeting started.</em></li></ul>",
        three_sets(
            [
                ic("[*Never have I|I have never] felt so embarrassed in a meeting.", "Inversion after Never at the start."),
                ic("[*Not only did|Not only] he win the prize, but he also broke the record.", "Not only + auxiliary + subject."),
                ic("[*Hardly had|Hardly] the train left when it began to rain.", "Hardly had + subject + past participle."),
                ic("[*Rarely do|Rarely] people admit their mistakes so openly.", "Rarely do + subject + base verb."),
                ic("[*Only then did|Only then] she realise how serious the problem was.", "Only then did + subject."),
            ],
            [
                lg("Not until the report was published ____ the public understand the scale of the crisis.", "did", "do", "had", "Not until triggers inversion in the main clause."),
                lg("Seldom ____ such a talented group of musicians perform together.", "do", "does", "did", "Seldom do + plural subject."),
                lg("Little ____ that their decision would change everything.", "did they know", "they knew", "they did know", "Little did they know."),
                lg("No sooner ____ the door than the phone rang.", "had he closed", "he had closed", "did he close", "No sooner had + subject + past participle."),
            ],
            [
                ic("[*Under no circumstances should|Under no circumstances should not] employees share passwords.", "Under no circumstances should + subject."),
                ic("[*Not once did|Not once] the speaker mention the budget.", "Not once did + subject."),
                ic("[*Only by working together can|Only by working together we can] we solve this problem.", "Only by + phrase + can + subject."),
                ic("[*Never before has|Never before have] the company received so many complaints.", "Never before has + subject."),
                ic("[*Hardly ever do|Hardly ever] politicians answer the question directly.", "Hardly ever do + subject."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-past-modals", lesson(
        "Advanced past modals",
        "grammar",
        2,
        "<h2>Advanced past modals</h2><p>Past modals express criticism, regret, deduction or unnecessary action about the past.</p><ul><li><strong>should have done</strong> = criticism / regret</li><li><strong>needn't have done</strong> = unnecessary action</li><li><strong>might/could have done</strong> = past possibility</li><li><strong>must have done</strong> = strong past deduction</li></ul>",
        three_sets(
            [
                ic("You [*should have told|should tell|must tell] me earlier - I missed the deadline.", "Regret about a past action."),
                ic("She [*needn't have bought|mustn't have bought|shouldn't buy] so much food; we had plenty already.", "The action was unnecessary."),
                ic("He [*must have forgotten|can't have forgotten|might forget] about the meeting - he never came.", "Strong deduction about the past."),
                ic("They [*could have taken|could take|must take] the earlier train and avoided the delay.", "Missed opportunity in the past."),
                ic("I [*shouldn't have said|needn't have said|mustn't say] that in front of everyone.", "Regret about something said."),
            ],
            [
                lg("The lights were on, so someone ____ home.", "must have been", "can't have been", "needn't have been", "Logical deduction."),
                lg("You ____ so much money on a jacket you never wear.", "needn't have spent", "must have spent", "should spend", "Unnecessary past spending."),
                lg("She looks upset. She ____ the results already.", "might have heard", "must hear", "should hear", "Possible explanation."),
                lg("He ____ more carefully before signing the contract.", "should have read", "needn't have read", "can't have read", "Criticism of a past failure."),
            ],
            [
                ic("The document is missing. Someone [*must have removed|should remove|needn't remove] it.", "Strong deduction about a past action."),
                ic("We [*needn't have worried|shouldn't worry|mustn't worry] - the exam was easier than expected.", "Worry was unnecessary."),
                ic("She [*could have become|could become|must become] a lawyer, but she chose teaching instead.", "Past possibility that did not happen."),
                ic("You [*should have checked|need have checked|must check] the address before sending the parcel.", "Advice about a past mistake."),
                ic("He [*can't have seen|must have seen|should see] the warning sign - it was huge.", "Impossible deduction."),
            ],
        ),
    )))
    items.append(("grammar", "cleft-sentences", lesson(
        "Cleft sentences",
        "grammar",
        3,
        "<h2>Cleft sentences</h2><p>Cleft sentences emphasise one part of a sentence.</p><ul><li><strong>It is/was ... that/who:</strong> It was Maria who solved the problem.</li><li><strong>What ... is/was:</strong> What I need is a short break.</li><li><strong>All ... is/was:</strong> All I want is an honest answer.</li></ul>",
        three_sets(
            [
                ic("It [*was|is|were] the manager who made the final decision.", "Past emphasis with It was ... who."),
                ic("[*What|That|Which] surprised me most was her confidence.", "What-clause for emphasis."),
                ic("It [*is|was|are] honesty that matters most in this job.", "It is ... that emphasises honesty."),
                ic("[*All|Every|Each] I asked for was five more minutes.", "All I asked for."),
                ic("It [*was|is|were] in 2019 that the company expanded abroad.", "Emphasis on time."),
            ],
            [
                lg("It was the poor lighting ____ made photography difficult.", "that", "who", "where", "Thing, not person."),
                lg("What we need now ____ a clear plan.", "is", "are", "was", "What we need is ..."),
                lg("It was Julia ____ recommended the software.", "who", "which", "where", "Person: who."),
                lg("All he wanted ____ to be left alone.", "was", "were", "is", "All he wanted was ..."),
            ],
            [
                ic("It [*was|is|were] because of the storm that the flight was cancelled.", "Reason emphasised with It was because ..."),
                ic("[*What|That|Which] I cannot understand is their silence.", "What-clause as subject."),
                ic("It [*is|was|are] your attitude that worries me.", "Emphasis on attitude."),
                ic("[*All|Every|Both] she did was smile and walk away.", "All she did was ..."),
                ic("It [*was|is|were] the first edition that collectors value most.", "Emphasis on object."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-reported-speech", lesson(
        "Advanced reported speech",
        "grammar",
        4,
        "<h2>Advanced reported speech</h2><p>At B2 level, use a wide range of reporting verbs and structures: <em>advise + gerund</em>, <em>warn + not to</em>, <em>deny + gerund</em>, <em>accuse + of</em>, passive reporting (<em>He was said to be ...</em>).</p>",
        three_sets(
            [
                ic("She advised me [*to apply|applying|apply] for the scholarship.", "Advise + to-infinitive."),
                ic("The guide warned us [*not to touch|to not touch|not touching] the exhibits.", "Warn + not to."),
                ic("He denied [*taking|to take|take] the money from the till.", "Deny + gerund."),
                ic("They accused her [*of lying|to lie|lie] in the interview.", "Accuse + of + gerund/noun."),
                ic("The journalist was reported [*to have resigned|resigning|resigned] the previous day.", "Passive reporting with perfect infinitive."),
            ],
            [
                lg("The teacher encouraged the students ____ questions.", "to ask", "asking", "ask", "Encourage + to-infinitive."),
                lg("He apologised ____ late.", "for arriving", "to arrive", "arriving to", "Apologise for + gerund."),
                lg("She reminded me ____ the documents.", "to bring", "bring", "bringing", "Remind + to-infinitive."),
                lg("The company is believed ____ planning major job cuts.", "to be", "being", "be", "Believed to be + -ing."),
            ],
            [
                ic("The witness claimed [*to have seen|seeing|seen] the suspect near the station.", "Claim + perfect infinitive."),
                ic("They insisted on [*paying|to pay|pay] for dinner themselves.", "Insist on + gerund."),
                ic("He threatened [*to report|reporting|report] them to the police.", "Threaten + to-infinitive."),
                ic("She was said [*to be|being|be] one of the best surgeons in the country.", "Passive reporting structure."),
                ic("The manager refused [*to discuss|discussing|discuss] salaries in public.", "Refuse + to-infinitive."),
            ],
        ),
    )))
    items.append(("grammar", "ellipsis-and-substitution", lesson(
        "Ellipsis and substitution",
        "grammar",
        5,
        "<h2>Ellipsis and substitution</h2><p>We avoid repetition with auxiliary verbs, so/neither, and pronouns like <em>one/ones</em>, <em>do so</em>, <em>such</em>.</p><ul><li><em>I enjoy hiking, and so does my sister.</em></li><li><em>He didn't call, nor did she.</em></li><li><em>I'd like the blue one, not the red one.</em></li></ul>",
        three_sets(
            [
                ic("She speaks French fluently, and so [*does|is|has] her brother.", "So + auxiliary + subject."),
                ic("I haven't finished the report, and neither [*have|has|do] my colleagues.", "Neither + auxiliary for negative agreement."),
                ic("This laptop is faster than the old [*one|ones|it].", "One substitutes a singular countable noun."),
                ic("If you need help, please [*do so|do it so|do] immediately.", "Do so = do that action."),
                ic("They promised to attend, but they didn't [*do|did|done].", "Auxiliary verb replaces the main verb phrase."),
            ],
            [
                lg("He loves jazz, and so ____ his wife.", "does", "is", "has", "So does for present simple."),
                lg("I won't accept the offer, and neither ____ she.", "will", "do", "did", "Neither will she."),
                lg("These shoes are more comfortable than the previous ____. ", "ones", "one", "pair one", "Plural ones."),
                lg("She said she would call, but she never ____. ", "did", "was", "had", "Did replaces called."),
            ],
            [
                ic("A: 'I'm exhausted.' B: 'So [*am|do|have] I.'", "So am I for be."),
                ic("He didn't enjoy the film, and nor [*did|do|was] I.", "Nor did I."),
                ic("I'll take the green scarf rather than the grey [*one|ones|it].", "One for singular scarf."),
                ic("They asked us to leave early, and we [*did so|did it|were so].", "Did so = left early."),
                ic("She can swim well, but her brother [*can't|doesn't|isn't].", "Can't replaces can swim well."),
            ],
        ),
    )))
    items.append(("grammar", "nominalisation", lesson(
        "Nominalisation",
        "grammar",
        6,
        "<h2>Nominalisation</h2><p>Nominalisation turns verbs or adjectives into nouns to make writing more formal and concise.</p><ul><li>decide → decision</li><li>develop → development</li><li>aware → awareness</li><li>fail → failure</li></ul>",
        three_sets(
            [
                ic("The government's [*decision|decide|decisive] surprised many voters.", "Decide → decision."),
                ic("There has been rapid [*development|develop|developed] in renewable energy.", "Develop → development."),
                ic("The campaign aims to raise public [*awareness|aware|awaring] of mental health.", "Aware → awareness."),
                ic("His [*failure|fail|failed] to reply cost him the contract.", "Fail → failure."),
                ic("We need a full [*explanation|explain|explanatory] of the new policy.", "Explain → explanation."),
            ],
            [
                lg("The ____ of the new law took several months.", "introduction", "introduce", "introduced", "Introduce → introduction."),
                lg("There was widespread ____ after the announcement.", "confusion", "confuse", "confused", "Confuse → confusion."),
                lg("Her ____ to the team was immediate.", "contribution", "contribute", "contributing", "Contribute → contribution."),
                lg("The report highlights the ____ of better training.", "importance", "important", "importantly", "Important → importance."),
            ],
            [
                ic("The company's [*expansion|expand|expanded] into Asia was successful.", "Expand → expansion."),
                ic("There is growing [*concern|concerned|concerning] about data security.", "Concern as noun."),
                ic("The judge questioned the [*accuracy|accurate|accurately] of the statement.", "Accurate → accuracy."),
                ic("His sudden [*departure|depart|departing] shocked colleagues.", "Depart → departure."),
                ic("We discussed the [*possibility|possible|possibly] of remote work.", "Possible → possibility."),
            ],
        ),
    )))
    items.append(("grammar", "causative-have-get", lesson(
        "Causative have and get",
        "grammar",
        7,
        "<h2>Causative have and get</h2><p>Use <strong>have/get + object + past participle</strong> when someone else does something for you.</p><ul><li><em>I had my hair cut yesterday.</em></li><li><em>She got her car repaired at the garage.</em></li><li><em>We need to have the documents translated.</em></li></ul>",
        three_sets(
            [
                ic("I need to [*have|get|make] my laptop repaired before the trip.", "Have + object + past participle."),
                ic("She [*got|had|made] her passport renewed last week.", "Get + object + past participle."),
                ic("They are [*having|getting|making] the house painted this month.", "Present continuous causative."),
                ic("He [*had|got|made] his suit cleaned before the interview.", "Past causative."),
                ic("We should [*have|get|do] the contract checked by a lawyer.", "Have something done by someone."),
            ],
            [
                lg("I must ____ my eyes tested soon.", "have", "make", "do", "Have my eyes tested."),
                lg("She ____ her phone screen replaced at the shop.", "got", "made", "did", "Got + object + replaced."),
                lg("They are ____ the roof fixed after the storm.", "having", "making", "doing", "Having the roof fixed."),
                lg("He finally ____ his documents translated professionally.", "had", "made", "got to", "Had + object + translated."),
            ],
            [
                ic("We [*had|made|did] the invitations printed yesterday.", "Had + object + past participle."),
                ic("She wants to [*get|have|make] her nails done before the wedding.", "Get + object + done."),
                ic("They [*are having|are making|are doing] the garden redesigned.", "Present continuous."),
                ic("You should [*have|get|make] that tooth looked at.", "Have + object + looked at."),
                ic("We [*had|made|did] the windows cleaned before the guests arrived.", "Have + object + past participle."),
            ],
        ),
    )))
    items.append(("grammar", "subjunctive-formal", lesson(
        "Subjunctive and formal structures",
        "grammar",
        8,
        "<h2>Subjunctive and formal structures</h2><p>After certain adjectives and verbs (essential, vital, recommend, suggest, insist), we use the base form of the verb, especially in formal English.</p><ul><li><em>It is essential that he be present.</em></li><li><em>I recommend that she apply early.</em></li><li><em>They insisted that he leave immediately.</em></li></ul>",
        three_sets(
            [
                ic("It is vital that every employee [*be|is|was] informed.", "Subjunctive: be, not is."),
                ic("The doctor recommended that she [*rest|rests|rested] for a week.", "Recommend that + base form."),
                ic("They insisted that he [*leave|leaves|left] the building.", "Insist that + base form."),
                ic("It is important that the report [*remain|remains|remained] confidential.", "Remain, not remains."),
                ic("I suggest that he [*apply|applies|applied] for the grant.", "Suggest that + base form."),
            ],
            [
                lg("It is essential that she ____ on time.", "arrive", "arrives", "arrived", "Base form after essential that."),
                lg("The committee demanded that the minister ____ an explanation.", "give", "gives", "gave", "Demand that + base form."),
                lg("It is crucial that the data ____ accurate.", "be", "is", "was", "Subjunctive be."),
                lg("They proposed that the meeting ____ postponed.", "be", "is", "was", "Propose that + be + past participle."),
            ],
            [
                ic("It is necessary that he [*submit|submits|submitted] the form today.", "Base form after necessary that."),
                ic("The rules require that every visitor [*sign|signs|signed] in.", "Require that + base form."),
                ic("It is imperative that the issue [*be|is|was] resolved quickly.", "Imperative that + be."),
                ic("She requested that I [*not share|do not share|did not share] the file.", "Negative subjunctive."),
                ic("The judge ordered that the witness [*remain|remains|remained] silent.", "Order that + base form."),
            ],
        ),
    )))
    return items


def build_vocabulary():
    items = []

    def make_vocab(title, slug, sort_order, explanation, lettered1, dropdown, bank, lettered2):
        items.append(("vocabulary", slug, lesson(title, "vocabulary", sort_order, explanation, vocab_sets(lettered1, dropdown, bank, lettered2))))

    make_vocab(
        "Politics and government",
        "politics-and-government",
        1,
        "<h2>Politics and government</h2><ul><li>election, parliament, policy, candidate, coalition</li><li>legislation, referendum, opposition, campaign, mandate</li><li>verbs: vote, govern, debate, legislate</li></ul>",
        [
            lg("Citizens will vote in the general ____ next month.", "election", "platform", "receipt", "General election."),
            lg("The new ____ aims to reduce carbon emissions by 2030.", "policy", "slogan", "habit", "Government policy."),
            lg("Several parties formed a ____ to stay in power.", "coalition", "subscription", "runway", "Coalition government."),
            lg("The ____ debated the proposed law for hours.", "parliament", "laboratory", "terminal", "Parliament debates legislation."),
        ],
        [
            dd("Each ____ presented their programme to voters.", "candidate"),
            dd("The government introduced new ____ on data protection.", "legislation"),
            dd("The ____ called for an investigation into the scandal.", "opposition"),
            dd("Activists organised a ____ to raise public support.", "campaign"),
            dd("The president claimed a strong ____ after winning decisively.", "mandate"),
        ],
        ["candidate", "legislation", "opposition", "campaign", "mandate", "referendum", "debate", "govern", "vote", "policy"],
        [
            lg("The country held a ____ on whether to leave the trade bloc.", "referendum", "deadline", "discount", "Referendum = public vote."),
            lg("Politicians often ____ complex issues in televised discussions.", "debate", "repair", "depart", "Debate issues."),
            lg("Elected officials are expected to ____ responsibly.", "govern", "commute", "subscribe", "Govern a country."),
            lg("Every citizen over eighteen has the right to ____.", "vote", "charge", "queue", "Vote in elections."),
        ],
    )
    make_vocab(
        "Environment and climate policy",
        "environment-climate-policy",
        2,
        "<h2>Environment and climate policy</h2><ul><li>emissions, renewable, sustainability, biodiversity, drought</li><li>carbon footprint, ecosystem, conservation, mitigation</li><li>verbs: recycle, conserve, emit, adapt</li></ul>",
        [
            lg("The city plans to cut carbon ____ by forty per cent.", "emissions", "receipts", "platforms", "Carbon emissions."),
            lg("Solar and wind power are examples of ____ energy.", "renewable", "disposable", "temporary", "Renewable energy."),
            lg("Long ____ can destroy crops and threaten water supplies.", "droughts", "deadlines", "discounts", "Drought = lack of rain."),
            lg("Protecting ____ is essential for healthy ecosystems.", "biodiversity", "publicity", "furniture", "Biodiversity."),
        ],
        [
            dd("Companies are trying to reduce their carbon ____. ", "footprint"),
            dd("Governments must invest in climate ____ strategies.", "mitigation"),
            dd("The national park was created for wildlife ____. ", "conservation"),
            dd("An ____ can collapse if key species disappear.", "ecosystem"),
            dd("We should ____ more plastic instead of throwing it away.", "recycle"),
        ],
        ["footprint", "mitigation", "conservation", "ecosystem", "recycle", "sustainability", "emit", "adapt", "conserve", "renewable"],
        [
            lg("Long-term ____ requires changes in production and consumption.", "sustainability", "competition", "negotiation", "Sustainability."),
            lg("Factories should ____ fewer harmful gases.", "emit", "donate", "interrupt", "Emit gases."),
            lg("Coastal cities must ____ to rising sea levels.", "adapt", "complain", "depart", "Adapt to change."),
            lg("We need stronger laws to ____ natural habitats.", "conserve", "advertise", "persuade", "Conserve habitats."),
        ],
    )
    make_vocab(
        "Law and justice",
        "law-and-justice",
        3,
        "<h2>Law and justice</h2><ul><li>verdict, evidence, defendant, prosecution, sentence</li><li>witness, jury, appeal, bail, conviction</li><li>verbs: sue, acquit, testify, convict</li></ul>",
        [
            lg("The jury reached a guilty ____ after two days.", "verdict", "platform", "recipe", "Verdict = decision."),
            lg("The ____ presented strong proof in court.", "prosecution", "subscription", "headline", "Prosecution brings the case."),
            lg("The judge gave him a five-year ____.", "sentence", "agenda", "campaign", "Prison sentence."),
            lg("The ____ claimed he was at home when the crime happened.", "defendant", "candidate", "consumer", "Defendant in a trial."),
        ],
        [
            dd("The ____ described exactly what she had seen.", "witness"),
            dd("His lawyer filed an ____ against the decision.", "appeal"),
            dd("The court decided to ____ him of all charges.", "acquit"),
            dd("She was asked to ____ in front of the jury.", "testify"),
            dd("The company threatened to ____ the newspaper for libel.", "sue"),
        ],
        ["witness", "appeal", "acquit", "testify", "sue", "conviction", "evidence", "jury", "bail", "convict"],
        [
            lg("Without clear ____, the case may fail.", "evidence", "publicity", "furniture", "Evidence in court."),
            lg("The ____ must decide whether the accused is guilty.", "jury", "audience", "crowd", "Jury of citizens."),
            lg("He was released on ____ until the next hearing.", "bail", "debt", "salary", "Released on bail."),
            lg("A criminal ____ can affect future employment.", "conviction", "vacation", "discount", "Conviction = guilty verdict."),
        ],
    )
    make_vocab(
        "Psychology and behaviour",
        "psychology-and-behaviour",
        4,
        "<h2>Psychology and behaviour</h2><ul><li>anxiety, motivation, perception, resilience, instinct</li><li>stimulus, behaviour, trait, coping, bias</li><li>verbs: perceive, motivate, cope, influence</li></ul>",
        [
            lg("High levels of ____ can affect sleep and concentration.", "anxiety", "luggage", "traffic", "Anxiety."),
            lg("Her ____ helped her recover quickly from failure.", "resilience", "receipt", "platform", "Resilience = ability to recover."),
            lg("Some decisions are based on ____ rather than logic.", "instinct", "agenda", "deadline", "Instinct."),
            lg("A positive environment can increase student ____.", "motivation", "compensation", "customs", "Motivation."),
        ],
        [
            dd("Our ____ of colour can be affected by lighting.", "perception"),
            dd("Loud noise acted as a powerful ____ in the experiment.", "stimulus"),
            dd("She developed better ____ strategies during therapy.", "coping"),
            dd("Advertisers try to ____ consumer choices.", "influence"),
            dd("Confirmation ____ makes people favour information they already believe.", "bias"),
        ],
        ["perception", "stimulus", "coping", "influence", "bias", "behaviour", "trait", "motivate", "perceive", "resilience"],
        [
            lg("Aggressive ____ is often linked to stress.", "behaviour", "furniture", "platform", "Behaviour."),
            lg("Honesty is considered an important personality ____.", "trait", "ticket", "recipe", "Personality trait."),
            lg("Good leaders know how to ____ their teams.", "motivate", "recycle", "depart", "Motivate teams."),
            lg("Children ____ danger differently from adults.", "perceive", "charge", "queue", "Perceive danger."),
        ],
    )
    make_vocab(
        "Business and economics",
        "business-and-economics",
        5,
        "<h2>Business and economics</h2><ul><li>revenue, profit, merger, recession, inflation</li><li>shareholder, investment, startup, bankruptcy, turnover</li><li>verbs: invest, expand, compete, forecast</li></ul>",
        [
            lg("Rising ____ has increased the cost of everyday goods.", "inflation", "pollution", "humidity", "Inflation."),
            lg("The two companies announced a ____ worth billions.", "merger", "holiday", "recipe", "Merger = joining companies."),
            lg("During a ____, many businesses close or cut jobs.", "recession", "celebration", "vacation", "Economic recession."),
            lg("Annual ____ rose after the successful product launch.", "revenue", "luggage", "weather", "Revenue = income."),
        ],
        [
            dd("They decided to ____ in renewable technology.", "invest"),
            dd("Small ____ often struggle to access bank loans.", "startups"),
            dd("The firm warned it might face ____ without new funding.", "bankruptcy"),
            dd("____ want higher returns on their shares.", "Shareholders"),
            dd("Analysts ____ slower growth next year.", "forecast"),
        ],
        ["invest", "startups", "bankruptcy", "Shareholders", "forecast", "profit", "turnover", "compete", "expand", "investment"],
        [
            lg("Net ____ increased despite higher production costs.", "profit", "debt", "traffic", "Profit after costs."),
            lg("The shop's annual ____ exceeded expectations.", "turnover", "sentence", "verdict", "Turnover = total sales."),
            lg("Local firms must ____ with cheaper imports.", "compete", "apologise", "testify", "Compete in the market."),
            lg("They plan to ____ into three new European markets.", "expand", "recycle", "interrupt", "Expand business."),
        ],
    )
    make_vocab(
        "Arts and media",
        "arts-and-media",
        6,
        "<h2>Arts and media</h2><ul><li>exhibition, critic, masterpiece, censorship, premiere</li><li>documentary, screenplay, genre, curator, broadcast</li><li>verbs: perform, publish, review, adapt</li></ul>",
        [
            lg("The museum's new ____ features contemporary photography.", "exhibition", "election", "recession", "Art exhibition."),
            lg("The film received praise from every major ____.", "critic", "witness", "defendant", "Film critic."),
            lg("Many consider the novel a literary ____.", "masterpiece", "receipt", "platform", "Masterpiece."),
            lg("The ____ of the play attracted celebrities from across Europe.", "premiere", "verdict", "deadline", "Premiere = first performance."),
        ],
        [
            dd("The director decided to ____ the novel for television.", "adapt"),
            dd("The orchestra will ____ live at the festival.", "perform"),
            dd("The journalist wrote a detailed ____ of the concert.", "review"),
            dd("The channel will ____ the debate tonight.", "broadcast"),
            dd("She hopes to ____ her first collection of poems next year.", "publish"),
        ],
        ["adapt", "perform", "review", "broadcast", "publish", "documentary", "screenplay", "genre", "censorship", "curator"],
        [
            lg("The ____ explored the history of protest movements.", "documentary", "sentence", "bail", "Documentary film."),
            lg("He spent months writing the ____.", "screenplay", "verdict", "mandate", "Screenplay for a film."),
            lg("Horror is a popular film ____ worldwide.", "genre", "policy", "debt", "Genre = type."),
            lg("The ____ selected works from emerging artists.", "curator", "jury", "witness", "Museum curator."),
        ],
    )
    make_vocab(
        "Globalisation and society",
        "globalisation-and-society",
        7,
        "<h2>Globalisation and society</h2><ul><li>migration, integration, diversity, trade, outsourcing</li><li>multinational, supply chain, cultural exchange, inequality</li><li>verbs: relocate, integrate, outsource, connect</li></ul>",
        [
            lg("Global ____ has changed labour markets in many countries.", "trade", "weather", "furniture", "International trade."),
            lg("Cities with high ____ often have vibrant food and arts scenes.", "diversity", "pollution", "debt", "Cultural diversity."),
            lg("Many firms ____ customer support to other countries.", "outsource", "apologise", "testify", "Outsource work."),
            lg("Successful ____ requires language support and community programmes.", "integration", "inflation", "censorship", "Social integration."),
        ],
        [
            dd("Economic ____ can create both opportunities and pressure on wages.", "migration"),
            dd("A ____ corporation operates in dozens of countries.", "multinational"),
            dd("The pandemic disrupted global ____ chains.", "supply"),
            dd("The festival promoted cultural ____ between nations.", "exchange"),
            dd("Some communities worry about rising social ____.", "inequality"),
        ],
        ["migration", "multinational", "supply", "exchange", "inequality", "relocate", "integrate", "connect", "outsourcing", "globalisation"],
        [
            lg("The factory plans to ____ production to eastern Europe.", "relocate", "recycle", "perform", "Relocate production."),
            lg("Schools help new arrivals ____ into local society.", "integrate", "compete", "forecast", "Integrate into society."),
            lg("Technology helps people ____ across continents instantly.", "connect", "convict", "depart", "Connect globally."),
            lg("____ has made products cheaper but jobs more mobile.", "Globalisation", "Censorship", "Bankruptcy", "Globalisation."),
        ],
    )
    make_vocab(
        "Health and medicine",
        "health-and-medicine",
        8,
        "<h2>Health and medicine</h2><ul><li>diagnosis, symptom, chronic, immune, vaccine</li><li>treatment, prescription, surgery, rehabilitation, epidemic</li><li>verbs: diagnose, prescribe, recover, prevent</li></ul>",
        [
            lg("The doctor made an accurate ____ after several tests.", "diagnosis", "campaign", "platform", "Medical diagnosis."),
            lg("A persistent cough can be a common ____ of infection.", "symptom", "verdict", "mandate", "Symptom."),
            lg("Patients with ____ conditions need long-term care.", "chronic", "temporary", "optional", "Chronic illness."),
            lg("The ____ programme helped reduce cases dramatically.", "vaccine", "screenplay", "receipt", "Vaccine programme."),
        ],
        [
            dd("The nurse will ____ antibiotics for the infection.", "prescribe"),
            dd("He needed months of ____ after the knee injury.", "rehabilitation"),
            dd("Good hygiene can ____ many illnesses.", "prevent"),
            dd("She began to ____ quickly after the operation.", "recover"),
            dd("The hospital specialises in heart ____.", "surgery"),
        ],
        ["prescribe", "rehabilitation", "prevent", "recover", "surgery", "treatment", "immune", "epidemic", "diagnose", "prescription"],
        [
            lg("The new ____ proved effective in clinical trials.", "treatment", "genre", "coalition", "Medical treatment."),
            lg("A strong ____ system helps the body fight disease.", "immune", "trade", "supply", "Immune system."),
            lg("The region faced a flu ____ last winter.", "epidemic", "premiere", "merger", "Epidemic."),
            lg("You need a ____ to collect the medication.", "prescription", "referendum", "screenplay", "Doctor's prescription."),
        ],
    )
    return items


def build_listening():
    return [
        ("listening", "university-lecture-excerpt", lesson(
            "University lecture excerpt",
            "listening",
            1,
            "<h2>University lecture excerpt</h2><p>Listen to part of a lecture on urban planning.</p><h3>Transcript</h3><p><strong>Lecturer:</strong> Today I want to focus on why some cities become more liveable than others. It is not enough to build taller buildings or wider roads. Successful cities invest in public transport, green spaces and affordable housing. They also encourage mixed neighbourhoods where people live, work and study close together. Without this balance, cities may grow economically but still fail to improve everyday life for residents.</p>",
            three_sets(
                [
                    ic("The lecturer says taller buildings alone are [*not enough|the main solution|too expensive].", "It is not enough to build taller buildings."),
                    ic("Successful cities invest in affordable [*housing|advertising|entertainment].", "Affordable housing is mentioned."),
                    ic("Mixed neighbourhoods combine living, working and [*studying|shopping only|tourism].", "Live, work and study close together."),
                    ic("Some cities grow economically but fail to improve [*everyday life|international trade|weather conditions].", "That is the lecturer's warning."),
                ],
                [
                    lg("The topic is urban ____. ", "planning", "farming", "painting", "Urban planning lecture."),
                    lg("Green spaces are presented as an important ____. ", "investment", "competition", "sentence", "Investment in green spaces."),
                    lg("The lecturer criticises cities that grow but remain ____. ", "unliveable", "silent", "private", "Fail to improve everyday life."),
                    lg("Public ____ is one key factor.", "transport", "debate", "recipe", "Public transport."),
                ],
                [
                    ic("The speaker's tone is [*academic and analytical|emotional and angry|casual and humorous].", "University lecture style."),
                    ic("The main message is that growth must be [*balanced|avoided|secret].", "Balance is central."),
                    ic("The lecture would interest [*city planners and students|only doctors|only artists].", "Urban planning audience."),
                    ic("The lecturer implies design affects [*quality of life|only business profits|only tourism].", "Everyday life for residents."),
                ],
            ),
            "https://www.youtube.com/watch?v=8O6272q0Awo",
        )),
        ("listening", "job-interview-feedback", lesson(
            "Job interview feedback",
            "listening",
            2,
            "<h2>Job interview feedback</h2><p>Listen to a manager giving feedback after an interview.</p><h3>Transcript</h3><p><strong>Manager:</strong> Thank you for coming in today. You communicated clearly and gave strong examples from your previous role. However, we felt you did not show enough detail about how you handle conflict in a team. We are keeping your application on file and may contact you if another position opens. I would advise you to prepare more concrete stories about problem-solving before your next interview.</p>",
            three_sets(
                [
                    ic("The candidate communicated [*clearly|unclearly|too formally].", "Communicated clearly."),
                    ic("The manager wanted more detail about handling [*conflict|salary|travel].", "Conflict in a team."),
                    ic("The application will be kept [*on file|rejected immediately|published online].", "Keeping application on file."),
                    ic("The manager advises preparing stories about [*problem-solving|holiday plans|office design].", "Concrete problem-solving stories."),
                ],
                [
                    lg("The feedback mentions strong examples from a previous ____. ", "role", "flight", "recipe", "Previous role."),
                    lg("The company may contact the candidate if another ____ opens.", "position", "platform", "storm", "Another position."),
                    lg("The manager's advice is to prepare more ____ stories.", "concrete", "musical", "ancient", "Concrete stories."),
                    lg("The overall result is not an immediate job ____. ", "offer", "ticket", "vaccine", "No immediate offer."),
                ],
                [
                    ic("The feedback is [*constructive|hostile|unclear].", "Advice for improvement."),
                    ic("The candidate's communication was seen as a [*strength|weakness|irrelevant detail].", "Communicated clearly."),
                    ic("Team conflict was treated as an area needing more [*evidence|money|equipment].", "More detail needed."),
                    ic("The manager sounds [*professional and direct|rude|uninterested].", "Professional feedback."),
                ],
            ),
            "https://www.youtube.com/watch?v=4jpdlG8EJhE",
        )),
        ("listening", "panel-discussion-education", lesson(
            "Panel discussion on education",
            "listening",
            3,
            "<h2>Panel discussion on education</h2><p>Listen to part of a panel discussion.</p><h3>Transcript</h3><p><strong>Speaker 1:</strong> Digital tools can personalise learning, but they cannot replace good teaching.<br><strong>Speaker 2:</strong> I agree, yet many schools still lack reliable internet and trained staff.<br><strong>Speaker 1:</strong> That is why investment in teachers matters as much as investment in software.<br><strong>Speaker 2:</strong> Exactly. Technology should support learning, not become an excuse to cut resources.</p>",
            three_sets(
                [
                    ic("Speaker 1 believes digital tools cannot replace [*good teaching|exams|school buildings].", "Cannot replace good teaching."),
                    ic("Speaker 2 mentions unreliable [*internet|transport|weather].", "Lack reliable internet."),
                    ic("Both speakers emphasise investment in [*teachers|stadiums|advertising].", "Investment in teachers."),
                    ic("Technology should not be an excuse to cut [*resources|holidays|sports].", "Cut resources."),
                ],
                [
                    lg("Digital tools can ____ learning.", "personalise", "replace", "cancel", "Personalise learning."),
                    lg("Many schools lack trained ____. ", "staff", "buses", "menus", "Trained staff."),
                    lg("Speaker 2 thinks technology should ____ learning.", "support", "interrupt", "replace", "Support learning."),
                    lg("The discussion is about education and ____. ", "technology", "fashion", "cooking", "Ed-tech topic."),
                ],
                [
                    ic("The speakers largely [*agree|disagree completely|avoid the topic].", "They agree on key points."),
                    ic("The discussion highlights a gap between ideal tools and real [*infrastructure|tourism|entertainment].", "Lack of internet and staff."),
                    ic("The tone is [*balanced|aggressive|comic].", "Balanced panel discussion."),
                    ic("The main warning is against using tech to justify [*fewer resources|more homework|longer holidays].", "Excuse to cut resources."),
                ],
            ),
            "https://www.youtube.com/watch?v=7y_hbz6lM9E",
        )),
        ("listening", "news-report-climate", lesson(
            "News report on climate policy",
            "listening",
            4,
            "<h2>News report on climate policy</h2><p>Listen to a short news report.</p><h3>Transcript</h3><p><strong>Reporter:</strong> Ministers have agreed to reduce national emissions by fifty per cent before 2035. The plan includes subsidies for electric vehicles, stricter rules for heavy industry and funding for home insulation. Environmental groups welcomed the targets but warned that enforcement will be critical. Opposition politicians argued the measures could raise energy costs for households in the short term.</p>",
            three_sets(
                [
                    ic("The plan aims to cut emissions by [*fifty|thirty|seventy] per cent.", "Fifty per cent before 2035."),
                    ic("Subsidies will support [*electric vehicles|air travel|coal mining].", "Electric vehicles."),
                    ic("Environmental groups welcomed the targets but stressed [*enforcement|advertising|tourism].", "Enforcement will be critical."),
                    ic("Opposition politicians fear higher [*energy costs|school fees|ticket prices].", "Energy costs for households."),
                ],
                [
                    lg("The report mentions stricter rules for heavy ____. ", "industry", "fashion", "theatre", "Heavy industry."),
                    lg("Funding will help improve home ____. ", "insulation", "decoration", "parking", "Home insulation."),
                    lg("Ministers have agreed on a new climate ____. ", "plan", "holiday", "concert", "Climate plan."),
                    lg("The deadline mentioned is the year ____. ", "2035", "2020", "2055", "Before 2035."),
                ],
                [
                    ic("The report presents [*both support and criticism|only praise|only jokes].", "Groups welcome targets; opposition warns."),
                    ic("The policy focuses on [*reducing emissions|increasing tourism|building stadiums].", "Climate emissions."),
                    ic("The reporter's style is [*factual|emotional|humorous].", "News report tone."),
                    ic("Environmental groups think targets matter less than [*implementation|celebrities|sports].", "Enforcement is critical."),
                ],
            ),
            "https://www.youtube.com/watch?v=HwMkN_2BTqs",
        )),
        ("listening", "museum-audio-guide", lesson(
            "Museum audio guide",
            "listening",
            5,
            "<h2>Museum audio guide</h2><p>Listen to part of a museum audio guide.</p><h3>Transcript</h3><p><strong>Guide:</strong> You are now standing in front of the museum's most visited painting. Created in 1889, it captures the artist's view from his room during a difficult period of his life. Notice the thick brushstrokes and intense colours, which were highly unusual at the time. Many visitors are surprised to learn that the work was barely recognised during the artist's lifetime and only became famous after his death.</p>",
            three_sets(
                [
                    ic("The painting was created in [*1889|1789|1989].", "Created in 1889."),
                    ic("It shows the artist's view from his [*room|garden|boat].", "View from his room."),
                    ic("The style includes thick brushstrokes and intense [*colours|sounds|smells].", "Thick brushstrokes and intense colours."),
                    ic("The work became famous mainly [*after the artist's death|during his childhood|last year only].", "Famous after his death."),
                ],
                [
                    lg("This is the museum's most ____ painting.", "visited", "hidden", "broken", "Most visited."),
                    lg("The artist painted during a difficult ____ of his life.", "period", "ticket", "recipe", "Difficult period."),
                    lg("The technique was highly ____ at the time.", "unusual", "boring", "cheap", "Highly unusual."),
                    lg("Many visitors are ____ by the story.", "surprised", "charged", "delayed", "Surprised to learn."),
                ],
                [
                    ic("The guide's purpose is to [*inform visitors about the artwork|sell tickets|discuss sports].", "Museum audio guide."),
                    ic("The tone is [*educational|angry|sarcastic].", "Educational guide."),
                    ic("The painting was [*not widely recognised|immediately famous|recently discovered] in the artist's lifetime.", "Barely recognised then."),
                    ic("Visual features mentioned include brushstrokes and [*colours|music|food].", "Colours."),
                ],
            ),
            "https://www.youtube.com/watch?v=fSrLeyfk9SM",
        )),
    ]


def build_reading():
    return [
        ("reading", "ai-and-employment", lesson(
            "AI and the future of employment",
            "reading",
            1,
            "<h2>AI and the future of employment</h2><p>Artificial intelligence is transforming workplaces faster than many governments expected. Routine administrative tasks, basic translation and some forms of data analysis can already be automated. However, experts argue that AI is more likely to change jobs than eliminate them entirely. Workers who combine technical skills with creativity, communication and ethical judgement may become more valuable. The real challenge, therefore, is not only technological development but also education systems that help people adapt throughout their careers.</p>",
            three_sets(
                [
                    ic("AI can already automate some [*administrative tasks|sports events|weather patterns only].", "Routine administrative tasks."),
                    ic("Experts think AI will probably [*change jobs rather than remove all of them|end all employment immediately|have no effect].", "Change jobs rather than eliminate entirely."),
                    ic("Valuable workers may combine technical skills with creativity and [*ethical judgement|physical strength only|holiday planning].", "Ethical judgement is mentioned."),
                    ic("The main challenge includes helping people adapt through [*education|tourism|fashion].", "Education systems."),
                ],
                [
                    lg("Governments did not always expect such rapid ____. ", "transformation", "vacation", "recipe", "Transforming workplaces."),
                    lg("Basic translation is one task that can be ____. ", "automated", "painted", "cooked", "Automated."),
                    lg("Communication is one skill that may become more ____. ", "valuable", "illegal", "distant", "More valuable."),
                    lg("People may need to adapt throughout their ____. ", "careers", "holidays", "meals", "Throughout careers."),
                ],
                [
                    ic("The writer's attitude is [*cautiously optimistic|completely negative|uninterested].", "Change is serious but manageable."),
                    ic("The passage focuses on [*work and skills|museum design|airport security].", "AI and employment."),
                    ic("The text suggests technology alone is [*not the only issue|the only solution|irrelevant].", "Education also matters."),
                    ic("The final sentence emphasises lifelong [*adaptation|competition|isolation].", "Adapt throughout careers."),
                ],
            ),
        )),
        ("reading", "press-freedom-debate", lesson(
            "The debate over press freedom",
            "reading",
            2,
            "<h2>The debate over press freedom</h2><p>In democratic societies, a free press is often described as essential for holding power to account. Journalists investigate corruption, question official statements and inform public debate. Yet the same freedom can be misused to spread misinformation or invade privacy. Recent legislation in several countries attempts to balance protection for journalists with penalties for harmful false reporting. Critics warn that vague laws may silence legitimate criticism, while supporters argue that unchecked false stories can damage democracy itself.</p>",
            three_sets(
                [
                    ic("A free press helps hold [*power|sport|weather] to account.", "Holding power to account."),
                    ic("Journalists may investigate [*corruption|recipes|fashion trends only].", "Investigate corruption."),
                    ic("Freedom can be misused to spread [*misinformation|healthy food|classical music].", "Misinformation."),
                    ic("New laws try to balance journalist protection with penalties for harmful [*false reporting|travel delays|school holidays].", "False reporting."),
                ],
                [
                    lg("Some laws may silence legitimate ____. ", "criticism", "furniture", "sunshine", "Legitimate criticism."),
                    lg("Unchecked false stories can damage ____. ", "democracy", "gardens", "shoes", "Damage democracy."),
                    lg("Journalists also inform public ____. ", "debate", "sleep", "traffic", "Public debate."),
                    lg("The issue involves privacy and ____. ", "misinformation", "cooking", "parking", "Privacy invasion."),
                ],
                [
                    ic("The article presents [*competing viewpoints|only one joke|no arguments].", "Critics and supporters."),
                    ic("The tone is [*serious and balanced|comic|romantic].", "Serious debate."),
                    ic("The text is mainly about [*media regulation|space travel|gardening].", "Press freedom."),
                    ic("Supporters of new laws worry about unchecked [*false stories|art exhibitions|train tickets].", "False stories."),
                ],
            ),
        )),
        ("reading", "housing-crisis-cities", lesson(
            "The housing crisis in major cities",
            "reading",
            3,
            "<h2>The housing crisis in major cities</h2><p>Rising property prices have made it increasingly difficult for young professionals and families to live near city centres. Developers argue that limited land and high construction costs make affordable housing hard to provide. Tenant groups counter that too many new flats are sold to investors rather than local residents. Some cities have introduced rent controls and requirements for social housing in new projects. While these policies may stabilise prices in the short term, economists debate whether they reduce investment in the long run.</p>",
            three_sets(
                [
                    ic("High prices make it hard for families to live near [*city centres|airports only|mountains only].", "City centres."),
                    ic("Developers mention limited land and high [*construction costs|ticket prices|food quality].", "Construction costs."),
                    ic("Tenant groups say many flats go to [*investors|tourists only|students only].", "Sold to investors."),
                    ic("Some cities require [*social housing|swimming pools|car parks only] in new projects.", "Social housing."),
                ],
                [
                    lg("Young ____ struggle to afford central districts.", "professionals", "rivers", "storms", "Young professionals."),
                    lg("Rent controls may stabilise prices in the short ____. ", "term", "flight", "song", "Short term."),
                    lg("Economists question whether controls reduce long-term ____. ", "investment", "sunlight", "humour", "Reduce investment."),
                    lg("The text describes a housing ____. ", "crisis", "festival", "concert", "Housing crisis."),
                ],
                [
                    ic("The writer presents arguments from [*developers and tenant groups|only children|only athletes].", "Both sides."),
                    ic("The issue is mainly about [*affordable housing|museum funding|film reviews].", "Housing in cities."),
                    ic("Policies may help prices short term but raise questions about [*long-term investment|sports funding|weather].", "Long-run investment."),
                    ic("The tone is [*analytical|humorous|poetic].", "Analytical article."),
                ],
            ),
        )),
        ("reading", "language-extinction", lesson(
            "Why languages disappear",
            "reading",
            4,
            "<h2>Why languages disappear</h2><p>Linguists estimate that nearly half of the world's languages could disappear within a century. Many small communities switch to dominant languages for education, work and digital communication. When fewer children learn a language at home, its vocabulary, stories and cultural knowledge may be lost forever. Preservation projects record oral histories, publish dictionaries and support bilingual schools. Although these efforts cannot save every language, they can maintain cultural diversity and respect for minority communities.</p>",
            three_sets(
                [
                    ic("Nearly half of the world's languages could vanish within [*a century|a week|a day].", "Within a century."),
                    ic("Communities may switch to dominant languages for education and [*work|sport only|cooking only].", "Education, work and digital communication."),
                    ic("Loss of language can mean loss of stories and [*cultural knowledge|building materials|car engines].", "Cultural knowledge."),
                    ic("Preservation projects include recording oral histories and publishing [*dictionaries|novels only|menus only].", "Publish dictionaries."),
                ],
                [
                    lg("When fewer children learn a language at home, it may ____. ", "disappear", "expand", "translate", "Languages disappear."),
                    lg("Digital communication is one factor pushing communities to switch ____. ", "languages", "jobs", "cities", "Switch languages."),
                    lg("Bilingual schools are one form of ____. ", "support", "punishment", "competition", "Support for preservation."),
                    lg("Minority communities deserve ____. ", "respect", "isolation", "silence", "Respect for minorities."),
                ],
                [
                    ic("The writer views preservation efforts as [*valuable but limited|useless|harmful].", "Cannot save every language but still valuable."),
                    ic("The passage is mainly about [*language loss|airport design|computer games].", "Language extinction."),
                    ic("The tone is [*informative and concerned|angry|sarcastic].", "Informative."),
                    ic("Cultural [*diversity|pollution|inflation] is one benefit of preservation.", "Cultural diversity."),
                ],
            ),
        )),
        ("reading", "space-tourism-ethics", lesson(
            "The ethics of space tourism",
            "reading",
            5,
            "<h2>The ethics of space tourism</h2><p>Commercial space flights for wealthy tourists have moved from science fiction to reality. Supporters claim the industry will inspire innovation and fund research that benefits everyone. Critics respond that the enormous cost of a single ticket could finance thousands of clean water projects on Earth. They also question the environmental impact of rocket launches. As space tourism expands, society will need clear rules about safety, access and the responsible use of resources both on Earth and beyond.</p>",
            three_sets(
                [
                    ic("Space tourism is now a [*commercial reality|impossible dream|school subject only].", "Moved from fiction to reality."),
                    ic("Supporters say the industry may fund research that benefits [*everyone|only pilots|only artists].", "Benefits everyone."),
                    ic("Critics compare ticket prices with funding for clean [*water projects|football stadiums|bookshops].", "Clean water projects."),
                    ic("Society may need rules about safety, access and responsible use of [*resources|jokes|music].", "Responsible use of resources."),
                ],
                [
                    lg("Critics also question the environmental impact of rocket ____. ", "launches", "books", "meals", "Rocket launches."),
                    lg("Early tourists are mostly very ____. ", "wealthy", "young", "silent", "Wealthy tourists."),
                    lg("Supporters believe the industry can inspire ____. ", "innovation", "silence", "hunger", "Inspire innovation."),
                    lg("The debate is partly ____. ", "ethical", "musical", "culinary", "Ethics of space tourism."),
                ],
                [
                    ic("The article presents [*arguments on both sides|no viewpoints|only jokes].", "Supporters and critics."),
                    ic("The writer suggests future regulation will be [*necessary|impossible|irrelevant].", "Society will need clear rules."),
                    ic("The tone is [*thoughtful|comic|nostalgic only].", "Thoughtful ethics piece."),
                    ic("The issue connects technology with questions of [*justice and environment|fashion and sport|food and travel only].", "Justice and environment."),
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
            "<h2>Use of English - B2 Test 1</h2><p>Mixed grammar and vocabulary review.</p>",
            three_sets(
                [
                    ic("Never before [*have I|I have|did I] seen such an enthusiastic audience.", "Never before have I - inversion."),
                    ic("You [*should have backed|should back|must back] up the files before the update.", "Regret about past action."),
                    ic("It was the CEO who [*made|did|had] the final decision.", "It was ... who."),
                    ic("The report is believed [*to contain|containing|contain] several inaccuracies.", "Passive reporting."),
                ],
                [
                    lg("The government introduced new legislation on data ____. ", "protection", "protect", "protective", "Protection as noun."),
                    lg("Rising inflation has affected household ____. ", "budgets", "budgeting", "budgeted", "Household budgets."),
                    lg("The witness was asked ____ in court.", "to testify", "testify", "testifying", "Asked to testify."),
                    lg("The museum's latest ____ opens on Friday.", "exhibition", "exhibit", "exhibited", "Exhibition."),
                ],
                [
                    ic("She had her car [*serviced|service|servicing] at the garage.", "Causative have + past participle."),
                    ic("I enjoy hiking, and so [*do|am|have] my friends.", "So do my friends."),
                    ic("It is essential that he [*be|is|was] present at the meeting.", "Subjunctive be."),
                    ic("[*What|That|Which] worries me most is the lack of transparency.", "What-clause for emphasis."),
                ],
            ),
        )),
        ("use-of-english", "test-2", lesson(
            "Use of English - Test 2",
            "use-of-english",
            2,
            "<h2>Use of English - B2 Test 2</h2><p>Second mixed review at B2 level.</p>",
            three_sets(
                [
                    ic("Not only [*did|does|do] the team win, but they also broke the record.", "Not only did + subject."),
                    ic("He [*needn't have printed|mustn't print|should print] the whole document; it was online.", "Unnecessary past action."),
                    ic("She denied [*leaking|to leak|leak] the confidential email.", "Deny + gerund."),
                    ic("All I wanted [*was|were|is] a straight answer.", "All I wanted was ..."),
                ],
                [
                    lg("The jury reached a unanimous ____. ", "verdict", "verdicts", "sentence", "Verdict in court."),
                    lg("The company plans to ____ into Asian markets.", "expand", "expansion", "expanded", "Expand into markets."),
                    lg("There is growing public ____ about climate policy.", "debate", "debating", "debated", "Public debate."),
                    lg("The patient made a full ____ after surgery.", "recovery", "recover", "recovered", "Full recovery."),
                ],
                [
                    ic("Hardly [*had|have|did] we sat down when the fire alarm rang.", "Hardly had + subject."),
                    ic("They accused him [*of fraud|for fraud|to fraud].", "Accuse of."),
                    ic("The development of renewable energy is a key [*priority|prior|prioritise].", "Priority as noun."),
                    ic("Nor [*did|do|was] the minister answer the question directly.", "Nor did."),
                ],
            ),
        )),
        ("use-of-english", "test-3", lesson(
            "Use of English - Test 3",
            "use-of-english",
            3,
            "<h2>Use of English - B2 Test 3</h2><p>Final mixed review.</p>",
            three_sets(
                [
                    ic("She got her passport [*renewed|renew|renewing] in one day.", "Get + object + past participle."),
                    ic("The politician was reported [*to have resigned|resigning|resign] last week.", "Reported to have resigned."),
                    ic("It is vital that the data [*remain|remains|remained] confidential.", "Subjunctive remain."),
                    ic("I haven't read the report, and neither [*has|have|do] my assistant.", "Neither has."),
                ],
                [
                    lg("The artist's latest work is considered a ____. ", "masterpiece", "master", "mastering", "Masterpiece."),
                    lg("Governments must reduce carbon ____. ", "emissions", "emit", "emitted", "Carbon emissions."),
                    lg("The lecture focused on urban ____. ", "planning", "plan", "planned", "Urban planning."),
                    lg("Good leaders know how to ____ teams under pressure.", "motivate", "motivation", "motivated", "Motivate teams."),
                ],
                [
                    ic("Only by working together [*can|we can|could] we solve the problem.", "Only by ... can we."),
                    ic("He [*must have misunderstood|can't have misunderstood|should misunderstand] the instructions.", "Strong past deduction."),
                    ic("I'd prefer the blue jacket rather than the black [*one|ones|it].", "One substitutes jacket."),
                    ic("The doctor recommended that she [*rest|rests|rested] for several days.", "Recommend that + base form."),
                ],
            ),
        )),
    ]


def build_writing():
    return [
        ("writing", "discursive-essay", lesson(
            "Writing a discursive essay",
            "writing",
            1,
            "<h2>Writing a discursive essay</h2><p>A discursive essay examines an issue from several angles before reaching a measured conclusion.</p><ul><li>Introduction: present the issue clearly.</li><li>Body: explore arguments fairly.</li><li>Conclusion: summarise and state your view.</li></ul>",
            three_sets(
                [
                    ic("[*This essay will examine whether social media does more harm than good.|Social media harm good essay examine.|Essay social media harm good.]", "Clear academic opening."),
                    ic("[*One argument in favour is that social media connects isolated communities.|One argument favour social media connects.|Argument social media connects isolated.]", "Balanced argument sentence."),
                    ic("[*On the other hand, excessive use may reduce face-to-face interaction.|Other hand excessive use reduce interaction.|On other hand use excessive.]", "Contrast linker."),
                    ic("[*Overall, the benefits depend on how platforms are used.|Overall benefits depend used platforms.|Benefits overall depend how.]", "Measured conclusion."),
                ],
                [
                    lg("A discursive essay should avoid overly ____ language.", "emotional", "formal", "precise", "Stay measured."),
                    lg("Use linkers such as however, therefore and ____. ", "consequently", "yesterday", "quickly", "Consequently shows result."),
                    lg("Each paragraph should develop one clear ____. ", "point", "ticket", "recipe", "One point per paragraph."),
                    lg("The conclusion should summarise the main ____. ", "arguments", "ingredients", "flights", "Summarise arguments."),
                ],
                [
                    ic("[*It could be argued that remote work increases productivity.|Could argued remote work productivity increases.|Remote work argued productivity.]", "Impersonal argument."),
                    ic("[*Nevertheless, not every job can be done from home.|Nevertheless every job home done.|Not every nevertheless job.]", "Nevertheless for contrast."),
                    ic("[*In my view, a hybrid model offers the best balance.|My view hybrid model best balance.|Hybrid model my view.]", "Personal conclusion."),
                    ic("[*For instance, employees save commuting time.|For instance employees save commuting.|Instance for employees commuting.]", "Example linker."),
                ],
            ),
        )),
        ("writing", "formal-letter-complaint", lesson(
            "Writing a formal letter of complaint",
            "writing",
            2,
            "<h2>Writing a formal letter of complaint</h2><p>A formal complaint letter should be polite, precise and solution-focused.</p><ul><li>State the reason for writing.</li><li>Give dates and facts.</li><li>Explain the impact.</li><li>Request a specific remedy.</li></ul>",
            three_sets(
                [
                    ic("[*I am writing to complain about the poor service I received on 12 March.|I write complain poor service 12 March.|Complaint poor service March 12.]", "Formal opening."),
                    ic("[*Despite several reminders, the issue has not been resolved.|Despite reminders issue not resolved.|Issue despite reminders.]", "Polite but firm."),
                    ic("[*As a result, I have been unable to use the product I paid for.|As result unable use product paid.|Result unable product.]", "Explain impact."),
                    ic("[*I would be grateful if you could offer a full refund.|Grateful full refund offer could.|Refund full grateful.]", "Specific request."),
                ],
                [
                    lg("A formal letter should use polite but ____ language.", "firm", "casual", "humorous", "Firm and polite."),
                    lg("Include exact dates and useful ____. ", "details", "jokes", "opinions", "Factual details."),
                    lg("Avoid vague complaints; state the problem ____. ", "clearly", "secretly", "slowly", "Clearly."),
                    lg("End with a professional ____.", "closing", "recipe", "headline", "Professional closing."),
                ],
                [
                    ic("[*I look forward to hearing from you within fourteen days.|Look forward hearing fourteen days.|Forward look hearing days.]", "Polite deadline."),
                    ic("[*I have enclosed copies of the receipt and correspondence.|Enclosed copies receipt correspondence.|Receipt copies enclosed.]", "Supporting evidence."),
                    ic("[*Yours faithfully,|Yours friend,|Bye,]", "Formal ending when name unknown."),
                    ic("[*I trust this matter will be dealt with promptly.|Trust matter dealt promptly.|Matter trust promptly.]", "Polite expectation."),
                ],
            ),
        )),
        ("writing", "article-for-magazine", lesson(
            "Writing an article for a magazine",
            "writing",
            3,
            "<h2>Writing an article for a magazine</h2><p>A magazine article should engage the reader with a strong opening, clear sections and a memorable ending.</p><ul><li>Hook the reader in the first sentence.</li><li>Use examples and direct address where appropriate.</li><li>Keep paragraphs short.</li><li>End with a thought-provoking line.</li></ul>",
            three_sets(
                [
                    ic("[*Have you ever wondered why some cities feel easier to live in than others?|Ever wondered cities easier live others?|Cities wondered easier live.]", "Engaging opening question."),
                    ic("[*In this article, I will explore three features of liveable cities.|Article explore three features liveable cities.|Explore article three features.]", "Clear purpose."),
                    ic("[*First, reliable public transport saves time and reduces stress.|First reliable public transport saves stress.|Public transport first reliable.]", "Structured body."),
                    ic("[*Next time you visit a new city, notice how these details shape daily life.|Next time visit city details shape life.|Visit city next time details.]", "Memorable ending."),
                ],
                [
                    lg("A magazine article often uses a conversational but ____ tone.", "informed", "legal", "aggressive", "Informed conversational tone."),
                    lg("Short ____ make articles easier to read online.", "paragraphs", "sentences only", "footnotes", "Short paragraphs."),
                    lg("Examples help the reader relate to the ____. ", "topic", "ticket", "recipe", "Relate to topic."),
                    lg("A strong title should catch the reader's ____. ", "attention", "luggage", "salary", "Catch attention."),
                ],
                [
                    ic("[*Another key factor is access to parks and green spaces.|Another key factor parks green spaces.|Factor another parks green.]", "Clear supporting point."),
                    ic("[*You might be surprised by how much design affects wellbeing.|Might surprised design affects wellbeing.|Surprised design wellbeing.]", "Direct reader address."),
                    ic("[*However, liveability is not only about infrastructure.|However liveability only infrastructure.|Liveability however infrastructure.]", "Balanced contrast."),
                    ic("[*Ultimately, the best cities balance efficiency with humanity.|Ultimately best cities balance efficiency humanity.|Cities ultimately balance.]", "Strong final line."),
                ],
            ),
        )),
    ]


def validate_items(items: list[tuple[str, str, dict]]) -> list[str]:
    errors = []
    for section, slug, data in items:
        if data["level"] != LEVEL:
            errors.append(f"{slug}: wrong level {data['level']}")
        if len(data["exercise_sets"]) != 3:
            errors.append(f"{slug}: expected 3 exercise sets")
        for i, es in enumerate(data["exercise_sets"], 1):
            if not es.get("questions"):
                errors.append(f"{slug}: exercise {i} has no questions")
    return errors


def main() -> None:
    items: list[tuple[str, str, dict]] = []
    items.extend(build_grammar())
    items.extend(build_vocabulary())
    items.extend(build_listening())
    items.extend(build_reading())
    items.extend(build_use_of_english())
    items.extend(build_writing())

    errors = validate_items(items)
    if errors:
        print(f"Validation errors: {len(errors)}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)

    for section, slug, data in items:
        write_json(section, slug, data)
    print(f"Wrote {len(items)} B2 lessons with 0 validation errors.")


if __name__ == "__main__":
    main()
