import markovify

with open('poetry_dataset.txt', encoding='utf-8') as f:
    read_text = f.read()

model = markovify.NewlineText(read_text)


def markov_generate(init_state):
    init_state = tuple((e.lower() for e in init_state))
    result = None
    try:
        result = model.make_sentence(init_state=init_state)
    except KeyError:
        init_state = None

    while result is None:
        result = model.make_sentence(init_state=init_state)
    lines = result.split('$')

    words_to_remove = init_state if init_state is not None else ()
    pos = 0

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        while pos < len(words_to_remove) and lines[i].startswith(words_to_remove[pos]):
            lines[i] = lines[i][len(words_to_remove[pos]):]
            lines[i] = lines[i].strip()
            pos += 1

    lines = [e for e in lines if e != ""]

    return '\n'.join(lines)
