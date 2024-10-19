import requests
from fastapi import APIRouter

from payrolls.settings import FH_APP_REPORT_URL

router = APIRouter()


def get_personal_reports_list():
    api_url = f"http://{FH_APP_REPORT_URL}/report/personal-workload-report/list"
    personal_reports_list = requests.get(api_url).json()
    if personal_reports_list is None:
        raise Exception("Personal reports list not found")
    return personal_reports_list
