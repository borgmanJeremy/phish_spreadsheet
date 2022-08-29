"""This application will download phish recordings from the spreadsheet"""
import re
from time import sleep
from os import mkdir
from os.path import join, exists
import argparse
import openpyxl
import requests
from tqdm import tqdm


def download(url, output_dir=None):
    """Downloads the file from the url and displays a progress bar"""

    print(f"Downloading {url}")

    response = requests.get(url, stream=True, timeout=5)

    if response.status_code != 200:
        raise RuntimeError("HTML status code not 200")

    content_type = response.headers["content-type"]

    if content_type == "text/html; charset=UTF-8":
        raise RuntimeError("Timeout page returned")

    disposition = response.headers["content-disposition"]
    file_name = re.findall("filename=(.+)", disposition)[0]

    if output_dir is not None:
        if exists(output_dir) is False:
            mkdir(output_dir)
        file_name = join(output_dir, file_name)

    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    with open(file_name, "wb") as fname:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            fname.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        raise RuntimeError("Download incomplete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Phish Recordings from the Spreadsheet"
    )
    parser.add_argument("-f", "--file", help="Path to The Spreadsheet", required=True)
    parser.add_argument(
        "-t", "--tab", help="Name of tab to download (typically a year)", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Output Directory", required=False, default=None
    )

    args = parser.parse_args()

    filename = args.file
    sheet = args.tab

    workbook = openpyxl.load_workbook(filename)
    ws = workbook[sheet]

    for row in ws.rows:
        val = row[7].value
        if val is not None:
            # grab the url from the cell
            link = re.findall('"([^"]*)"', val)
            if len(link) > 0:
                link = link[0]

                if link is not None:
                    # pylint: disable=C0103
                    retry_count = 1
                    downloaded = False

                    while downloaded is False and retry_count <= 5:
                        try:
                            download(link, args.output)
                            downloaded = True
                        except RuntimeError as e:
                            print(e)
                            print(f"Waiting 35 seconds before retry {retry_count} of 5")
                            sleep(35)
                            retry_count += 1
                            if retry_count >5:
                                print("Max retries reached")
