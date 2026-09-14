# Impact Works website

A deliberately minimal Hugo website for [impactworks.dev](https://impactworks.dev/). The public page contains only the Impact Works name, vision, and mission.

## Local development

The project uses the same Hugo and GitHub Pages pattern as the NCLT websites. Enter the devenv shell, then preview or build:

```sh
devenv shell
dev
build
check
```

`check` builds the site and verifies that the generated homepage contains exactly the approved visible copy, one heading and one main landmark, with no scripts or remote assets.

## Deployment

Pushes to `main` run `.github/workflows/gh-pages.yaml`, build with Hugo Extended 0.152.2, check the output, and deploy it with GitHub Pages Actions.

The custom domain is `impactworks.dev`.
