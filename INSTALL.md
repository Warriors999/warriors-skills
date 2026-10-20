# Installation

## Skills CLI

The public repository can be installed with Vercel's open Skills CLI:

```bash
npx skills add Warriors999/warriors-skills
```

Select only the skills needed for your workflow. To install one skill globally:

```bash
npx skills add Warriors999/warriors-skills --skill ppt-design-collaboration -g
```

To generate a prompt without installing:

```bash
npx skills use Warriors999/warriors-skills@warriors-work-principles
```

The CLI currently requires Node.js 22.20 or later. Run `npx skills add --help` for the current options and supported agents.

## Manual installation

Copy one or more directories under `skills/` into the skill directory used by your agent. Keep each skill's directory name unchanged and preserve its `SKILL.md` entrypoint. Do not copy credentials or local runtime configuration into a skill directory.

## Dependencies

Some workflows refer to optional capabilities such as a presentation renderer, an image-generation plugin, vision tools, or Photoshop MCP. Those dependencies are intentionally not bundled here. Read the relevant skill before use and verify the capability in your environment.
