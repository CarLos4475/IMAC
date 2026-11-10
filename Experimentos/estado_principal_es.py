"""Protocolo y persistencia del estudio principal; solo biblioteca estándar."""
import hashlib
import json
import random
from pathlib import Path
from controles import stable_seed


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_name(path.name+'.pending')
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    pending.replace(path)


def make_plan(repetitions=3, cycles=5, alphas=(0.0, 0.5, 1.0)):
    jobs = []
    for rep in range(repetitions):
        initial = f'r{rep}_M0'
        jobs.append({'id': initial, 'rep': rep, 'cycle': 0, 'alpha': None, 'parent': None})
        for alpha in alphas:
            for cycle in range(1, cycles+1):
                name = f'r{rep}_a{round(alpha*100):03d}_g{cycle}'
                parent = initial if cycle == 1 else f'r{rep}_a{round(alpha*100):03d}_g{cycle-1}'
                jobs.append({'id': name, 'rep': rep, 'cycle': cycle, 'alpha': alpha, 'parent': parent})
    return jobs


def freeze_protocol(root, spec, environment):
    spec = json.loads(json.dumps(spec, ensure_ascii=False, allow_nan=False))
    environment = json.loads(json.dumps(environment, ensure_ascii=False, allow_nan=False))
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    path = root/'protocol.json'
    record = {'spec': spec, 'environment': environment,
              'signature': canonical_hash({'spec': spec, 'environment': environment})}
    if path.exists():
        previous = json.loads(path.read_text(encoding='utf-8'))
        if previous != record:
            raise ValueError('El protocolo o entorno cambió. No mezclar ejecuciones; conservar esta carpeta.')
    else:
        if any(root.iterdir()):
            raise ValueError('Directorio no vacío sin protocolo identificable. Usar otra carpeta.')
        atomic_json(path, record)
    return record['signature']


def commit_stage(folder, signature, artifacts, details):
    folder = Path(folder)
    for name in artifacts:
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Artefacto fuera del directorio de etapa.')
    record = {'signature': signature, 'files': {name: file_hash(folder/name) for name in artifacts},
              'details': details}
    atomic_json(folder/'complete.json', record)


def stage_complete(folder, signature):
    folder = Path(folder)
    marker = folder/'complete.json'
    if not marker.exists():
        return False
    record = json.loads(marker.read_text(encoding='utf-8'))
    if record['signature'] != signature:
        raise ValueError('Marcador de otro protocolo.')
    for name, digest in record['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Ruta de artefacto inválida.')
        path = folder/name
        if not path.is_file() or file_hash(path) != digest:
            raise ValueError(f'Artefacto ausente o modificado: {path}. No se sobrescribe silenciosamente.')
    return True


def final_selection(pools, counts, seed):
    selected, article_ids, contents, windows = {}, set(), set(), set()
    for split, count in zip(('train', 'validation', 'test'), counts):
        if len(pools[split]) < count:
            raise ValueError(f'{split}: faltan artículos elegibles ({len(pools[split])}/{count}).')
        selected[split] = random.Random(stable_seed(seed, 'final_selection', split)).sample(pools[split], count)
        for row in selected[split]:
            block = tuple(row['context']+row['target'])
            if row['article'] in article_ids or row['text_sha256'] in contents or block in windows:
                raise ValueError('Duplicados en la muestra final; no se sustituyen según resultados.')
            article_ids.add(row['article'])
            contents.add(row['text_sha256'])
            windows.add(block)
    return selected


def cached_chunk(path, input_hash):
    path = Path(path)
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding='utf-8'))
    if record['input_hash'] != input_hash or record['output_hash'] != canonical_hash(record['outputs']):
        raise ValueError('Lote guardado incompatible o modificado.')
    return record['outputs']


def save_chunk(path, input_hash, outputs):
    atomic_json(path, {'input_hash': input_hash, 'output_hash': canonical_hash(outputs), 'outputs': outputs})
