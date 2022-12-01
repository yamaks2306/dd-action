import json
import os
from datetime import datetime
from requests import Session
import requests
from mode import mode


MODE = os.getenv('MODE')
assert MODE in mode, \
    f'The MODE must be "init" or "upload_report".\nGot MODE: {MODE}'

MAIN_URL = os.getenv('DD_URL')
assert MAIN_URL is not None and MAIN_URL != "", \
    f'The URL must be not empty and not None\nGot URL: {MAIN_URL}'

TOKEN = os.getenv('DD_TOKEN')
assert TOKEN is not None and TOKEN != "", \
    f'The TOKEN must be not empty and not None\nGot TOKEN: {TOKEN}'

BUILD_ID = os.getenv('GITHUB_RUN_ID')
assert BUILD_ID is not None and BUILD_ID != "", \
    f'The BUILD_ID must be not empty and not None\nGot BUILD_ID: {BUILD_ID}'

COMMIT_HASH = os.getenv('GITHUB_SHA')
assert COMMIT_HASH is not None and COMMIT_HASH != "", \
    f'The COMMIT_HASH must be not empty and not None\nGot COMMIT_HASH: {COMMIT_HASH}'

SCAN_TYPE = os.getenv('SCAN_TYPE')

ENGAGEMENT_ID = os.getenv('ENGAGEMENT_ID')

TEST_TITLE = os.getenv('TEST_TITLE')

ACTIVE = os.getenv('ACTIVE')

VERIFIED = os.getenv('VERIFIED')

CLOSE_OLD_FINDINGS = os.getenv('CLOSE_OLD_FINDINGS')

DEDUPLICATION_ON_ENGAGEMENT = os.getenv('DEDUPLICATION_ON_ENGAGEMENT')

FILE = os.getenv('FILE')

PRODUCT_TYPE = os.getenv('PRODUCT_TYPE')

PRODUCT = os.getenv('PRODUCT')

PRODUCT_DESCRIPTION = os.getenv('PRODUCT_DESCRIPTION')

ENGAGEMENT_NAME = os.getenv('GITHUB_WORKFLOW')

ENGAGEMENT_DESCRIPTION = os.getenv('GITHUB_REF_NAME')

SOURCE_CODE_MANAGEMENT_URL = os.getenv('GITHUB_REPOSITORY')

ENGAGEMENT_TYPE = os.getenv('ENGAGEMENT_TYPE')

CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')


def create_session():
    s = Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Authorization": "Token " + TOKEN
    })
    return s


def get_product_type_id(product_type: str, main_url: str, session: Session):

    url = main_url + '/api/v2/product_types/'

    payload = { "name": product_type }

    responce = session.get(url, params=payload)

    if responce.json()['count'] == 0:
        print(f'Product type {product_type} not found and will be created...')
        return create_product_type(product_type, main_url, session)

    return responce.json()['results'][0]['id']


def create_product_type(product_type: str, main_url: str, session: Session):

    url = main_url + '/api/v2/product_types/'

    payload = json.dumps({
        "name": product_type,
        "description": "Some description",
        "critical_product": True,
        "key_product": True
    })

    responce = session.post(url, data=payload)

    return responce.json()['id']


def create_product(product: str, product_description: str, product_type_id: int, main_url: str, session: Session):

    url = main_url + '/api/v2/products/'

    payload = json.dumps({
        "name": product,
        "description": product_description,
        "prod_type": product_type_id
    })

    responce = session.post(url, data=payload)
    return responce.json()['id']


def get_product_id(product: str, product_description: str, product_type_id: int, main_url: str, session: Session):

    url = main_url + '/api/v2/products/'

    payload = { "name": product }

    responce = session.get(url, params=payload)

    if responce.json()['count'] == 0:
        print(f'Product {product} not found and will be created...')
        return create_product(product, product_description, product_type_id, main_url, session)

    return responce.json()['results'][0]['id']


def create_engagement(
    date: str,
    product_id: int,
    engagement_name: str,
    build_id: str,
    commit_hash: str,
    engagement_description: str,
    source_code_management_url: str,
    engagement_type: str,
    main_url: str,
    session: Session
):
    url = main_url + '/api/v2/engagements/'

    payload = json.dumps({
           "target_start": date,
           "target_end": date,
           "product": product_id,
           "name": engagement_name,
           "build_id": build_id,
           "commit_hash": commit_hash,
           "description": engagement_description,
           "source_code_management_uri": source_code_management_url,
           "engagement_type": engagement_type
          })

    responce = session.post(url, data=payload)

    return responce.json()['id']


def upload_scan(
    file: str,
    main_url: str,
    scan_type: str,
    engagement_id: int,
    test_title: str,
    active: bool,
    verified: bool,
    close_old_findings: bool,
    deduplication_on_engagement: bool,
    build_id: str,
    commit_hash: str,
    date: str
):
    url = main_url + '/api/v2/import-scan/'

    payload = {
        'scan_type': scan_type,
        'engagement': engagement_id,
        'test_title': test_title,
        'active': active,
        'verified': verified,
        'close_old_findings': close_old_findings,
        'deduplication_on_engagement': deduplication_on_engagement,
        'build_id': build_id,
        'commit_hash': commit_hash,
        'scan_date': date
    }

    files = [
        ('file', (file, open(file, 'rb')))
    ]

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Token ' + TOKEN
    }

    responce = requests.post(url, headers=headers, data=payload, files=files)

    print(responce.text)


def check_upload_report_environment():
    assert SCAN_TYPE is not None and SCAN_TYPE != "", \
        f'The SCAN_TYPE must be not empty and not None\nGot SCAN_TYPE: {SCAN_TYPE}'
    assert ENGAGEMENT_ID is not None and ENGAGEMENT_ID != "", \
        f'The ENGAGEMENT_ID must be not empty and not None\nGot ENGAGEMENT_ID: {ENGAGEMENT_ID}'
    assert TEST_TITLE is not None and TEST_TITLE != "", \
        f'The TEST_TITLE must be not empty and not None\nGot TEST_TITLE: {TEST_TITLE}'
    assert ACTIVE is not None and ACTIVE != "", \
        f'The ACTIVE must be not empty and not None\nGot ACTIVE: {ACTIVE}'
    assert VERIFIED is not None and VERIFIED != "", \
        f'The VERIFIED must be not empty and not None\nGot VERIFIED: {VERIFIED}'
    assert CLOSE_OLD_FINDINGS is not None and CLOSE_OLD_FINDINGS != "", \
        f'The CLOSE_OLD_FINDINGS must be not empty and not None\nGot CLOSE_OLD_FINDINGS: {CLOSE_OLD_FINDINGS}'
    assert DEDUPLICATION_ON_ENGAGEMENT is not None and DEDUPLICATION_ON_ENGAGEMENT != "", \
        f'The DEDUPLICATION_ON_ENGAGEMENT must be not empty and not None\nGot DEDUPLICATION_ON_ENGAGEMENT: {DEDUPLICATION_ON_ENGAGEMENT}'
    assert FILE is not None and FILE != "", \
        f'The FILE must be not empty and not None\nGot FILE: {FILE}'



def upload_report():
    check_upload_report_environment()

    upload_scan(
        FILE,  # type: ignore
        MAIN_URL,
        SCAN_TYPE,  # type: ignore
        ENGAGEMENT_ID,  # type: ignore
        TEST_TITLE,  # type: ignore
        ACTIVE,  # type: ignore
        VERIFIED, # type: ignore
        CLOSE_OLD_FINDINGS, # type: ignore
        DEDUPLICATION_ON_ENGAGEMENT, # type: ignore
        BUILD_ID,
        COMMIT_HASH,
        CURRENT_DATE
    )


def check_init_environment():
    assert PRODUCT_TYPE is not None and PRODUCT_TYPE != "", \
        f'The PRODUCT_TYPE must be not empty and not None\nGot PRODUCT_TYPE: {PRODUCT_TYPE}'
    assert PRODUCT is not None and PRODUCT != "", \
        f'The PRODUCT must be not empty and not None\nGot PRODUCT: {PRODUCT}'
    assert PRODUCT_DESCRIPTION is not None and PRODUCT_DESCRIPTION != "", \
        f'The PRODUCT must be not empty and not None\nGot PRODUCT_DESCRIPTIO: {PRODUCT_DESCRIPTION}'
    assert ENGAGEMENT_NAME is not None and ENGAGEMENT_NAME != "", \
        f'The ENGAGEMENT_NAME must be not empty and not None\nGot ENGAGEMENT_NAME: {ENGAGEMENT_NAME}'
    assert ENGAGEMENT_DESCRIPTION is not None and ENGAGEMENT_DESCRIPTION != "", \
        f'The ENGAGEMENT_DESCRIPTION must be not empty and not None\nGot ENGAGEMENT_DESCRIPTION: {ENGAGEMENT_DESCRIPTION}'
    assert SOURCE_CODE_MANAGEMENT_URL is not None and SOURCE_CODE_MANAGEMENT_URL != "", \
        f'The SOURCE_CODE_MANAGEMENT_URL must be not empty and not None\nGot SOURCE_CODE_MANAGEMENT_URL: {SOURCE_CODE_MANAGEMENT_URL}'
    assert ENGAGEMENT_TYPE is not None and ENGAGEMENT_TYPE != "", \
        f'The ENGAGEMENT_TYPE must be not empty and not None\nGot ENGAGEMENT_TYPE: {ENGAGEMENT_TYPE}'


def init():
    check_init_environment()
    
    session = create_session()

    product_type_id = get_product_type_id(PRODUCT_TYPE, MAIN_URL, session)  # type: ignore
    product_id = get_product_id(PRODUCT, PRODUCT_DESCRIPTION, product_type_id, MAIN_URL, session)  # type: ignore
    engagement_id = create_engagement(
        CURRENT_DATE,
        product_id,
        ENGAGEMENT_NAME,  # type: ignore
        BUILD_ID,
        COMMIT_HASH,
        ENGAGEMENT_DESCRIPTION,  # type: ignore
        "https://github.com/" + SOURCE_CODE_MANAGEMENT_URL,  # type: ignore
        ENGAGEMENT_TYPE,  # type: ignore
        MAIN_URL,
        session
    )

    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            print(f'PRODUCT_TYPE_ID={product_type_id}', file=f)
            print(f'PRODUCT_ID={product_id}', file=f)
            print(f'ENGAGEMENT_ID={engagement_id}', file=f)
    else:
        print(f'PRODUCT_TYPE_ID={product_type_id}')
        print(f'PRODUCT_ID={product_id}')
        print(f'ENGAGEMENT_ID={engagement_id}')

    session.close()

def main():

    if MODE == mode[0]:
        init()
    if MODE == mode[1]:
        upload_report()


if __name__ == '__main__':
    main()
