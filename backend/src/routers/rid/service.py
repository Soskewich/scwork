from datetime import datetime
import requests
import json
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Keyword, Author, Organization, Subject,\
    OrganizationIdentifier, KeywordRid, RidSubject, OrganizationExecutor, AuthorRid, Rid
from src.model.storage import get_or_create_identifier, get_count, create_rid
from src.routers.rid.schema import Rid_params
from src.schemas.schemas import SchemeRid, SchemeRidPage


# Создаём сессию и проставляем стандартные заголовки, что бы не сильно отличаться от браузера

async def service_update_rid(db: Session):
    identifier_rid = await get_or_create_identifier("Rid", db)
    uid = []
    uid.append('9569096')  # ОмГТУ
    start_date = '2014-12-23'
    end_date = '2024-03-01'
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
        "nioktrs": False,
        "organization": uid,
        "page": 1,
        "priority_directions": [],
        "rids": True,
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
                await upload_rid(json_resp, identifier_rid, db)

                if page >= count_of_pages:
                    break
                payload['page'] += 1

        except BaseException as e:
            await db.rollback()
            print('Retry connection', str(e))
            search_results = await service_update_rid(db)
    return 'ok'

        #Start Test
        # Сначала сделать зависимости с которыми связаны nioktr и параллельно заполнять поля
        #     nioktr_type = await get_or_create_budget_type()


async def upload_rid(json_resp, identifier_rid, db: Session):

    for rid in json_resp['hits']['hits']:
        count_rid = 0
        if rid['_id']:
            rid_id_result = await db.execute(select(Rid).filter(Rid.rosrid_id == rid['_id']))
            rid_id = rid_id_result.scalars().first()
            if rid_id is None:
                work_supervisor_name = rid['_source']['work_supervisor']['name']
                work_supervisor_surname = rid['_source']['work_supervisor']['surname']
                work_supervisor_patronymic = rid['_source']['work_supervisor']['patronymic']
                if work_supervisor_name is None:

                    new_work_supervisor_fullname = work_supervisor_surname.split(' ')
                    if len(new_work_supervisor_fullname) >= 3:
                        new_work_supervisor_fullname = new_work_supervisor_fullname[
                                                       ::len(new_work_supervisor_fullname) - 1]
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
                            surname=rid['_source']['work_supervisor']['surname'],
                            patronymic=work_supervisor_patronymic,
                            confirmed=False
                        )
                        db.add(work_supervisor)
                        await db.commit()

                organization_supervisor_name = rid['_source']['organization_supervisor']['name']
                organization_supervisor_patronymic = rid['_source']['organization_supervisor']['patronymic']
                organization_supervisor_surname = rid['_source']['organization_supervisor']['surname']

                if organization_supervisor_name is None:

                    new_organization_supervisor_fullname = organization_supervisor_surname.split(' ')
                    new_organization_supervisor_name_and_patronymic = new_organization_supervisor_fullname[1].split('.')
                    organization_supervisor_result = await db.execute(
                        select(Author).filter(and_(Author.name == new_organization_supervisor_name_and_patronymic[0],
                                                   Author.surname == new_organization_supervisor_fullname[0],
                                                   Author.patronymic == new_organization_supervisor_name_and_patronymic[
                                                       1])))

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

        #Organization
                customer_full = rid['_source']['customer']
                if not customer_full:
                    customer_full_result = await db.execute(select(Organization)
                                                   .filter(Organization.name == '-'))

                    customer = customer_full_result.scalars().first()
                    if customer is None:
                        customer = Organization(
                            name="-",
                            ogrn=None,
                            inn=None,
                        )
                        db.add(customer)

                        continue
                else:

                    customer_name = rid['_source']['customer']['name']
                    if customer_name is not None:
                        customer_ogrn = rid['_source']['customer']['ogrn']
                        customer_inn = rid['_source']['customer']['inn']

                        customer_result = await db.execute(select(Organization)
                                                           .filter(Organization.name == customer_name))

                        customer = customer_result.scalars().first()

                        if customer is None:
                            customer = Organization(
                                name=customer_name,
                                ogrn=customer_ogrn,
                                inn=customer_inn,
                            )
                            db.add(customer)
                        await db.commit()

                        if str(rid['_source']['customer']['organization_id']) != '':
                            organization_identifier_customer_result = await db.execute(select(OrganizationIdentifier)
                                                        .filter(and_(OrganizationIdentifier.organization_id == customer.id,
                                                    OrganizationIdentifier.identifier_id == identifier_rid.id,
                                                  OrganizationIdentifier.identifier_value == rid['_source']['customer']['organization_id'])))
                            organization_identifier_customer = organization_identifier_customer_result.scalars().first()
                            if organization_identifier_customer is None:
                                organization_identifier_customer = OrganizationIdentifier(
                                    organization=customer,
                                    identifier=identifier_rid,
                                    identifier_value=rid['_source']['customer']['organization_id']
                                )
                                db.add(organization_identifier_customer)
                                await db.commit()

                            await db.commit()


                # Rid

                rid_create = await create_rid(work_supervisor,
                                                    organization_supervisor,
                                                    customer,
                                                    rid['_id'],
                                                    rid['_source']['name'],
                                                    rid['_source']['abstract'],
                                                    rid['_source']['last_status']['registration_number'],
                                                    datetime.strptime(rid['_source']['last_status']['created_date'][:10], "%Y-%m-%d").date(),
                                                    rid['_source']['rid_type']['name'],
                                                    rid['_source']['expected']['name'],
                                                    rid['_source']['using_ways'],
                                                    rid['_source']['number_of_prototypes'],
                                                    db)



                # keywords_rid
                key_len = len(rid['_source']['keyword_list'])

                # keyword

                for keyword_value in range(key_len):
                    if count_rid < key_len:
                        keyword_list = rid['_source']['keyword_list'][count_rid]['name']
                        keyword_result = await db.execute(select(Keyword).filter(and_(Keyword.keyword == keyword_list,
                                                                                      )))
                        keyword = keyword_result.scalars().first()
                        if keyword is None:
                            keyword = Keyword(
                                keyword=keyword_list
                            )
                        count_rid += 1
                        db.add(keyword)

                        keyword_rids = KeywordRid(
                            rid=rid_create,
                            keyword=keyword
                        )
                        db.add(keyword_rids)


                # #Subject (Rubrics)

                rubrics_len = len(rid['_source']['rubrics'])
                count_rubrics = 0
                for rubrics_value in range(rubrics_len):
                    if count_rubrics < rubrics_len:
                        rubrics_name = rid['_source']['rubrics'][count_rubrics]['name']
                        rubrics_code = rid['_source']['rubrics'][count_rubrics]['code']
                        rubrics_result = await db.execute(select(Subject).filter(and_(Subject.name == rubrics_name,
                                                                                      Subject.subj_code == rubrics_code,)))
                        rubrics = rubrics_result.scalars().first()
                        if rubrics is None:
                            rubrics = Subject(
                                subj_code=rubrics_code,
                                name=rubrics_name
                            )

                            db.add(rubrics)
                        rid_subject_rubrics_result = await db.execute(
                            select(RidSubject).filter(and_(RidSubject.rid_id == rid_create.id,
                                                              RidSubject.subject_id == rubrics.id)))
                        rid_subject_rubrics = rid_subject_rubrics_result.scalars().first()
                        if rid_subject_rubrics is None:
                            rid_subject_rubrics = RidSubject(
                                rid=rid_create,
                                subject=rubrics
                            )
                            db.add(rid_subject_rubrics)
                            count_rubrics += 1
                            await db.commit()

                # Subject (OECD)

                oecds_len = len(rid['_source']['oecds'])
                count_oecds = 0
                for oecds_value in range(oecds_len):
                    if count_oecds < oecds_len:
                        oecds_name = rid['_source']['oecds'][count_oecds]['name']
                        oecds_code = rid['_source']['oecds'][count_oecds]['code']
                        oecds_result = await db.execute(select(Subject).filter(and_(Subject.name == oecds_name,
                                                                                    Subject.subj_code == oecds_code,)))
                        oecds = oecds_result.scalars().first()
                        if oecds is None:
                            oecds = Subject(
                                subj_code=oecds_code,
                                name=oecds_name
                            )

                            db.add(oecds)

                        rid_subject_oecds_result = await db.execute(
                            select(RidSubject).filter(and_(RidSubject.rid_id == rid_create.id,
                                                              RidSubject.subject_id == oecds.id)))
                        rid_subject_oecds = rid_subject_oecds_result.scalars().first()
                        if rid_subject_oecds is None:
                            rid_subject_oecds = RidSubject(
                                rid=rid_create,
                                subject=oecds
                            )
                            db.add(rid_subject_oecds)
                            count_oecds += 1
                            await db.commit()


                # #NioktrSubject ПЕРЕНЕСТИ ФУНКЦИЮ ВЫШЕ КАК В SUBJECT AND KEYWORD
                # #написать функцию в storage, чтобы код не дублировался  ???

                executors_len = len(rid['_source']['executors'])
                count_executors = 0
                for executors_value in range(executors_len):
                    if count_executors < executors_len:
                        executors_name = rid['_source']['executors'][count_executors]['name']
                        executors_ogrn = rid['_source']['executors'][count_executors]['ogrn']
                        executors_inn = rid['_source']['executors'][count_executors]['inn']

                        executors_result = await db.execute(
                            select(Organization).filter(and_(Organization.name == executors_name, Organization.ogrn == executors_ogrn,
                                                             Organization.inn == executors_inn)))
                        executors = executors_result.scalars().first()
                        if executors is None:
                            executors = Organization(
                                name=executors_name,
                                ogrn=executors_ogrn,
                                inn=executors_inn,
                            )

                            db.add(executors)

                        organization_executors_result = await db.execute(
                            select(OrganizationExecutor).filter(and_(OrganizationExecutor.organization_id == executors.id,
                                                                       OrganizationExecutor.rid_id == rid_create.id)))
                        organization_executors = organization_executors_result.scalars().first()
                        if organization_executors is None:
                            organization_executors = OrganizationExecutor(
                                rid=rid_create,
                                organization=executors
                            )
                            db.add(organization_executors)
                            count_executors += 1
                            await db.commit()

                authors_len = len(rid['_source']['authors'])
                count_authors = 0
                for authors_value in range(authors_len):
                    if count_authors < authors_len:
                        authors_name = rid['_source']['authors'][count_authors]['name']
                        authors_surname = rid['_source']['authors'][count_authors]['surname']
                        authors_patronymic = rid['_source']['authors'][count_authors]['patronymic']

                        authors_result = await db.execute(
                            select(Author).filter(
                                and_(Author.name == authors_name, Author.surname == authors_surname,
                                     Author.patronymic == authors_patronymic)))
                        authors = authors_result.scalars().first()
                        if authors is None:
                            authors = Author(
                                name=authors_name,
                                surname=authors_surname,
                                patronymic=authors_patronymic,
                                confirmed=False
                            )

                            db.add(authors)

                        author_rid_result = await db.execute(
                            select(AuthorRid).filter(
                                and_(AuthorRid.author_id == authors.id,
                                     AuthorRid.rid_id == rid_create.id)))
                        author_rid = author_rid_result.scalars().first()
                        if author_rid is None:
                            author_rid = AuthorRid(
                                rid=rid_create,
                                author=authors
                            )
                            db.add(author_rid)
                            count_authors += 1
                            await db.commit()

    await db.commit()




async def service_get_rids(params: Rid_params, db: Session):
    query = select(Rid).filter(Rid.rid_date >= params.from_date)\
        .filter(Rid.rid_date <= params.to_date)

    if not (params.search is None) and params.search != "":
        query = query.filter(func.lower(Rid.title).contains(params.search.lower()))

    if not (params.author_id is None):
        query = query.join(Author).filter(Author.author_id == params.author_id).distinct()

    offset = params.limit * params.page
    rid_result = await db.execute(query.order_by(desc(Rid.rid_date))
                                      .order_by(Rid.title)
                                      .options(joinedload(Rid.keyword_rids).joinedload(KeywordRid.keyword))
                                      .options(joinedload(Rid.work_supervisor))
                                      .offset(offset).limit(params.limit))
    rids = rid_result.scalars().unique().all()
    scheme_rids = [SchemeRid.from_orm(rid) for rid in rids]
    count = await get_count(query, db)
    return dict(rids=scheme_rids, count=count)


async def service_get_rid(id: int, db: Session):
    rid_result = await db.execute(select(Rid).filter(Rid.id == id)
                                     .options(joinedload(Rid.organization_executor)
                                              .joinedload(OrganizationExecutor.organization))

                                     .options(joinedload(Rid.rid_subject)
                                              .joinedload(RidSubject.subject))

                                     .options(joinedload(Rid.keyword_rids)
                                              .joinedload(KeywordRid.keyword))

                                     .options(joinedload(Rid.rid_authors)
                                              .joinedload(AuthorRid.author))

                                     .options(joinedload(Rid.work_supervisor))
                                     .options(joinedload(Rid.organization_supervisor))
                                     .options(joinedload(Rid.customer))
                                     )
    rid = rid_result.scalars().first()
    if rid is None:
        return False
    scheme_rid = SchemeRidPage.from_orm(rid)
    return dict(rid=scheme_rid)



# Разобраться с датой 2019-04-11
# Пустые customer не добавляются