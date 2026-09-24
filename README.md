# Portfólio — Ermírio A. Bonfim

Portfólio profissional para posicionamento como Arquiteto de Soluções para Manufatura Inteligente e Transformação Digital.

## Visualização local

Abra `index.html` no navegador ou execute:

```bash
python3 -m http.server 8088
```

## Publicação no GitHub Pages

1. Crie um repositório público, por exemplo `portfolio-manufatura-inteligente`.
2. Envie `index.html`, `styles.css` e o PDF para a raiz.
3. Em **Settings → Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/root`.
4. Antes de publicar, substitua `contato@exemplo.com` pelo contato profissional correto.

## Atualização do PDF

```bash
./build-pdf.sh
```

O PDF é gerado a partir do mesmo conteúdo do site para manter consistência.

## Ilustração MIS-Vision

A seção MIS-Vision usa uma animação conceitual própria, sem imagens de clientes ou de plantas reais:

- `assets/mis-vision-showcase.gif` — sequência animada de detecção, contexto e geração de evento;
- `assets/mis-vision-showcase-poster.png` — quadro final para revisão e fallback;
- `assets/mis-vision-architecture.svg` — fluxo câmera → edge → contexto → evento → decisão.

Para regenerar a animação:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/generate_mis_vision_assets.py
```

A comunicação de EPIs descreve presença/ausência aparente de itens visíveis e exige validação no piloto. Ela não deve ser apresentada como certificação automática de conformidade.
