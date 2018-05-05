from dsst_server.data_access import sql
from dsst_server.auth import check_write


class DeleteFunctions:

    @staticmethod
    @check_write
    def delete_death(death_id: int):
        return sql.Death.delete().where(sql.Death.id == death_id).execute()

    @staticmethod
    @check_write
    def delete_victory(victory_id: int):
        return sql.Victory.delete().where(sql.Death.id == victory_id).execute()
