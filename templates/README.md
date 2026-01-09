# Resume Templates

Choose a template style that matches your target company culture.

## Available Templates

| Template        | Best For                 | Style                                   |
| --------------- | ------------------------ | --------------------------------------- |
| `style.tex`     | Default - Tech companies | Modern professional, slate blue accent  |
| `minimal.tex`   | Traditional industries   | Clean, no color, conservative           |
| `creative.tex`  | Startups, design roles   | Bold colors, icons, eye-catching        |
| `executive.tex` | Senior/management roles  | Sophisticated, navy/gold, authoritative |

## Usage

### Option 1: Set in identity.json

```json
{
  "preferences": {
    "template": "creative"
  }
}
```

### Option 2: Specify in job_desc.md frontmatter

```yaml
---
company: Acme Startup
role: Senior Engineer
template: creative
---
```

### Option 3: Build with specific template

```bash
# Using compile script
python scripts/compile_all.py --template creative

# Or copy template manually
cp templates/creative.tex templates/style.tex
```

## Template Previews

### Default (style.tex)

- **Color**: Slate blue (#2E5984)
- **Headers**: Small caps with colored rule
- **Bullets**: Colored bullet points
- **Feel**: Modern, professional, tech-forward

### Minimal (minimal.tex)

- **Color**: Black only
- **Headers**: Bold uppercase with thin rule
- **Bullets**: Simple bullets
- **Feel**: Clean, conservative, timeless

### Creative (creative.tex)

- **Colors**: Indigo, pink, teal accents
- **Headers**: Bold with thick color bar
- **Bullets**: Chevron icons
- **Feel**: Bold, energetic, memorable

### Executive (executive.tex)

- **Colors**: Navy blue, gold accents
- **Headers**: Small caps with gold rule
- **Bullets**: Angle icons
- **Feel**: Distinguished, authoritative, premium

## Customization

Each template defines:

- `\contactline{name}{location}{phone}{email}{linkedin}{github}{portfolio}`
- Section formatting via `titlesec`
- Bullet styling via `enumitem`
- Color scheme via `xcolor`

To create your own template:

1. Copy an existing template
2. Modify colors in `\definecolor`
3. Adjust `\titleformat` for headers
4. Update `\contactline` for header layout
5. Save as `templates/your_style.tex`
