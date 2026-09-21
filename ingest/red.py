"""Cliente http con user agent propio, timeout, reintentos, limite por host y robots.txt."""

from __future__ import annotations

import logging
import time
import urllib.robotparser
from typing import Any
from urllib.parse import urlsplit

import httpx

log = logging.getLogger("ingesta.red")

CODIGOS_REINTENTO = {408, 425, 429, 500, 502, 503, 504}


class ClienteHttp:
    def __init__(self, user_agent: str, timeout_s: float = 20, reintentos: int = 2,
                 req_por_seg_por_host: float = 1.0, backoff_s: float = 1.0,
                 intervalo_por_host: dict[str, float] | None = None) -> None:
        self.user_agent = user_agent
        self.timeout_s = timeout_s
        self.reintentos = reintentos
        self.intervalo_min = 1.0 / req_por_seg_por_host if req_por_seg_por_host > 0 else 0.0
        self.backoff_s = backoff_s
        self.intervalo_por_host = {h.lower(): float(v) for h, v in (intervalo_por_host or {}).items()}
        self._ultimo_por_host: dict[str, float] = {}
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self._cliente = httpx.Client(
            headers={"User-Agent": user_agent},
            timeout=timeout_s,
            follow_redirects=True,
        )

    def cerrar(self) -> None:
        self._cliente.close()

    def __enter__(self) -> "ClienteHttp":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.cerrar()

    def _esperar_host(self, url: str) -> None:
        host = urlsplit(url).hostname or ""
        ultimo = self._ultimo_por_host.get(host)
        if ultimo is not None:
            faltan = self.intervalo_por_host.get(host, self.intervalo_min) - (time.monotonic() - ultimo)
            if faltan > 0:
                time.sleep(faltan)
        self._ultimo_por_host[host] = time.monotonic()

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Get con reintentos y backoff. Lanza httpx.HTTPError si agota los intentos."""
        ultimo_error: Exception | None = None
        for intento in range(self.reintentos + 1):
            if intento:
                espera = self.backoff_s * (2 ** (intento - 1))
                log.info("reintento %d para %s en %.1fs", intento, url, espera)
                time.sleep(espera)
            self._esperar_host(url)
            try:
                resp = self._cliente.get(url, **kwargs)
            except httpx.HTTPError as e:
                ultimo_error = e
                continue
            if resp.status_code in CODIGOS_REINTENTO:
                ultimo_error = httpx.HTTPStatusError(
                    f"http {resp.status_code}", request=resp.request, response=resp)
                continue
            resp.raise_for_status()
            return resp
        assert ultimo_error is not None
        raise ultimo_error

    def permitido_por_robots(self, url: str) -> bool:
        """Consulta robots.txt del host (cacheado). Si no se puede leer, se asume permitido."""
        partes = urlsplit(url)
        base = f"{partes.scheme}://{partes.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                resp = self.get(f"{base}/robots.txt")
                rp.parse(resp.text.splitlines())
                self._robots[base] = rp
            except httpx.HTTPError as e:
                log.info("robots.txt no disponible en %s (%s)", base, e)
                self._robots[base] = None
        rp = self._robots[base]
        return True if rp is None else rp.can_fetch(self.user_agent, url)
