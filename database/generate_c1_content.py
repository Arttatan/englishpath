from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
LEVEL = "c1"


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
    items.append(("grammar", "advanced-inversion", lesson(
        "Advanced inversion",
        "grammar",
        1,
        "<h2>Advanced inversion</h2><p>At C1 level, inversion appears after more complex triggers: <em>So + adjective ... that</em>, <em>Such ... that</em>, and conditional <em>Should/Were/Had</em> without <em>if</em>.</p><ul><li><em>So complex was the problem that experts were called in.</em></li><li><em>Such was the demand that the website crashed.</em></li><li><em>Should you require assistance, please contact us.</em></li></ul>",
        three_sets(
            [
                ic("[*So intense was|Was so intense] the debate that no agreement was reached.", "So + adjective + inversion."),
                ic("[*Such was|Was such] the public reaction that the minister resigned.", "Such was + noun phrase."),
                ic("[*Should|If should] you change your mind, let us know immediately.", "Should + subject + verb (formal conditional)."),
                ic("[*Were|If were] the proposal accepted, funding would be released.", "Were + subject (formal unreal condition)."),
                ic("[*Had|If had] we known about the delay, we would have rebooked.", "Had + subject + past participle."),
            ],
            [
                lg("So convincing ____ the evidence that the jury decided quickly.", "was", "is", "were", "So convincing was the evidence."),
                lg("____ you need further clarification, do not hesitate to ask.", "Should", "If", "When", "Formal Should you..."),
                lg("Such ____ the scale of the disaster that aid arrived from abroad.", "was", "were", "is", "Such was the scale."),
                lg("____ I in your position, I would seek independent advice.", "Were", "Was", "Am", "Were I in your position."),
            ],
            [
                ic("[*So rapidly did|Did so rapidly] prices rise that many tenants protested.", "So rapidly did + subject."),
                ic("[*Had they not intervened|If they had not intervened] earlier, losses would have been greater.", "Had they not intervened."),
                ic("[*Little did|Did little] anyone suspect the quiet colleague was the author.", "Little did anyone suspect."),
                ic("[*Such is|Is such] the influence of social media on public opinion today.", "Such is the influence."),
                ic("[*Were it not for|If it was not for] her research, the project would have failed.", "Were it not for."),
            ],
        ),
    )))
    items.append(("grammar", "hedging-and-tentative-language", lesson(
        "Hedging and tentative language",
        "grammar",
        2,
        "<h2>Hedging and tentative language</h2><p>Hedging softens claims in academic and professional English.</p><ul><li><em>It would appear that...</em></li><li><em>There is some evidence to suggest...</em></li><li><em>This may well indicate...</em></li><li><em>Tends to, appears to, seems to</em></li></ul>",
        three_sets(
            [
                ic("It [*would appear|appears definitely|must appear] that consumer habits are changing.", "Would appear hedges the claim."),
                ic("There is [*some|no|total] evidence to suggest a link between sleep and memory.", "Some evidence hedges."),
                ic("The results [*may well|must certainly|will never] indicate a broader trend.", "May well = cautious possibility."),
                ic("Urban populations [*tend to|always|never] grow faster than rural ones.", "Tend to softens generalisation."),
                ic("This [*could arguably|definitely must|clearly cannot] be seen as a turning point.", "Could arguably hedges."),
            ],
            [
                lg("The policy ____ to have reduced emissions slightly.", "appears", "proves", "guarantees", "Appears to hedge."),
                lg("It is ____ possible that the figures were incomplete.", "entirely", "somewhat", "absolutely", "Somewhat possible."),
                lg("The author ____ that further study is required.", "implies", "proclaims", "orders", "Implies is tentative."),
                lg("These findings should be interpreted with ____.", "caution", "certainty", "anger", "Interpret with caution."),
            ],
            [
                ic("It [*seems reasonable to assume|is proven absolutely|is impossible to assume] that costs will rise.", "Seems reasonable to assume."),
                ic("The data [*suggests rather than proves|proves without doubt|denies completely] a connection.", "Suggests rather than proves."),
                ic("One [*might argue|must argue|cannot argue] that the law needs reform.", "Might argue hedges."),
                ic("The trend is [*likely to|definitely going to|never going to] continue.", "Likely to hedge."),
                ic("It is [*not entirely clear|completely obvious|absolutely certain] why sales fell.", "Not entirely clear."),
            ],
        ),
    )))
    items.append(("grammar", "complex-noun-phrases", lesson(
        "Complex noun phrases",
        "grammar",
        3,
        "<h2>Complex noun phrases</h2><p>C1 writers pack information into noun phrases using pre-modifiers and post-modifiers.</p><ul><li><em>the recently published government report on climate policy</em></li><li><em>a highly controversial decision taken by the board</em></li><li><em>the extent to which regulations are enforced</em></li></ul>",
        three_sets(
            [
                ic("Choose the most natural phrase: [*the government's recently published climate report|the climate report government published recent|recent climate government report published].", "Natural pre- and post-modification."),
                ic("[*The extent to which|The extent which|The extent in which] regulations are enforced remains unclear.", "The extent to which."),
                ic("A [*widely accepted|accepted widely|accepting wide] theory explains the phenomenon.", "Adverb before participle as pre-modifier."),
                ic("[*A decision taken by the board|A taken decision by board|Decision by board taken] surprised investors.", "Post-modifier with past participle."),
                ic("The [*analysis of long-term economic trends|analysis long-term of trends economic|long-term trends analysis economic of] informed the policy.", "Natural noun phrase."),
            ],
            [
                lg("We need a more detailed ____ of the risks involved.", "assessment", "assess", "assessing", "Assessment as head noun."),
                lg("The committee discussed the ____ to which funding should increase.", "extent", "extend", "extensive", "Extent to which."),
                lg("This is a highly ____ proposal with serious implications.", "contentious", "content", "contently", "Contentious pre-modifies proposal."),
                lg("The report contains an ____ of recent migration patterns.", "overview", "oversee", "overseen", "Overview of patterns."),
            ],
            [
                ic("[*The factors influencing public trust|The factors public trust influencing|Influencing factors public trust] are complex.", "Factors + post-modifying -ing clause."),
                ic("[*A strategy designed to reduce waste|A designed strategy to waste reduce|Strategy reduce designed waste] was adopted.", "Designed to reduce as post-modifier."),
                ic("[*The degree of public support|The degree public support of|The public degree support of] surprised analysts.", "Degree of public support."),
                ic("[*An approach favoured by many experts|An favoured approach by experts many|Approach by favoured experts] gained attention.", "Favoured by experts."),
                ic("[*The implications of the ruling|The implications the ruling of|Of implications the ruling] are still debated.", "Implications of the ruling."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-participle-clauses", lesson(
        "Advanced participle clauses",
        "grammar",
        4,
        "<h2>Advanced participle clauses</h2><p>C1 users combine perfect, passive and negative participle clauses for concise formal style.</p><ul><li><em>Having been warned repeatedly, he ignored the advice.</em></li><li><em>Seen from above, the city looks surprisingly green.</em></li><li><em>Not having been consulted, staff opposed the plan.</em></li></ul>",
        three_sets(
            [
                ic("[*Having been warned repeatedly|Warned repeatedly having|To warn repeatedly], he still ignored the advice.", "Perfect passive participle clause."),
                ic("[*Seen from above|Seeing from above|To see from above], the city looks surprisingly green.", "Past participle with different subject."),
                ic("[*Not having been consulted|Not consulting|Not to consult], staff opposed the plan.", "Negative perfect passive participle."),
                ic("[*Assuming the data are accurate|Assumed the data accurate|To assume accurate data], the trend is worrying.", "Assuming clause."),
                ic("[*Compared with last year|Comparing with last year|To compare last year], profits have risen.", "Compared with."),
            ],
            [
                lg("____ by the evidence, the committee changed its recommendation.", "Convinced", "Convincing", "To convince", "Convinced by the evidence."),
                lg("____ completed the survey, researchers analysed the responses.", "Having", "Have", "Had", "Having completed."),
                lg("____ into account inflation, wages have barely grown.", "Taken", "Taking", "Take", "Taken into account."),
                lg("____ what she had said, he revised his conclusion.", "Remembering", "Remembered", "Remember", "Remembering what..."),
            ],
            [
                ic("[*Given the limited budget|Giving the limited budget|To give limited budget], the project was delayed.", "Given = considering."),
                ic("[*Having signed the contract|Signing the contract|Signed the contract], they began work immediately.", "Having signed before beginning."),
                ic("[*Viewed in context|Viewing in context|To view context], the remark seems less offensive.", "Viewed in context."),
                ic("[*Unless told otherwise|Unless telling otherwise|Unless to tell otherwise], assume the meeting is on.", "Unless told otherwise."),
                ic("[*Broadly speaking|Broad speaking|To speak broadly], the policy has succeeded.", "Broadly speaking as discourse marker."),
            ],
        ),
    )))
    items.append(("grammar", "academic-reporting-structures", lesson(
        "Academic reporting structures",
        "grammar",
        5,
        "<h2>Academic reporting structures</h2><p>Report research and views formally without overusing <em>said</em>.</p><ul><li><em>Smith (2020) argues that...</em></li><li><em>It has been widely acknowledged that...</em></li><li><em>The findings are consistent with the hypothesis that...</em></li></ul>",
        three_sets(
            [
                ic("Smith (2020) [*argues|tells|speaks] that urban design affects wellbeing.", "Argues in academic context."),
                ic("It has been widely [*acknowledged|shouted|guessed] that inequality is rising.", "Acknowledged = formally accepted."),
                ic("The findings are [*consistent with|angry with|bored with] earlier studies.", "Consistent with."),
                ic("The author [*contends|whispers|runs] that the law should be revised.", "Contends = argues strongly."),
                ic("These results [*lend support to|borrow money from|run away from] the original hypothesis.", "Lend support to."),
            ],
            [
                lg("Previous research ____ that sleep deprivation impairs judgement.", "suggests", "yells", "dances", "Research suggests."),
                lg("The data do not necessarily ____ a causal link.", "establish", "celebrate", "paint", "Establish a link."),
                lg("Critics have ____ the methodology used in the study.", "questioned", "sung", "cooked", "Questioned methodology."),
                lg("The paper ____ several limitations of the current model.", "identifies", "hides", "forgets", "Identifies limitations."),
            ],
            [
                ic("According [*to the latest review|with the latest review|on the latest review], the trend is accelerating.", "According to."),
                ic("The study [*draws attention to|draws pictures of|draws water from] gaps in existing policy.", "Draws attention to."),
                ic("It is [*widely held|narrowly held|never held] that education reduces poverty.", "Widely held view."),
                ic("The evidence [*points to|points at the sky|points away from] structural causes.", "Points to."),
                ic("The researchers [*attribute the decline to|attribute the decline with|attribute to decline] several factors.", "Attribute X to Y."),
            ],
        ),
    )))
    items.append(("grammar", "cohesion-and-reference", lesson(
        "Cohesion and reference",
        "grammar",
        6,
        "<h2>Cohesion and reference</h2><p>C1 texts use reference chains, substitution and conjunction precisely.</p><ul><li><em>this phenomenon, the former, the latter, such measures</em></li><li><em>do so, one, ones, the same</em></li><li><em>thereby, hence, accordingly</em></li></ul>",
        three_sets(
            [
                ic("Two policies were proposed; [*the former|the ladder|the weather] focused on tax, [*the latter|the former|the ceiling] on spending.", "Former/latter reference."),
                ic("The board approved the plan and [*did so|did it|did this] without delay.", "Did so substitutes approved the plan."),
                ic("If regulations fail, [*such measures|such weather|such music] may lose public support.", "Such measures refers back."),
                ic("The first model is cheaper; I prefer [*that one|that ones|those one].", "That one substitutes model."),
                ic("Costs rose; [*hence|however|for instance] profits fell.", "Hence = therefore."),
            ],
            [
                lg("The experiment failed twice. ____ , the team redesigned the method.", "Accordingly", "Nevertheless", "For example", "Accordingly follows logically."),
                lg("Three options were discussed, but only two of ____ were realistic.", "them", "it", "this", "Them refers to options."),
                lg("She supported the proposal, and he did ____.", "likewise", "never", "backward", "Likewise = similarly."),
                lg("The policy reduced emissions and ____ improved air quality.", "thereby", "although", "whereas", "Thereby shows result."),
            ],
            [
                ic("The report criticised delays; [*this criticism|this weather|this colour] angered officials.", "This criticism refers back."),
                ic("I need a copy of the contract - do you have [*one|ones|it]?", "One substitutes copy."),
                ic("Sales improved in Q1; [*by contrast|for instance|as usual] Q2 was weaker.", "By contrast."),
                ic("They reached the same conclusion and wrote [*the same|same the|same it] in the summary.", "The same."),
                ic("The law was vague; [*as a result|for example|on the other hand] courts interpreted it differently.", "As a result."),
            ],
        ),
    )))
    items.append(("grammar", "fronting-and-end-focus", lesson(
        "Fronting and end-focus",
        "grammar",
        7,
        "<h2>Fronting and end-focus</h2><p>Speakers front information for emphasis and place new or important information at the end (end-focus).</p><ul><li><em>What we need is more time.</em> (fronted)</li><li><em>It was in 2019 that the law changed.</em> (cleft for focus)</li><li><em>She bought a house in Lisbon.</em> (new place at end)</li></ul>",
        three_sets(
            [
                ic("[*What concerns me most|Concerns me most what] is the lack of transparency.", "What-clause fronted for focus."),
                ic("It [*was in 2019 that|in 2019 was that|was that in 2019] the law finally changed.", "Cleft for time focus."),
                ic("[*A solution we urgently need|We urgently need a solution] is better training.", "Fronted noun phrase."),
                ic("She met [*a renowned architect from Barcelona|from Barcelona a renowned architect met she] at the conference.", "End-focus: Barcelona as new info."),
                ic("[*Particularly worrying|Worrying particularly] is the speed of change.", "Fronted adjective phrase."),
            ],
            [
                lg("____ I cannot accept is deliberate misinformation.", "What", "That", "Which", "What I cannot accept."),
                lg("It was the director ____ approved the budget.", "who", "which", "where", "Person: who."),
                lg("____ remarkable was their ability to adapt.", "Particularly", "Rarely", "Seldom", "Particularly remarkable fronted."),
                lg("He gave the files to Maria, not to ____. ", "James", "file", "desk", "End-focus contrast."),
            ],
            [
                ic("[*The question we must ask|The question must we ask] is who benefits.", "Fronted question."),
                ic("It [*is transparency that|transparency is that|is that transparency] builds trust.", "Cleft emphasis."),
                ic("[*Especially significant|Significant especially] was the role of local media.", "Especially significant fronted."),
                ic("They announced [*a major investment in renewable energy|in renewable energy a major investment announced they].", "Natural end-focus."),
                ic("[*More pressing than ever|Pressing more than ever] is the need for reform.", "Comparative fronting."),
            ],
        ),
    )))
    items.append(("grammar", "advanced-modality-and-stance", lesson(
        "Advanced modality and stance",
        "grammar",
        8,
        "<h2>Advanced modality and stance</h2><p>C1 speakers express stance with nuanced modals and semi-modals: <em>be bound to, be likely to, be supposed to, would rather, had better</em>.</p>",
        three_sets(
            [
                ic("Given the evidence, the jury [*is bound to|is never going to|is forbidden to] reach a verdict soon.", "Be bound to = almost certain."),
                ic("You [*would rather|would better|would sooner not] discuss this in public, wouldn't you?", "Would rather + bare infinitive."),
                ic("We [*had better|would rather|must better] leave before the storm arrives.", "Had better for urgent advice."),
                ic("The package [*is supposed to|is bound to|is likely not to] arrive today, but tracking says otherwise.", "Supposed to = expected."),
                ic("She [*would sooner resign|would better resign|had rather resign] than compromise her principles.", "Would sooner = would rather."),
            ],
            [
                lg("The policy is likely ____ face legal challenges.", "to", "for", "that", "Likely to face."),
                lg("He is ____ to know the answer; he wrote the report.", "bound", "afraid", "slow", "Bound to know."),
                lg("You ____ not have interrupted the speaker.", "should", "would", "might", "Should not have interrupted."),
                lg("I ____ rather you didn't share that document.", "would", "had", "must", "Would rather + subject + past."),
            ],
            [
                ic("They [*are unlikely to|are likely to|are bound to] abandon the project entirely.", "Unlikely to hedge."),
                ic("You [*had better not|would rather not|are supposed not] forget the deadline.", "Had better not."),
                ic("He [*is meant to|is meaning to|is minded to] chair the meeting tomorrow.", "Is meant to = supposed to."),
                ic("The outcome [*could hardly have been|could easily have been|must always be] worse.", "Could hardly have been worse."),
                ic("I [*would just as soon|would rather just|had better just] stay at home tonight.", "Would just as soon = would rather."),
            ],
        ),
    )))
    return items


def build_vocabulary():
    items = []

    def make_vocab(title, slug, sort_order, explanation, lettered1, dropdown, bank, lettered2):
        items.append(("vocabulary", slug, lesson(title, "vocabulary", sort_order, explanation, vocab_sets(lettered1, dropdown, bank, lettered2))))

    make_vocab(
        "Philosophy and ethics",
        "philosophy-and-ethics",
        1,
        "<h2>Philosophy and ethics</h2><ul><li>morality, autonomy, utilitarianism, dilemma, conscience</li><li>virtue, obligation, consent, integrity, impartiality</li><li>verbs: justify, condemn, uphold, compromise</li></ul>",
        [
            lg("The documentary explores a classic moral ____ faced by doctors.", "dilemma", "receipt", "platform", "Moral dilemma."),
            lg("Respect for patient ____ is central to medical ethics.", "autonomy", "economy", "anatomy", "Patient autonomy."),
            lg("She acted according to her ____ and resigned.", "conscience", "contract", "campaign", "Conscience."),
            lg("Judges are expected to remain ____.", "impartial", "impatient", "informal", "Impartial judges."),
        ],
        [
            dd("Critics ____ the decision as deeply unfair.", "condemn"),
            dd("The committee tried to ____ a difficult compromise.", "reach"),
            dd("He refused to ____ his principles for profit.", "compromise"),
            dd("The court must ____ the law even when it is unpopular.", "uphold"),
            dd("Can violence ever be ____ in self-defence?", "justified"),
        ],
        ["condemn", "reach", "compromise", "uphold", "justified", "consent", "integrity", "obligation", "virtue", "morality"],
        [
            lg("Informed ____ is required before the procedure.", "consent", "content", "comment", "Informed consent."),
            lg("Professional ____ matters in public office.", "integrity", "industry", "inflation", "Integrity."),
            lg("They debated whether pleasure should define ____. ", "morality", "mobility", "majority", "Morality."),
            lg("Courage is often described as a moral ____. ", "virtue", "verdict", "vaccine", "Virtue."),
        ],
    )
    make_vocab(
        "Diplomacy and international relations",
        "diplomacy-and-international-relations",
        2,
        "<h2>Diplomacy and international relations</h2><ul><li>treaty, sanction, envoy, sovereignty, alliance</li><li>negotiation, ceasefire, summit, ratification, embargo</li><li>verbs: mediate, deploy, recognise, escalate</li></ul>",
        [
            lg("The two states signed a peace ____ after months of talks.", "treaty", "ticket", "recipe", "Peace treaty."),
            lg("The ambassador acted as an ____ during the crisis.", "envoy", "enemy", "editor", "Envoy = diplomatic representative."),
            lg("Economic ____ were imposed to pressure the regime.", "sanctions", "salaries", "slogans", "Economic sanctions."),
            lg("National ____ was a key issue in the debate.", "sovereignty", "solidarity", "software", "Sovereignty."),
        ],
        [
            dd("Leaders met at an emergency ____ in Geneva.", "summit"),
            dd("The UN attempted to ____ between the warring parties.", "mediate"),
            dd("Parliament delayed ____ of the agreement.", "ratification"),
            dd("Troops were ____ to the border region.", "deployed"),
            dd("An ____ on oil exports increased tensions.", "embargo"),
        ],
        ["summit", "mediate", "ratification", "deployed", "embargo", "ceasefire", "alliance", "negotiation", "escalate", "recognise"],
        [
            lg("Both sides agreed to a temporary ____. ", "ceasefire", "campaign", "concert", "Ceasefire."),
            lg("The military ____ strengthened regional security.", "alliance", "audience", "article", "Military alliance."),
            lg("Analysts fear the conflict could ____ further.", "escalate", "educate", "estimate", "Escalate."),
            lg("Many countries refused to ____ the new government.", "recognise", "recycle", "recover", "Recognise a government."),
        ],
    )
    make_vocab(
        "Linguistics and language",
        "linguistics-and-language",
        3,
        "<h2>Linguistics and language</h2><ul><li>syntax, semantics, dialect, fluency, corpus</li><li>pronunciation, register, bilingualism, acquisition, utterance</li><li>verbs: articulate, translate, interpret, coin</li></ul>",
        [
            lg("The course examines how ____ shapes sentence structure.", "syntax", "symptom", "system", "Syntax."),
            lg("She speaks with remarkable ____ in three languages.", "fluency", "frequency", "fluids", "Fluency."),
            lg("Researchers analysed a large ____ of spoken English.", "corpus", "campus", "census", "Language corpus."),
            lg("Formal ____ differs from casual conversation.", "register", "receipt", "refund", "Language register."),
        ],
        [
            dd("Children acquire grammar through gradual language ____. ", "acquisition"),
            dd("The interpreter had to ____ a highly technical speech.", "interpret"),
            dd("He struggled to ____ his ideas under pressure.", "articulate"),
            dd("Shakespeare helped ____ hundreds of new words.", "coin"),
            dd("The ____ of the phrase changed over centuries.", "meaning"),
        ],
        ["acquisition", "interpret", "articulate", "coin", "meaning", "semantics", "dialect", "bilingualism", "utterance", "pronunciation"],
        [
            lg("____ studies how words combine to create sense.", "Semantics", "Sematic", "Semantician", "Semantics."),
            lg("Regional ____ can vary sharply within one country.", "dialects", "dialecting", "dialected", "Dialects."),
            lg("Early ____ may give children cognitive advantages.", "bilingualism", "bilinguality", "bilinguist", "Bilingualism."),
            lg("Clear ____ helps learners be understood.", "pronunciation", "pronounce", "pronounced", "Pronunciation."),
        ],
    )
    make_vocab(
        "Neuroscience and cognition",
        "neuroscience-and-cognition",
        4,
        "<h2>Neuroscience and cognition</h2><ul><li>neuron, cortex, cognition, perception, stimulus</li><li>memory, neural, synapse, consciousness, impairment</li><li>verbs: process, retain, stimulate, perceive</li></ul>",
        [
            lg("Information is ____ in different regions of the brain.", "processed", "printed", "promoted", "Processed in the brain."),
            lg("Damage to the frontal ____ can affect decision-making.", "cortex", "context", "contract", "Frontal cortex."),
            lg("Repeated ____ strengthens certain neural pathways.", "stimulation", "station", "stipulation", "Neural stimulation."),
            lg("Mild cognitive ____ may affect short-term recall.", "impairment", "improvement", "implement", "Cognitive impairment."),
        ],
        [
            dd("A ____ transmits signals between nerve cells.", "synapse"),
            dd("The experiment measured reaction to a visual ____. ", "stimulus"),
            dd("Sleep helps the brain ____ important memories.", "retain"),
            dd("Patients reported altered ____ after the injury.", "perception"),
            dd("Scientists study how ____ emerges from brain activity.", "consciousness"),
        ],
        ["synapse", "stimulus", "retain", "perception", "consciousness", "neuron", "neural", "cognition", "memory", "process"],
        [
            lg("Each ____ connects to thousands of others.", "neuron", "notion", "nation", "Neuron."),
            lg("____ decline is common in advanced age.", "Memory", "Memorial", "Memorise", "Memory decline."),
            lg("The study focuses on higher-order ____. ", "cognition", "cognitive", "cognise", "Cognition."),
            lg("Brain scans reveal ____ activity during tasks.", "neural", "neutral", "natural", "Neural activity."),
        ],
    )
    make_vocab(
        "Corporate governance",
        "corporate-governance",
        5,
        "<h2>Corporate governance</h2><ul><li>shareholder, accountability, compliance, audit, fiduciary</li><li>board, transparency, misconduct, stakeholder, oversight</li><li>verbs: delegate, disclose, regulate, scrutinise</li></ul>",
        [
            lg("The scandal raised questions about executive ____. ", "accountability", "ability", "availability", "Accountability."),
            lg("____ require accurate financial reporting.", "Shareholders", "Shareholds", "Sharing", "Shareholders."),
            lg("The firm failed ____ with safety regulations.", "compliance", "complaint", "compliment", "Compliance."),
            lg("Independent ____ reviewed the company's accounts.", "auditors", "authors", "actors", "Auditors."),
        ],
        [
            dd("Directors have a ____ duty to act in the firm's interest.", "fiduciary"),
            dd("The report calls for greater ____ in public spending.", "transparency"),
            dd("Regulators will ____ the merger closely.", "scrutinise"),
            dd("Managers must ____ conflicts of interest.", "disclose"),
            dd("The board decided to ____ more authority to regional heads.", "delegate"),
        ],
        ["fiduciary", "transparency", "scrutinise", "disclose", "delegate", "oversight", "stakeholder", "misconduct", "board", "regulate"],
        [
            lg("Strong ____ helps prevent fraud.", "oversight", "overview", "overtime", "Oversight."),
            lg("Employees are important ____ in any reform.", "stakeholders", "stockholders only", "strangers", "Stakeholders."),
            lg("Alleged financial ____ is under investigation.", "misconduct", "misconnect", "misplace", "Misconduct."),
            lg("Governments ____ industries to protect consumers.", "regulate", "recycle", "resign", "Regulate industries."),
        ],
    )
    make_vocab(
        "Architecture and urban design",
        "architecture-and-urban-design",
        6,
        "<h2>Architecture and urban design</h2><ul><li>facade, blueprint, sustainability, zoning, renovation</li><li>pedestrianisation, skyline, heritage, infrastructure, density</li><li>verbs: refurbish, integrate, preserve, construct</li></ul>",
        [
            lg("The building's glass ____ reflects the historic square.", "facade", "factor", "failure", "Facade."),
            lg("City planners debated new ____ rules for high-rise blocks.", "zoning", "zooming", "zoning only", "Zoning regulations."),
            lg("The project prioritised environmental ____. ", "sustainability", "suitability", "supervision", "Sustainability."),
            lg("Population ____ affects transport and housing demand.", "density", "destiny", "dignity", "Urban density."),
        ],
        [
            dd("Architects worked from an original ____. ", "blueprint"),
            dd("The council approved ____ of the riverfront.", "pedestrianisation"),
            dd("Engineers will ____ the nineteenth-century theatre.", "refurbish"),
            dd("The design seeks to ____ green space into the district.", "integrate"),
            dd("Laws protect buildings of cultural ____. ", "heritage"),
        ],
        ["blueprint", "pedestrianisation", "refurbish", "integrate", "heritage", "skyline", "infrastructure", "renovation", "construct", "preserve"],
        [
            lg("The city's ____ changed dramatically after the tower opened.", "skyline", "skylight", "skill line", "Skyline."),
            lg("Reliable ____ supports economic growth.", "infrastructure", "instruction", "insurance", "Infrastructure."),
            lg("They plan to ____ the landmark rather than demolish it.", "preserve", "prevent", "predict", "Preserve a landmark."),
            lg("The firm will ____ a new cultural centre by 2028.", "construct", "conduct", "contact", "Construct a building."),
        ],
    )
    make_vocab(
        "Literary criticism",
        "literary-criticism",
        7,
        "<h2>Literary criticism</h2><ul><li>narrative, motif, allegory, protagonist, subtext</li><li>irony, symbolism, canon, interpretation, ambiguity</li><li>verbs: evoke, critique, juxtapose, allude</li></ul>",
        [
            lg("The novel's central ____ questions the nature of power.", "motif", "motion", "motor", "Literary motif."),
            lg("Readers debated the political ____ beneath the romance plot.", "subtext", "subtitle", "subway", "Subtext."),
            lg("The ____ undergoes a profound moral transformation.", "protagonist", "protein", "protester", "Protagonist."),
            lg("Critics praised the author's use of ____.", "symbolism", "sympathy", "symphony", "Symbolism."),
        ],
        [
            dd("The poem seems to ____ classical mythology.", "allude"),
            dd("The essay offers a sharp ____ of colonial narratives.", "critique"),
            dd("The director chose to ____ past and present scenes.", "juxtapose"),
            dd("The opening image ____ a sense of isolation.", "evokes"),
            dd("Some readers enjoy deliberate ____ in modern fiction.", "ambiguity"),
        ],
        ["allude", "critique", "juxtapose", "evokes", "ambiguity", "allegory", "irony", "canon", "narrative", "interpretation"],
        [
            lg("The story works as an ____ of political corruption.", "allegory", "allergy", "algebra", "Allegory."),
            lg("Dramatic ____ undercuts the hero's confident speech.", "irony", "ivory", "ideal", "Irony."),
            lg("The novel entered the literary ____ within a decade.", "canon", "cannon", "canal", "Literary canon."),
            lg("Every ____ depends partly on cultural context.", "interpretation", "interruption", "integration", "Interpretation."),
        ],
    )
    make_vocab(
        "Biotechnology and genetics",
        "biotechnology-and-genetics",
        8,
        "<h2>Biotechnology and genetics</h2><ul><li>genome, mutation, hereditary, embryo, sequencing</li><li>CRISPR, ethics, therapy, clone, modification</li><li>verbs: engineer, inherit, diagnose, manipulate</li></ul>",
        [
            lg("Scientists mapped the entire human ____. ", "genome", "genre", "gym", "Human genome."),
            lg("The rare ____ increases cancer risk.", "mutation", "mansion", "motion", "Genetic mutation."),
            lg("Some conditions are ____ and pass through families.", "hereditary", "heroic", "harmful only", "Hereditary conditions."),
            lg("Gene ____ raises profound ethical questions.", "editing", "eating", "ending", "Gene editing."),
        ],
        [
            dd("The lab uses ____ to alter specific DNA sequences.", "CRISPR"),
            dd("Doctors hope gene ____ can treat inherited diseases.", "therapy"),
            dd("Researchers must not ____ data to support a theory.", "manipulate"),
            dd("Tests can ____ disorders before symptoms appear.", "diagnose"),
            dd("Children ____ traits from both parents.", "inherit"),
        ],
        ["CRISPR", "therapy", "manipulate", "diagnose", "inherit", "embryo", "sequencing", "modification", "clone", "engineer"],
        [
            lg("DNA ____ has become faster and cheaper.", "sequencing", "seasoning", "seating", "DNA sequencing."),
            lg("Research on human ____ is tightly regulated.", "embryos", "embargo", "emblems", "Human embryos."),
            lg("Critics fear unsafe genetic ____. ", "modification", "motivation", "migration", "Genetic modification."),
            lg("Scientists can ____ cells to resist certain viruses.", "engineer", "enjoy", "enroll", "Engineer cells."),
        ],
    )
    return items


def build_listening():
    return [
        ("listening", "academic-conference-panel", lesson(
            "Academic conference panel",
            "listening",
            1,
            "<h2>Academic conference panel</h2><p>Listen to part of a panel on education policy.</p><h3>Transcript</h3><p><strong>Moderator:</strong> Our final question: can standardised testing improve equity?<br><strong>Speaker A:</strong> Only if results are used to support schools, not punish them.<br><strong>Speaker B:</strong> I would argue that excessive testing narrows the curriculum and increases anxiety.<br><strong>Speaker A:</strong> Agreed, but abandoning measurement altogether is not realistic either.<br><strong>Moderator:</strong> So the challenge is designing assessment that informs teaching without distorting it.</p>",
            three_sets(
                [
                    ic("Speaker A says results should [*support schools|punish schools|replace teachers].", "Support schools, not punish them."),
                    ic("Speaker B believes too much testing [*narrows the curriculum|improves creativity|reduces anxiety].", "Narrows the curriculum."),
                    ic("Speaker A thinks abandoning measurement is [*not realistic|essential|already happening].", "Not realistic."),
                    ic("The moderator concludes the challenge is assessment that [*informs teaching|eliminates homework|reduces funding].", "Informs teaching without distorting it."),
                ],
                [
                    lg("The panel discusses standardised ____.", "testing", "cooking", "driving", "Standardised testing."),
                    lg("Speaker B mentions increased student ____. ", "anxiety", "salary", "traffic", "Increases anxiety."),
                    lg("The tone is largely ____ despite disagreement.", "constructive", "hostile", "comic", "They agree on key points."),
                    lg("The issue is how to design better ____. ", "assessment", "furniture", "weather", "Assessment design."),
                ],
                [
                    ic("The discussion is [*balanced|one-sided|unrelated to education].", "Both speakers nuance their views."),
                    ic("Speaker B uses hedging with [*I would argue|I definitely prove|Everyone knows].", "I would argue."),
                    ic("The panel would interest [*policymakers and educators|only athletes|only tourists].", "Education policy audience."),
                    ic("The final message rejects both extremes: punishment and [*no measurement|more punishment|less teaching].", "Abandoning measurement."),
                ],
            ),
            "https://www.youtube.com/watch?v=8O6272q0Awo",
        )),
        ("listening", "legal-commentary-podcast", lesson(
            "Legal commentary podcast",
            "listening",
            2,
            "<h2>Legal commentary podcast</h2><p>Listen to a lawyer discussing a court ruling.</p><h3>Transcript</h3><p><strong>Host:</strong> Did the ruling surprise you?<br><strong>Guest:</strong> Not entirely. The judges emphasised that freedom of expression is not absolute and must be balanced against privacy rights. They did not create new law; they applied existing principles to digital platforms. However, the dissenting opinion warned that the decision could chill legitimate journalism.</p>",
            three_sets(
                [
                    ic("The guest was [*not entirely|completely|never] surprised.", "Not entirely surprised."),
                    ic("Freedom of expression must be balanced with [*privacy rights|traffic laws|tax rules].", "Privacy rights."),
                    ic("The court [*applied existing principles|created entirely new law|ignored all precedent].", "Applied existing principles."),
                    ic("The dissenting opinion feared the ruling could [*chill journalism|increase profits|end the internet].", "Chill legitimate journalism."),
                ],
                [
                    lg("The case concerns digital ____. ", "platforms", "plants", "planes", "Digital platforms."),
                    lg("The judges said free speech is not ____. ", "absolute", "available", "ancient", "Not absolute."),
                    lg("A dissenting ____ was mentioned.", "opinion", "option", "opera", "Dissenting opinion."),
                    lg("The guest speaks as a ____. ", "lawyer", "chef", "driver", "Legal expert."),
                ],
                [
                    ic("The tone is [*analytical|humorous|angry throughout].", "Legal commentary."),
                    ic("The ruling relates to [*balancing rights|sports funding|cooking recipes].", "Expression vs privacy."),
                    ic("The guest suggests the decision was [*moderate in scope|revolutionary|irrelevant].", "Did not create new law."),
                    ic("Journalists might self-censor if they fear [*legal consequences|bad weather|high prices].", "Chill journalism."),
                ],
            ),
            "https://www.youtube.com/watch?v=4jpdlG8EJhE",
        )),
        ("listening", "startup-founder-interview", lesson(
            "Startup founder interview",
            "listening",
            3,
            "<h2>Startup founder interview</h2><p>Listen to an interview with a tech founder.</p><h3>Transcript</h3><p><strong>Interviewer:</strong> What almost killed the company in year two?<br><strong>Founder:</strong> Cash flow. We scaled too fast and underestimated how long enterprise clients take to sign contracts. We had to cut staff and renegotiate with investors. It was painful, but it forced us to focus on sustainable growth rather than hype.</p>",
            three_sets(
                [
                    ic("The main problem in year two was [*cash flow|product design|office location].", "Cash flow."),
                    ic("They scaled [*too fast|too slowly|not at all].", "Scaled too fast."),
                    ic("Enterprise clients take a long time to [*sign contracts|visit offices|choose logos].", "Sign contracts."),
                    ic("The crisis forced a focus on [*sustainable growth|publicity stunts|luxury offices].", "Sustainable growth rather than hype."),
                ],
                [
                    lg("They had to cut ____. ", "staff", "coffee", "windows", "Cut staff."),
                    lg("They renegotiated with ____. ", "investors", "tourists", "actors", "Renegotiate with investors."),
                    lg("The experience was ____. ", "painful", "boring", "silent", "Painful but instructive."),
                    lg("They previously chased too much ____. ", "hype", "sleep", "silence", "Rather than hype."),
                ],
                [
                    ic("The founder's tone is [*reflective|aggressive|uninterested].", "Reflective interview."),
                    ic("The lesson concerns [*business discipline|recipe design|sports training].", "Startup survival."),
                    ic("The company survived by [*changing strategy|ignoring investors|stopping sales].", "Focus and renegotiation."),
                    ic("Enterprise sales are portrayed as [*slow|instant|impossible].", "Take long to sign."),
                ],
            ),
            "https://www.youtube.com/watch?v=7y_hbz6lM9E",
        )),
        ("listening", "museum-curator-talk", lesson(
            "Museum curator talk",
            "listening",
            4,
            "<h2>Museum curator talk</h2><p>Listen to a curator introducing an exhibition.</p><h3>Transcript</h3><p><strong>Curator:</strong> This exhibition does not present a single national story. Instead, it traces how trade, migration and conflict shaped the region over five centuries. Many objects on display have only recently been reinterpreted using new archival research. We invite visitors to question familiar narratives and notice what earlier exhibitions chose to omit.</p>",
            three_sets(
                [
                    ic("The exhibition avoids a single [*national story|shopping guide|sports timeline].", "Does not present a single national story."),
                    ic("It traces trade, migration and [*conflict|weather|fashion].", "Trade, migration and conflict."),
                    ic("Some objects were reinterpreted using new [*archival research|social media|recipes].", "Archival research."),
                    ic("Visitors are invited to notice what earlier exhibitions [*omitted|invented|sold].", "Chose to omit."),
                ],
                [
                    lg("The display covers five ____. ", "centuries", "minutes", "meters", "Five centuries."),
                    lg("The curator wants visitors to question familiar ____. ", "narratives", "noodles", "numbers", "Familiar narratives."),
                    lg("The approach is deliberately ____. ", "critical", "careless", "comic", "Critical historiography."),
                    lg("Many items have been recently ____. ", "reinterpreted", "recycled", "removed", "Reinterpreted."),
                ],
                [
                    ic("The talk is [*academic and accessible|purely technical|unrelated to history].", "Museum curator style."),
                    ic("The exhibition emphasises [*complexity|simplicity only|fiction only].", "Multiple forces shaped the region."),
                    ic("The curator encourages active [*questioning|shopping|sleeping].", "Question familiar narratives."),
                    ic("The tone is [*thought-provoking|aggressive|indifferent].", "Thought-provoking."),
                ],
            ),
            "https://www.youtube.com/watch?v=HwMkN_2BTqs",
        )),
        ("listening", "health-policy-briefing", lesson(
            "Health policy briefing",
            "listening",
            5,
            "<h2>Health policy briefing</h2><p>Listen to a briefing on public health strategy.</p><h3>Transcript</h3><p><strong>Official:</strong> Prevention must remain our priority. That means expanding screening programmes, reducing smoking rates and improving access to mental health services. Hospital capacity matters, but treating illness alone will not solve rising long-term costs. We are allocating additional funding to community care so that fewer patients require emergency admission.</p>",
            three_sets(
                [
                    ic("The priority is [*prevention|advertising|tourism].", "Prevention must remain priority."),
                    ic("Plans include expanding [*screening programmes|football stadiums|film festivals].", "Screening programmes."),
                    ic("Treating illness alone will not solve rising [*long-term costs|ticket prices|hotel bills].", "Long-term costs."),
                    ic("Extra funding targets [*community care|luxury hotels|car parks].", "Community care."),
                ],
                [
                    lg("They aim to reduce smoking ____. ", "rates", "music", "colours", "Smoking rates."),
                    lg("Mental health services need better ____. ", "access", "accession", "accent", "Access to services."),
                    lg("Fewer patients should need emergency ____. ", "admission", "adoption", "addition", "Emergency admission."),
                    lg("Hospital ____ still matters.", "capacity", "captain", "caption", "Hospital capacity."),
                ],
                [
                    ic("The strategy is [*long-term and holistic|short-term only|unrelated to health].", "Prevention + community care."),
                    ic("The speaker's tone is [*policy-focused|comic|nostalgic].", "Official briefing."),
                    ic("Emergency admissions should become [*less common|mandatory|more expensive only].", "Fewer emergency admissions."),
                    ic("The briefing addresses [*physical and mental health|only sports|only transport].", "Mental health included."),
                ],
            ),
            "https://www.youtube.com/watch?v=fSrLeyfk9SM",
        )),
    ]


def build_reading():
    return [
        ("reading", "algorithmic-bias", lesson(
            "Algorithmic bias in decision-making",
            "reading",
            1,
            "<h2>Algorithmic bias in decision-making</h2><p>Automated systems now influence hiring, lending and policing, yet algorithms can reproduce historical inequalities if they are trained on biased data. Proponents argue that well-designed models may reduce subjective human prejudice. Critics respond that opacity makes discrimination harder to detect and challenge. Regulators increasingly demand audits, documentation and the right to explanation, though technical complexity may limit how meaningful such explanations are for ordinary citizens.</p>",
            three_sets(
                [
                    ic("Algorithms can reproduce inequalities when trained on [*biased data|perfect data|random art].", "Trained on biased data."),
                    ic("Proponents believe good models might reduce [*human prejudice|internet speed|museum visits].", "Reduce subjective human prejudice."),
                    ic("Critics worry that opacity makes discrimination harder to [*detect|celebrate|ignore voluntarily].", "Harder to detect and challenge."),
                    ic("Regulators want audits and the right to [*explanation|entertainment|exercise].", "Right to explanation."),
                ],
                [
                    lg("Automated systems affect hiring, lending and ____. ", "policing", "gardening", "cooking", "Policing mentioned."),
                    lg("Technical complexity may limit meaningful ____. ", "explanations", "vacations", "recipes", "Meaningful explanations."),
                    lg("Critics emphasise model ____. ", "opacity", "opacity only wrong", "openness only", "Opacity."),
                    lg("Documentation is increasingly ____. ", "demanded", "forbidden", "ignored", "Regulators demand it."),
                ],
                [
                    ic("The article is [*balanced|entirely optimistic|completely dismissive of technology].", "Both sides presented."),
                    ic("The main issue is [*fairness and accountability|fashion design|recipe quality].", "Algorithmic bias."),
                    ic("Ordinary citizens may struggle to understand technical [*explanations|competition|isolation].", "Technical explanations."),
                    ic("The tone is [*analytical|comic|romantic].", "Analytical."),
                ],
            ),
        )),
        ("reading", "post-truth-politics", lesson(
            "Politics in a 'post-truth' era",
            "reading",
            2,
            "<h2>Politics in a 'post-truth' era</h2><p>Some commentators argue that emotional appeal now rivals factual evidence in public debate. Social media amplifies sensational claims and allows false stories to spread before they can be corrected. Defenders of the term 'post-truth' say it describes a structural shift, not mere lying. Others reject the label as elitist, claiming voters still care about evidence but distrust institutions that present it. Either way, democratic debate depends on media literacy and transparent verification.</p>",
            three_sets(
                [
                    ic("Emotional appeal may now rival [*factual evidence|sports results|weather forecasts only].", "Rivals factual evidence."),
                    ic("Social media helps false stories spread [*before correction|after everyone forgets|only in print].", "Before they can be corrected."),
                    ic("'Post-truth' describes a [*structural shift|grammar rule|musical trend].", "Structural shift."),
                    ic("Democratic debate depends on media literacy and [*transparent verification|secret voting only|luxury travel].", "Transparent verification."),
                ],
                [
                    lg("Sensational claims spread quickly on social ____. ", "media", "menus", "museums", "Social media."),
                    lg("Some critics call the label ____. ", "elitist", "tiny", "tasty", "Reject as elitist."),
                    lg("Voters may distrust the ____ that present evidence.", "institutions", "instruments", "ingredients", "Distrust institutions."),
                    lg("False stories can spread with little immediate ____. ", "correction", "collection", "connection", "Before correction."),
                ],
                [
                    ic("The writer presents [*multiple perspectives|no argument|only jokes].", "Commentators and critics."),
                    ic("The passage concerns [*public discourse|garden design|train schedules].", "Post-truth politics."),
                    ic("The tone is [*concerned but measured|angry throughout|purely comic].", "Measured analysis."),
                    ic("Media literacy is presented as [*essential|irrelevant|dangerous].", "Democratic debate depends on it."),
                ],
            ),
        )),
        ("reading", "universal-basic-income", lesson(
            "The case for and against universal basic income",
            "reading",
            3,
            "<h2>The case for and against universal basic income</h2><p>Universal basic income (UBI) proposes regular unconditional payments to all citizens. Supporters claim it would simplify welfare systems, reduce poverty and give workers flexibility in a changing labour market. Opponents warn of enormous fiscal cost and reduced incentive to work. Pilot programmes have produced mixed results, partly because short trials cannot capture long-term behavioural effects. The debate ultimately hinges on whether security or conditionality better promotes social trust.</p>",
            three_sets(
                [
                    ic("UBI means payments that are [*unconditional|secret|temporary only for students].", "Unconditional payments."),
                    ic("Supporters say UBI could [*simplify welfare|ban all jobs|end education].", "Simplify welfare systems."),
                    ic("Opponents fear high fiscal cost and less incentive to [*work|travel|sleep].", "Incentive to work."),
                    ic("Pilot programmes have produced [*mixed results|no data|uniform success everywhere].", "Mixed results."),
                ],
                [
                    lg("Short trials cannot capture long-term ____ effects.", "behavioural", "musical", "weather", "Behavioural effects."),
                    lg("Supporters believe UBI could reduce ____. ", "poverty", "poetry", "parking", "Reduce poverty."),
                    lg("The debate concerns security versus ____. ", "conditionality", "celebrity", "certainty only", "Security vs conditionality."),
                    lg("UBI could give workers greater ____. ", "flexibility", "furniture", "fluency only", "Flexibility in labour market."),
                ],
                [
                    ic("The article is [*balanced|one-sided propaganda|unrelated to economics].", "For and against."),
                    ic("The central question involves [*social trust|recipe design|film reviews].", "Security vs conditionality."),
                    ic("Fiscal cost is a concern for [*opponents|supporters only|no one].", "Opponents warn of cost."),
                    ic("The tone is [*policy-oriented|poetic|sarcastic only].", "Policy debate."),
                ],
            ),
        )),
        ("reading", "consciousness-and-ai", lesson(
            "Can machines be conscious?",
            "reading",
            4,
            "<h2>Can machines be conscious?</h2><p>Philosophers and neuroscientists still lack a single definition of consciousness, which makes the question of machine consciousness especially difficult. Some researchers argue that if a system behaves intelligently and reports inner states, we should treat it cautiously for ethical reasons. Others insist consciousness requires biological processes that silicon cannot replicate. The disagreement matters because rights, responsibility and regulation may one day depend on how societies answer it.</p>",
            three_sets(
                [
                    ic("There is still no single definition of [*consciousness|gravity|photosynthesis].", "Lack a single definition."),
                    ic("Some researchers cite behaviour and reported [*inner states|weather patterns|ticket prices].", "Reports inner states."),
                    ic("Others insist consciousness needs [*biological processes|only faster chips|better screens].", "Biological processes."),
                    ic("The answer may affect future [*rights and regulation|fashion trends|recipe books].", "Rights, responsibility, regulation."),
                ],
                [
                    lg("Silicon systems may not replicate certain biological ____. ", "processes", "profits", "products", "Biological processes."),
                    lg("Ethical caution is advised by some ____. ", "researchers", "recipes", "rivers", "Some researchers."),
                    lg("The question is both philosophical and ____. ", "scientific", "culinary", "musical", "Philosophers and neuroscientists."),
                    lg("Societies may need new rules about ____. ", "responsibility", "restaurants", "rainfall", "Responsibility."),
                ],
                [
                    ic("The passage presents [*competing views|one definitive answer|no arguments].", "Some vs others."),
                    ic("The topic sits at the intersection of ethics and [*technology|gardening|cooking].", "AI and consciousness."),
                    ic("The writer suggests the debate is [*practically important|trivial|already settled].", "May affect rights and regulation."),
                    ic("The tone is [*thoughtful|comic|nostalgic only].", "Thoughtful."),
                ],
            ),
        )),
        ("reading", "decolonising-museums", lesson(
            "Decolonising museum collections",
            "reading",
            5,
            "<h2>Decolonising museum collections</h2><p>Museums in former colonial powers increasingly face demands to return artefacts acquired during empire. Institutions reply that they can preserve objects and educate global audiences. Critics argue that retention often reproduces historical injustice and that provenance records are sometimes incomplete because colonial administrators cared little about documenting consent. Recent agreements favour collaboration, long-term loans and shared digital access, suggesting a shift from ownership debates toward partnership models.</p>",
            three_sets(
                [
                    ic("Demands focus on artefacts acquired during [*empire|recent holidays|local festivals only].", "During empire."),
                    ic("Museums claim they can preserve objects and [*educate audiences|sell tickets only|avoid all research].", "Educate global audiences."),
                    ic("Critics say retention may reproduce historical [*injustice|weather|music].", "Historical injustice."),
                    ic("Recent agreements favour collaboration and [*shared digital access|complete silence|random sales].", "Shared digital access."),
                ],
                [
                    lg("Provenance records are sometimes ____. ", "incomplete", "perfect", "musical", "Incomplete records."),
                    lg("Colonial administrators often failed to document ____. ", "consent", "concerts", "coffee", "Document consent."),
                    lg("Some returns are replaced by long-term ____. ", "loans", "lawsuits only", "lunches", "Long-term loans."),
                    lg("The shift moves toward ____ models.", "partnership", "partnership only wrong", "isolation", "Partnership models."),
                ],
                [
                    ic("The article presents arguments from [*institutions and critics|only tourists|only athletes].", "Both sides."),
                    ic("The issue concerns [*cultural justice|airport design|recipe quality].", "Decolonising museums."),
                    ic("Digital access is part of a [*compromise|ban|joke].", "Collaboration and access."),
                    ic("The tone is [*serious and analytical|purely comic|indifferent].", "Serious."),
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
            "<h2>Use of English - C1 Test 1</h2><p>Mixed advanced grammar and vocabulary review.</p>",
            three_sets(
                [
                    ic("So complex [*was|is|were] the issue that experts were consulted.", "So complex was - inversion."),
                    ic("It [*would appear|must appear definitely|appears without doubt] that costs are rising.", "Hedging with would appear."),
                    ic("[*What|That|Which] the report challenges is the official narrative.", "What-clause fronting."),
                    ic("The findings are [*consistent with|angry with|bored with] previous studies.", "Consistent with."),
                ],
                [
                    lg("The ambassador acted as a diplomatic ____. ", "envoy", "envy", "envoying", "Envoy."),
                    lg("Judges must remain ____. ", "impartial", "impatient", "impartially", "Impartial."),
                    lg("The study draws attention ____ gaps in the data.", "to", "for", "at", "Draw attention to."),
                    lg("DNA ____ has become much faster.", "sequencing", "sequence", "sequenced", "DNA sequencing."),
                ],
                [
                    ic("[*Having been warned|Warning|To warn] repeatedly, he ignored the advice.", "Perfect passive participle."),
                    ic("The jury is [*bound to|never going to|forbidden to] reach a verdict soon.", "Bound to."),
                    ic("[*Had|If had] we known, we would have acted differently.", "Had we known."),
                    ic("The former policy focused on tax; [*the latter|the ladder|the weather] on spending.", "Former/latter."),
                ],
            ),
        )),
        ("use-of-english", "test-2", lesson(
            "Use of English - Test 2",
            "use-of-english",
            2,
            "<h2>Use of English - C1 Test 2</h2><p>Second mixed review at C1 level.</p>",
            three_sets(
                [
                    ic("[*Should|If should] you require assistance, contact the office.", "Formal Should you..."),
                    ic("There is [*some|total|no] evidence to suggest a link.", "Hedged some evidence."),
                    ic("Smith (2020) [*argues|tells|whispers] that reform is necessary.", "Argues academically."),
                    ic("I would [*rather|better|sooner not] you did not publish that draft.", "Would rather + past."),
                ],
                [
                    lg("The scandal raised questions about ____. ", "accountability", "account", "accounting", "Accountability."),
                    lg("The poet seems to ____ classical myth.", "allude to", "allude", "allusion", "Allude to."),
                    lg("Economic ____ were imposed on the regime.", "sanctions", "sanction", "sanctioned", "Sanctions."),
                    lg("The frontal ____ is involved in planning.", "cortex", "cortical", "cortexes", "Cortex."),
                ],
                [
                    ic("[*Such was|Was such] the demand that servers crashed.", "Such was the demand."),
                    ic("The board approved the plan and [*did so|did it|did this] quickly.", "Did so."),
                    ic("[*It is transparency that|Transparency is that|Is transparency that] builds trust.", "Cleft sentence."),
                    ic("The treaty requires parliamentary [*ratification|ratify|ratified].", "Ratification."),
                ],
            ),
        )),
        ("use-of-english", "test-3", lesson(
            "Use of English - Test 3",
            "use-of-english",
            3,
            "<h2>Use of English - C1 Test 3</h2><p>Final mixed review.</p>",
            three_sets(
                [
                    ic("[*Were|Was|Am] I in your position, I would seek advice.", "Were I in your position."),
                    ic("The results [*may well|must certainly|will never] indicate a trend.", "May well hedge."),
                    ic("[*Not having been consulted|Not consulting|Not to consult], staff objected.", "Negative perfect passive participle."),
                    ic("You [*had better|would rather|must better] leave now.", "Had better."),
                ],
                [
                    lg("The novel's central ____ recurs throughout.", "motif", "motive", "motion", "Motif."),
                    lg("Gene ____ raises ethical concerns.", "editing", "editor", "edited", "Gene editing."),
                    lg("The city changed its ____. ", "skyline", "skylight", "sky", "Skyline."),
                    lg("Critics fear the ruling could ____ journalism.", "chill", "heat", "warm", "Chill journalism."),
                ],
                [
                    ic("[*The extent to which|The extent which|The extent in which] rules are enforced is unclear.", "The extent to which."),
                    ic("He is [*meant to|meaning to|minded to] chair the meeting.", "Meant to = supposed to."),
                    ic("Costs rose; [*hence|however|for instance] profits fell.", "Hence."),
                    ic("The author [*attributes the decline to|attributes the decline with|attributes to decline] several factors.", "Attribute X to Y."),
                ],
            ),
        )),
    ]


def build_writing():
    return [
        ("writing", "academic-essay", lesson(
            "Writing an academic essay",
            "writing",
            1,
            "<h2>Writing an academic essay</h2><p>Academic essays at C1 level require a clear thesis, hedged claims and coherent argumentation.</p><ul><li>Thesis statement in the introduction</li><li>Topic sentences in each paragraph</li><li>Evidence and cautious interpretation</li><li>Formal conclusion</li></ul>",
            three_sets(
                [
                    ic("[*This essay contends that remote work reshapes urban economies in complex ways.|Essay contends remote work reshapes urban economies complex.|Remote work essay contends urban.]", "Clear thesis."),
                    ic("[*It could be argued that flexibility benefits employees, but it may also blur work-life boundaries.|Could argued flexibility benefits employees blur boundaries.|Flexibility argued employees benefits.]", "Hedged argument."),
                    ic("[*The evidence suggests, rather than proves, a link between commuting time and wellbeing.|Evidence proves definitely link commuting wellbeing.|Link evidence commuting proves.]", "Cautious interpretation."),
                    ic("[*In conclusion, policymakers should treat remote work as a structural shift, not a temporary trend.|Conclusion policymakers remote work temporary trend.|Policymakers conclusion remote work.]", "Strong conclusion."),
                ],
                [
                    lg("Academic essays should avoid overly ____ claims.", "absolute", "formal", "precise", "Avoid absolute claims."),
                    lg("Each paragraph needs a clear topic ____. ", "sentence", "picture", "ticket", "Topic sentence."),
                    lg("Use reporting verbs such as argue, suggest and ____. ", "maintain", "shout", "run", "Maintain."),
                    lg("Reference sources ____ to avoid plagiarism.", "accurately", "rarely", "secretly", "Reference accurately."),
                ],
                [
                    ic("[*One limitation of the study is its short time frame.|Limitation study short time frame one.|Study limitation short frame.]", "Academic limitation."),
                    ic("[*Furthermore, the data were collected in a single region.|Furthermore data collected single region.|Data furthermore single region.]", "Furthermore linker."),
                    ic("[*Nevertheless, the findings remain relevant to broader debates.|Nevertheless findings remain relevant broader.|Findings nevertheless relevant.]", "Nevertheless."),
                    ic("[*To summarise, the benefits depend on how policies are designed.|Summarise benefits depend policies designed.|Benefits summarise depend designed.]", "To summarise."),
                ],
            ),
        )),
        ("writing", "critical-review", lesson(
            "Writing a critical review",
            "writing",
            2,
            "<h2>Writing a critical review</h2><p>A critical review evaluates a book, film or article with balanced judgement and precise language.</p>",
            three_sets(
                [
                    ic("[*Although the plot is predictable, the performances are compelling.|Plot predictable although performances compelling.|Although performances plot predictable.]", "Balanced evaluation."),
                    ic("[*The director juxtaposes wealth and poverty to expose social tension.|Director juxtaposes wealth poverty social tension.|Juxtaposes director wealth poverty.]", "Precise critical vocabulary."),
                    ic("[*On balance, the novel succeeds as a character study rather than as thriller.|Balance novel succeeds character study thriller.|Novel balance succeeds study.]", "On balance."),
                    ic("[*Readers seeking subtle moral ambiguity will not be disappointed.|Readers seeking moral ambiguity disappointed not.|Seeking readers ambiguity moral.]", "Audience-focused recommendation."),
                ],
                [
                    lg("A critical review should combine summary and ____. ", "evaluation", "recipe", "ticket", "Evaluation."),
                    lg("Use precise adjectives such as compelling, uneven and ____. ", "thought-provoking", "tasty", "noisy", "Thought-provoking."),
                    lg("Avoid vague praise like 'very nice' or 'pretty ____. '", "good", "loud", "fast", "Pretty good is vague."),
                    lg("Support judgements with brief ____. ", "examples", "jokes", "titles only", "Brief examples."),
                ],
                [
                    ic("[*The pacing falters in the second half.|Pacing falters second half the.|Second half pacing falters.]", "Specific criticism."),
                    ic("[*The author's prose is economical yet evocative.|Author prose economical evocative yet.|Prose author economical.]", "Stylistic praise."),
                    ic("[*Ultimately, the film raises more questions than it answers.|Ultimately film raises questions answers than.|Film ultimately questions raises.]", "Final judgement."),
                    ic("[*I would recommend it to viewers who enjoy slow, reflective drama.|Recommend viewers enjoy slow reflective drama.|Viewers recommend enjoy drama.]", "Targeted recommendation."),
                ],
            ),
        )),
        ("writing", "proposal-document", lesson(
            "Writing a proposal",
            "writing",
            3,
            "<h2>Writing a proposal</h2><p>Proposals persuade decision-makers by defining a problem, objectives, method and expected outcomes.</p>",
            three_sets(
                [
                    ic("[*This proposal outlines a pilot programme to improve digital literacy among older adults.|Proposal outlines pilot programme digital literacy older adults.|Pilot proposal literacy digital adults.]", "Clear opening."),
                    ic("[*The primary objective is to reduce social isolation through structured training.|Primary objective reduce social isolation structured training.|Objective primary isolation reduce.]", "Objective statement."),
                    ic("[*The project will be evaluated using attendance records and participant surveys.|Project evaluated attendance records participant surveys.|Evaluated project attendance surveys.]", "Method."),
                    ic("[*We request funding of 18,000 euros for the initial six-month phase.|Request funding 18,000 euros initial six-month phase.|Funding request euros 18,000.]", "Specific request."),
                ],
                [
                    lg("A proposal should identify a clear ____. ", "problem", "joke", "colour", "Problem."),
                    lg("Objectives should be measurable and ____. ", "realistic", "secret", "musical", "Realistic objectives."),
                    lg("Include a brief timeline and ____. ", "budget", "poem", "menu", "Budget."),
                    lg("The tone should remain professional and ____. ", "persuasive", "aggressive", "casual", "Persuasive."),
                ],
                [
                    ic("[*If approved, the programme could be expanded to neighbouring districts.|Approved programme expanded neighbouring districts.|Programme approved expanded districts.]", "Future benefit."),
                    ic("[*The need for action is supported by recent community surveys.|Need action supported community surveys recent.|Action need surveys supported.]", "Evidence."),
                    ic("[*We would be happy to provide further details upon request.|Happy provide further details upon request.|Details happy provide request.]", "Polite closing."),
                    ic("[*Thank you for considering this proposal.|Thank considering proposal this.|Proposal thank considering.]", "Professional ending."),
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
    print(f"Wrote {len(items)} C1 lessons with 0 validation errors.")


if __name__ == "__main__":
    main()
