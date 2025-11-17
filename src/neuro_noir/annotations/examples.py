import dspy

#
# ✨ ENTITY TYPE ONTOLOGY
#
#  Person, Statement, Location, Event, Object, Evidence, Organization
#
# ✨ RELATION ONTOLOGY
#
#  said, responded_to, testified, denied, refers_to,
#  motive_for, has_alibi_for, used_as_means, has_opportunity_for,
#  suspected_of, present_at, visited, describes, evidence_of
#
# Each annotation is:
# {
#   "subject": { "text": ..., "type": ... },
#   "relation": "...",
#   "object": { "text": ..., "type": ... },
#   "category": "...",
#   "reasoning": "..."
# }
#


def ex(history, paragraph, annotations):
    return dspy.Example(
        history=history,
        paragraph=paragraph,
        annotations=annotations
    ).with_inputs("history", "paragraph")


training_examples: list[dspy.Example] = [

# ----------------------------------------------------------
# 🟨 1
# ----------------------------------------------------------
ex(
    history=[
        "\"Did you see him?\" asked Watson.",
        "\"You mean the old fellow who has just gone out?\""
    ],
    paragraph="\"Precisely,\" Holmes replied.",
    annotations=[
        {
            "subject": {"text": "Sherlock Holmes", "type": "Person"},
            "relation": "said",
            "object": {"text": "\"Precisely.\"", "type": "Statement"},
            "category": "Testimony",
            "reasoning": "Holmes is the speaker of the quoted reply."
        },
        {
            "subject": {"text": "\"Precisely.\"", "type": "Statement"},
            "relation": "responded_to",
            "object": {"text": "\"You mean the old fellow...\"", "type": "Statement"},
            "category": "Testimony",
            "reasoning": "The new line explicitly answers the prior question."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 2
# ----------------------------------------------------------
ex(
    history=[
        "\"Lady Ashcroft loathed her husband,\" whispered the maid.",
        "The victim died from poison."
    ],
    paragraph="Holmes lifted the teacup. \"This reeks of bitter almonds.\"",
    annotations=[
        {
            "subject": {"text": "teacup", "type": "Object"},
            "relation": "used_as_means",
            "object": {"text": "poisoning", "type": "Event"},
            "category": "Means",
            "reasoning": "Cyanide is known for its almond scent and was delivered via tea."
        },
        {
            "subject": {"text": "Lady Ashcroft", "type": "Person"},
            "relation": "motive_for",
            "object": {"text": "murder of husband", "type": "Event"},
            "category": "Motive",
            "reasoning": "Prior hatred establishes motive."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 3
# ----------------------------------------------------------
ex(
    history=[
        "The gardener claimed he never entered the house.",
        "A muddy footprint was found beside the study window."
    ],
    paragraph="\"Your boots are still wet,\" Holmes observed.",
    annotations=[
        {
            "subject": {"text": "gardener", "type": "Person"},
            "relation": "present_at",
            "object": {"text": "study window", "type": "Location"},
            "category": "Opportunity",
            "reasoning": "Wet boots contradict claim of staying outside."
        },
        {
            "subject": {"text": "wet boots", "type": "Evidence"},
            "relation": "evidence_of",
            "object": {"text": "muddy footprint", "type": "Evidence"},
            "category": "Fact",
            "reasoning": "Matching soil traces connect suspect to scene."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 4
# ----------------------------------------------------------
ex(
    history=[
        "\"I was at the opera that night,\" said Mr. Black.",
        "The murder occurred after midnight."
    ],
    paragraph="Holmes inspected the ticket stub. \"This ended at 11:45 PM.\"",
    annotations=[
        {
            "subject": {"text": "Mr. Black", "type": "Person"},
            "relation": "has_alibi_for",
            "object": {"text": "murder", "type": "Event"},
            "category": "Alibi",
            "reasoning": "He could not reach the scene in fifteen minutes."
        },
        {
            "subject": {"text": "\"I was at the opera that night.\"", "type": "Statement"},
            "relation": "supported_by",
            "object": {"text": "ticket stub", "type": "Evidence"},
            "category": "Testimony",
            "reasoning": "Physical evidence confirms timeline."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 5
# ----------------------------------------------------------
ex(
    history=[
        "\"I never touched the letter!\" shouted Miss Grey.",
        "The ransom note was typed on her typewriter."
    ],
    paragraph="Holmes slid open the ribbon tray. \"Freshly changed ink.\"",
    annotations=[
        {
            "subject": {"text": "Miss Grey", "type": "Person"},
            "relation": "suspected_of",
            "object": {"text": "ransom note", "type": "Statement"},
            "category": "Identity",
            "reasoning": "Fresh ink contradicts her denial."
        },
        {
            "subject": {"text": "typewriter", "type": "Object"},
            "relation": "used_as_means",
            "object": {"text": "blackmail demand", "type": "Event"},
            "category": "Means",
            "reasoning": "Device produced the incriminating document."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 6
# ----------------------------------------------------------
ex(
    history=[
        "\"The Colonel died instantly,\" said the doctor.",
        "Gunshot residue was found on the window frame."
    ],
    paragraph="Holmes held the empty flowerpot. \"Someone fired from the garden.\"",
    annotations=[
        {
            "subject": {"text": "unknown shooter", "type": "Person"},
            "relation": "present_at",
            "object": {"text": "garden", "type": "Location"},
            "category": "Opportunity",
            "reasoning": "Firing angle matches garden placement."
        },
        {
            "subject": {"text": "\"Someone fired from the garden.\"", "type": "Statement"},
            "relation": "describes",
            "object": {"text": "gunshot event", "type": "Event"},
            "category": "Testimony",
            "reasoning": "Holmes’ deduction establishes location of the shot."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 7
# ----------------------------------------------------------
ex(
    history=[
        "No weapon was found near the corpse.",
        "The fireplace tools had been recently cleaned."
    ],
    paragraph="\"These tongs were scrubbed with lye,\" Holmes noted.",
    annotations=[
        {
            "subject": {"text": "fireplace tongs", "type": "Object"},
            "relation": "used_as_means",
            "object": {"text": "killing", "type": "Event"},
            "category": "Means",
            "reasoning": "Cleaning suggests blood removal."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 8
# ----------------------------------------------------------
ex(
    history=[
        "The safe contained bearer bonds.",
        "\"Only one man knew the combination,\" said Watson."
    ],
    paragraph="Holmes tapped the scorched vault door. \"This fire was set deliberately.\"",
    annotations=[
        {
            "subject": {"text": "combination holder", "type": "Person"},
            "relation": "motive_for",
            "object": {"text": "arson", "type": "Event"},
            "category": "Motive",
            "reasoning": "Fire hides evidence of theft."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 9
# ----------------------------------------------------------
ex(
    history=[
        "\"I saw him in the corridor at midnight,\" testified the butler.",
        "The stabbing happened at 12:05 AM."
    ],
    paragraph="\"Yet the corridor clock is five minutes slow,\" Holmes observed.",
    annotations=[
        {
            "subject": {"text": "\"I saw him in the corridor at midnight.\"", "type": "Statement"},
            "relation": "contradicted_by",
            "object": {"text": "clock discrepancy", "type": "Evidence"},
            "category": "Testimony",
            "reasoning": "Corrected time places the suspect near scene."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 10
# ----------------------------------------------------------
ex(
    history=[
        "The bank manager vanished the same night as the vault robbery.",
        "No forced entry marks were found."
    ],
    paragraph="\"Inside job,\" Holmes murmured.",
    annotations=[
        {
            "subject": {"text": "bank manager", "type": "Person"},
            "relation": "has_opportunity_for",
            "object": {"text": "vault robbery", "type": "Event"},
            "category": "Opportunity",
            "reasoning": "Exclusive access implies opportunity."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 11
# ----------------------------------------------------------
ex(
    history=[
        "\"He threatened to ruin me!\" cried the victim’s partner.",
        "The victim was shot in his office."
    ],
    paragraph="Holmes pointed at the dropped revolver. \"A left-handed grip.\"",
    annotations=[
        {
            "subject": {"text": "partner", "type": "Person"},
            "relation": "motive_for",
            "object": {"text": "shooting", "type": "Event"},
            "category": "Motive",
            "reasoning": "Anger + weapon detail incriminates him."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 12
# ----------------------------------------------------------
ex(
    history=[
        "\"I never spoke to Miss Adler,\" said Lord Cavendish.",
        "A calling card was found in her parlor."
    ],
    paragraph="Holmes lifted the seal. \"This is his personal crest.\"",
    annotations=[
        {
            "subject": {"text": "Lord Cavendish", "type": "Person"},
            "relation": "said",
            "object": {"text": "\"I never spoke to Miss Adler.\"", "type": "Statement"},
            "category": "Testimony",
            "reasoning": "He is speaker of the denial."
        },
        {
            "subject": {"text": "calling card", "type": "Object"},
            "relation": "evidence_of",
            "object": {"text": "meeting with Miss Adler", "type": "Event"},
            "category": "Evidence",
            "reasoning": "The crest proves physical presence."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 13
# ----------------------------------------------------------
ex(
    history=[
        "\"The jewels were locked away,\" said the countess.",
        "Yet the drawer showed scratch marks."
    ],
    paragraph="Holmes held the bent hairpin. \"This was the lockpick.\"",
    annotations=[
        {
            "subject": {"text": "hairpin", "type": "Object"},
            "relation": "used_as_means",
            "object": {"text": "jewel theft", "type": "Event"},
            "category": "Means",
            "reasoning": "Bending indicates improvised lockpick."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 14
# ----------------------------------------------------------
ex(
    history=[
        "\"I never left the card table,\" boasted Sir Roland.",
        "The murder happened in the billiard room."
    ],
    paragraph="Holmes studied the untouched cigar. \"Then who dropped ashes there?\"",
    annotations=[
        {
            "subject": {"text": "Sir Roland", "type": "Person"},
            "relation": "suspected_of",
            "object": {"text": "presence in billiard room", "type": "Event"},
            "category": "Identity",
            "reasoning": "Ash trail contradicts alibi."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 15
# ----------------------------------------------------------
ex(
    history=[
        "\"I heard the clock strike two,\" said the maid.",
        "But the body was cold to the touch."
    ],
    paragraph="Holmes lifted the candlestick. \"This is covered in frozen grease.\"",
    annotations=[
        {
            "subject": {"text": "frozen grease", "type": "Evidence"},
            "relation": "evidence_of",
            "object": {"text": "earlier death time", "type": "Event"},
            "category": "Fact",
            "reasoning": "Melting rate contradicts reported hour."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 16
# ----------------------------------------------------------
ex(
    history=[
        "\"I saw the vicar enter at dusk,\" said the sexton.",
        "The relic was stolen just before evening mass."
    ],
    paragraph="Holmes examined a torn cassock thread by the altar rail.",
    annotations=[
        {
            "subject": {"text": "vicar", "type": "Person"},
            "relation": "present_at",
            "object": {"text": "altar", "type": "Location"},
            "category": "Opportunity",
            "reasoning": "Physical thread proves proximity."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 17
# ----------------------------------------------------------
ex(
    history=[
        "\"The door was locked from inside,\" said Inspector Gregson.",
        "No key was found."
    ],
    paragraph="Holmes pointed at the string spool. \"He pulled it closed from outside.\"",
    annotations=[
        {
            "subject": {"text": "string spool", "type": "Object"},
            "relation": "used_as_means",
            "object": {"text": "fake locked room", "type": "Event"},
            "category": "Means",
            "reasoning": "Classic trick for staging locked room."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 18
# ----------------------------------------------------------
ex(
    history=[
        "\"He hated the Colonel,\" said the housekeeper.",
        "The Colonel was found drowned in the bath."
    ],
    paragraph="Holmes held up the broken soap dish. \"He struggled.\"",
    annotations=[
        {
            "subject": {"text": "suspect", "type": "Person"},
            "relation": "motive_for",
            "object": {"text": "Colonel's death", "type": "Event"},
            "category": "Motive",
            "reasoning": "Hatred + signs of struggle indicate intent."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 19
# ----------------------------------------------------------
ex(
    history=[
        "\"I never wore gloves,\" said Miss Turner.",
        "Yet a glove was found in the garden."
    ],
    paragraph="Holmes measured the glove. \"This fits her hand perfectly.\"",
    annotations=[
        {
            "subject": {"text": "Miss Turner", "type": "Person"},
            "relation": "present_at",
            "object": {"text": "garden", "type": "Location"},
            "category": "Opportunity",
            "reasoning": "Fit proves she was there."
        }
    ]
),

# ----------------------------------------------------------
# 🟨 20
# ----------------------------------------------------------
ex(
    history=[
        "\"The telegram warned him,\" said Watson.",
        "But the victim never left his study."
    ],
    paragraph="Holmes tapped the torn envelope. \"Someone intercepted it.\"",
    annotations=[
        {
            "subject": {"text": "interceptor", "type": "Person"},
            "relation": "prevented",
            "object": {"text": "victim escape", "type": "Event"},
            "category": "Opportunity",
            "reasoning": "Blocking warning created chance to kill."
        }
    ]
)

]

