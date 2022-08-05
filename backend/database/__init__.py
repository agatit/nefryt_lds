import sqlalchemy as sql
from sqlalchemy.orm import Session
from .models import lds, editor, obj

session: Session = None


# def columns_to_dict(self):
#     dict_ = {}
#     for key in self.__mapper__.c.keys():
#         dict_[key] = getattr(self, key)
#     return dict_

# # modele są generowane, więc uzupełniam metodę columns_to_dict w runtime
# lds.Base.columns_to_dict = columns_to_dict
# editor.Base.columns_to_dict = columns_to_dict