from datetime import datetime
import requests
import json
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload

from src.model.model import Keyword, Author, Organization, Subject, \
    OrganizationIdentifier, Dissertation, \
    KeywordDissertation, DissertationSubject, AuthorSupervisorsDissertation, AuthorOpponentsDissertation
from src.model.storage import get_or_create_identifier, create_dissertation




# Создаём сессию и проставляем стандартные заголовки, что бы не сильно отличаться от браузера

async def service_update_dissertation(db: Session):
    identifier_dissertation = await get_or_create_identifier("Dissertation", db)
    uid = []
    uid.append('9569096')  # ОмГТУ
    start_date = '2014-02-03'
    end_date = '2024-01-01'
    items_in_page = 10

    # URL API, который осуществляет поиск по ИС
    search_url = 'https://rosrid.ru/api/base/search'
    # Формируем заготовку для основного тела поиска
    payload = {
        "search_query": None,
        "critical_technologies": [],
        "dissertations": True,
        "full_text_available": False,
        "ikrbses": False,
        "nioktrs": False,
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
                await upload_dissertation(json_resp, identifier_dissertation, db)

                if page >= count_of_pages:
                    break
                payload['page'] += 1

        except BaseException as e:
            await db.rollback()
            print('Retry connection', str(e))
            search_results = await service_update_dissertation(db)
    return 'ok'


async def upload_dissertation(json_resp, identifier_dissertation, db: Session):

    for dissertation in json_resp['hits']['hits']:
        count_dissertation = 0
        if dissertation['_id']:
            dissertation_id_result = await db.execute(select(Dissertation).filter(Dissertation.rosrid_id == dissertation['_id']))
            dissertation_id = dissertation_id_result.scalars().first()
            if dissertation_id is None:
                chairman_dissertation_council_name = dissertation['_source']['chairman_dissertation_council']['name']
                chairman_dissertation_council_surname = dissertation['_source']['chairman_dissertation_council']['surname']
                chairman_dissertation_council_patronymic = dissertation['_source']['chairman_dissertation_council']['patronymic']
                if chairman_dissertation_council_name is None:

                    new_chairman_dissertation_council_fullname = chairman_dissertation_council_surname.split(' ')
                    if len(new_chairman_dissertation_council_fullname) >= 3:
                        new_chairman_dissertation_council_fullname = new_chairman_dissertation_council_fullname[
                                                       ::len(new_chairman_dissertation_council_fullname) - 1]
                    new_work_chairman_dissertation_name_and_patronymic = new_chairman_dissertation_council_fullname[1].split('.')

                    chairman_dissertation_council_result = await db.execute(
                        select(Author).filter(and_(Author.name == new_work_chairman_dissertation_name_and_patronymic[0],
                                                   Author.surname == new_chairman_dissertation_council_fullname[0],
                                                   Author.patronymic == new_work_chairman_dissertation_name_and_patronymic[1])))
                    chairman_dissertation_council = chairman_dissertation_council_result.scalars().first()

                    if chairman_dissertation_council is None:
                        chairman_dissertation_council = Author(
                            name=new_work_chairman_dissertation_name_and_patronymic[0],
                            surname=new_chairman_dissertation_council_fullname[0],
                            patronymic=new_work_chairman_dissertation_name_and_patronymic[1],
                            confirmed=False
                        )
                        db.add(chairman_dissertation_council)
                        await db.commit()

                else:

                    chairman_dissertation_council_result = await db.execute(
                        select(Author).filter(and_(Author.name == chairman_dissertation_council_name,
                                                   Author.surname == chairman_dissertation_council_surname,
                                                   Author.patronymic == chairman_dissertation_council_patronymic)))
                    chairman_dissertation_council = chairman_dissertation_council_result.scalars().first()

                    if chairman_dissertation_council is None:
                        chairman_dissertation_council = Author(
                            name=chairman_dissertation_council_name,
                            surname=dissertation['_source']['chairman_dissertation_council']['surname'],
                            patronymic=chairman_dissertation_council_patronymic,
                            confirmed=False
                        )
                        db.add(chairman_dissertation_council)
                        await db.commit()

                organization_supervisor_name = dissertation['_source']['organization_supervisor']['name']
                organization_supervisor_patronymic = dissertation['_source']['organization_supervisor']['patronymic']
                organization_supervisor_surname = dissertation['_source']['organization_supervisor']['surname']

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
                author_organization_full = dissertation['_source']['author_organization']
                if not author_organization_full:
                    author_organization_full_result = await db.execute(select(Organization)
                                                   .filter(Organization.name == '-'))

                    author_organization = author_organization_full_result.scalars().first()
                    if author_organization is None:
                        author_organization = Organization(
                            name="-",
                            ogrn=None,
                            inn=None,
                        )
                        db.add(author_organization)

                        continue
                else:

                    author_organization_name = dissertation['_source']['author_organization']['name']
                    if author_organization_name is not None:

                        author_organization_ogrn = dissertation['_source']['author_organization']['ogrn']
                        author_organization_inn = dissertation['_source']['author_organization']['inn']
                        city = dissertation['_source']['author_organization']['region']

                        author_organization_result = await db.execute(select(Organization)
                                                           .filter(Organization.name == author_organization_name))

                        author_organization = author_organization_result.scalars().first()

                        if author_organization is None:
                            if not city:
                                author_organization = Organization(
                                    name=author_organization_name,
                                    city=None,
                                    ogrn=author_organization_ogrn,
                                    inn=author_organization_inn,
                                )
                                db.add(author_organization)
                            else:
                                author_organization = Organization(
                                    name=author_organization_name,
                                    city=dissertation['_source']['author_organization']['region']['name'],
                                    ogrn=author_organization_ogrn,
                                    inn=author_organization_inn,
                                )
                                db.add(author_organization)
                            await db.commit()

                        if str(dissertation['_source']['author_organization']['organization_id']) != '':
                            organization_identifier_author_organization_result = await db.execute(select(OrganizationIdentifier)
                                                        .filter(and_(OrganizationIdentifier.organization_id == author_organization.id,
                                                    OrganizationIdentifier.identifier_id == identifier_dissertation.id,
                                                  OrganizationIdentifier.identifier_value == dissertation['_source']['author_organization']['organization_id'])))
                            organization_identifier_author_organization = organization_identifier_author_organization_result.scalars().first()
                            if organization_identifier_author_organization is None:
                                organization_identifier_author_organization = OrganizationIdentifier(
                                    organization=author_organization,
                                    identifier=identifier_dissertation,
                                    identifier_value=dissertation['_source']['author_organization']['organization_id']
                                )
                                db.add(organization_identifier_author_organization)
                                await db.commit()

                            await db.commit()


                protection_organization_full = dissertation['_source']['protection_organization']
                if not protection_organization_full:
                    protection_organization_full_result = await db.execute(select(Organization)
                                                                       .filter(Organization.name == '-'))

                    protection_organization = protection_organization_full_result.scalars().first()
                    if protection_organization is None:
                        protection_organization = Organization(
                            name="-",
                            ogrn=None,
                            inn=None,
                        )
                        db.add(protection_organization)

                        continue
                else:

                    protection_organization_name = dissertation['_source']['protection_organization']['name']
                    if protection_organization_name is not None:
                        protection_organization_ogrn = dissertation['_source']['protection_organization']['ogrn']
                        protection_organization_inn = dissertation['_source']['protection_organization']['inn']
                        protection_organization_city = dissertation['_source']['protection_organization']['region']['name']

                        protection_organization_result = await db.execute(select(Organization)
                                                                      .filter(
                            Organization.name == protection_organization_name))

                        protection_organization = protection_organization_result.scalars().first()

                        if protection_organization is None:
                            protection_organization = Organization(
                                name=protection_organization_name,
                                ogrn=protection_organization_ogrn,
                                inn=protection_organization_inn,
                                city=protection_organization_city

                            )
                            db.add(protection_organization)
                        await db.commit()

                        if str(dissertation['_source']['protection_organization']['organization_id']) != '':
                            organization_identifier_protection_organization_result = await db.execute(
                                select(OrganizationIdentifier)
                                .filter(and_(OrganizationIdentifier.organization_id == protection_organization.id,
                                             OrganizationIdentifier.identifier_id == identifier_dissertation.id,
                                             OrganizationIdentifier.identifier_value ==
                                             dissertation['_source']['protection_organization']['organization_id'])))
                            organization_identifier_protection_organization = organization_identifier_protection_organization_result.scalars().first()
                            if organization_identifier_protection_organization is None:
                                organization_identifier_protection_organization = OrganizationIdentifier(
                                    organization=protection_organization,
                                    identifier=identifier_dissertation,
                                    identifier_value=dissertation['_source']['protection_organization']['organization_id']
                                )
                                db.add(organization_identifier_protection_organization)
                                await db.commit()

                            await db.commit()



                # Diss

                dissertation_create = await create_dissertation(chairman_dissertation_council,
                                                    organization_supervisor,
                                                    author_organization,
                                                    protection_organization,
                                                    dissertation['_id'],
                                                    dissertation['_source']['name'],
                                                    dissertation['_source']['abstract'],
                                                    dissertation['_source']['last_status']['registration_number'],
                                                    datetime.strptime(dissertation['_source']['last_status']['created_date'][:10], "%Y-%m-%d").date(),
                                                    datetime.strptime(dissertation['_source']['protection_date'], "%Y-%m-%d").date(),
                                                    dissertation['_source']['dissertation_type']['name'],
                                                    dissertation['_source']['dissertation_report_type']['name'],
                                                    dissertation['_source']['tables_count'],
                                                    dissertation['_source']['pictures_count'],
                                                    dissertation['_source']['applications_count'],
                                                    dissertation['_source']['pages_count'],
                                                    dissertation['_source']['sources_count'],
                                                    dissertation['_source']['books_count'],
                                                    dissertation['_source']['bibliography'],
                                                    db)



                # keywords_dis
                key_len = len(dissertation['_source']['keyword_list'])

                # keyword

                for keyword_value in range(key_len):
                    if count_dissertation < key_len:
                        keyword_list = dissertation['_source']['keyword_list'][count_dissertation]['name']
                        keyword_result = await db.execute(select(Keyword).filter(and_(Keyword.keyword == keyword_list,
                                                                                      )))
                        keyword = keyword_result.scalars().first()
                        if keyword is None:
                            keyword = Keyword(
                                keyword=keyword_list
                            )
                        count_dissertation += 1
                        db.add(keyword)

                        keyword_disseratation = KeywordDissertation(
                            dissertation=dissertation_create,
                            keyword=keyword
                        )
                        db.add(keyword_disseratation)


                # #Subject (Rubrics)

                rubrics_len = len(dissertation['_source']['rubrics'])
                count_rubrics = 0
                for rubrics_value in range(rubrics_len):
                    if count_rubrics < rubrics_len:
                        rubrics_name = dissertation['_source']['rubrics'][count_rubrics]['name']
                        rubrics_code = dissertation['_source']['rubrics'][count_rubrics]['code']
                        rubrics_result = await db.execute(select(Subject).filter(and_(Subject.name == rubrics_name,
                                                                                      Subject.subj_code == rubrics_code,)))
                        rubrics = rubrics_result.scalars().first()
                        if rubrics is None:
                            rubrics = Subject(
                                subj_code=rubrics_code,
                                name=rubrics_name
                            )

                            db.add(rubrics)
                        dissertation_subject_rubrics_result = await db.execute(
                            select(DissertationSubject).filter(and_(DissertationSubject.dissertation_id == dissertation_create.id,
                                                              DissertationSubject.subject_id == rubrics.id)))
                        dissertation_subject_rubrics = dissertation_subject_rubrics_result.scalars().first()
                        if dissertation_subject_rubrics is None:
                            dissertation_subject_rubrics = DissertationSubject(
                                dissertation=dissertation_create,
                                subject=rubrics
                            )
                            db.add(dissertation_subject_rubrics)
                            count_rubrics += 1
                            await db.commit()

                # Subject (OECD)

                oecds_len = len(dissertation['_source']['oecds'])
                count_oecds = 0
                for oecds_value in range(oecds_len):
                    if count_oecds < oecds_len:
                        oecds_name = dissertation['_source']['oecds'][count_oecds]['name']
                        oecds_code = dissertation['_source']['oecds'][count_oecds]['code']
                        oecds_result = await db.execute(select(Subject).filter(and_(Subject.name == oecds_name,
                                                                                    Subject.subj_code == oecds_code,)))
                        oecds = oecds_result.scalars().first()
                        if oecds is None:
                            oecds = Subject(
                                subj_code=oecds_code,
                                name=oecds_name
                            )

                            db.add(oecds)

                        dissertation_subject_oecds_result = await db.execute(
                            select(DissertationSubject).filter(and_(DissertationSubject.dissertation_id == dissertation_create.id,
                                                              DissertationSubject.subject_id == oecds.id)))
                        dissertation_subject_oecds = dissertation_subject_oecds_result.scalars().first()
                        if dissertation_subject_oecds is None:
                            dissertation_subject_oecds = DissertationSubject(
                                dissertation=dissertation_create,
                                subject=oecds
                            )
                            db.add(dissertation_subject_oecds)
                            count_oecds += 1
                            await db.commit()

                # Subject (Speciality_code)

                speciality_codes_len = len(dissertation['_source']['speciality_codes'])
                count_speciality_codes = 0
                for speciality_codes_value in range(speciality_codes_len):
                    if count_speciality_codes < speciality_codes_len:
                        speciality_codes_name = dissertation['_source']['speciality_codes'][count_speciality_codes]['name']
                        speciality_codes_code = dissertation['_source']['speciality_codes'][count_speciality_codes]['code']
                        speciality_codes_result = await db.execute(select(Subject).filter(and_(Subject.name == speciality_codes_name,
                                                                                    Subject.subj_code == speciality_codes_code, )))
                        speciality_codes = speciality_codes_result.scalars().first()
                        if speciality_codes is None:
                            speciality_codes = Subject(
                                subj_code=speciality_codes_code,
                                name=speciality_codes_name
                            )

                            db.add(speciality_codes)

                        dissertation_subject_speciality_codes_result = await db.execute(
                            select(DissertationSubject).filter(
                                and_(DissertationSubject.dissertation_id == dissertation_create.id,
                                     DissertationSubject.subject_id == speciality_codes.id)))
                        dissertation_subject_speciality_codes = dissertation_subject_speciality_codes_result.scalars().first()
                        if dissertation_subject_speciality_codes is None:
                            dissertation_subject_speciality_codes = DissertationSubject(
                                dissertation=dissertation_create,
                                subject=speciality_codes
                            )
                            db.add(dissertation_subject_speciality_codes)
                            count_oecds += 1
                            await db.commit()

                # #NioktrSubject ПЕРЕНЕСТИ ФУНКЦИЮ ВЫШЕ КАК В SUBJECT AND KEYWORD
                # #написать функцию в storage, чтобы код не дублировался  ???



                supervisors_len = len(dissertation['_source']['supervisors'])
                count_supervisors = 0
                for supervisors_value in range(supervisors_len):
                    if count_supervisors < supervisors_len:
                        supervisors_fio = dissertation['_source']['supervisors']['fio']
                        supervisors_fio_new = supervisors_fio.split(' ')
                        supervisors_fio_new = supervisors_fio_new[::len(supervisors_fio_new) - 1]
                        supervisors_name_and_patronymic = supervisors_fio_new[1].split('.')

                        supervisors_result = await db.execute(
                            select(Author).filter(
                                and_(Author.name == supervisors_name_and_patronymic[0], Author.surname == supervisors_fio_new[0],
                                     Author.patronymic == supervisors_name_and_patronymic[1])))
                        supervisors = supervisors_result.scalars().first()
                        if supervisors is None:
                            supervisors = Author(
                                name=supervisors_name_and_patronymic[0],
                                surname=supervisors_fio_new[0],
                                patronymic=supervisors_name_and_patronymic[1],
                                confirmed=False
                            )

                            db.add(supervisors)

                        supervisors_dissertation_result = await db.execute(
                            select(AuthorSupervisorsDissertation).filter(
                                and_(AuthorSupervisorsDissertation.author_id == supervisors.id,
                                     AuthorSupervisorsDissertation.dissertation_id == dissertation_create.id)))
                        supervisors_dissertation = supervisors_dissertation_result.scalars().first()
                        if supervisors_dissertation is None:
                            supervisors_dissertation = AuthorSupervisorsDissertation(
                                dissertation=dissertation_create,
                                author=supervisors
                            )
                            db.add(supervisors_dissertation)
                            count_supervisors += 1
                            await db.commit()

                #Opponents

                opponents_len = len(dissertation['_source']['opponents'])
                count_opponents = 0
                for opponents_value in range(opponents_len):
                    if count_opponents < opponents_len:
                        opponents_fio = dissertation['_source']['opponents']['fio']
                        opponents_fio_new = opponents_fio.split(' ')
                        opponents_fio_new = opponents_fio_new[::len(opponents_fio_new) - 1]
                        opponents_name_and_patronymic = opponents_fio_new[1].split('.')

                        opponents_result = await db.execute(
                            select(Author).filter(
                                and_(Author.name == opponents_name_and_patronymic[0],
                                     Author.surname == opponents_fio_new[0],
                                     Author.patronymic == opponents_name_and_patronymic[1])))
                        opponents = opponents_result.scalars().first()
                        if opponents is None:
                            opponents = Author(
                                name=opponents_name_and_patronymic[0],
                                surname=opponents_fio_new[0],
                                patronymic=opponents_name_and_patronymic[1],
                                confirmed=False
                            )

                            db.add(opponents)

                        opponents_dissertation_result = await db.execute(
                            select(AuthorOpponentsDissertation).filter(
                                and_(AuthorOpponentsDissertation.author_id == opponents.id,
                                     AuthorOpponentsDissertation.dissertation_id == dissertation_create.id)))
                        opponents_dissertation = opponents_dissertation_result.scalars().first()
                        if opponents_dissertation is None:
                            opponents_dissertation = AuthorOpponentsDissertation(
                                dissertation=dissertation_create,
                                author=opponents
                            )
                            db.add(opponents_dissertation)
                            count_opponents += 1
                            await db.commit()

    await db.commit()

#Протестировать дисы и накатить миграцию endpoint

#
# async def service_get_rids(params: Rid_params, db: Session):
#     query = select(Rid).filter(Rid.rid_date >= params.from_date)\
#         .filter(Rid.rid_date <= params.to_date)
#
#     if not (params.search is None) and params.search != "":
#         query = query.filter(func.lower(Rid.title).contains(params.search.lower()))
#
#     if not (params.author_id is None):
#         query = query.join(Author).filter(Author.author_id == params.author_id).distinct()
#
#     offset = params.limit * params.page
#     rid_result = await db.execute(query.order_by(desc(Rid.rid_date))
#                                       .order_by(Rid.title)
#                                       .options(joinedload(Rid.keyword_rids).joinedload(KeywordRid.keyword))
#                                       .options(joinedload(Rid.work_supervisor))
#                                       .offset(offset).limit(params.limit))
#     rids = rid_result.scalars().unique().all()
#     scheme_rids = [SchemeRid.from_orm(rid) for rid in rids]
#     count = await get_count(query, db)
#     return dict(rids=scheme_rids, count=count)
#
#
# async def service_get_rid(id: int, db: Session):
#     rid_result = await db.execute(select(Rid).filter(Rid.id == id)
#                                      .options(joinedload(Rid.organization_executor)
#                                               .joinedload(OrganizationExecutor.organization))
#
#                                      .options(joinedload(Rid.rid_subject)
#                                               .joinedload(RidSubject.subject))
#
#                                      .options(joinedload(Rid.keyword_rids)
#                                               .joinedload(KeywordRid.keyword))
#
#                                      .options(joinedload(Rid.rid_authors)
#                                               .joinedload(AuthorRid.author))
#
#                                      .options(joinedload(Rid.work_supervisor))
#                                      .options(joinedload(Rid.organization_supervisor))
#                                      .options(joinedload(Rid.customer))
#                                      )
#     rid = rid_result.scalars().first()
#     if rid is None:
#         return False
#     scheme_rid = SchemeRidPage.from_orm(rid)
#     return dict(rid=scheme_rid)



# Разобраться с датой 2019-04-11
# Пустые customer не добавляются