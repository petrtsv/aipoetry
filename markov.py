import markovify

with open('poetry_dataset.txt', encoding='utf-8') as f:
    read_text = f.read()

model = markovify.NewlineText(read_text)


def markov_generate():
    result = model.make_sentence()
    while result is None:
        result = model.make_sentence()
    return result.replace('$', '\n')
