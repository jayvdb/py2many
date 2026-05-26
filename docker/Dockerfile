# syntax=docker/dockerfile:1
#
# .github/workflows/main.yml builds and pushes this image before running tests.
#
# The image intentionally contains the language runtimes and test helpers that
# used to be assembled by GitHub Actions setup actions in main.yml.
FROM alpine:3.20

ARG FOCUS=
ARG V_VERSION=0.5.1
ARG RUST_TOOLCHAIN=nightly-2024-01-01
ARG DART_VERSION=3.4.4
ARG FLUTTER_VERSION=3.22.3
ARG GO_VERSION=1.26.0
ARG JULIA_VERSION=1.10.5
ARG KOTLIN_VERSION=2.0.21
ARG ZIG_VERSION=0.14.0

ENV HOME=/root \
    PATH="/root/.venv/bin:/root/go/bin:/usr/local/go/bin:/root/.cargo/bin:/root/.pub-cache/bin:/opt/v:/opt/flutter/bin:/opt/dart-sdk/bin:/opt/julia/bin:/opt/kotlinc/bin:/opt/zig:${PATH}" \
    CXX=clang++ \
    CXXFLAGS="-fuse-ld=lld" \
    CLANG_FORMAT_STYLE=Google \
    KOTLIN_HOME=/opt/kotlinc \
    PUB_CACHE=/root/.pub-cache \
    VFLAGS="-cc gcc -gc none"

RUN apk add --no-cache \
      astyle \
      bash \
      build-base \
      ca-certificates \
      catch2 \
      clang \
      clang-extra-tools \
      cmake \
      curl \
      dub \
      gc-dev \
      git \
      gcompat \
      libc++ \
      libc++-dev \
      libstdc++ \
      linux-headers \
      lld \
      ldc \
      make \
      maven \
      nim \
      openjdk17-jdk \
      python3 \
      py3-pip \
      py3-virtualenv \
      sudo \
      tar \
      unzip \
      xz \
      z3 \
      z3-dev \
      zip \
      zstd

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN ln -sf /usr/bin/ldmd2 /usr/local/bin/dmd

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    echo "Building py2many CI image for focus: ${FOCUS:-all}"

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install go; then \
      arch="$(apk --print-arch)" \
      && case "${arch}" in \
        x86_64) go_arch="amd64" ;; \
        aarch64) go_arch="arm64" ;; \
        *) echo "Unsupported Go release target: ${arch}" >&2; exit 1 ;; \
      esac \
      && curl -fsSL -o /tmp/go.tar.gz "https://go.dev/dl/go${GO_VERSION}.linux-${go_arch}.tar.gz" \
      && rm -rf /usr/local/go \
      && tar -C /usr/local -xzf /tmp/go.tar.gz \
      && rm /tmp/go.tar.gz \
      && go version; \
    fi

RUN python3 -m venv "${HOME}/.venv" \
    && source "${HOME}/.venv/bin/activate" \
    && pip install --upgrade pip \
    && pip install \
      black==24.10.0 \
      conan \
      cpplint \
      flake8 \
      isort \
      jgo \
      setuptools \
      tox

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install rust; then \
      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
        | sh -s -- -y --default-toolchain "${RUST_TOOLCHAIN}" --component clippy,rustfmt; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install vlang; then \
      curl -fsSL -o /tmp/v.zip "https://github.com/vlang/v/releases/download/${V_VERSION}/v_linux.zip" \
      && unzip -q /tmp/v.zip -d /opt \
      && rm /tmp/v.zip \
      && ln -sf /opt/v/v /usr/local/bin/v \
      && v version; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install julia; then \
      curl -fsSL -o /tmp/julia.tar.gz \
        "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%.*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" \
      && mkdir -p /opt/julia \
      && tar -xzf /tmp/julia.tar.gz -C /opt/julia --strip-components=1 \
      && rm /tmp/julia.tar.gz \
      && ln -sf /usr/lib/libgcc_s.so.1 /opt/julia/lib/julia/libgcc_s.so.1 \
      && julia --version; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install kotlin; then \
      curl -fsSL -o /tmp/kotlin.zip \
        "https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/kotlin-compiler-${KOTLIN_VERSION}.zip" \
      && unzip -q /tmp/kotlin.zip -d /opt \
      && rm /tmp/kotlin.zip \
      && kotlin -version; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install dart; then \
      curl -fsSL -o /tmp/dart.zip \
        "https://storage.googleapis.com/dart-archive/channels/stable/release/${DART_VERSION}/sdk/dartsdk-linux-x64-release.zip" \
      && unzip -q /tmp/dart.zip -d /opt \
      && rm /tmp/dart.zip; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install dart; then \
      curl -fsSL -o /tmp/flutter.tar.xz \
        "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" \
      && tar -xJf /tmp/flutter.tar.xz -C /opt \
      && rm /tmp/flutter.tar.xz \
      && git config --global --add safe.directory /opt/flutter \
      && flutter config --no-analytics \
      && flutter --version; \
    fi

ARG GLIBC_VERSION=2.35-r1
# Glibc-linked libstdc++ and libgcc_s from conda-forge; Alpine's apk versions
# are musl-linked and can't satisfy mojo's manylinux binaries loaded via
# sgerrand's glibc ld.so.
ARG LIBSTDCXX_CONDA=libstdcxx-15.2.0-h934c35e_19.conda
ARG LIBGCC_CONDA=libgcc-15.2.0-he0feb66_19.conda
RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    extract_conda_libs() { \
      curl -fsSL -O "https://conda.anaconda.org/conda-forge/linux-64/$1" \
      && unzip -q "$1" -d "/tmp/conda-ext" \
      && zstd -qd /tmp/conda-ext/pkg-*.tar.zst -o /tmp/conda.tar \
      && tar -xf /tmp/conda.tar -C /usr/glibc-compat --wildcards "$2" \
      && rm -rf "$1" /tmp/conda-ext /tmp/conda.tar; \
    }; \
    if should_install mojo; then \
      curl -fsSL -o /etc/apk/keys/sgerrand.rsa.pub \
        https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
      && curl -fsSL -O \
        "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk" \
      && apk add --no-cache --force-overwrite "glibc-${GLIBC_VERSION}.apk" \
      && rm "glibc-${GLIBC_VERSION}.apk" \
      && extract_conda_libs "${LIBSTDCXX_CONDA}" 'lib/libstdc++.so.6*' \
      && extract_conda_libs "${LIBGCC_CONDA}" 'lib/libgcc_s.so*' \
      && source "${HOME}/.venv/bin/activate" \
      # Alpine's python3 is musl-linked, so pip rejects mojo's manylinux wheels
      # by default. --platform + --target lets us install glibc-tagged wheels
      # into a sibling tree; sgerrand glibc on /lib lets the bundled binaries
      # actually run. A .pth file pulls the tree into the venv's sys.path
      # without shadowing venv-installed packages (e.g. click for black).
      && pip install \
           --platform=manylinux_2_34_x86_64 \
           --python-version=3.12 \
           --only-binary=:all: \
           --target=/opt/mojo \
           mojo==0.26.2.0 \
      && site_packages=$(python3 -c 'import site; print(site.getsitepackages()[0])') \
      && echo "/opt/mojo" > "${site_packages}/mojo-target.pth" \
      && for bin in /opt/mojo/bin/*; do \
           ln -sf "${bin}" "/usr/local/bin/$(basename ${bin})"; \
         done \
      # mojo's `mojo format` hardcodes /bin/mblack (Alpine /bin isn't a
      # symlink to /usr/bin like on Debian, so PATH search doesn't help).
      && ln -sf /opt/mojo/bin/mblack /bin/mblack \
      && mojo --version \
      && echo 'fn main(): pass' > /tmp/check.mojo \
      && mojo format /tmp/check.mojo \
      && rm /tmp/check.mojo; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install julia; then \
      julia -e 'using Pkg; Pkg.add("JuliaFormatter"); Pkg.add("SuperEnum")' \
      && JULIA_FORMATTER_ROOT="$(julia -e 'import JuliaFormatter;print(dirname(dirname(pathof(JuliaFormatter))));')" \
      && ln -sf "${JULIA_FORMATTER_ROOT}/bin/format.jl" /usr/local/bin/format.jl; \
    fi

COPY scripts /scripts

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install cpp; then \
      source "${HOME}/.venv/bin/activate" \
      && mkdir -p /work/tests \
      && cd /work \
      && /scripts/cpp-setup.sh; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install dart; then \
      mkdir -p /work/tests \
      && cd /work \
      && /scripts/dart-setup.sh; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install dlang; then \
      /scripts/dlang-setup.sh; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install go; then \
      mkdir -p /work/tests \
      && cd /work \
      && /scripts/go-setup.sh; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install zig; then \
      arch="$(apk --print-arch)" \
      && curl -fsSL -o /tmp/zig.tar.xz \
        "https://ziglang.org/download/${ZIG_VERSION}/zig-linux-${arch}-${ZIG_VERSION}.tar.xz" \
      && mkdir -p /opt/zig \
      && tar -xJf /tmp/zig.tar.xz -C /opt/zig --strip-components=1 \
      && rm /tmp/zig.tar.xz \
      && zig version \
      && mkdir -p /work/tests \
      && cd /work \
      && /scripts/zig-setup.sh; \
    fi

RUN should_install() { case "${FOCUS}" in ""|all|omni|"${1}") return 0 ;; *) return 1 ;; esac; }; \
    if should_install vlang; then \
      /scripts/v-setup.sh; \
    fi

COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
