rem call sqlacodegen.exe --option nobidi --schema lds  --outfile ../backend/database/models/lds.py mssql+pymssql://sa:Onyks$us@serverdb:1447/NefrytLDSDemo
rem call sqlacodegen.exe --option nobidi --schema editor --outfile ../backend/database/models/editor.py mssql+pymssql://sa:Onyks$us@serverdb:1447/NefrytLDSDemo

call sqlacodegen.exe --option nobidi --schema lds  --outfile ../backend/database/models/lds.py mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server
call sqlacodegen.exe --option nobidi --schema editor --outfile ../backend/database/models/editor.py mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server
call sqlacodegen.exe --option nobidi --schema obj --outfile ../backend/database/models/obj.py mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server


@echo done