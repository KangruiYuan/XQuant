import models

intern_member_1 = models.InternshipMember(
    name="Alkaid Yuan",
    age=24,
    gender='male',
)

intern_member_2 = models.InternshipMember(
    name="Euclid",
    age=23,
    gender='male',
)

intern_address_1 = models.Address(
    id=1,
    email_address="kryuan@qq.com",
    user_id=1
)

intern_address_2 = models.Address(
    id=2,
    email_address="euclid@qq.com",
    user_id=2
)

models.ScopedSession.add_all(
    (
        intern_member_1,
        intern_member_2,
        intern_address_1,
        intern_address_2
    )
)

# 提交
models.ScopedSession.commit()
# 关闭链接，亦可使用session.remove()，它将回收该链接
models.ScopedSession.close()