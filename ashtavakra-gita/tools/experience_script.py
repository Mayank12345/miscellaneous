"""Script for the guided Experience: nine movements following the arc of the Ashtavakra Gita.

Each beat: (text, hold_seconds_after_narration, kind)
  kind "say"  : narrate, hold, advance
  kind "tap"  : narrate, then wait for the listener to tap
  kind "quiet": narrate, then a silent timer of hold seconds shown as a breathing light
Each movement ends with a verse: (ref, devanagari, iast, english, intro_line)
"""

MOVEMENTS = [
 {"name": "The question", "beats": [
   ("Find a comfortable way to sit. This will take about ten minutes. There is nothing to get right.", 3, "say"),
   ("Long ago, a king named Janaka sat before a twelve-year-old sage, and asked him three questions.", 1.5, "say"),
   ("How is wisdom found? How does freedom come? How do I let go?", 2.5, "say"),
   ("Tonight, you sit where the king sat. Ask yourself, honestly: what do I want to be free of?", 10, "say"),
  ],
  "verse": ("1.1", "कथं ज्ञानमवाप्नोति कथं मुक्तिर्भविष्यति।<br>वैराग्यं च कथं प्राप्तमेतद् ब्रूहि मम प्रभो॥",
            "kathaṃ jñānam avāpnoti kathaṃ muktir bhaviṣyati | vairāgyaṃ ca kathaṃ prāptam etad brūhi mama prabho ||",
            "How is knowledge gained? How does freedom come? How is letting go reached? Tell me this, master.",
            "The king's words:")},
 {"name": "Not this", "beats": [
   ("The sage did not hand the king a practice. He pointed. Let's do what he did.", 1.5, "say"),
   ("Look at your hand.", 4, "say"),
   ("You can see it. Your hand is seen. So who is doing the seeing?", 6, "say"),
   ("Now feel your breath. The breath is felt. So who is feeling it?", 6, "say"),
   ("Whatever you can notice, you are the one who notices it.", 3, "say"),
  ],
  "verse": ("1.3", "न पृथ्वी न जलं नाग्निर्न वायुर्द्यौर्न वा भवान्।<br>एषां साक्षिणमात्मानं चिद्रूपं विद्धि मुक्तये॥",
            "na pṛthvī na jalaṃ nāgnir na vāyur dyaur na vā bhavān | eṣāṃ sākṣiṇam ātmānaṃ cidrūpaṃ viddhi muktaye ||",
            "You are not earth, water, fire, air or sky. To be free, know yourself as awareness, the witness of all these.",
            "And the sage said:")},
 {"name": "The witness", "beats": [
   ("After this sentence, close your eyes, and listen for the furthest sound you can hear.", 12, "say"),
   ("The sound came to you. You did not have to make the hearing happen. It simply happens, in you.", 2, "say"),
   ("Now, instead of the sound, notice the listening itself. The quiet space in which every sound appears.", 9, "say"),
   ("That space has no edges. It was here before the sound, and it is here after it.", 3, "say"),
  ],
  "verse": ("1.7", "एको द्रष्टासि सर्वस्य मुक्तप्रायोऽसि सर्वदा।<br>अयमेव हि ते बन्धो द्रष्टारं पश्यसीतरम्॥",
            "eko draṣṭāsi sarvasya muktaprāyo'si sarvadā | ayam eva hi te bandho draṣṭāraṃ paśyasītaram ||",
            "You are the one seer of everything, and always free. Your only bondage is this: you take the seer to be something else.",
            "The sage said:")},
 {"name": "A thought passes", "beats": [
   ("Now wait for a thought to appear. Any thought at all. When you notice one, tap the screen.", 0, "tap"),
   ("There it was. Now watch where it goes.", 8, "say"),
   ("The thought came, and the thought went. Did you come and go with it?", 6, "say"),
   ("Thoughts are like weather. You are like the sky the weather moves through.", 3, "say"),
  ],
  "verse": ("1.4", "यदि देहं पृथक्कृत्य चिति विश्राम्य तिष्ठसि।<br>अधुनैव सुखी शान्तो बन्धमुक्तो भविष्यसि॥",
            "yadi dehaṃ pṛthak kṛtya citi viśrāmya tiṣṭhasi | adhunaiva sukhī śānto bandhamukto bhaviṣyasi ||",
            "If you set the body aside and simply rest in awareness, right now you will be happy, at peace, and free.",
            "The sage said:")},
 {"name": "Aho!", "beats": [
   ("When Janaka heard this, something in him turned around. He did not learn a new idea. He recognised what had always been there.", 1.5, "say"),
   ("And he cried out: Aho! How wonderful!", 2.5, "say"),
   ("Look now, while these words appear. Is anything missing from the simple fact of being aware?", 9, "say"),
   ("Nothing to add. Nothing to fix. It was never touched.", 3, "say"),
  ],
  "verse": ("2.1", "अहो निरञ्जनः शान्तो बोधोऽहं प्रकृतेः परः।<br>एतावन्तमहं कालं मोहेनैव विडम्बितः॥",
            "aho nirañjanaḥ śānto bodho'haṃ prakṛteḥ paraḥ | etāvantam ahaṃ kālaṃ mohenaiva viḍambitaḥ ||",
            "Wonder! I am spotless, at peace, pure awareness, beyond nature. All this time I have been fooled.",
            "The king said:")},
 {"name": "The test", "beats": [
   ("But the sage did not let the king off easily. He asked: if you know this, why do you still grab, and fear, and want?", 1.5, "say"),
   ("Let's be honest too. Bring to mind one real worry. A small one is fine.", 8, "say"),
   ("Watch what the mind does with it. Does it want something? Push something away? Replay it? Hold on?", 9, "say"),
   ("That grabbing and pushing, the sage said, is the whole of bondage. Not the situation. The grip.", 3, "say"),
  ],
  "verse": ("8.1", "तदा बन्धो यदा चित्तं किञ्चिद्वाञ्छति शोचति।<br>किञ्चिन्मुञ्चति गृह्णाति किञ्चिद्धृष्यति कुप्यति॥",
            "tadā bandho yadā cittaṃ kiñcid vāñchati śocati | kiñcin muñcati gṛhṇāti kiñcid dhṛṣyati kupyati ||",
            "It is bondage when the mind wants something, grieves over something, rejects something, holds on to something, is thrilled or angered by something.",
            "The sage said:")},
 {"name": "No one holding", "beats": [
   ("Keep the worry where it is. Don't push it away. Just notice: who is holding it?", 7, "say"),
   ("Look for the one who is worried. Not the worry. The one who has it.", 9, "say"),
   ("For one breath, let the worry be there, without anyone gripping it.", 7, "say"),
   ("When there is no 'I', there is freedom. Lightly. No grabbing, and no pushing away.", 3, "say"),
  ],
  "verse": ("8.4", "यदा नाहं तदा मोक्षो यदाहं बन्धनं तदा।<br>मत्वेति हेलया किञ्चिन्मा गृहाण विमुञ्च मा॥",
            "yadā nāhaṃ tadā mokṣo yadāhaṃ bandhanaṃ tadā | matveti helayā kiñcin mā gṛhāṇa vimuñca mā ||",
            "When there is no 'I', there is freedom. When there is 'I', there is bondage. Knowing this, lightly, grab nothing and push nothing away.",
            "The sage said:")},
 {"name": "The ocean", "beats": [
   ("Thoughts, feelings, sounds and worries keep arriving. Let them. They are waves.", 2, "say"),
   ("The ocean never fights its waves. It doesn't need them to stop.", 2, "say"),
   ("Let everything rise and fall, on its own, in you.", 12, "say"),
  ],
  "verse": ("7.1", "मय्यनन्तमहाम्भोधौ विश्वपोत इतस्ततः।<br>भ्रमति स्वान्तवातेन न ममास्त्यसहिष्णुता॥",
            "mayy ananta-mahāmbhodhau viśva-pota itas tataḥ | bhramati svānta-vātena na mamāsty asahiṣṇutā ||",
            "In me, the endless ocean, the ship of the world drifts this way and that on its own winds. I am not troubled.",
            "The king said:")},
 {"name": "Silence", "beats": [
   ("At the very end of the book, Janaka asks a string of questions. Where is bondage? Where is freedom? Where is the teacher? Where is the student?", 2, "say"),
   ("And then, he says nothing at all.", 2.5, "say"),
   ("Let's end the same way. Thirty seconds, with nothing to do.", 30, "quiet"),
   ("Whatever was aware during that silence is here now. It is what you are. It doesn't need this page, or any book. Go gently.", 4, "say"),
  ],
  "verse": ("18.1", "यस्य बोधोदये तावत्स्वप्नवद्भवति भ्रमः।<br>तस्मै सुखैकरूपाय नमः शान्ताय तेजसे॥",
            "yasya bodhodaye tāvat svapnavad bhavati bhramaḥ | tasmai sukhaikarūpāya namaḥ śāntāya tejase ||",
            "Bow to That which is happiness itself, peace and light. When it is known, all confusion becomes like a dream.",
            "And the book bows:")},
]
