# Deploying Report with `Mkdocs`

## Objective

This section is

The report was written in `Markdown` and `mkdocs` was used to build a static site with the report.

## Installing `mkdocs`

* Installed `mkdocs` with help from the official [documentation](https://www.mkdocs.org/#installation).
* Installed `Material` theme from the official [documentation](https://squidfunk.github.io/mkdocs-material/).

## Site Configuration

```yaml
site_name: 'Jenkins Pipeline'

pages:
- Introduction: 'index.md'
- Problem Statement: 'problem_statement.md'
- Setting Up VMs: 'setting_up_vms.md'
- Static Analysis: 'static_analysis.md'
- Comparing SAST Tools: comparing_sast_tools.md
- Setting Up Pipeline: setting_up_pipeline.md
- Configuring Webhook: configuring_webhook.md
- Deploying Documentation: deploying_report.md
- Resources: resources.md


theme: material
```

## Deploying Static Site

* The static site was built with `mkdocs` with the following command:

```bash
mkdocs build
```

* Installed Apache following Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-18-04-quickstart#step-1-%E2%80%94-installing-apache) as the server to host the site
* Copied the static site directory (`/site`) to web root
