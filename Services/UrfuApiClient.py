import requests

class Formatter:
  '''
  Будет форматировать полученные данные для читаемого вида
  '''
  def format_brs(self, brs: dict) -> str:
    '''
    Возвращает многострочную строку с баллами по каждой дисциплине
    за выбранный период. Оценка округляется до 2 знаков после запятой
    '''
    formatted_brs = 'Ваши баллы за выбранный период: \n\n'
    for discipline in brs:
      if discipline.get('srd_score') is None: 
        continue
      score = float(discipline.get('srd_score'))
      if score == 0:
        continue

      formatted_brs += discipline.get('srd_title') + ' ' + \
        str(round(float(discipline.get('srd_score')), 2)) + '\n\n'
    if formatted_brs == 'Ваши баллы за выбранный период: \n\n':
       return 'Отсутствуют баллы за выбранный период'
    return formatted_brs

  def format_debts(self, debts: dict) -> str:
    '''
    Возвращает строку, в которой будут задолженности студента
    '''
    dormitory_debts = debts.get('DormitoryDebts', [])
    operational_debts = debts.get('OperationalPaymentBalance', [])

    dormitory_info = []
    for debt in dormitory_debts:
        contract = debt.get('Договор', 'неизвестен')
        amount = debt.get('Долг', 0)
        dormitory_info.append(f"  договор {contract}, долг {amount} руб")


    operational_info = []
    for debt in operational_debts:
        contract = debt.get('Договор', 'неизвестен')
        amount = debt.get('Долг', 0)
        operational_info.append(f"  Договор {contract}, долг {amount} руб")

    result = ["Ваши долги:\n"]
    if dormitory_info:
        result.append("Общежитие:")
        result.extend(dormitory_info)
    else:
        result.append("Общежитие: нет долгов")

    if operational_info != 0 or not operational_info is None:
        result.append("Операционные платежи:")
        result.extend(operational_info)
    else:
        result.append("Операционные платежи: нет долгов")

    return "\n".join(result)


  def format_eduplan(self, eduplan: dict, sem: int):
    '''
    Возвращает отформатированный учебный план
    '''
    result = f'Ваши дисциплины за {sem}-й семестр: \n\n'

    for discipline in eduplan:
        terms = discipline.get('terms')
        if any([term.get('showInLk') and term.get('number')==sem for term in terms]):
            result += discipline['title'] + '\n'
    return result

class UrfuApiClient:
  """
  Класс, который будет ходить в апи урфу и забирать данные
  для передаваемого токена
  
  Методы:
    get_brs - получить брс
    get_periods - получить фильтры для брс
    get_eduplan - получить учебный план
    get_debts - получить задолженности
  """
  brs_path = '/api/for-minitoken/brs/new-brs'
  brs_filter_path = '/api/for-minitoken/brs/new-filters' 
  eduplan_path = '/api/for-minitoken/student-schedule/eduplan'
  debts_path = '/api/for-minitoken/ubu/debts'
  user_info_path = '/api/for-minitoken/user-info'
  error_msg = 'Произошла ошибка, попробуйте позднее'
  formatter = Formatter()

  def __init__(self, base_url: str="https://urfu-study-api-test.my1.urfu.ru"):
    self.base_url = base_url
  
  def _get_brs_filters(self, token: str) -> list[dict]:
    '''
    Возвращаеn возможные фильтры
    '''
    authorization_header = {"Authorization": f"Bearer {token}"}

    brs_filters = requests.get(self.base_url+self.brs_filter_path,
                                headers=authorization_header)
    if brs_filters.status_code != 200:
       return self.error_msg
    return brs_filters.json()[0]
  
  def _select_period(self, filter, year, semester):
    
    data = filter.copy()

    for period in data.get('periods', []):
        if period['year'] == year and semester in period['semesters']:
            return {
                'studentUid': data['studentUid'],
                'groupUid': data['groupUid'],
                'year': year,
                'semester': semester
            }
  def get_raw_eduplan(self, token):
    authorization_header = {"Authorization": f"Bearer {token}"}
    return requests.get(self.base_url+self.eduplan_path,
                        headers=authorization_header)
    
  def get_periods(self, token):
    '''
    Возвращает список возможных периодов
    '''
    active_filters = self._get_brs_filters(token)
    if isinstance(active_filters, str):
       return active_filters
    return active_filters['periods']

  def get_semesters(self, token):
    '''
    Возвращает список семестров
    '''
    raw_eduplan = self.get_raw_eduplan(token)
    if raw_eduplan.status_code != 200:
       return self.error_msg
    all_sems = list(dict.fromkeys([_.get('number')\
                                   for i in [d.get('terms')\
                                             for d in raw_eduplan.json()] for _ in i]))
    return all_sems

  def get_brs(self, token: str, year:str, semester:str): 
    # Важно что год - строка
    authorization_header = {"Authorization": f"Bearer {token}"}
    active_filters = self._get_brs_filters(token)
    
    filters = self._select_period(
        filter=active_filters,
        year=year,
        semester=semester
    )
    response = requests.get(self.base_url+self.brs_path,
                        headers=authorization_header,
                        params=filters)
    print(response.json())
    if response.status_code != 200:
       return self.error_msg
    return self.formatter.format_brs(response.json())


  def get_debts(self, token: str):
    authorization_header = {"Authorization": f"Bearer {token}"}
    response = requests.get(self.base_url+self.debts_path,
                        headers=authorization_header)
    
    if response.status_code != 200:
       return self.error_msg
    return self.formatter.format_debts(response.json())

  def get_eduplan(self, token: str, sem:int):
    authorization_header = {"Authorization": f"Bearer {token}"}
    response = requests.get(self.base_url+self.eduplan_path,
                        headers=authorization_header)
    if response.status_code != 200:
       return self.error_msg
    return self.formatter.format_eduplan(response.json(), sem=sem)
  
  def get_user_info(self, token:str):
    authorization_header = {"Authorization": f"Bearer {token}"}
    return requests.get(self.base_url+self.user_info_path,
                        headers=authorization_header).json()