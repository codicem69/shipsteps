from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Cambio Accosto'

class Main(BaseResourcePrint):
    batch_title = 'Cambio Accosto'
    html_res = 'html_res/cambio_accosto'
    batch_immediate = 'print'

    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=3,border_spacing='3px')
        #fb.div("""Vessel Details""")
        #In kwargs['record_count'] viene automaticamente immagazzinato il conteggio dei record della selezione
        fb.div("Cambiare nell'arrivo la banchina di ormeggio")
        fb.br()
        fb.datetimetextbox(value='^.datetime_ca', lbl='Data e ora cambio accosto',validate_notnull=True, colspan=3)
        fb.dbSelect(value='^.banchina_prov',lbl='Banchina di provenienza', table='shipsteps.dock',selected_dock_name='.dock_name',validate_notnull=True, hasDownArrow=True, width='15em', colspan=3)
        fb.textbox(value='^.dock_name', lbl='dock name', hidden=True, colspan=3)
        fb.textbox(value='^.extra_info', lbl='Ulteriori informazioni', width='30em', colspan=3)
        fb.br()
        fb.textbox(value='^.carbordo', lbl='Specifica Carico a bordo', validate_notnull=True, width='30em', placeholder='Insert cargo on board or NIL', colspan=3)
        fb.br()
        fb.div("""SPECIFICA CARICO:<br>
                  - Se trattasi di merci pericolose precisare la classe IMO<br>
                  - se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità<br>
	              - se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE<br>
                  - se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario""", colspan=3)
        fb.textbox(value='^.carbordo_extra', lbl='Specifica Carico a bordo',placeholder='indicare se trattasi di merce pericolosa o rinfusa', width='30em', colspan=3)
        fb.br()
        fb.textbox(value='^.draft_poppa', lbl='Draft Poppa', validate_notnull=True, validate_regex=" ^[0-9,]*$",validate_regex_error='Insert only numbers and comma', placeholder='eg:10 or 10,00')
        fb.textbox(value='^.draft_prua', lbl='Draft Prua', validate_notnull=True, validate_regex=" ^[0-9,]*$",validate_regex_error='Insert only numbers and comma', placeholder='eg:10 or 10,00')
        fb.br()
        fb.checkbox(value='^.pilota', lbl='Pilota')
        fb.checkbox(value='^.pilota_vhf', lbl='Pilota VHF')
        fb.br()
        fb.checkbox(value='^.antincendio', lbl='Antincendio')
        fb.checkbox(value='^.antinquinamento', lbl='Antinquinamento')
        fb.br()
        fb.checkbox(value='^.moor', lbl='Ormeggiatori')
        fb.textbox(value='^.n_moor', lbl='Numero Ormeggiatori')
        fb.br()
        fb.checkbox(value='^.tug', lbl='Rimorchiatori')
        fb.textbox(value='^.n_tug', lbl='Numero Rimorchiatori')
