# 🗃️ Gentoo Cache Manager

[![CI][ci-badge]][ci]

**Gentoo Cache Manager** aims to help you tweaking build cache settings for individual packages in [Gentoo Linux][gentoo] and some [Gentoo-based][gentoo-based] operating systems.

## 🧑🏽‍🔬 Usage

To enable [ccache][ccache] for `glibc`, run:
```shell
gcm enable glibc
```

To disable it, run:
```shell
gcm disable glibc
```

[ci-badge]: https://img.shields.io/github/actions/workflow/status/Jamim/gentoo-cache-manager/ci.yml.svg
[ci]: https://github.com/Jamim/gentoo-cache-manager/actions/workflows/ci.yml
[gentoo]: https://www.gentoo.org
[gentoo-based]: https://wiki.gentoo.org/wiki/Distributions_based_on_Gentoo
[ccache]: https://wiki.gentoo.org/wiki/Ccache
