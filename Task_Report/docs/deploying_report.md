# Deploying Report with `MkDocs`

## Objective

The aim of this section is to create a documentation in Markdown and use `MkDocs` to deploy the documentation generated as a static site in reference to the 7th point of the [problem statement](problem_statement.md).

## Format and Tools

The report was written in `Markdown` as required by the problem statement. [Markdown](https://en.wikipedia.org/wiki/Markdown) is a markup language which allows text formatting using the defined syntax. It is extensively used for documentation and can be converted to various other formats, including HTML, which allows many tools to build static sites with markdown documentation.

[`MkDocs`](https://www.mkdocs.org/) was used to build a static site with the report. MkDocs is a static site generator which creates sites with content written in Markdown and the site is configured with a [YAML](https://yaml.org/) (YAML is a human-friendly data serialization standard and has various applications) file.

## Installing `MkDocs`

* Installed `MkDocs` with help from the official [documentation](https://www.mkdocs.org/#installation).
* Installed `Material` theme from the official [documentation](https://squidfunk.github.io/mkdocs-material/).

## Site Configuration

```yaml
site_name: 'Jenkins Pipeline'

pages:
- Introduction: 'index.md'
- Problem Statement: 'problem_statement.md'
- Glossary: 'gloassary.md'
- Setting Up VMs: 'setting_up_vms.md'
- Static Analysis: 'static_analysis.md'
- Comparing SAST Tools: 'comparing_sast_tools.md'
- Setting Up Pipeline: 'setting_up_pipeline.md'
- Configuring Webhook: 'configuring_webhook.md'
- Deploying the Report: 'deploying_report.md'
- Resources: 'resources.md'


theme: 'material'
```

## Deploying Static Site

* The static site was built with `MkDocs` with the following command:

```bash
mkdocs build
```

* Installed Apache following Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04-quickstart#step-1-%E2%80%94-installing-apache) as the server to host the site
* Copied the static site directory (`/site`) to web root
