import glob
import pickle
import numpy as np

from music21 import converter, note, chord, stream

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# ==========================
# STEP 1: LOAD MIDI FILES
# ==========================

notes = []

for file in glob.glob("dataset/*.mid"):
    print("Reading:", file)

    midi = converter.parse(file)

    for element in midi.flat.notes:

        if isinstance(element, note.Note):
            notes.append(str(element.pitch))

        elif isinstance(element, chord.Chord):
            notes.append(
                '.'.join(str(n)
                for n in element.normalOrder)
            )

print("Total Notes:", len(notes))

# ==========================
# STEP 2: PREPARE DATA
# ==========================

sequence_length = 100

pitchnames = sorted(set(notes))

note_to_int = dict(
    (note, number)
    for number, note in enumerate(pitchnames)
)

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):

    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]

    network_input.append(
        [note_to_int[n]
         for n in sequence_in]
    )

    network_output.append(
        note_to_int[sequence_out]
    )

n_patterns = len(network_input)

network_input = np.reshape(
    network_input,
    (n_patterns, sequence_length, 1)
)

network_input = network_input / float(
    len(pitchnames)
)

network_output = to_categorical(
    network_output
)

# ==========================
# STEP 3: BUILD MODEL
# ==========================

model = Sequential()

model.add(
    LSTM(
        256,
        input_shape=(
            network_input.shape[1],
            network_input.shape[2]
        )
    )
)

model.add(Dropout(0.3))

model.add(Dense(128, activation='relu'))

model.add(
    Dense(
        len(pitchnames),
        activation='softmax'
    )
)

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam'
)

# ==========================
# STEP 4: TRAIN MODEL
# ==========================

print("Training Started...")

model.fit(
    network_input,
    network_output,
    epochs=20,
    batch_size=64
)

print("Training Complete!")

# ==========================
# STEP 5: GENERATE NOTES
# ==========================

int_to_note = dict(
    (number, note)
    for number, note in enumerate(pitchnames)
)

start = np.random.randint(
    0,
    len(network_input)-1
)

pattern = network_input[start]

prediction_output = []

for _ in range(100):

    prediction_input = np.reshape(
        pattern,
        (1, len(pattern), 1)
    )

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern = np.append(
        pattern,
        index
    )

    pattern = pattern[1:]

# ==========================
# STEP 6: CREATE MIDI FILE
# ==========================

output_notes = []

offset = 0

for pattern in prediction_output:

    try:
        new_note = note.Note(pattern)

        new_note.offset = offset

        output_notes.append(new_note)

        offset += 0.5

    except:
        pass

midi_stream = stream.Stream(
    output_notes
)

midi_stream.write(
    'midi',
    fp='generated_music.mid'
)

print("generated_music.mid created successfully!")