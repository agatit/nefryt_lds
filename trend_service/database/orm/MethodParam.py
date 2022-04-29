
from ...database import Base_lds
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class MethodParam(Base_lds):
    __tablename__ = 'MethodParam'
    __table_args__ = {'schema': 'lds'}
    MethodParamDefID = Column("MethodParamDefID",
                              Integer, primary_key=True, autoincrement=False, nullable=False)  # , ForeignKey('method.ID'))
    MethodID = Column("MethodID", Integer, primary_key=True,
                      autoincrement=False, nullable=False)
    Value = Column("Value", String(30))

    def __repr__(self):
        return '<MethodParam> ' + str(self.columns_to_dict())

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_

    # schemas/orm/MethodParam.yaml
# type: object
# x-tablename: MethodParam
# x-schema-name: lds
# required:
#     - MethodParamDefID
#     - MethodID
# properties:
#     MethodParamDefID:
#         x-primary-key: true
#         x-autoincrement: false
#         type: integer
#         nullable: false
#         description: none
#         example: 0
#     MethodID:
#         x-primary-key: true
#         x-autoincrement: false
#         type: integer
#         nullable: false
#         description: none
#     Value:
#         type: string
#         pattern: ^ .{0, 30}
#         description: none
