"""empty message

Revision ID: bb2280bf16a9
Revises: 
Create Date: 2020-12-17 00:40:20.057788

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bb2280bf16a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kursy_prowadzacy',
    sa.Column('nr_kursu', sa.Integer(), nullable=False),
    sa.Column('nazwa', sa.String(length=255), nullable=True),
    sa.Column('prowadzacy', sa.String(length=33), nullable=True),
    sa.PrimaryKeyConstraint('nr_kursu')
    )
    op.create_table('nowe_linki',
    sa.Column('nr_linku', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('nazwa', sa.String(length=255), nullable=True),
    sa.Column('linkk', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('nr_linku')
    )
    op.drop_table('linki')
    op.drop_table('zadania')
    op.drop_table('kursy')
    op.drop_table('kursy_studenci')
    op.alter_column('prowadzacy', 'imie',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=True)
    op.alter_column('prowadzacy', 'nazwisko',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=True)
    op.create_unique_constraint(None, 'prowadzacy', ['nr_uzytkownika'])
    op.drop_constraint('prowadzacy_ibfk_1', 'prowadzacy', type_='foreignkey')
    op.create_foreign_key(None, 'prowadzacy', 'uzytkownicy', ['nr_uzytkownika'], ['nr_uzytkownika'])
    op.alter_column('studenci', 'imie',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=True)
    op.alter_column('studenci', 'nazwisko',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=True)
    op.create_unique_constraint(None, 'studenci', ['nr_uzytkownika'])
    op.drop_constraint('studenci_ibfk_1', 'studenci', type_='foreignkey')
    op.create_foreign_key(None, 'studenci', 'uzytkownicy', ['nr_uzytkownika'], ['nr_uzytkownika'])
    op.alter_column('uzytkownicy', 'czy_admin',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('uzytkownicy', 'haslo',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=True)
    op.alter_column('uzytkownicy', 'nazwa',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=True)
    op.create_index(op.f('ix_uzytkownicy_nazwa'), 'uzytkownicy', ['nazwa'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_uzytkownicy_nazwa'), table_name='uzytkownicy')
    op.alter_column('uzytkownicy', 'nazwa',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=False)
    op.alter_column('uzytkownicy', 'haslo',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=False)
    op.alter_column('uzytkownicy', 'czy_admin',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.drop_constraint(None, 'studenci', type_='foreignkey')
    op.create_foreign_key('studenci_ibfk_1', 'studenci', 'uzytkownicy', ['nr_uzytkownika'], ['nr_uzytkownika'], ondelete='CASCADE')
    op.drop_constraint(None, 'studenci', type_='unique')
    op.alter_column('studenci', 'nazwisko',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=False)
    op.alter_column('studenci', 'imie',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=False)
    op.drop_constraint(None, 'prowadzacy', type_='foreignkey')
    op.create_foreign_key('prowadzacy_ibfk_1', 'prowadzacy', 'uzytkownicy', ['nr_uzytkownika'], ['nr_uzytkownika'], ondelete='CASCADE')
    op.drop_constraint(None, 'prowadzacy', type_='unique')
    op.alter_column('prowadzacy', 'nazwisko',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=False)
    op.alter_column('prowadzacy', 'imie',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=16),
               nullable=False)
    op.create_table('kursy_studenci',
    sa.Column('nr_indeksu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('nr_kursu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['nr_indeksu'], ['studenci.nr_indeksu'], name='kursy_studenci_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['nr_kursu'], ['kursy.nr_kursu'], name='kursy_studenci_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('nr_indeksu', 'nr_kursu'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('kursy',
    sa.Column('nr_kursu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('nazwa', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=False),
    sa.Column('nr_gl_prowadzacego', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['nr_gl_prowadzacego'], ['prowadzacy.nr_prowadzacego'], name='kursy_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('nr_kursu'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('zadania',
    sa.Column('nr_zadania', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nr_kursu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('termin', sa.DATE(), nullable=False),
    sa.Column('typ', mysql.ENUM('kolokwium', 'projekt', 'raport', collation='utf8mb4_unicode_ci'), nullable=False),
    sa.Column('opis', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=False),
    sa.ForeignKeyConstraint(['nr_kursu'], ['kursy.nr_kursu'], name='zadania_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('nr_zadania'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('linki',
    sa.Column('nr_linku', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('nr_kursu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('data', sa.DATE(), nullable=False),
    sa.Column('linkk', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=False),
    sa.ForeignKeyConstraint(['nr_kursu'], ['kursy.nr_kursu'], name='linki_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('nr_linku'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('nowe_linki')
    op.drop_table('kursy_prowadzacy')
    # ### end Alembic commands ###