import models

# 在SQLAlchemy中，四则运算符号只能用于数值类型
# 如果是字符串类型需要在原本的基础值上做改变，必须设置synchronize_session=False

models.ScopedSession.query(models.InternshipMember).filter_by(name="Euclid").update(
    {
        "name": models.InternshipMember.name + " Jie",
    },
    synchronize_session=False,
)

# 提交
models.ScopedSession.commit()
# 关闭链接，亦可使用session.remove()，它将回收该链接
models.ScopedSession.close()