"""Selección de artículos del corpus español; sin librerías externas."""
import hashlib
import random
import unicodedata
from controles import stable_seed, words as base_words, lexical_metrics as base_lexical_metrics


def normalized_text(text):
    return unicodedata.normalize('NFC', text.replace('\r\n', '\n').replace('\r', '\n')).strip()


def words(text):
    return base_words(normalized_text(text))


def lexical_metrics(texts, limit):
    return base_lexical_metrics([normalized_text(t) for t in texts], limit)


def article_partition(article_id, seed):
    digest = hashlib.sha256(f'{seed}:article_split:{article_id}'.encode()).digest()
    bucket = int.from_bytes(digest[:8], 'big') % 100
    return 'train' if bucket < 80 else 'validation' if bucket < 90 else 'test'


def spanish_candidates(records, tokenize, context_len, target_len, seed, max_articles):
    """Prefijo acotado del streaming; una ventana aleatoria por artículo elegible.

    Las particiones son propias (80/10/10 aproximado por hash), no oficiales.
    Los artículos asignados a test no se tokenizan ni se usan para medir.
    El prefijo no es una muestra representativa de toda Wikipedia.
    """
    if context_len <= 0 or target_len <= 0 or max_articles <= 0:
        raise ValueError('Longitudes y límite de artículos deben ser positivos.')
    pools = {'train': [], 'validation': []}
    width = context_len + target_len
    audit = {'scanned_articles': 0, 'reserved_test_articles': 0,
             'too_short_articles': 0, 'duplicate_ids': 0}
    seen = set()
    for row in records:
        if audit['scanned_articles'] >= max_articles:
            break
        audit['scanned_articles'] += 1
        article = str(row['id'])
        if article in seen:
            audit['duplicate_ids'] += 1
            continue
        seen.add(article)
        split = article_partition(article, seed)
        if split == 'test':
            audit['reserved_test_articles'] += 1
            continue
        text = normalized_text(row['text'])
        tokens = tokenize(text)
        count = len(tokens) // width
        if not count:
            audit['too_short_articles'] += 1
            continue
        offset = random.Random(stable_seed(seed, 'window', article)).randrange(count) * width
        block = tokens[offset:offset + width]
        pools[split].append({'id': f'es:{split}:{article}:{offset}', 'split': split,
            'article': article, 'title': row.get('title', ''), 'url': row.get('url', ''),
            'offset': offset, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'context': block[:context_len], 'target': block[context_len:]})
    return pools, audit


def select_spanish_rows(pools, train_count, valid_count, seed):
    selected = {}
    for split, count in (('train', train_count), ('validation', valid_count)):
        if len(pools[split]) < count:
            raise ValueError(f'{split}: solo {len(pools[split])} artículos elegibles; se necesitan {count}. '
                             'Revisar el límite antes de generar o entrenar.')
        selected[split] = random.Random(stable_seed(seed, 'data', split)).sample(pools[split], count)
    train_ids = {r['article'] for r in selected['train']}
    train_text = {r['text_sha256'] for r in selected['train']}
    if any(r['article'] in train_ids or r['text_sha256'] in train_text for r in selected['validation']):
        raise ValueError('Artículo o contenido idéntico entre entrenamiento y validación.')
    for split, rows in selected.items():
        if len({r['text_sha256'] for r in rows}) != len(rows):
            raise ValueError(f'Contenido duplicado en la muestra de {split}; revisar sin reemplazos silenciosos.')
    return selected
