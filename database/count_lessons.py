import os
import psycopg2

conn = psycopg2.connect(os.environ["SUPA_DB_URL"], sslmode="require")
cur = conn.cursor()
cur.execute(
    """
    select level, section, count(*)
    from public.lessons
    where is_published = true
    group by 1, 2
    order by 1, 2
    """
)
for level, section, count in cur.fetchall():
    print(f"{level}\t{section}\t{count}")
cur.execute("select level, count(*) from public.lessons where is_published = true group by 1 order by 1")
print("---")
for level, count in cur.fetchall():
    print(f"{level}\tTOTAL\t{count}")
cur.execute("select count(*) from public.lessons where is_published = true")
print(f"ALL\tTOTAL\t{cur.fetchone()[0]}")
conn.close()
