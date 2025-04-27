#!/usr/bin/python

from os import makedirs

from tqdm import tqdm
from requests import get
from json import dump

API_BASE = "https://ezamowienia.gov.pl/mp-readmodels/api"


def get_tender(id: str) -> dict:
    req = get(f"{API_BASE}/Search/GetTender", params={"id": id})
    req.raise_for_status()
    return req.json()


def save_attachment(
    tender_id: str,
    attachment_id: str,
    path: str,
    *,
    chunk_size: int = 1024 * 1024 * 5,
    total_size: int | None = None,
):
    req = get(
        f"{API_BASE}/Tender/DownloadDocument/{tender_id}/{attachment_id}", stream=True
    )
    req.raise_for_status()
    with tqdm(
        total=total_size, unit="B", unit_scale=True, desc=path.split("/")[-1]
    ) as progress_bar:
        with open(path, "wb") as f:
            for chunk in req.iter_content(chunk_size):
                progress_bar.update(len(chunk))
                f.write(chunk)


def save_tender(id: str, base_path: str | None):
    tender = get_tender(id)
    if base_path == None:
        base_path = id
    makedirs(f"{base_path}/attachments", exist_ok=True)
    print(f"found: {tender["objectId"]}:{tender["title"]}")
    for n, attachment in enumerate(tender["tenderDocuments"], start=1):
        if attachment["attachment"]["isDeleted"]:
            print(
                f"attachment {n}/{len(tender["tenderDocuments"])} was deleted: {attachment["objectId"]}:{attachment["attachment"]["hash"]}:{attachment["attachment"]["fileName"]} -> {attachment["attachment"]["fileSize"]} bytes"
            )
            continue
        save_attachment(
            id,
            attachment["objectId"],
            f"{base_path}/attachments/{attachment["attachment"]["fileName"]}",
            total_size=attachment["attachment"]["fileSize"]
        )

    with open(f"{base_path}/data.json", "w") as f:
        dump(tender, f, indent=4)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        "ez_dl", description="https://ezamowienia.gov.pl downloader"
    )
    parser.add_argument("id", help="The tender id", type=str)
    parser.add_argument(
        "-o",
        "--output",
        help="Output path. Defaults to ./{tender_id}",
        type=str,
        default=None,
    )

    args = parser.parse_args()
    save_tender(args.id, args.output)
