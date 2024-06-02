import re
import requests
from stock_ainalyst import db


def fetch_analysts_comments(symbol: str) -> list[str]:
    symbol = symbol.split(".")[0]

    r = requests.get(f"https://finance.naver.com/research/company_list.naver?searchType=itemCode&itemCode={symbol}")

    comments = []
    for nid in re.findall(f"company_read.naver\?nid=(\d+)&page=1&searchType=itemCode&itemCode={symbol}", r.text)[:5]:
        r = requests.get(f"https://finance.naver.com/research/company_read.naver?nid={nid}&page=1&searchType=itemCode&itemCode={symbol}")
        text = r.text.split('class="view_cnt">')[1].split("</td>")[0].strip()
        text = re.sub("</?[^>]*>", "", text)
        text = re.sub("[\w]+\.pdf", "", text)
        text = re.sub("\s+", " ", text)
        text = text.strip()
        comments.append(text)
    return comments
