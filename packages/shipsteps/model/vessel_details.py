# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('vessel_details', pkey='id', name_long='!![en]Vessel details', name_plural='!![en]Vessel details',caption_field='vessel_descr')
        self.sysFields(tbl)
        
        tbl.column('imbarcazione_id', size='22', name_short='imbarcazione_id').relation('pfda.imbarcazione.id', mode='foreignkey', onDelete='raise', one_one='*')
        tbl.column('owner_id', size='22', name_short='owner_id').relation('owner.id',relation_name='owner_vessdet', mode='foreignkey', onDelete='raise')
        tbl.column('callsign', size=':10', name_short='!![en]Call sign',validate_case='u')#validate u imposta tutte lettere maiuscole
        tbl.column('built', size='4', name_short='!![en]Built')
        tbl.column('dwt', name_short='dwt')
        tbl.column('beam', name_short='!![en]Beam')
        tbl.column('mmsi', name_short='mmsi')
        tbl.column('reg_place', size='22', name_short='!![en]Registration place').relation('unlocode.place.id',relation_name='reg_place_un', mode='foreignkey', onDelete='raise')
        tbl.column('reg_num', name_short='!![en]Registration no.')
        tbl.column('n_eliche', name_short='!![en]Propellers no.')
        tbl.column('n_eliche_poppa', name_short='!![en]Stern propellers no.')
        tbl.column('n_eliche_prua', name_short='!![en]Bow propellers no.')
        tbl.column('ex_name', name_short='!![en]Ex name',validate_case='t')#validate t imposta tutte le prime lettere maiuscole
        tbl.column('type', name_short='!![en]Type of ship')
        tbl.column('vessel_type_code',size=':3',name_short='!![en]Vessel type').relation('vessel_type.code',relation_name='vesseltype', mode='foreignkey', onDelete='raise')
        tbl.column('vess_note', name_short='!![en]Note')
        tbl.column('vess_image', dtype='P', name_short='!![en]Vessel photo')
        tbl.aliasColumn('vessel_name','@imbarcazione_id.nome',name_long='!![en]Vessel Name')
        tbl.aliasColumn('imo', '@imbarcazione_id.imo', name_long='IMO')
        tbl.aliasColumn('flag', '@imbarcazione_id.bandiera', name_long='!![en]Flag')
        tbl.aliasColumn('tsl', '@imbarcazione_id.gt', name_long='GT')
        tbl.formulaColumn('vessel_descr',"""@imbarcazione_id.nome || coalesce(' - IMO ' || $imo, '')""")
        
