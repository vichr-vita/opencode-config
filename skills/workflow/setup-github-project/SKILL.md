---
name: setup-github-project
description: Set up a GitHub repository with dev as the default PR target and main for releases. Use only when the user explicitly invokes this skill or explicitly asks for this setup workflow.
---

# Set up a GitHub project

Run only on explicit user invocation. Do not select this skill automatically while doing ordinary coding, PR work, or deployment.

## Establish the target

Inspect the current repository, its instructions, remotes, worktree, local Git identity, and authenticated GitHub account. Check whether the GitHub repository already exists before creating it. Preserve unrelated work, remote URLs, and existing history. Never force-push or recreate an existing branch to impose this layout.

When the user names a reference project, inspect its README, actual workflows, and GitHub settings. The usual local reference is `~/projects/vikunja-cli`, backed by `vichr-vita/vikunja-cli`. Use its established visibility and conventions when the request explicitly says to follow that project. Otherwise establish repository owner and visibility from the user's instructions; ask if publishing visibility is unclear.

## Branch model

- `dev` is the default branch and target for ordinary contribution PRs.
- `main` is the release branch. Promote accumulated changes through a `dev` to `main` PR.
- Use merge commits for promotions so the two long-lived branches retain shared history. Feature PRs may use the project's preferred merge strategy.
- Keep both branches. Disable automatic head-branch deletion because promotion PRs use `dev` as their head.
- Do not add required human approvals, rulesets, or paid features merely because this skill was invoked. Match the reference project's protection policy unless the user requests something different.

For a new repository, create an initial commit containing only reviewed project files, publish `main` and `dev` from it, set GitHub's default branch to `dev`, and leave the local checkout on `dev` tracking `origin/dev`. This bootstraps the first release when release automation is enabled. For an existing repository, fetch and inspect divergence before changing defaults or creating missing branches.

## CI and release automation

Adapt commands to the project's language and existing build system. Do not transplant a Go workflow into another stack.

CI should run relevant tests, static checks, and a build for PRs targeting `dev` or `main`, and for pushes to `dev`. Validate a container build when the project ships a Dockerfile. Documentation-only jobs may skip expensive checks when path detection is reliable; preserve a useful final check result.

A push to `main` validates the release, chooses a version, builds release artifacts, and publishes a GitHub release. Serialize release runs without canceling an in-flight publication. Fetch full Git history and tags. Use narrowly scoped job permissions: ordinary CI needs contents read; release publication needs contents write; GHCR publication also needs packages write.

[assets/next-release-tag.sh](assets/next-release-tag.sh) is the conventional-commit version selector used by this workflow. Copy it to `scripts/next-release-tag.sh` and preserve executable permissions. It starts at `v0.1.0`, uses breaking changes for major bumps, `feat:` for minor bumps, and patch bumps otherwise. It reuses an existing version tag on the current commit. Do not silently replace an existing project's versioning policy.

For Go CLI or service binaries, the reference archive targets are Linux amd64/arm64, macOS amd64/arm64, and Windows amd64, with `SHA256SUMS`. Use `CGO_ENABLED=0` only if dependencies support it. For a containerized service, publish versioned and `latest` GHCR images for supported architectures, with a source-repository label. Cross-compile in a native build stage when possible. Verify package pull visibility; a public repository alone does not prove an image is publicly pullable.

Check referenced action versions against current upstream tags or the working reference repository. Keep remote mutations separate from pull-request CI; never publish releases or pass publishing credentials to untrusted PR code.

## README badges

Add linked badges immediately below the README title as part of setup:

- CI status, linked to the CI workflow. Scope it to the actual integration-branch run, such as `?branch=dev&event=push`. If CI only runs on PRs, use `?event=pull_request` instead.
- Release workflow status, scoped to `?branch=main&event=push` and linked to that workflow. Label it Release; publishing artifacts does not mean the service was deployed.
- Latest release version, using `https://img.shields.io/github/v/release/OWNER/REPO`, linked to `https://github.com/OWNER/REPO/releases/latest`.

GitHub workflow badge URLs use `https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml/badge.svg`. Substitute the real owner, repository, workflow filenames, branch names, and events. Verify every badge returns an image and every link points to the intended workflow or release.

For an existing repository, carry README changes through a normal feature PR into `dev`, then a merge-commit promotion PR from `dev` into `main` when the user requests both branches. Do not bypass that PR workflow with direct pushes to the long-lived branches. Verify the badges exist on both branches after merging.

## Finish the setup

Document the branch model, promotion method, artifact locations, and versioning rules. Repository release automation does not authorize a production deployment.

Run local checks appropriate to the new workflows. After pushing, inspect the first CI and release runs and fix setup failures. Check the default branch, tracking branches, merge settings, release assets, and image availability when applicable. Report the repository URL, release URL, branch model, and any remaining blocker.

When opening a PR, follow repository instructions for rebasing, title, body, and author signature. Open a real PR rather than a draft when that is the user's convention. Do not invent an exact model identifier if runtime metadata does not expose one.
