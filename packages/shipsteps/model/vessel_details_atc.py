from gnr.app.gnrdbo import AttachmentTable
class Table(AttachmentTable):
    
    def onTableConfig(self, tbl):
        tbl.column('expire_date', dtype='D', name_short='!![en]Expire date')
        tbl.column('att_email', dtype='B', name_short='!![en]Email attached')
