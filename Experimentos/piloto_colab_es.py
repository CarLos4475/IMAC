"""Fuente del nuevo notebook en español. No entrena al importar este módulo.

Ejecutar en un entorno preparado: python piloto_colab_es.py
En Colab se recomienda usar piloto_model_collapse_es.ipynb, que incluye instalación.
"""
from controles import *
from controles_es import normalized_text, article_partition, spanish_candidates, select_spanish_rows, words, lexical_metrics

# %% Imports y configuración
import csv
import importlib.metadata
import os
import platform
import shutil
import sys
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

# No se necesitan tokens para estos repositorios públicos.
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from datasets import load_dataset
from huggingface_hub import HfApi
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, GPT2Config, GPT2LMHeadModel
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Config:
    language: str = 'es'
    model: str = 'datificate/gpt2-small-spanish'
    dataset: str = 'wikimedia/wikipedia'
    subset: str = '20231101.es'
    embedding: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    article_pool: int = 2000
    seed: int = 20261109
    train_examples: int = 64
    eval_examples: int = 32
    context_tokens: int = 64
    target_tokens: int = 128
    cycles: int = 2
    alphas: tuple = (0.0, 1.0)
    micro_batch: int = 2
    effective_batch: int = 8
    sample_batch: int = 8
    learning_rate: float = 2e-5
    betas: tuple = (0.9, 0.999)
    epsilon: float = 1e-8
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    temperature: float = 1.0
    top_p: float = 0.95
    max_words: int = 32
    embedding_max_tokens: int = 128
    allow_cpu: bool = False
    save_checkpoints: bool = False


CFG = Config()


def validate_config(cfg):
    if cfg.language != 'es' or cfg.subset != '20231101.es':
        raise ValueError('Este piloto debe trabajar con el corpus en español.')
    if (cfg.train_examples != 64 or cfg.eval_examples != 32 or cfg.cycles != 2
            or tuple(cfg.alphas) != (0.0, 1.0)):
        raise ValueError('Este notebook está acotado al piloto; no activar el estudio final aquí.')
    if cfg.train_examples % cfg.effective_batch or cfg.effective_batch % cfg.micro_batch:
        raise ValueError('Los lotes deben dividir el corpus y el lote efectivo exactamente.')
    if not 0 < cfg.top_p <= 1 or cfg.temperature <= 0:
        raise ValueError('Parámetros de muestreo inválidos.')


def seed_training(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def weight_hash(model):
    digest = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        digest.update(name.encode())
        digest.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def cpu_state(model):
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def reset_for_fit(model, base_state, expected_hash, cfg, seed):
    model.load_state_dict(base_state, strict=True)
    model.zero_grad(set_to_none=True)
    observed_hash = weight_hash(model)
    if observed_hash != expected_hash:
        raise RuntimeError('La inicialización no coincide con el modelo base.')
    seed_training(seed)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg.learning_rate, betas=cfg.betas,
        eps=cfg.epsilon, weight_decay=cfg.weight_decay, foreach=False)
    if len(optimizer.state):
        raise RuntimeError('El optimizador no empieza vacío.')
    return optimizer, observed_hash


def batch_tensors(rows, pad_id, device):
    packed = [labelled(x['context'], x['target'], pad_id) for x in rows]
    return {name: torch.tensor([x[i] for x in packed], dtype=torch.long, device=device)
            for i, name in enumerate(('input_ids', 'attention_mask', 'labels'))}


def fit_one(model, base_state, base_hash, rows, cfg, seed, device, pad_id):
    optimizer, initial_hash = reset_for_fit(model, base_state, base_hash, cfg, seed)
    generator = torch.Generator().manual_seed(stable_seed(seed, 'shuffle'))
    loader = DataLoader(rows, batch_size=cfg.micro_batch, shuffle=True,
                        generator=generator, collate_fn=list, num_workers=0)
    accumulation = cfg.effective_batch // cfg.micro_batch
    model.train()
    losses, updates, seen = [], 0, 0
    for step, batch in enumerate(loader, start=1):
        data = batch_tensors(batch, pad_id, device)
        labels = data['labels']
        assert (labels[:, :cfg.context_tokens] == -100).all().item()
        assert (labels[:, cfg.context_tokens:] != -100).sum().item() == len(batch) * cfg.target_tokens
        output = model(**data, use_cache=False)
        if not torch.isfinite(output.loss).item():
            raise RuntimeError('Pérdida no finita; no se cambian parámetros automáticamente.')
        losses.append(float(output.loss.detach().cpu()))
        (output.loss / accumulation).backward()
        seen += len(batch) * cfg.target_tokens
        if step % accumulation == 0:
            norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.max_grad_norm)
            if not torch.isfinite(norm).item():
                raise RuntimeError('Gradiente no finito.')
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            updates += 1
    assert updates == len(rows) // cfg.effective_batch
    assert seen == len(rows) * cfg.target_tokens
    del optimizer
    model.eval()
    return {'initial_weight_sha256': initial_hash, 'train_seed': seed,
            'optimizer_initial_entries': 0, 'updates': updates,
            'target_tokens_seen': seen, 'train_loss_mean': sum(losses)/len(losses),
            'final_weight_sha256': weight_hash(model)}

# %% Muestreo y controles con un modelo diminuto
def nucleus_draw(logits, generators, cfg, forbidden_ids):
    logits = logits.float().clone() / cfg.temperature
    logits[:, forbidden_ids] = -float('inf')
    values, indices = torch.sort(logits, descending=True, dim=-1)
    probs = torch.softmax(values, dim=-1)
    remove = (torch.cumsum(probs, dim=-1) - probs) >= cfg.top_p
    values[remove] = -float('inf')
    probs = torch.softmax(values, dim=-1)
    draws = [torch.multinomial(p, 1, generator=g) for p, g in zip(probs, generators)]
    return indices.gather(1, torch.stack(draws))


@torch.inference_mode()
def sample_targets(model, rows, cfg, device, forbidden_ids, namespace, progress=True):
    """Un RNG por solicitud; no se hereda el RNG de entrenamiento.

    Política piloto: longitud fija y ningún token especial (incluye EOS/PAD/BOS).
    Se conserva el token que cruza el umbral top-p. Sin top-k ni penalizaciones.
    """
    model.eval()
    targets, seeds = [], []
    for start in range(0, len(rows), cfg.sample_batch):
        batch = rows[start:start+cfg.sample_batch]
        batch_seeds = [stable_seed(cfg.seed, 'sampling', namespace, x['id']) for x in batch]
        generators = [torch.Generator(device=device).manual_seed(s) for s in batch_seeds]
        ids = torch.tensor([x['context'] for x in batch], dtype=torch.long, device=device)
        generated, cache = [], None
        attention = torch.ones_like(ids)
        for _ in range(cfg.target_tokens):
            output = model(input_ids=ids, attention_mask=attention,
                           past_key_values=cache, use_cache=True)
            ids = nucleus_draw(output.logits[:, -1, :], generators, cfg, forbidden_ids)
            generated.append(ids)
            cache = output.past_key_values
            attention = torch.cat([attention, torch.ones_like(ids)], dim=1)
        result = torch.cat(generated, dim=1).cpu().tolist()
        assert all(len(x) == cfg.target_tokens for x in result)
        assert all(not (set(x) & set(forbidden_ids)) for x in result)
        targets.extend(result)
        seeds.extend(batch_seeds)
        if progress:
            print(f'  Muestreo {min(start+cfg.sample_batch, len(rows))}/{len(rows)}', flush=True)
    return targets, seeds


def torch_smoke_checks():
    """Sin descargas: GPT-2 diminuto; pérdida causal, caché, semillas y reinicio."""
    from dataclasses import replace
    seed_training(17)
    toy = GPT2LMHeadModel(GPT2Config(vocab_size=32, n_embd=16, n_inner=32,
        n_layer=1, n_head=2, n_positions=32,
        resid_pdrop=0.0, embd_pdrop=0.0, attn_pdrop=0.0,
        pad_token_id=1, bos_token_id=2, eos_token_id=2)).cpu()
    config = replace(CFG, context_tokens=2, target_tokens=4,
                     micro_batch=1, effective_batch=2, sample_batch=2)
    rows = [{'id': str(i), 'context': [4, 5], 'target': [6, 7, 8, 9]} for i in range(2)]
    data = batch_tensors(rows, 1, 'cpu')
    toy.eval()
    output = toy(**data, use_cache=False)
    manual = F.cross_entropy(output.logits[:, :-1, :].reshape(-1, 32),
                             data['labels'][:, 1:].reshape(-1), ignore_index=-100)
    assert torch.allclose(output.loss, manual, atol=1e-6)
    assert data['labels'][:, 1:].ne(-100).sum().item() == 8
    a, _ = sample_targets(toy, rows, config, 'cpu', [0, 1, 2, 3], 'check', False)
    torch.rand(123)  # Perturbar RNG global no debe cambiar la generación.
    b, _ = sample_targets(toy, rows, config, 'cpu', [0, 1, 2, 3], 'check', False)
    assert a == b
    base, signature = cpu_state(toy), weight_hash(toy)
    fit_one(toy, base, signature, rows, config, 99, 'cpu', 1)
    assert weight_hash(toy) != signature
    optimizer, observed = reset_for_fit(toy, base, signature, config, 99)
    assert observed == signature and len(optimizer.state) == 0
    # El relleno debe estar excluido también después del desplazamiento causal.
    ids, mask, labels = labelled([4, 5], [6, 7], 1, 7)
    padded = {k: torch.tensor([v]) for k, v in
              zip(('input_ids', 'attention_mask', 'labels'), (ids, mask, labels))}
    toy.eval()
    output = toy(**padded, use_cache=False)
    loss = F.cross_entropy(output.logits[:, :-1].reshape(-1, 32),
                           padded['labels'][:, 1:].reshape(-1), ignore_index=-100)
    assert torch.allclose(output.loss, loss, atol=1e-6)
    del optimizer, toy
    print('Controles PyTorch: pérdida causal, relleno, muestreo y reinicio correctos.')

# %% Archivos, tiempos y corpus
def write_json(path, obj):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temp.replace(path)


def write_jsonl(path, rows):
    with Path(path).open('w', encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n')


def hash_json(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


class Clock:
    def __init__(self, path, device):
        self.path, self.device, self.records = path, device, []

    @contextmanager
    def measure(self, stage, **tags):
        if self.device == 'cuda':
            torch.cuda.synchronize()
        start = time.perf_counter()
        status = 'error'
        try:
            yield
            status = 'ok'
        finally:
            if self.device == 'cuda':
                torch.cuda.synchronize()
            self.records.append(dict(stage=stage, seconds=time.perf_counter()-start,
                                     status=status, **tags))
            write_json(self.path, self.records)


def select_data(cfg, tokenizer, revision):
    # El repositorio solo tiene train: nuestras particiones se definen por artículo.
    # Streaming evita descargar toda la Wikipedia; puede transferir buffers adicionales.
    raw = load_dataset(cfg.dataset, cfg.subset, split='train', revision=revision,
                       streaming=True, token=False)
    def tokenize(text):
        return tokenizer(text, add_special_tokens=False, truncation=False,
                         verbose=False)['input_ids']
    pools, audit = spanish_candidates(raw, tokenize, cfg.context_tokens, cfg.target_tokens,
                                      cfg.seed, cfg.article_pool)
    print('Artículos examinados:', audit['scanned_articles'],
          '| Candidatos:', {k: len(v) for k, v in pools.items()}, flush=True)
    selected = select_spanish_rows(pools, cfg.train_examples, cfg.eval_examples, cfg.seed)
    fingerprints = {'selection': audit, 'official_split': 'train',
        'partition_policy': 'SHA256(seed:article_split:id) mod100; train<80, validation<90, test>=90',
        'sampling_scope': f'Prefijo de hasta {cfg.article_pool} artículos; una ventana por artículo',
        'test_tokenized_or_evaluated': False,
        'normalization': 'NFC y saltos de línea; se conservan tildes y ñ',
        'provenance': 'Referencia Wikipedia; no se acredita autoría humana individual'}
    for split, chosen in selected.items():
        fingerprints[split] = {'available_articles': len(pools[split]),
                              'selected_sha256': hash_json(chosen)}
    # Comprobar también igualdad exacta de las ventanas seleccionadas entre particiones.
    train_blocks = {tuple(x['context'] + x['target']) for x in selected['train']}
    if any(tuple(x['context'] + x['target']) in train_blocks for x in selected['validation']):
        raise RuntimeError('Hay bloques idénticos seleccionados entre train y validation; revisar corpus.')
    return selected, fingerprints

# %% Métricas de evaluación
@torch.inference_mode()
def human_perplexity(model, rows, cfg, device, pad_id):
    model.eval()
    nll, count = 0.0, 0
    for start in range(0, len(rows), cfg.micro_batch):
        batch = batch_tensors(rows[start:start+cfg.micro_batch], pad_id, device)
        output = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'], use_cache=False)
        labels = batch['labels'][:, 1:].contiguous()
        loss = F.cross_entropy(output.logits[:, :-1, :].float().reshape(-1, output.logits.size(-1)),
                               labels.reshape(-1), reduction='sum', ignore_index=-100)
        nll += float(loss.cpu())
        count += int(labels.ne(-100).sum().item())
    assert count == len(rows) * cfg.target_tokens
    mean = nll / count
    if not math.isfinite(mean) or mean > 700:
        raise RuntimeError('Perplejidad no finita o fuera de rango.')
    return {'human_nll': mean, 'human_perplexity': math.exp(mean), 'ppl_target_tokens': count}


@torch.inference_mode()
def semantic_dispersion(texts, encoder, encoder_tokenizer, cfg, limit):
    # Mismas primeras W palabras que en diversidad léxica; sin descartar textos cortos.
    if any(len(words(t)) < limit for t in texts):
        return {'semantic_dispersion': None, 'embedding_truncated_texts': None}
    embeddings, truncated = [], 0
    encoder.eval()
    for start in range(0, len(texts), 16):
        batch = [' '.join(words(t)[:limit]) for t in texts[start:start+16]]
        lengths = [len(x) for x in encoder_tokenizer(batch, truncation=False)['input_ids']]
        truncated += sum(n > cfg.embedding_max_tokens for n in lengths)
        inputs = encoder_tokenizer(batch, padding=True, truncation=True,
                                   max_length=cfg.embedding_max_tokens, return_tensors='pt')
        output = encoder(**inputs).last_hidden_state
        mask = inputs['attention_mask'].unsqueeze(-1).to(output.dtype)
        pooled = (output * mask).sum(1) / mask.sum(1).clamp_min(1)
        embeddings.append(F.normalize(pooled, p=2, dim=1))
    matrix = torch.cat(embeddings)
    similarity = matrix @ matrix.T
    upper = torch.triu_indices(len(texts), len(texts), offset=1)
    dispersion = 1 - similarity[upper[0], upper[1]].mean().item()
    return {'semantic_dispersion': dispersion, 'embedding_truncated_texts': truncated}


def evaluate_stage(model, valid, tokenizer, encoder, enc_tokenizer, cfg,
                   device, forbidden, limit, folder, clock):
    with clock.measure('eval_generation', stage_id=folder.name):
        generated, seeds = sample_targets(model, valid, cfg, device, forbidden, 'validation_paired')
    texts = tokenizer.batch_decode(generated, skip_special_tokens=True)
    with clock.measure('eval_perplexity', stage_id=folder.name):
        metrics = human_perplexity(model, valid, cfg, device, tokenizer.pad_token_id)
    metrics.update(lexical_metrics(texts, limit))
    with clock.measure('eval_embeddings', stage_id=folder.name):
        metrics.update(semantic_dispersion(texts, encoder, enc_tokenizer, cfg, limit))
    with clock.measure('write_outputs', stage_id=folder.name):
        write_jsonl(folder/'validation_generations.jsonl', [
            {'id': row['id'], 'seed': seed, 'target_ids': ids, 'text': text}
            for row, seed, ids, text in zip(valid, seeds, generated, texts)])
        write_json(folder/'metrics.json', metrics)
    return metrics

# %% Ejecución del piloto
def run_pilot(cfg=CFG):
    validate_config(cfg)
    if sys.version_info < (3, 11):
        raise RuntimeError('Se requiere Python 3.11 o posterior.')
    major_minor = tuple(int(n) for n in torch.__version__.split('+')[0].split('.')[:2])
    if major_minor < (2, 6):
        raise RuntimeError('Se requiere PyTorch >=2.6. Usar un runtime reciente de Colab.')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('PyTorch:', torch.__version__, '| Dispositivo:', device, flush=True)
    if device == 'cpu' and not cfg.allow_cpu:
        raise RuntimeError('No hay GPU CUDA. Elegir GPU en Colab y ejecutar desde el principio. '
                           'Para CPU deliberada, cambiar allow_cpu=True; no se promete duración.')
    torch.use_deterministic_algorithms(True)
    if device == 'cuda':
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        torch.backends.cudnn.benchmark = False
        print('GPU:', torch.cuda.get_device_name(0), flush=True)
    torch_smoke_checks()
    root = Path('/content/imac_piloto_es') if Path('/content').is_dir() else Path.cwd()/'salidas_piloto_es'
    run = root/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid.uuid4().hex[:8])
    run.mkdir(parents=True, exist_ok=False)
    clock = Clock(run/'timings.json', device)
    # Solo nombres/versiones; no pip freeze con posibles URLs privadas o credenciales.
    versions = dict(sorted((dist.metadata['Name'], dist.version)
                           for dist in importlib.metadata.distributions()
                           if dist.metadata.get('Name')))
    manifest = {'status': 'running', 'kind': 'spanish_pilot_not_final_results', 'config': asdict(cfg),
                'python': platform.python_version(), 'versions': versions, 'device': device,
                'started_utc': datetime.now(timezone.utc).isoformat(), 'test_used': False,
                'gpu': torch.cuda.get_device_name(0) if device == 'cuda' else None,
                'gpu_bytes': torch.cuda.get_device_properties(0).total_memory if device == 'cuda' else None,
                'eos_policy': '128 tokens; todos los IDs especiales excluidos; sin rechazo ni filtrado',
                'seed_policy': 'SHA256; entrenamiento separado; evaluación pareada entre etapas',
                'optimizer': 'AdamW; una época; sin scheduler; decay uniforme en parámetros',
                'precision': 'float32; sin AMP ni TF32; determinismo estricto en este entorno',
                'checkpoints_saved': cfg.save_checkpoints,
                'resume_policy': 'no reanudación automática; cada ejecución crea otra carpeta'}
    write_json(run/'manifest.json', manifest)
    print('Directorio de salida:', run, flush=True)
    try:
        api = HfApi(token=False)
        with clock.measure('resolve_revisions'):
            model_info = api.model_info(cfg.model)
            dataset_info = api.dataset_info(cfg.dataset)
            embed_info = api.model_info(cfg.embedding)
            revisions = {'model': model_info.sha, 'dataset': dataset_info.sha, 'embedding': embed_info.sha}
            safe_model = any(x.rfilename.endswith('.safetensors') for x in model_info.siblings)
        manifest.update(revisions=revisions, model_uses_safetensors=safe_model)
        write_json(run/'manifest.json', manifest)
        with clock.measure('load_tokenizer_data'):
            tokenizer = AutoTokenizer.from_pretrained(cfg.model, revision=revisions['model'],
                                                      trust_remote_code=False, token=False)
            if tokenizer.pad_token_id is None:
                if tokenizer.eos_token_id is None:
                    raise RuntimeError('El tokenizador no define PAD ni EOS para usar como relleno.')
                tokenizer.pad_token = tokenizer.eos_token  # No añade vocabulario ni pesos nuevos.
            selected, fingerprints = select_data(cfg, tokenizer, revisions['dataset'])
            human, valid = selected['train'], selected['validation']
            references = tokenizer.batch_decode([r['target'] for r in valid], skip_special_tokens=True)
            limit = min(cfg.max_words, min(len(words(t)) for t in references))
            if limit < 4:
                raise RuntimeError('La referencia no permite un límite léxico común >=4; revisar antes de continuar.')
            manifest.update(data=fingerprints, word_limit=limit, word_regex=WORD_PATTERN,
                            forbidden_generation_ids=tokenizer.all_special_ids)
            write_json(run/'manifest.json', manifest)
            write_jsonl(run/'train_human.jsonl', human)
            write_jsonl(run/'validation_human.jsonl', valid)
        with clock.measure('load_model'):
            model = AutoModelForCausalLM.from_pretrained(cfg.model, revision=revisions['model'],
                trust_remote_code=False, token=False, use_safetensors=safe_model,
                weights_only=True, dtype=torch.float32, attn_implementation='eager').to(device)
            model.config.pad_token_id = tokenizer.pad_token_id
            if max(tokenizer.all_special_ids) >= model.get_input_embeddings().num_embeddings:
                raise RuntimeError('Los tokens especiales no corresponden al vocabulario del modelo.')
            if not all(p.requires_grad for p in model.parameters()):
                raise RuntimeError('No están habilitados todos los parámetros.')
            base = cpu_state(model)
            base_hash = weight_hash(model)
            manifest['base_weight_sha256'] = base_hash
            manifest['parameters'] = sum(p.numel() for p in model.parameters())
            write_json(run/'manifest.json', manifest)
        with clock.measure('load_embeddings'):
            enc_tokenizer = AutoTokenizer.from_pretrained(cfg.embedding, revision=revisions['embedding'],
                                                          trust_remote_code=False, token=False)
            encoder = AutoModel.from_pretrained(cfg.embedding, revision=revisions['embedding'],
                trust_remote_code=False, token=False, use_safetensors=True,
                dtype=torch.float32).cpu().eval()
        with clock.measure('reference_embeddings'):
            reference_metrics = lexical_metrics(references, limit)
            reference_metrics.update(semantic_dispersion(references, encoder, enc_tokenizer, cfg, limit))
        write_json(run/'human_reference_metrics.json', reference_metrics)
        results = []

        def stage(name, rows, cycle, alpha):
            folder = run/name
            folder.mkdir(exist_ok=False)
            write_jsonl(folder/'training_corpus.jsonl', rows)
            # Misma semilla de ajuste para ambas proporciones en el mismo ciclo.
            seed = stable_seed(cfg.seed, 'fit', 'replicate_0', cycle)
            with clock.measure('fit', stage_id=name):
                fit_record = fit_one(model, base, base_hash, rows, cfg, seed, device, tokenizer.pad_token_id)
            write_json(folder/'fit.json', fit_record)
            if cfg.save_checkpoints:
                with clock.measure('save_checkpoint', stage_id=name):
                    model.save_pretrained(folder/'checkpoint', safe_serialization=True)
                    tokenizer.save_pretrained(folder/'checkpoint')
            metrics = evaluate_stage(model, valid, tokenizer, encoder, enc_tokenizer, cfg,
                device, tokenizer.all_special_ids, limit, folder, clock)
            results.append(dict(stage=name, cycle=cycle, alpha=alpha, **metrics))
            write_json(run/'results.json', results)
            with (run/'results.csv').open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(results[0]))
                writer.writeheader()
                writer.writerows(results)
            print(f'{name}: PPL={metrics["human_perplexity"]:.3f}; '
                  f'Distinct-2={metrics["distinct_2"]}; cortos={metrics["short_texts"]}', flush=True)

        stage('M0_human', human, 0, None)
        initial = cpu_state(model)
        for alpha in cfg.alphas:
            model.load_state_dict(initial, strict=True)
            for cycle in range(1, cfg.cycles+1):
                name = f'alpha_{int(alpha*100):03d}_g{cycle}'
                synthetic, sample_seeds = None, []
                if alpha:
                    with clock.measure('train_generation', stage_id=name):
                        synthetic, sample_seeds = sample_targets(model, human, cfg, device,
                            tokenizer.all_special_ids, f'train_alpha_{alpha}_cycle_{cycle}')
                    write_jsonl(run/f'{name}_synthetic.jsonl', [
                        {'id': x['id'], 'seed': s, 'target_ids': ids}
                        for x, s, ids in zip(human, sample_seeds, synthetic)])
                mixture_seed = stable_seed(cfg.seed, 'mixture', alpha, cycle)
                rows = mix_targets(human, synthetic, alpha, mixture_seed)
                assert sum(x['synthetic'] for x in rows) * cfg.target_tokens == int(alpha * len(rows) * cfg.target_tokens)
                stage(name, rows, cycle, alpha)
        assert len(results) == 5
        manifest.update(status='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                        fit_count=len(results), test_used=False)
        write_json(run/'manifest.json', manifest)
        print('Piloto terminado. Son controles de viabilidad, no resultados del estudio final.', flush=True)
        return run, results
    except Exception as error:
        # No volcar variables de entorno, credenciales ni encabezados de red.
        manifest.update(status='interrupted_or_failed', error_type=type(error).__name__)
        write_json(run/'manifest.json', manifest)
        print('Ejecución detenida; se conservan archivos parciales en', run, flush=True)
        raise

# %% Gráficas y paquete de salida
def summarize_pilot(run, results):
    columns = ['distinct_2', 'distinct_3', 'repeat_4_mean', 'semantic_dispersion', 'human_perplexity']
    fig, axes = plt.subplots(1, len(columns), figsize=(19, 3.6))
    for ax, metric in zip(axes, columns):
        for alpha in CFG.alphas:
            points = [results[0]] + [r for r in results[1:] if r['alpha'] == alpha]
            ys = [r[metric] if r[metric] is not None else float('nan') for r in points]
            ax.plot([r['cycle'] for r in points], ys, marker='o', label=f'{alpha:.0%}')
        ax.set_title(metric)
        ax.set_xlabel('Ciclo')
        ax.set_xticks([0, 1, 2])
        ax.grid(alpha=.3)
    axes[0].legend(title='Objetivos sintéticos')
    fig.suptitle('Piloto: una cadena por condición; sin inferencia estadística')
    fig.tight_layout()
    fig.savefig(run/'pilot_metrics.png', dpi=160, bbox_inches='tight')
    plt.show()
    times = json.loads((run/'timings.json').read_text(encoding='utf-8'))
    print('\nTiempos observados (segundos):')
    totals = Counter()
    for record in times:
        totals[record['stage']] += record['seconds']
    for name, seconds in totals.items():
        print(f'  {name}: {seconds:.1f}')
    print('No extrapolar solo desde ajuste: incluir generación, evaluación, carga y guardado.')
    print('Revisar los tiempos antes de decidir la escala final de 48 ajustes.')
    archive = shutil.make_archive(str(run)+'_resultados', 'zip', root_dir=run)
    print('Paquete:', archive)
    return archive


if __name__ == '__main__':
    RUN_DIR, RESULTS = run_pilot(CFG)
    ARCHIVE = summarize_pilot(RUN_DIR, RESULTS)
