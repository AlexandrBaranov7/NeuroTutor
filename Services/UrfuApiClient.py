import requests
from typing import Any, Optional, Union
import UI.messages.from_bot_messages as messages
from functools import lru_cache


class Formatter:
    """
    Класс форматирует полученные данные в читаемый вид.
    """

    def __init__(self):
      self.DORMITORY_DEBTS_KEY = "DormitoryDebts"
      self.OPERATIONAL_DEBTS_KEY = "OperationalPaymentBalance"

    def format_brs(self, brs: list[dict[str, Any]]) -> str:
        results = [
            f"{discipline['srd_title']} {round(float(discipline['srd_score']), 2)}"
            for discipline in brs
            if discipline.get('srd_score') not in (None, 0)
        ]
        return messages.header_no_brs_msg if not results else messages.header_brs_msg + "\n\n".join(results)

    def format_debts(self, debts: dict[str, Any]) -> str:
        def format_debt_list(debt_list: list[dict], label: str) -> list[str]:
            if not debt_list:
                return [f"{label}: {messages.header_no_debts_msg}"]
            formatted = [f"{label}:"]
            for debt in debt_list:
                contract = debt.get('Договор', messages.unknown_msg)
                amount = debt.get('Долг', 0)
                formatted.append(messages.debt_line_template_msg.format(contract=contract, amount=amount))
            return formatted

        result = [messages.header_debts_msg]
        result += format_debt_list(debts.get(self.DORMITORY_DEBTS_KEY, []), messages.dormitory_label_msg)
        result += format_debt_list(debts.get(self.OPERATIONAL_DEBTS_KEY, []), messages.operational_label_msg)

        return "\n".join(result)

    def format_eduplan(self, eduplan: list[dict[str, Any]], sem: int) -> str:
        disciplines = [
            discipline['title']
            for discipline in eduplan
            if any(term.get('showInLk') and term.get('number') == sem for term in discipline.get('terms', []))
        ]

        result = messages.your_disciplines_template_msg.format(sem=sem)
        return result + "\n".join(disciplines) if disciplines else result + messages.header_no_discipline_msg
    

class UrfuApiClient:
    """
    Класс, который будет ходить в апи УрФУ и забирать данные
    для передаваемого токена.
    """

    BASE_URL = "https://urfu-study-api-test.my1.urfu.ru"
    PATHS = {
        "brs": "/api/for-minitoken/brs/new-brs",
        "filters": "/api/for-minitoken/brs/new-filters",
        "eduplan": "/api/for-minitoken/student-schedule/eduplan",
        "debts": "/api/for-minitoken/ubu/debts",
        "user_info": "/api/for-minitoken/user-info"
    }

    ERROR_MSG = messages.default_error_msg

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or self.BASE_URL
        self.formatter = Formatter()

    def _get_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    @lru_cache(maxsize=128)
    def _get(self, path: str, token: str, params: Optional[dict] = None) -> Union[dict, str]:
        response = requests.get(
            self.base_url + path,
            headers=self._get_headers(token),
            params=params
        )
        if response.status_code != 200:
            return self.ERROR_MSG
        return response.json()

    def _get_brs_filters(self, token: str) -> Union[dict[str, Any], str]:
        data = self._get(self.PATHS["filters"], token)
        if isinstance(data, str):
            return data
        return data[0]  # предполагается, что это всегда список с одним словарем

    def _build_period_filter(self, filters: dict[str, Any], year: str, semester: str) -> Optional[dict[str, Any]]:
        for period in filters.get("periods", []):
            if period["year"] == year and semester in period["semesters"]:
                return {
                    "studentUid": filters["studentUid"],
                    "groupUid": filters["groupUid"],
                    "year": year,
                    "semester": semester
                }
        return None

    def get_brs(self, token: str, year: str, semester: str) -> Union[list[dict], str]:
        filters = self._get_brs_filters(token)
        if isinstance(filters, str):
            return filters

        period_filter = self._build_period_filter(filters, year, semester)
        if not period_filter:
            return self.ERROR_MSG

        data = self._get(self.PATHS["brs"], token, period_filter)
        if isinstance(data, str):
            return data
        return self.formatter.format_brs(data)

    def get_periods(self, token: str) -> Union[list[dict], str]:
        filters = self._get_brs_filters(token)
        if isinstance(filters, str):
            return filters
        return filters.get("periods", [])

    @lru_cache(maxsize=128)
    def get_raw_eduplan(self, token: str) -> requests.Response:
        return requests.get(self.base_url + self.PATHS["eduplan"], headers=self._get_headers(token))

    def get_semesters(self, token: str) -> Union[list[int], str]:
        response = self.get_raw_eduplan(token)
        if response.status_code != 200:
            return self.ERROR_MSG

        try:
            data = response.json()
            semesters = {
                term["number"]
                for plan in data
                for term in plan.get("terms", [])
                if "number" in term
            }
            return list(semesters)
        except Exception:
            return self.ERROR_MSG

    @lru_cache(maxsize=128)
    def get_eduplan(self, token: str, sem: int) -> Union[list[dict], str]:
        data = self._get(self.PATHS["eduplan"], token)
        if isinstance(data, str):
            return data
        return self.formatter.format_eduplan(data, sem=sem)

    def get_debts(self, token: str) -> Union[list[dict], str]:
        data = self._get(self.PATHS["debts"], token)
        if isinstance(data, str):
            return data
        return self.formatter.format_debts(data)

    def get_user_info(self, token: str) -> dict[str, Any]:
        return requests.get(self.base_url + self.PATHS["user_info"], headers=self._get_headers(token)).json()