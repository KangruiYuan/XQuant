# 获取链接池、ORM表对象
import models

result = models.ScopedSession.query(models.InternshipMember).all()

for row in result:
    print(row)


result = models.ScopedSession.query(
    models.InternshipMember.id,
    models.InternshipMember.name,
    models.InternshipMember.age,
).all()

for row in result:
    print(row)

result = models.ScopedSession.query(
    models.InternshipMember.name.label("s_name"),
    models.InternshipMember.age.label("s_age"),
).all()

for row in result:
    print(row.s_name)
    print(row.s_age)


for u, a in (
    models.ScopedSession.query(models.InternshipMember, models.Address)
    .filter(models.InternshipMember.id == models.Address.user_id)
    .filter(models.Address.email_address == "kryuan@qq.com")
    .all()
):
    print(u)
    print(a)

u = (
    models.ScopedSession.query(models.InternshipMember)
    .join(models.Address)
    .filter(models.Address.email_address == "kryuan@qq.com")
    .one()
)

print(u)


# 关闭链接，亦可使用session.remove()，它将回收该链接
models.ScopedSession.close()
