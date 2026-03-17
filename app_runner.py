from pathlib import Path
import yaml

from src.sitemap import parse_sitemap
from src.crawl import crawl_all


def run_link_checker():
    # 1) Config laden
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 2) Sitemap parsen
    urls_csv = Path(cfg["data_dir"]) / "urls_initial.csv"

    if cfg.get("mock_mode", True):
        count = parse_sitemap(
            sitemap_url=cfg.get("sitemap_url", ""),
            output_csv=str(urls_csv),
            mock_mode=True,
            mock_path=cfg["mock"]["sitemap_path"],
        )
    else:
        count = parse_sitemap(
            sitemap_url=cfg["sitemap_url"],
            output_csv=str(urls_csv),
            mock_mode=False,
        )

    # 3) URLs laden
    with open(urls_csv, "r", encoding="utf-8") as f:
        next(f)
        all_urls = [line.strip() for line in f if line.strip()]

    # 4) Limit anwenden
    max_n = int(cfg.get("max_urls", 0))
    if max_n > 0:
        url_batch = all_urls[:max_n]
    else:
        url_batch = all_urls

    # 5) Crawl starten
    result = crawl_all(url_batch, cfg)

    # 6) Zusätzliche Infos ergänzen
    result["urls_from_sitemap"] = count
    result["config_output_dir"] = cfg["output_dir"]

    return result