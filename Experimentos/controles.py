"""Controles del protocolo; solo biblioteca estándar, también embebidos en el notebook."""
import hashlib
import json
import math
import random
import re
from collections import Counter


def stable_seed(*parts):
    raw = json.dumps(parts, ensure_ascii=False, separators=(',', ':')).encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:4], 'big')


def articles(rows):
    """WikiText: solo un encabezado = título = inicia otro artículo.

    Se retiran encabezados de cualquier nivel; se conservan párrafos y saltos.
    Un fragmento inicial sin título se conserva como artículo propio.
    """
    out, body, title = [], [], 'untitled'
    for row in rows:
        text = row.strip()
        if re.match(r'^=\s+[^=].*?\s+=$', text):
            if body:
                out.append({'article': f'{len(out)}:{title}', 'text': '\n'.join(body)})
            body, title = [], text.strip('= ').strip()
        elif text and not re.match(r'^=+\s.*?\s=+$', text):
            body.append(text)
    if body:
        out.append({'article': f'{len(out)}:{title}', 'text': '\n'.join(body)})
    return out


def windows(docs, context_len, target_len, split):
    width = context_len + target_len
    out = []
    for doc in docs:
        for offset in range(0, len(doc['tokens']) - width + 1, width):
            block = doc['tokens'][offset:offset + width]
            out.append({'id': f"{split}:{doc['article']}:{offset}",
                        'split': split, 'article': doc['article'], 'offset': offset,
                        'context': block[:context_len], 'target': block[context_len:]})
    return out


def labelled(context, target, pad_id, length=None):
    if not context or not target:
        raise ValueError('Contexto y objetivo deben ser no vacíos.')
    ids = list(context) + list(target)
    length = len(ids) if length is None else length
    if length < len(ids):
        raise ValueError('El relleno no puede truncar el objetivo.')
    padding = length - len(ids)
    return (ids + [pad_id] * padding,
            [1] * len(ids) + [0] * padding,
            [-100] * len(context) + list(target) + [-100] * padding)


def mix_targets(human, synthetic, alpha, seed):
    """Reemplaza ejemplos completos; longitud fija implica proporción exacta de tokens."""
    if not human or not 0 <= alpha <= 1:
        raise ValueError('Corpus vacío o proporción inválida.')
    count = len(human) * alpha
    if not math.isclose(count, round(count)):
        raise ValueError('La proporción debe dar un número entero de ejemplos.')
    length = len(human[0]['target'])
    if any(len(x['target']) != length for x in human):
        raise ValueError('Objetivos humanos de longitud desigual.')
    if alpha and (synthetic is None or len(synthetic) != len(human)
                  or any(len(x) != length for x in synthetic)):
        raise ValueError('Objetivos sintéticos incompletos o de longitud desigual.')
    chosen = set(random.Random(seed).sample(range(len(human)), round(count)))
    return [dict(x, context=list(x['context']),
                 target=list(synthetic[i] if i in chosen else x['target']),
                 synthetic=i in chosen) for i, x in enumerate(human)]


WORD_PATTERN = r"\w+(?:['’]\w+)*"


def words(text):
    return re.findall(WORD_PATTERN, text.lower(), flags=re.UNICODE)


def lexical_metrics(texts, limit):
    if not texts or limit < 4:
        raise ValueError('Se requieren textos y al menos cuatro palabras por texto.')
    seqs = [words(t) for t in texts]
    short = sum(len(s) < limit for s in seqs)
    result = {'word_limit': limit, 'n_texts': len(texts), 'short_texts': short,
              'distinct_2': None, 'distinct_3': None, 'repeat_4_mean': None}
    if short:
        return result
    seqs = [s[:limit] for s in seqs]
    for n in (2, 3):
        grams = [tuple(s[i:i+n]) for s in seqs for i in range(len(s)-n+1)]
        result[f'distinct_{n}'] = len(set(grams)) / len(grams)
    repeats = []
    for s in seqs:
        grams = [tuple(s[i:i+4]) for i in range(len(s)-3)]
        repeats.append(1 - len(set(grams)) / len(grams))
    result['repeat_4_mean'] = sum(repeats) / len(repeats)
    return result
