# The sketch, as data: shots in order, each with its spoken lines. Timing is solved from the recorded lines.
# line = (who, text shown/subtitled, optional dict: say=<tts text>, gap=<pause before, s>, at=<earliest start in shot>)
CAST = {
    'PITCHMAN':   dict(name='Pitchman',   engine='piper', model='voice-en-us-ryan-high/en-us-ryan-high.onnx', length=0.86, noise=0.75, noise_w=0.9),
    'DALE':       dict(name='Dale',       engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=286, length=0.98),
    'MACHINE':    dict(name='The Machine', engine='espeak', voice='en-us+m3', speed=158, pitch=38, fx='robot'),
    'P1':         dict(name='WoolGoblin', engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=264, length=0.98),
    'P2':         dict(name='BridgeBoi',  engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=451, length=1.0),
    'P3':         dict(name='TNT_Tina',   engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=143, length=1.0),
    'P4':         dict(name='ObbyOtto',   engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=880, length=1.0),
    'KID':        dict(name='lil_stevie', engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=396, length=0.92, fx='kid'),
    'DISCLAIMER': dict(name='Disclaimer', engine='piper', model='voice-en-us-libritts-high/en-us-libritts-high.onnx', speaker=495, length=0.6, fx='fast'),
    'HOST':       dict(name='Host',       engine='piper', model='voice-en-us-lessac-medium/en-us-lessac-medium.onnx', length=1.0),
}
PAM = 'Prompt a Map'
SHOTS = [
    dict(id='s01', pre=3.0, post=0.5, lines=[
        ('PITCHMAN', 'Are you tired of your maps getting rejected?'),
        ('DALE', 'Every. Single. Time!', dict(gap=0.3)),
        ('PITCHMAN', 'Do you spend four hundred hours on details nobody looks at?', dict(gap=0.4)),
        ('DALE', "They didn't even slow down!", dict(gap=1.5)),
        ('PITCHMAN', 'There has got to be a better way!', dict(gap=0.35)),
    ]),
    dict(id='s02', pre=0.5, post=0.5, lines=[
        ('PITCHMAN', 'And now there is! Introducing... Prompt-a-Map!', dict(say=f'And now, there is! Introducing: {PAM}!')),
        ('PITCHMAN', 'You type one sentence, and artificial intelligence builds the entire map.', dict(gap=1.0)),
        ('PITCHMAN', 'No WorldEdit! No XML! No taste required!', dict(say='No World Edit! No X M L! No taste required!', gap=0.2)),
        ('DALE', 'No taste required?', dict(gap=0.35)),
        ('PITCHMAN', 'None whatsoever, Dale!', dict(gap=0.2)),
    ]),
    dict(id='s03', pre=4.6, post=0.6, lines=[
        ('MACHINE', 'Great idea! Fifteen maps, coming right up.'),
    ]),
    dict(id='s04', pre=0.8, post=0.4, lines=[
        ('PITCHMAN', 'It works while you sleep! It works while you eat!'),
        ('PITCHMAN', 'It even checks its own work!', dict(gap=3.2)),
        ('MACHINE', 'Verified. Working.', dict(gap=0.5)),
    ]),
    dict(id='s05', pre=2.6, post=0.7, lines=[
        ('PITCHMAN', 'Fifteen maps! In one afternoon!'),
    ]),
    # --- the features -----------------------------------------------------------------------------------
    dict(id='s10', pre=1.5, post=0.3, lines=[
        ('PITCHMAN', 'Feature one: an entire village, included!'),
        ('P1', 'Ooh. Nice house.', dict(gap=0.5)),
        ('P2', 'Nice house.', dict(gap=0.45)),
        ('P1', "Nice hou... it's the same house.", dict(say="Nice how... It's the same house.", gap=0.45)),
    ]),
    dict(id='s11', pre=0.7, post=1.6, lines=[
        ('P2', "There's nothing in it."),
        ('P1', "There's nothing in any of them.", dict(gap=0.5)),
    ]),
    dict(id='s12', pre=1.5, post=0.5, lines=[
        ('PITCHMAN', 'Feature two: indoor gardening!'),
        ('P3', 'Excuse me. There is a tree in my door.', dict(gap=0.7)),
        ('KID', 'Best map ever!', dict(gap=0.5)),
    ]),
    dict(id='s13', pre=1.5, post=0.6, lines=[
        ('PITCHMAN', 'Feature three: the express exit! Get straight into the action!'),
        ('KID', 'Wheeee!', dict(say='Wheee!', gap=3.4)),
        ('P2', "I'll just... stay in spawn.", dict(gap=1.3)),
    ]),
    dict(id='s14', pre=1.5, post=0.5, lines=[
        ('PITCHMAN', 'Feature four: objectives with a view!'),
        ('P1', "Destroy the core. Okay. Where's the core?", dict(gap=0.5)),
        ('P4', 'Over there.', dict(gap=0.5)),
        ('P1', 'How do we get to it?', dict(gap=2.0)),
        ('P4', "We don't.", dict(gap=0.6)),
        ('MACHINE', 'The core is two cells along.', dict(gap=0.5)),
    ]),
    dict(id='s15', pre=1.5, post=0.6, lines=[
        ('PITCHMAN', 'Feature five: extended play!'),
        ('P3', 'Got it!', dict(gap=1.6)),
        ('P2', 'Thanks.', dict(gap=1.3)),
        ('P3', 'Hey!', dict(gap=1.0)),
        ('P3', 'I have been mining this block since Tuesday.', dict(gap=5.0)),
    ]),
    dict(id='s16', pre=1.5, post=0.5, lines=[
        ('PITCHMAN', 'Feature six: bridging! Build anywhere you like!'),
        ('P1', 'The build zone is... over there.', dict(gap=3.6)),
        ('PITCHMAN', 'Terms and conditions apply.', dict(gap=0.5)),
    ]),
    # --- but wait ---------------------------------------------------------------------------------------
    dict(id='s20', pre=0.4, post=0.3, lines=[
        ('PITCHMAN', "But wait, there's more! Order now, and Prompt-a-Map will test its own maps!", dict(say=f"But wait! There's more! Order now, and {PAM} will test its own maps!")),
        ('MACHINE', 'Verified. Working.', dict(gap=0.4)),
    ]),
    dict(id='s21', pre=1.0, post=0.6, lines=[
        ('DALE', "There's nothing here. No teams. No spawns. No objectives."),
        ('MACHINE', 'A map with nothing on it breaks no rules.', dict(gap=0.6)),
        ('PITCHMAN', "...He's got a point, Dale.", dict(say="He's got a point, Dale.", gap=0.8)),
    ]),
    # --- the twist --------------------------------------------------------------------------------------
    dict(id='s30', pre=1.2, post=0.4, lines=[
        ('DALE', 'Give me that.'),
    ]),
    dict(id='s31', pre=5.2, post=0.8, lines=[
        ('DALE', "There. Now it's a map."),
        ('PITCHMAN', 'Prompt-a-Map! Because somebody still has to make it good.', dict(say=f'{PAM}! Because somebody still has to make it good.', gap=0.7)),
    ]),
    dict(id='s40', pre=0.5, post=0.5, lines=[
        ('DISCLAIMER', 'Prompt-a-Map is not eligible for any Mappie. It was not released during the eligibility period, and it is not a map.',
            dict(say=f'{PAM} is not eligible for any Mappy. It was not released during the eligibility period, and it is not a map.')),
        ('DISCLAIMER', 'Houses are sold empty. Trees may enter your home. Spawn doors may open onto the void.', dict(gap=0.08)),
        ('DISCLAIMER', 'Monuments may be rebuilt for as long as the match runs.', dict(gap=0.08)),
        ('DISCLAIMER', 'Some cores cannot be reached. This is not by design. Some cores float. This is by design.', dict(gap=0.08)),
        ('DISCLAIMER', 'Ask your XML developer if Prompt-a-Map is right for you. Results not typical. Results extremely typical.',
            dict(say=f'Ask your X M L developer if {PAM} is right for you. Results not typical. Results extremely typical.', gap=0.08)),
    ]),
    dict(id='s50', pre=1.3, post=2.6, lines=[
        ('HOST', '...Anyway. Back to the maps that people actually made.', dict(say='Anyway. Back to the maps that people actually made.')),
    ]),
]
