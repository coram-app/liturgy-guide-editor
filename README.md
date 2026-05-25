# Liturgy Guide Editor

Editor HTML para o boletim litúrgico da **Igreja Batista Redenção**.

Permite editar visualmente o conteúdo do boletim (cabeçalhos, hinos, leituras
bíblicas, catecismo, sermão, agenda) sem mexer no código. Suporta impressão
tri-fold em A4 paisagem, exportação em HTML/PDF e tema claro/escuro.

## Estrutura

```
.
├── editor.html          # Carcaça do editor (toolbar + área de visualização)
├── boletim.html         # Documento (conteúdo do boletim atual)
├── server.py            # Servidor local (Python) — opcional
├── start.command        # Atalho macOS pra iniciar tudo
├── netlify.toml         # Configuração de deploy estático
└── assets/
    ├── document.css     # Estilos do documento
    ├── editor.css       # Estilos da carcaça (toolbar/popup)
    ├── editor.js        # Lógica de edição
    ├── fonts/           # Collier, Bitter, Inter
    ├── brand/           # Logo + cruz
    └── images/          # QR Code PIX, etc.
```

## Rodando localmente

### Modo simples (file://) — só visualização

Abrir `editor.html` direto não funciona porque o navegador bloqueia `fetch()` em
`file://`. Mas você pode abrir `boletim.html` diretamente pra ver o documento
sem a carcaça do editor.

### Modo completo (com servidor local)

```bash
cd "Liturgy Guide Editor"
python3 server.py
```

Acesse `http://localhost:8765/editor.html`.

Recursos disponíveis com servidor local:
- Auto-save em `.cache/boletim.html` (persiste mesmo fechando o browser)
- "Salvar no Original" (sobrescreve `boletim.html`)

### Atalho macOS

Duplo-clique em `start.command` — inicia o servidor + abre o navegador
automaticamente.

## Deploy (Netlify)

O `netlify.toml` já está configurado pra deploy estático.

Push para o GitHub e conecte ao Netlify, ou faça deploy direto via
[app.netlify.com/drop](https://app.netlify.com/drop).

No modo Netlify (sem backend), o editor cai automaticamente pro `localStorage`
para persistência — cada usuário tem suas próprias edições no browser.

## Funcionalidades

- **Edição visual**: clica em qualquer texto para editar
- **Popup contextual** ao selecionar texto: negrito, itálico, sublinhado,
  listas, refrão, espaçamento, número manual de estrofe
- **Tema claro/escuro** com preferência salva
- **Marcas de dobra** discretas no lado interno (4 ticks pra alinhar dobra)
- **Numeração inteligente** de estrofes (refrão não conta, override manual via `data-num`)
- **Multi-modo de persistência**:
  - localStorage (sempre)
  - Cache em arquivo (`.cache/boletim.html`, quando servidor local rodando)
  - Sobrescrever original (quando servidor rodando)
- **Imprimir / Salvar como PDF** com fontes vetoriais (qualidade tipográfica)
- **Upload de HTML** para carregar um boletim diferente
- **Download** em HTML ou PDF

## Tipografia

- **Collier** — títulos de seção (vinho) e wordmark
- **Bitter** — subtítulos, referências bíblicas (semibold/italic)
- **Inter** — corpo, leitura responsiva, blockquotes
