"""20.02.24

Revision ID: ebcb7e9d555a
Revises: cd2c4e436982
Create Date: 2024-02-20 15:34:52.148746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebcb7e9d555a'
down_revision: Union[str, None] = 'cd2c4e436982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budget_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faculty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('solved', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('identifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('keyword')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('ogrn', sa.String(), nullable=True),
    sa.Column('inn', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('publication_link_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('publication_type_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('source_link_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('source_rating_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('source_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subj_code', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('faculty_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_identifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.Column('identifier_id', sa.Integer(), nullable=False),
    sa.Column('identifier_value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['identifier_id'], ['identifier.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publication_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('view_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['view_id'], ['publication_type_view.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['source_type_id'], ['source_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('abstract', sa.String(), nullable=True),
    sa.Column('publication_date', sa.Date(), nullable=False),
    sa.Column('accepted', sa.Boolean(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['publication_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('source_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('source_link_type_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.ForeignKeyConstraint(['source_link_type_id'], ['source_link_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('source_rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('source_rating_type_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.ForeignKeyConstraint(['source_rating_type_id'], ['source_rating_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_identifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('identifier_id', sa.Integer(), nullable=False),
    sa.Column('identifier_value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['identifier_id'], ['identifier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_publication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['publication_id'], ['publication.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dissertation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chairman_dissertation_council_id', sa.Integer(), nullable=False),
    sa.Column('organization_supervisor_id', sa.Integer(), nullable=False),
    sa.Column('author_organization_id', sa.Integer(), nullable=False),
    sa.Column('protection_organization_id', sa.Integer(), nullable=False),
    sa.Column('rosrid_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('abstract', sa.String(), nullable=True),
    sa.Column('registration_number', sa.String(), nullable=True),
    sa.Column('created_date', sa.Date(), nullable=True),
    sa.Column('protection_date', sa.Date(), nullable=True),
    sa.Column('dissertation_type', sa.String(), nullable=True),
    sa.Column('dissertation_report_type', sa.String(), nullable=True),
    sa.Column('tables_count', sa.Integer(), nullable=True),
    sa.Column('pictures_count', sa.Integer(), nullable=True),
    sa.Column('applications_count', sa.Integer(), nullable=True),
    sa.Column('pages_count', sa.Integer(), nullable=True),
    sa.Column('sources_count', sa.Integer(), nullable=True),
    sa.Column('books_count', sa.Integer(), nullable=True),
    sa.Column('bibliography', sa.String(), nullable=True),
    sa.Column('number_of_prototypes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['chairman_dissertation_council_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['organization_supervisor_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['protection_organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords_publication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.ForeignKeyConstraint(['publication_id'], ['publication.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nioktr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_supervisor_id', sa.Integer(), nullable=False),
    sa.Column('organization_supervisor_id', sa.Integer(), nullable=False),
    sa.Column('organization_executor_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('rosrid_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('abstract', sa.String(), nullable=True),
    sa.Column('contract_number', sa.String(), nullable=True),
    sa.Column('registration_number', sa.String(), nullable=True),
    sa.Column('nioktr_date', sa.Date(), nullable=True),
    sa.Column('document_date', sa.Date(), nullable=True),
    sa.Column('work_start_date', sa.Date(), nullable=True),
    sa.Column('work_end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_executor_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_supervisor_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['work_supervisor_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publication_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.Column('link_type_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['link_type_id'], ['publication_link_type.id'], ),
    sa.ForeignKeyConstraint(['publication_id'], ['publication.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_supervisor_id', sa.Integer(), nullable=False),
    sa.Column('organization_supervisor_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('rosrid_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('abstract', sa.String(), nullable=True),
    sa.Column('registration_number', sa.String(), nullable=True),
    sa.Column('created_date', sa.Date(), nullable=True),
    sa.Column('rid_type', sa.String(), nullable=True),
    sa.Column('expected', sa.String(), nullable=True),
    sa.Column('using_ways', sa.String(), nullable=True),
    sa.Column('number_of_prototypes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_supervisor_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['work_supervisor_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('source_rating_date',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_rating_id', sa.Integer(), nullable=False),
    sa.Column('rating_date', sa.Date(), nullable=False),
    sa.Column('to_rating_date', sa.Date(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['source_rating_id'], ['source_rating.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('source_rating_subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_rating_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('rating_date', sa.Date(), nullable=False),
    sa.Column('to_rating_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['source_rating_id'], ['source_rating.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_opponents_dissertation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('dissertation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['dissertation_id'], ['dissertation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_publication_organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_publication_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_publication_id'], ['author_publication.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_rid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('rid_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['rid_id'], ['rid.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_supervisors_dissertation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('dissertation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['dissertation_id'], ['dissertation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dissertation_subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('dissertation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dissertation_id'], ['dissertation.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords_dissertation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dissertation_id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dissertation_id'], ['dissertation.id'], ),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords_nioktr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nioktr_id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.ForeignKeyConstraint(['nioktr_id'], ['nioktr.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords_rid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid_id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.ForeignKeyConstraint(['rid_id'], ['rid.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nioktr_budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('funds', sa.Float(), nullable=True),
    sa.Column('kbk', sa.String(), nullable=True),
    sa.Column('budget_type_id', sa.Integer(), nullable=False),
    sa.Column('nioktr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['budget_type_id'], ['budget_type.id'], ),
    sa.ForeignKeyConstraint(['nioktr_id'], ['nioktr.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nioktr_subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('nioktr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nioktr_id'], ['nioktr.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nioktr_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('nioktr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nioktr_id'], ['nioktr.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_coexecutor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.Column('nioktr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nioktr_id'], ['nioktr.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_executor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.Column('rid_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['rid_id'], ['rid.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rid_subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('rid_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rid_id'], ['rid.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rid_subject')
    op.drop_table('organization_executor')
    op.drop_table('organization_coexecutor')
    op.drop_table('nioktr_types')
    op.drop_table('nioktr_subject')
    op.drop_table('nioktr_budget')
    op.drop_table('keywords_rid')
    op.drop_table('keywords_nioktr')
    op.drop_table('keywords_dissertation')
    op.drop_table('dissertation_subject')
    op.drop_table('author_supervisors_dissertation')
    op.drop_table('author_rid')
    op.drop_table('author_publication_organization')
    op.drop_table('author_opponents_dissertation')
    op.drop_table('source_rating_subject')
    op.drop_table('source_rating_date')
    op.drop_table('rid')
    op.drop_table('publication_link')
    op.drop_table('nioktr')
    op.drop_table('keywords_publication')
    op.drop_table('dissertation')
    op.drop_table('author_publication')
    op.drop_table('author_identifier')
    op.drop_table('author_department')
    op.drop_table('source_rating')
    op.drop_table('source_link')
    op.drop_table('publication')
    op.drop_table('author')
    op.drop_table('user')
    op.drop_table('source')
    op.drop_table('publication_type')
    op.drop_table('organization_identifier')
    op.drop_table('department')
    op.drop_table('subject')
    op.drop_table('source_type')
    op.drop_table('source_rating_type')
    op.drop_table('source_link_type')
    op.drop_table('role')
    op.drop_table('publication_type_view')
    op.drop_table('publication_link_type')
    op.drop_table('organization')
    op.drop_table('keyword')
    op.drop_table('identifier')
    op.drop_table('feedback')
    op.drop_table('faculty')
    op.drop_table('budget_type')
    # ### end Alembic commands ###