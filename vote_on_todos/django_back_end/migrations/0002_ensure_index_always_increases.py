from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('django_back_end', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""\
CREATE TRIGGER ensure_listevent_index_always_increases
BEFORE INSERT ON django_back_end_listeventsequence
BEGIN
    SELECT
    CASE WHEN NEW."index" <= (
        SELECT MAX("index") FROM django_back_end_listeventsequence
        WHERE "list_id"=NEW."list_id"
    ) THEN RAISE (ABORT,'index must be greater than all previous indexes')
    END;
END;
""",
            reverse_sql='DROP TRIGGER ensure_event_index_always_increases;',
        ),
        migrations.RunSQL(
            sql="""\
CREATE TRIGGER ensure_todoevent_index_always_increases
BEFORE INSERT ON django_back_end_todoeventsequence
BEGIN
    SELECT
    CASE WHEN NEW."index" <= (
        SELECT MAX("index")FROM django_back_end_todoeventsequence
        WHERE "todo_id"=NEW."todo_id"
    ) THEN RAISE (ABORT,'index must be greater than all previous indexes')
    END;
END;
""",
            reverse_sql='DROP TRIGGER ensure_event_index_always_increases;',
        ),
    ]
