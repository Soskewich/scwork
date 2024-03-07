from sqlalchemy import Column, String, Boolean, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import Relationship, relationship, backref
from passlib.hash import bcrypt

from src.model.database import Base


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    users = Relationship("User", backref='role')


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    author = Relationship("Author", uselist=False)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String)
    birthday = Column(Date)
    confirmed = Column(Boolean, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    author_identifiers = Relationship("AuthorIdentifier", backref='author', cascade='save-update, merge, delete')
    author_publications = Relationship("AuthorPublication", backref='author', cascade='save-update, merge, delete')
    author_rid = Relationship("AuthorRid", backref='author', cascade='save-update, merge, delete')
    author_supervisors_dissertation = Relationship("AuthorSupervisorsDissertation", backref='author', cascade='save-update, merge, delete')
    author_opponents_dissertation = Relationship("AuthorOpponentsDissertation", backref='author', cascade='save-update, merge, delete')
    author_departments = Relationship("AuthorDepartment", backref='author', cascade='save-update, merge, delete')


class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    departments = Relationship("Department", backref='faculty')


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)
    department_authors = Relationship("AuthorDepartment", backref='department')


class AuthorDepartment(Base):
    __tablename__ = "author_department"
    id = Column(Integer, primary_key=True)
    position = Column(String)
    rate = Column(Float, default=1.0, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)


class Identifier(Base):
    __tablename__ = "identifier"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    author_identifiers = Relationship("AuthorIdentifier", backref='identifier')
    organization_identifiers = Relationship("OrganizationIdentifier", backref='identifier')


class AuthorIdentifier(Base):
    __tablename__ = "author_identifier"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    identifier_id = Column(Integer, ForeignKey('identifier.id'), nullable=False)
    identifier_value = Column(String)


class SourceType(Base):
    __tablename__ = "source_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    sources = Relationship("Source", backref="source_type")


class SourceLinkType(Base):
    __tablename__ = "source_link_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    source_links = Relationship("SourceLink", backref='source_link_type')


class SourceRatingType(Base):
    __tablename__ = "source_rating_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    source_ratings = Relationship("SourceRating", backref='source_rating_type')


class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True)
    source_type_id = Column(Integer, ForeignKey('source_type.id'), nullable=False)
    name = Column(String, nullable=False)
    source_links = Relationship("SourceLink", backref='source')
    source_ratings = Relationship("SourceRating", backref='source')
    publications = Relationship("Publication", backref='source')


class SourceLink(Base):
    __tablename__ = "source_link"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source_link_type_id = Column(Integer, ForeignKey('source_link_type.id'), nullable=False)
    link = Column(String, nullable=False)


class SourceRatingDate(Base):
    __tablename__ = 'source_rating_date'
    id = Column(Integer, primary_key=True)
    source_rating_id = Column(Integer, ForeignKey('source_rating.id'), nullable=False)
    rating_date = Column(Date, nullable=False)
    to_rating_date = Column(Date, nullable=False)
    active = Column(Boolean, nullable=False)


class SourceRatingSubject(Base):
    __tablename__ = 'source_rating_subject'
    id = Column(Integer, primary_key=True)
    source_rating_id = Column(Integer, ForeignKey('source_rating.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    active = Column(Boolean, nullable=False)
    rating_date = Column(Date, nullable=False)
    to_rating_date = Column(Date, nullable=False)


class SourceRating(Base):
    __tablename__ = "source_rating"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source_rating_type_id = Column(Integer, ForeignKey('source_rating_type.id'), nullable=False)
    rating = Column(String)
    source_rating_dates = Relationship("SourceRatingDate", backref='source_rating')
    source_rating_subjects = Relationship("SourceRatingSubject", backref='source_rating')


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    subj_code = Column(String)
    name = Column(String)
    source_rating_subjects = Relationship("SourceRatingSubject", backref='subject')
    nioktr_subject = Relationship("NioktrSubject", backref='subject')
    rid_subject = Relationship("RidSubject", backref='subject')
    dissertation_subject = Relationship("DissertationSubject", backref='subject')


class PublicationType(Base):
    __tablename__ = "publication_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    view_id = Column(Integer, ForeignKey('publication_type_view.id'))
    publications = Relationship("Publication", backref='publication_type')


class PublicationTypeView(Base):
    __tablename__ = "publication_type_view"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    publication_types = Relationship("PublicationType", backref='publication_type_view')


class Publication(Base):
    __tablename__ = "publication"
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('publication_type.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(String)
    publication_date = Column(Date, nullable=False)
    accepted = Column(Boolean, nullable=False)
    rate = Column(Float)
    keyword_publications = Relationship("KeywordPublication", backref="publication")
    publication_authors = Relationship("AuthorPublication", backref="publication")
    publication_links = Relationship("PublicationLink", backref="publication")


class Keyword(Base):
    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, unique=True)
    keyword_publications = Relationship("KeywordPublication", backref="keyword")
    keyword_nioktr = Relationship("KeywordNioktr", backref="keyword")
    keyword_rid = Relationship("KeywordRid", backref="keyword")
    keyword_dissertation = Relationship("KeywordDissertation", backref="keyword")


class KeywordPublication(Base):
    __tablename__ = "keywords_publication"
    id = Column(Integer, primary_key=True)
    publication_id = Column(Integer, ForeignKey("publication.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)


class KeywordNioktr(Base):
    __tablename__ = "keywords_nioktr"
    id = Column(Integer, primary_key=True)
    nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)


class KeywordRid(Base):
    __tablename__ = "keywords_rid"
    id = Column(Integer, primary_key=True)
    rid_id = Column(Integer, ForeignKey("rid.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    country = Column(String)
    city = Column(String)
    ogrn = Column(String)
    inn = Column(String)
    organization_coexecutor = Relationship("OrganizationCoexecutor", backref='organization')
    organization_executor = Relationship("OrganizationExecutor", backref='organization')
    author_publication_organizations = Relationship("AuthorPublicationOrganization", backref="organization")
    organization_identifiers = Relationship("OrganizationIdentifier", backref='organization')


class OrganizationCoexecutor(Base):
    __tablename__ = "organization_coexecutor"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False)


class OrganizationExecutor(Base):
    __tablename__ = "organization_executor"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    rid_id = Column(Integer, ForeignKey("rid.id"), nullable=False)


class AuthorPublication(Base):
    __tablename__ = "author_publication"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    publication_id = Column(Integer, ForeignKey("publication.id"), nullable=False)
    author_publication_organizations = Relationship("AuthorPublicationOrganization", backref="author_publication")


class AuthorRid(Base):
    __tablename__ = "author_rid"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    rid_id = Column(Integer, ForeignKey("rid.id"), nullable=False)



class AuthorPublicationOrganization(Base):
    __tablename__ = "author_publication_organization"
    id = Column(Integer, primary_key=True)
    author_publication_id = Column(Integer, ForeignKey("author_publication.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)


class PublicationLinkType(Base):
    __tablename__ = "publication_link_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    publication_links = Relationship("PublicationLink", backref="publication_link_type")


class PublicationLink(Base):
    __tablename__ = "publication_link"
    id = Column(Integer, primary_key=True)
    publication_id = Column(Integer, ForeignKey("publication.id"), nullable=False)
    link_type_id = Column(Integer, ForeignKey("publication_link_type.id"), nullable=False)
    link = Column(String, nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    message = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    solved = Column(Boolean, nullable=False)


class Nioktr(Base):
    __tablename__ = "nioktr"
    id = Column(Integer, primary_key=True)
    work_supervisor_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    organization_supervisor_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    organization_executor_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    rosrid_id = Column(String)
    title = Column(String, nullable=False)
    abstract = Column(String)
    contract_number = Column(String)
    registration_number = Column(String)
    nioktr_date = Column(Date)
    document_date = Column(Date)
    work_start_date = Column(Date)
    work_end_date = Column(Date)
    types_nioktrs = Relationship("NioktrTypes", backref="nioktr")
    keyword_nioktrs = Relationship("KeywordNioktr", backref="nioktr")
    nioktr_budget = Relationship("NioktrBudget", backref="nioktr")
    organization_coexecutor = Relationship("OrganizationCoexecutor", backref="nioktr")
    nioktr_subject = Relationship("NioktrSubject", backref='nioktr', lazy="joined")
    work_supervisor = Relationship("Author", foreign_keys=[work_supervisor_id], lazy="joined")
    organization_supervisor = relationship("Author", foreign_keys=[organization_supervisor_id], lazy="joined")
    organization_executor = relationship("Organization", foreign_keys=[organization_executor_id], lazy="joined")
    customer = relationship("Organization", foreign_keys=[customer_id], lazy="joined")


class NioktrSubject(Base):
    __tablename__ = "nioktr_subject"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False)


class OrganizationIdentifier(Base):
    __tablename__ = "organization_identifier"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'), nullable=False)
    identifier_id = Column(Integer, ForeignKey('identifier.id'), nullable=False)
    identifier_value = Column(String)


class BudgetType(Base):
    __tablename__ = "budget_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nioktr_budget = Relationship("NioktrBudget", backref='budget_type')


class NioktrBudget(Base):
    __tablename__ = "nioktr_budget"
    id = Column(Integer, primary_key=True)
    funds = Column(Float)
    kbk = Column(String)
    budget_type_id = Column(Integer, ForeignKey("budget_type.id"), nullable=False)
    nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False)


class NioktrTypes(Base):
    __tablename__ = "nioktr_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False)


class Rid(Base):
    __tablename__ = "rid"
    id = Column(Integer, primary_key=True)
    work_supervisor_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    organization_supervisor_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    # nioktr_id = Column(Integer, ForeignKey("nioktr.id"), nullable=False) Обсудить как лучше сделать заполнение
    rosrid_id = Column(String)
    title = Column(String, nullable=False)
    abstract = Column(String)
    registration_number = Column(String)
    rid_date = Column(Date)
    rid_type = Column(String)
    expected = Column(String)
    using_ways = Column(String)
    number_of_prototypes = Column(Integer)
    rid_subject = Relationship("RidSubject", backref='rid', lazy="joined")
    keyword_rids = Relationship("KeywordRid", backref="rid")
    rid_authors = Relationship("AuthorRid", backref="rid")
    organization_executor = Relationship("OrganizationExecutor", backref="rid")
    work_supervisor = Relationship("Author", foreign_keys=[work_supervisor_id], lazy="joined")
    organization_supervisor = relationship("Author", foreign_keys=[organization_supervisor_id], lazy="joined")
    customer = relationship("Organization", foreign_keys=[customer_id], lazy="joined")
    # iksi and ikspo ???


class RidSubject(Base):
    __tablename__ = "rid_subject"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    rid_id = Column(Integer, ForeignKey("rid.id"), nullable=False)


class Dissertation(Base):
    __tablename__ = "dissertation"
    id = Column(Integer, primary_key=True)
    chairman_dissertation_council_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    organization_supervisor_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author_organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    protection_organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    rosrid_id = Column(String)
    title = Column(String, nullable=False)
    abstract = Column(String)
    registration_number = Column(String)
    dissertation_date = Column(Date)
    protection_date = Column(Date)
    dissertation_type = Column(String)
    dissertation_report_type = Column(String)
    tables_count = Column(Integer)
    pictures_count = Column(Integer)
    applications_count = Column(Integer)
    pages_count = Column(Integer)
    sources_count = Column(Integer)
    books_count = Column(Integer)
    bibliography = Column(String)
    dissertation_subject = Relationship("DissertationSubject", backref='dissertation', lazy="joined")
    dissertation_keywords = Relationship("KeywordDissertation", backref="dissertation")
    dissertation_supervisors = Relationship("AuthorSupervisorsDissertation", backref="dissertation")
    dissertation_opponents = Relationship("AuthorOpponentsDissertation", backref="dissertation")
    chairman_dissertation_council = Relationship("Author", foreign_keys=[chairman_dissertation_council_id], lazy="joined")
    organization_supervisor = relationship("Author", foreign_keys=[organization_supervisor_id], lazy="joined")
    author_organization = relationship("Organization", foreign_keys=[author_organization_id], lazy="joined")
    protection_organization = relationship("Organization", foreign_keys=[protection_organization_id], lazy="joined")


class KeywordDissertation(Base):
    __tablename__ = "keywords_dissertation"
    id = Column(Integer, primary_key=True)
    dissertation_id = Column(Integer, ForeignKey("dissertation.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)


class DissertationSubject(Base):
    __tablename__ = "dissertation_subject"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    dissertation_id = Column(Integer, ForeignKey("dissertation.id"), nullable=False)


class AuthorSupervisorsDissertation(Base):
    __tablename__ = "author_supervisors_dissertation"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    dissertation_id = Column(Integer, ForeignKey("dissertation.id"), nullable=False)


class AuthorOpponentsDissertation(Base):
    __tablename__ = "author_opponents_dissertation"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    dissertation_id = Column(Integer, ForeignKey("dissertation.id"), nullable=False)





    # изменеил create_date на rid_date
    # bpvtybk keyword_rids
    # сделать миграцию