# 获取链接池、ORM表对象
import models

models.ScopedSession.query(models.InternshipMember).filter_by(name="Mary").delete()
# 提交
models.ScopedSession.commit()
# 关闭链接，亦可使用session.remove()，它将回收该链接
models.ScopedSession.close()