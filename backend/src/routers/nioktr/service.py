from datetime import datetime
import requests
import json
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Nioktr, Keyword, KeywordNioktr, Author, Organization, NioktrTypes, BudgetType, \
    NioktrBudget, Subject, NioktrSubject, OrganizationCoexecutor, OrganizationIdentifier
from src.model.storage import create_nioktr, get_or_create_identifier, get_count
from src.routers.nioktr import Nioktr_params
from src.schemas.schemas import SchemeNioktr, SchemeNioktrPage


# Создаём сессию и проставляем стандартные заголовки, что бы не сильно отличаться от браузера

async def service_update_nioktr(db: Session):
    identifier_nioktr = await get_or_create_identifier("Nioktr", db)
    uid = []
    uid.append('9569096')  # ОмГТУ
    # start_date = '2022-11-30'
    # start_date = '2014-06-30'
    # end_date = '2024-01-01'
    start_date = '2022-06-06'
    end_date = '2023-01-01'
    items_in_page = 10

    # URL API, который осуществляет поиск по ИС
    search_url = 'https://rosrid.ru/api/base/search'

    # Формируем заготовку для основного тела поиска
    payload = {
        "search_query": None,
        "critical_technologies": [],
        "dissertations": False,
        "full_text_available": False,
        "ikrbses": False,
        "nioktrs": True,
        "organization": uid,
        "page": 1,
        "priority_directions": [],
        "rids": False,
        "rubrics": [],
        "search_area": "Во всех полях",
        "sort_by": "Дата регистрации",
        "open_license": False,
        "free_licenses": False,
        "expert_estimation_exist": False,
        "start_date": start_date,
        "end_date": end_date
    }
    session = requests.session()
    session.headers.update({
        'authority': 'rosrid.ru',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'origin': 'https://rosrid.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://rosrid.ru/global-search',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7'
    })

    while True:
        try:
            resp = session.request("POST", search_url, verify=False, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
            if resp.status_code == 200:
                json_resp = resp.json()
                page = payload['page']

                total = json_resp['hits']['total']['value']
                count_of_pages = (int(total / items_in_page) + 1) if total % items_in_page else total / items_in_page
                print(f"Downloaded data from page {page} of {count_of_pages}")
                await upload_nioktr(json_resp, identifier_nioktr, db)
                if page >= count_of_pages:
                    break
                payload['page'] += 1

        except BaseException as e:
            await db.rollback()
            print('Retry connection', str(e))
            search_results = await service_update_nioktr(db)

    return 'ok'

async def upload_nioktr(json_resp, identifier_nioktr, db: Session):
    for nioktr in json_resp['hits']['hits']:
        count_nir = 0
        count_types = 0
        count_budget = 0
        if nioktr['_id']:
            nioktr_id_result = await db.execute(select(Nioktr).filter(Nioktr.rosrid_id==nioktr['_id']))
            nioktr_id = nioktr_id_result.scalars().first()
            if nioktr_id is None:
                work_supervisor_name = nioktr['_source']['work_supervisor']['name']
                work_supervisor_patronymic = nioktr['_source']['work_supervisor']['patronymic']
                work_supervisor_surname = nioktr['_source']['work_supervisor']['surname']
                if work_supervisor_name is None:

                    new_work_supervisor_fullname = work_supervisor_surname.split(' ')
                    if len(new_work_supervisor_fullname) >= 3:
                        new_work_supervisor_fullname = new_work_supervisor_fullname[::len(new_work_supervisor_fullname) - 1]
                    new_work_supervisor_name_and_patronymic = new_work_supervisor_fullname[1].split('.')

                    work_supervisor_result = await db.execute(
                        select(Author).filter(and_(Author.name == new_work_supervisor_name_and_patronymic[0],
                                                   Author.surname == new_work_supervisor_fullname[0],
                                                   Author.patronymic == new_work_supervisor_name_and_patronymic[1])))
                    work_supervisor = work_supervisor_result.scalars().first()

                    if work_supervisor is None:
                        work_supervisor = Author(
                            name=new_work_supervisor_name_and_patronymic[0],
                            surname=new_work_supervisor_fullname[0],
                            patronymic=new_work_supervisor_name_and_patronymic[1],
                            confirmed=False
                        )
                        db.add(work_supervisor)
                        await db.commit()

                else:
                    # work_supervisor_surname = nioktr['_source']['work_supervisor']['surname']
                    work_supervisor_result = await db.execute(
                        select(Author).filter(and_(Author.name == work_supervisor_name,
                                                   Author.surname == work_supervisor_surname,
                                                   Author.patronymic == work_supervisor_patronymic)))
                    work_supervisor = work_supervisor_result.scalars().first()

                    if work_supervisor is None:
                        work_supervisor = Author(
                            name=work_supervisor_name,
                            surname=nioktr['_source']['work_supervisor']['surname'],
                            patronymic=work_supervisor_patronymic,
                            confirmed=False
                        )
                        db.add(work_supervisor)
                        await db.commit()




                organization_supervisor_name = nioktr['_source']['organization_supervisor']['name']
                organization_supervisor_patronymic = nioktr['_source']['organization_supervisor']['patronymic']
                organization_supervisor_surname = nioktr['_source']['organization_supervisor']['surname']

                if organization_supervisor_name is None:

                    new_organization_supervisor_fullname = organization_supervisor_surname.split(' ')
                    new_organization_supervisor_name_and_patronymic = new_organization_supervisor_fullname[1].split('.')
                    organization_supervisor_result = await db.execute(
                        select(Author).filter(and_(Author.name == new_organization_supervisor_name_and_patronymic[0],
                                                   Author.surname == new_organization_supervisor_fullname[0],
                                                   Author.patronymic == new_organization_supervisor_name_and_patronymic[1])))

                    organization_supervisor = organization_supervisor_result.scalars().first()

                    if organization_supervisor is None:
                        organization_supervisor = Author(
                            name=new_organization_supervisor_name_and_patronymic[0],
                            surname=new_organization_supervisor_fullname[0],
                            patronymic=new_organization_supervisor_name_and_patronymic[1],
                            confirmed=False
                        )
                        db.add(organization_supervisor)
                        await db.commit()

                else:

                    organization_supervisor_result = await db.execute(
                        select(Author).filter(and_(Author.name == organization_supervisor_name,
                                                   Author.surname == organization_supervisor_surname,
                                                   Author.patronymic == organization_supervisor_patronymic)))
                    organization_supervisor = organization_supervisor_result.scalars().first()

                    if organization_supervisor is None:
                        organization_supervisor = Author(
                            name=organization_supervisor_name,
                            surname=organization_supervisor_surname,
                            patronymic=organization_supervisor_patronymic,
                            confirmed=False
                        )
                        db.add(organization_supervisor)
                        await db.commit()



                # Organization

                organization_executor_name = nioktr['_source']['executor']['name']
                organization_executor_ogrn = nioktr['_source']['executor']['ogrn']
                organization_executor_inn = nioktr['_source']['executor']['inn']
                organization_executor_city = nioktr['_source']['executor']['region']['name']



                customer_name = nioktr['_source']['customer']['name']

                if customer_name is not None:

                    customer_ogrn = nioktr['_source']['customer']['ogrn']
                    customer_inn = nioktr['_source']['customer']['inn']

                    organization_executor_result = await db.execute(select(Organization)
                                                                    .filter(Organization.name == organization_executor_name))

                    customer_result = await db.execute(select(Organization)
                                                       .filter(Organization.name == customer_name))

                    organization_executor = organization_executor_result.scalars().first()
                    customer = customer_result.scalars().first()

                    if organization_executor is None:
                        organization_executor = Organization(
                            name=organization_executor_name,
                            ogrn=organization_executor_ogrn,
                            inn=organization_executor_inn,
                            city=organization_executor_city

                        )
                        db.add(organization_executor)
                    await db.commit()
                else:
                    continue

                if str(nioktr['_source']['executor']['organization_id']) != '':
                    organization_identifier_executor_result = await db.execute(select(OrganizationIdentifier)
                                                                               .filter(
                        and_(OrganizationIdentifier.organization_id == organization_executor.id,
                             OrganizationIdentifier.identifier_id == identifier_nioktr.id,
                             OrganizationIdentifier.identifier_value == nioktr['_source']['executor']['organization_id'])))
                    organization_identifier_executor = organization_identifier_executor_result.scalars().first()
                    if organization_identifier_executor is None:
                        organization_identifier_executor = OrganizationIdentifier(
                            organization=organization_executor,
                            identifier=identifier_nioktr,
                            identifier_value=nioktr['_source']['executor']['organization_id']
                        )
                        db.add(organization_identifier_executor)
                        await db.commit()

                if customer is None:
                    customer = Organization(
                        name=customer_name,
                        ogrn=customer_ogrn,
                        inn=customer_inn,

                    )
                    db.add(customer)
                await db.commit()

                if str(nioktr['_source']['customer']['organization_id']) != '':
                    organization_identifier_customer_result = await db.execute(select(OrganizationIdentifier)
                                                                               .filter(
                        and_(OrganizationIdentifier.organization_id == customer.id,
                             OrganizationIdentifier.identifier_id == identifier_nioktr.id,
                             OrganizationIdentifier.identifier_value == nioktr['_source']['customer']['organization_id'])))
                    organization_identifier_customer = organization_identifier_customer_result.scalars().first()
                    if organization_identifier_customer is None:
                        organization_identifier_customer = OrganizationIdentifier(
                            organization=customer,
                            identifier=identifier_nioktr,
                            identifier_value=nioktr['_source']['customer']['organization_id']
                        )
                        db.add(organization_identifier_customer)
                        await db.commit()

                    await db.commit()

                # Nioktr

                nioktr_create = await create_nioktr(work_supervisor,
                                                    organization_supervisor,
                                                    organization_executor,
                                                    customer,
                                                    nioktr['_id'],
                                                    nioktr['_source']['name'],
                                                    nioktr['_source']['annotation'],
                                                    nioktr['_source']['contract_number'],
                                                    nioktr['_source']['last_status']['registration_number'],
                                                    datetime.strptime(nioktr['_source']['last_status']['created_date'][:10],
                                                                      "%Y-%m-%d").date(),
                                                    datetime.strptime(nioktr['_source']['contract_date'], "%Y-%m-%d").date(),
                                                    datetime.strptime(nioktr['_source']['start_date'], "%Y-%m-%d").date(),
                                                    datetime.strptime(nioktr['_source']['end_date'], "%Y-%m-%d").date(),
                                                    db)

                # keywords_nioktr
                key_len = len(nioktr['_source']['keyword_list'])

                # keyword

                for keyword_value in range(key_len):
                    if count_nir < key_len:
                        keyword_list = nioktr['_source']['keyword_list'][count_nir]['name']
                        keyword_result = await db.execute(select(Keyword).filter(and_(Keyword.keyword == keyword_list,
                                                                                      )))
                        keyword = keyword_result.scalars().first()
                        if keyword is None:
                            keyword = Keyword(
                                keyword=keyword_list
                            )
                        count_nir += 1
                        db.add(keyword)

                        keywords_nioktr = KeywordNioktr(
                            nioktr=nioktr_create,
                            keyword=keyword
                        )
                        db.add(keywords_nioktr)

                # Nioktr Types
                nioktr_types_len = len(nioktr['_source']['nioktr_types'])

                for nioktr_types_value in range(nioktr_types_len):
                    if count_types < nioktr_types_len:
                        nioktr_types_name = nioktr['_source']['nioktr_types'][count_types]['name']
                        nioktr_types_result = await db.execute(
                            select(NioktrTypes).filter(and_(NioktrTypes.name == nioktr_types_name,
                                                            NioktrTypes.nioktr_id == nioktr_create.id)))
                        nioktr_types = nioktr_types_result.scalars().first()
                        if nioktr_types is None:
                            nioktr_types = NioktrTypes(
                                name=nioktr_types_name,
                                nioktr=nioktr_create
                            )
                        count_types += 1
                        db.add(nioktr_types)

                # Budget
                budget_len = len(nioktr['_source']['budgets'])

                for budget_value in range(budget_len):
                    if count_budget < budget_len:
                        budget_type_name = nioktr['_source']['budgets'][count_budget]['budget_type']['name']
                        budget_type_result = await db.execute(select(BudgetType).filter(BudgetType.name == budget_type_name))
                        budget_type = budget_type_result.scalars().first()
                        if budget_type is None:
                            budget_type = BudgetType(
                                name=budget_type_name
                            )

                        db.add(budget_type)

                        nioktr_budget_funds = nioktr['_source']['budgets'][count_budget]['funds']
                        nioktr_budget_kbk = nioktr['_source']['budgets'][count_budget]['kbk']

                        nioktr_budget_result = await db.execute(
                            select(NioktrBudget).filter(and_(NioktrBudget.funds == nioktr_budget_funds,
                                                             NioktrBudget.kbk == nioktr_budget_kbk,
                                                             NioktrBudget.budget_type_id == budget_type.id,
                                                             NioktrBudget.nioktr_id == nioktr_create.id
                                                             )))
                        nioktr_budget = nioktr_budget_result.scalars().first()

                        if nioktr_budget is None:
                            nioktr_budget = NioktrBudget(
                                funds=nioktr_budget_funds,
                                kbk=nioktr_budget_kbk,
                                budget_type=budget_type,
                                nioktr=nioktr_create
                            )
                            db.add(nioktr_budget)
                            count_budget += 1
                            await db.commit()

                # #Subject (Rubrics)

                rubrics_len = len(nioktr['_source']['rubrics'])
                count_rubrics = 0
                for rubrics_value in range(rubrics_len):
                    if count_rubrics < rubrics_len:
                        rubrics_name = nioktr['_source']['rubrics'][count_rubrics]['name']
                        rubrics_code = nioktr['_source']['rubrics'][count_rubrics]['code']
                        rubrics_result = await db.execute(select(Subject).filter(and_(Subject.name == rubrics_name,
                                                                                      Subject.subj_code == rubrics_code, )))
                        rubrics = rubrics_result.scalars().first()
                        if rubrics is None:
                            rubrics = Subject(
                                subj_code=rubrics_code,
                                name=rubrics_name
                            )

                            db.add(rubrics)
                        nioktr_subject_rubrics_result = await db.execute(
                            select(NioktrSubject).filter(and_(NioktrSubject.nioktr_id == nioktr_create.id,
                                                              NioktrSubject.subject_id == rubrics.id)))
                        nioktr_subject_rubrics = nioktr_subject_rubrics_result.scalars().first()
                        if nioktr_subject_rubrics is None:
                            nioktr_subject_rubrics = NioktrSubject(
                                nioktr=nioktr_create,
                                subject=rubrics
                            )
                            db.add(nioktr_subject_rubrics)
                            count_rubrics += 1
                            await db.commit()

                # Subject (OECD)

                oecds_len = len(nioktr['_source']['oecds'])
                count_oecds = 0
                for oecds_value in range(oecds_len):
                    if count_oecds < oecds_len:
                        oecds_name = nioktr['_source']['oecds'][count_oecds]['name']
                        oecds_code = nioktr['_source']['oecds'][count_oecds]['code']
                        oecds_result = await db.execute(select(Subject).filter(and_(Subject.name == oecds_name,
                                                                                    Subject.subj_code == oecds_code, )))
                        oecds = oecds_result.scalars().first()
                        if oecds is None:
                            oecds = Subject(
                                subj_code=oecds_code,
                                name=oecds_name
                            )

                            db.add(oecds)

                        nioktr_subject_oecds_result = await db.execute(
                            select(NioktrSubject).filter(and_(NioktrSubject.nioktr_id == nioktr_create.id,
                                                              NioktrSubject.subject_id == oecds.id)))
                        nioktr_subject_oecds = nioktr_subject_oecds_result.scalars().first()
                        if nioktr_subject_oecds is None:
                            nioktr_subject_oecds = NioktrSubject(
                                nioktr=nioktr_create,
                                subject=oecds
                            )
                            db.add(nioktr_subject_oecds)
                            count_oecds += 1
                            await db.commit()

                # Subject (OECD)

                oesrs_len = len(nioktr['_source']['oesrs'])
                if oesrs_len > 0:
                    count_oesrs = 0
                    for oesrs_value in range(oesrs_len):
                        if count_oesrs < oesrs_len:
                            oesrs_name = nioktr['_source']['oesrs'][count_oesrs]['name']
                            oesrs_code = nioktr['_source']['oesrs'][count_oesrs]['code']
                            oesrs_result = await db.execute(select(Subject).filter(and_(Subject.name == oesrs_name,
                                                                                        Subject.subj_code == oesrs_code, )))
                            oesrs = oesrs_result.scalars().first()
                            if oesrs is None:
                                oesrs = Subject(
                                    subj_code=oesrs_code,
                                    name=oesrs_name
                                )

                                db.add(oesrs)

                            nioktr_subject_oesrs_result = await db.execute(
                                select(NioktrSubject).filter(and_(NioktrSubject.nioktr_id == nioktr_create.id,
                                                                  NioktrSubject.subject_id == oesrs.id)))
                            nioktr_subject_oesrs = nioktr_subject_oesrs_result.scalars().first()
                            if nioktr_subject_oesrs is None:
                                nioktr_subject_oesrs = NioktrSubject(
                                    nioktr=nioktr_create,
                                    subject=oesrs
                                )
                                db.add(nioktr_subject_oesrs)
                                count_oesrs += 1
                                await db.commit()
                else:
                    continue
                # Subject (Priority Directions)

                priority_directions_len = len(nioktr['_source']['priority_directions'])
                count_priority_directions = 0
                for priority_directions_value in range(priority_directions_len):
                    if count_priority_directions < priority_directions_len:
                        priority_directions_name = nioktr['_source']['priority_directions'][count_priority_directions]['name']
                        priority_directions_result = await db.execute(
                            select(Subject).filter(and_(Subject.name == priority_directions_name)))
                        priority_directions = priority_directions_result.scalars().first()
                        if priority_directions is None:
                            priority_directions = Subject(
                                name=priority_directions_name
                            )

                            db.add(priority_directions)

                        nioktr_subject_priority_directions_result = await db.execute(
                            select(NioktrSubject).filter(and_(NioktrSubject.nioktr_id == nioktr_create.id,
                                                              NioktrSubject.subject_id == priority_directions.id)))
                        nioktr_subject_priority_directions = nioktr_subject_priority_directions_result.scalars().first()
                        if nioktr_subject_priority_directions is None:
                            nioktr_subject_priority_directions = NioktrSubject(
                                nioktr=nioktr_create,
                                subject=priority_directions
                            )
                            db.add(nioktr_subject_priority_directions)
                            count_priority_directions += 1
                            await db.commit()

                # Subject (critical_technologies)

                critical_technologies_len = len(nioktr['_source']['critical_technologies'])
                count_critical_technologies = 0
                for critical_technologies_value in range(critical_technologies_len):
                    if count_critical_technologies < critical_technologies_len:
                        critical_technologies_name = nioktr['_source']['critical_technologies'][count_critical_technologies][
                            'name']
                        critical_technologies_result = await db.execute(
                            select(Subject).filter(and_(Subject.name == critical_technologies_name)))
                        critical_technologies = critical_technologies_result.scalars().first()
                        if critical_technologies is None:
                            critical_technologies = Subject(
                                name=critical_technologies_name
                            )

                            db.add(critical_technologies)

                        nioktr_subject_critical_technologies_result = await db.execute(
                            select(NioktrSubject).filter(and_(NioktrSubject.nioktr_id == nioktr_create.id,
                                                              NioktrSubject.subject_id == critical_technologies.id)))
                        nioktr_subject_critical_technologies = nioktr_subject_critical_technologies_result.scalars().first()
                        if nioktr_subject_critical_technologies is None:
                            nioktr_subject_critical_technologies = NioktrSubject(
                                nioktr=nioktr_create,
                                subject=critical_technologies
                            )
                            db.add(nioktr_subject_critical_technologies)
                            count_critical_technologies += 1
                            await db.commit()
                #
                # #NioktrSubject ПЕРЕНЕСТИ ФУНКЦИЮ ВЫШЕ КАК В SUBJECT AND KEYWORD
                # #написать функцию в storage, чтобы код не дублировался  ???

                coexecutors_len = len(nioktr['_source']['coexecutors'])
                count_coexecutors = 0
                for coexecutors_value in range(coexecutors_len):
                    if count_coexecutors < coexecutors_len:
                        coexecutors_name = nioktr['_source']['coexecutors'][count_coexecutors]['name']
                        coexecutors_ogrn = nioktr['_source']['coexecutors'][count_coexecutors]['ogrn']
                        coexecutors_inn = nioktr['_source']['coexecutors'][count_coexecutors]['inn']

                        coexecutors_result = await db.execute(
                            select(Organization).filter(
                                and_(Organization.name == coexecutors_name, Organization.ogrn == coexecutors_ogrn,
                                     Organization.inn == coexecutors_inn)))
                        coexecutors = coexecutors_result.scalars().first()
                        if coexecutors is None:
                            coexecutors = Organization(
                                name=coexecutors_name,
                                ogrn=coexecutors_ogrn,
                                inn=coexecutors_inn,
                            )

                            db.add(coexecutors)

                        organization_coexecutors_result = await db.execute(
                            select(OrganizationCoexecutor).filter(and_(OrganizationCoexecutor.organization_id == coexecutors.id,
                                                                       OrganizationCoexecutor.nioktr_id == create_nioktr.id)))
                        organization_coexecutors = organization_coexecutors_result.scalars().first()
                        if organization_coexecutors is None:
                            organization_coexecutors = OrganizationCoexecutor(
                                nioktr=nioktr_create,
                                organization=coexecutors
                            )
                            db.add(organization_coexecutors)
                            count_coexecutors += 1
                            await db.commit()


    await db.commit()


async def service_get_nioktrs(params: Nioktr_params, db: Session):
    query = select(Nioktr).filter(Nioktr.nioktr_date >= params.from_date)\
        .filter(Nioktr.nioktr_date <= params.to_date)

    if not (params.search is None) and params.search != "":
        query = query.filter(func.lower(Nioktr.title).contains(params.search.lower()))

    if not (params.author_id is None):
        query = query.join(Author).filter(Author.author_id == params.author_id).distinct()

    offset = params.limit * params.page
    nioktrs_result = await db.execute(query.order_by(desc(Nioktr.nioktr_date))
                                      .order_by(Nioktr.title)
                                      .options(joinedload(Nioktr.keyword_nioktrs).joinedload(KeywordNioktr.keyword))
                                      .options(joinedload(Nioktr.work_supervisor))
                                      .offset(offset).limit(params.limit))
    nioktrs = nioktrs_result.scalars().unique().all()
    scheme_nioktrs = [SchemeNioktr.from_orm(nioktr) for nioktr in nioktrs]
    count = await get_count(query, db)
    return dict(nioktrs=scheme_nioktrs, count=count)


async def service_get_nioktr(id: int, db: Session):
    nioktr_result = await db.execute(select(Nioktr).filter(Nioktr.id == id)
                                     .options(joinedload(Nioktr.nioktr_budget)
                                              .joinedload(NioktrBudget.budget_type))
                                     .options(joinedload(Nioktr.keyword_nioktrs)
                                              .joinedload(KeywordNioktr.keyword))
                                     .options(joinedload(Nioktr.nioktr_subject)
                                              .joinedload(NioktrSubject.subject))
                                     .options(joinedload(Nioktr.organization_coexecutor)
                                              .joinedload(OrganizationCoexecutor.organization))
                                     .options(joinedload(Nioktr.types_nioktrs))
                                     .options(joinedload(Nioktr.customer))
                                     .options(joinedload(Nioktr.organization_executor))
                                     .options(joinedload(Nioktr.organization_supervisor))

                                     )
    nioktr = nioktr_result.scalars().first()
    if nioktr is None:
        return False
    scheme_nioktr = SchemeNioktrPage.from_orm(nioktr)
    return dict(nioktr=scheme_nioktr)