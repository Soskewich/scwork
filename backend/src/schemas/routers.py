from typing import List

from pydantic import BaseModel

from src.schemas.schemas import SchemePublication, SchemePublicationPage, SchemeAuthor, \
    SchemeAuthorProfile, SchemeSourceWithType, SchemeSourceWithRating, SchemeFeedback, SchemeFeedbackOutput, \
    SchemeAnalysis, SchemeAnalysisRating, SchemeAnalysisOrganization, SchemePublicationType, SchemeNioktr, \
    SchemeNioktrPage, SchemeRid, SchemeRidPage


class SchemePublicationsRouter(BaseModel):
    publications: List[SchemePublication]
    count: int


class SchemePublicationRouter(BaseModel):
    publication: SchemePublicationPage


class SchemeAuthorsRouter(BaseModel):
    authors: List[SchemeAuthor]
    count: int


class SchemeAuthorRouter(BaseModel):
    author: SchemeAuthorProfile


class SchemeSourcesRouter(BaseModel):
    sources: List[SchemeSourceWithType]
    count: int


class SchemeSourceRouter(BaseModel):
    source: SchemeSourceWithRating


class SchemeFeedbackPostRouter(BaseModel):
    feedback: SchemeFeedback
    token: str


class SchemeFeedbacksGetRouter(BaseModel):
    feedbacks: List[SchemeFeedbackOutput]
    count: int


class SchemeAnalysisRouter(BaseModel):
    result: List[SchemeAnalysis]
    total: int


class SchemeAnalysisRatingRouter(BaseModel):
    result: List[SchemeAnalysisRating]


class SchemeAnalysisOrganizationRouter(BaseModel):
    result: List[SchemeAnalysisOrganization]


class SchemePublicationTypesRouter(BaseModel):
    publication_types: List[SchemePublicationType]


class SchemeNioktrsRouter(BaseModel):
    nioktrs: List[SchemeNioktr]
    count: int


class SchemeNioktrRouter(BaseModel):
    nioktr: SchemeNioktrPage


class SchemeRidsRouter(BaseModel):
    rids: List[SchemeRid]
    count: int


class SchemeRidRouter(BaseModel):
    rid: SchemeRidPage


# class SchemePublicationRouter(BaseModel):
#     publication: SchemePublicationPage